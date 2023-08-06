"""
.. note:: Before calling any of the functions in this module, it must first
    be configured using :func:`configure`.

This module provides interaction with the IPFS cluster of a datacustodian. Note that in
order to implement custom security on requests (aka `didauth`) as well as to
supporting adding of files that are accessible on the local node's file system
we implement a second REST API for typical cluster methods. This provides:

1. Total control over authentication of requests.
2. Lock-down of basic cluster API so that it isn't even reachable publicly.
3. Referencing files on the local machine for adding to IPFS (for example, from
   attached USB devices) without the overhead of using a web-browser to send
   each one to the REST API as part of a HTTP request.

However, this comes with an obvious downside: when files *are* added via a
multipart-encoded HTTP request to *this* API, we must prepare a second HTTP
request to the API hosted in IPFS cluster. This is somewhat wasteful, so we
try to mitigate the problem by pulling the byte stream from the request to this
API and sending it directly, as bytes, into the next request to IPFS cluster.
Thus, our only overhead is in constructing the packet with headers, etc.

Given the importance of the features described above, the overhead seems worth
it for now. This could be optimized later by building support for `didauth` via
a decentralized ledger into the IPFS cluster code so that the API inherently
supports it. Not likely to happen in the short term...

"""
import os
import logging
from os import path
from flask import send_file, render_template, stream_with_context, Response, abort
import json
import ipfscluster
from ipfscluster import AddOptions, PinOptions
import ipfshttpclient
import yaml
from tempfile import SpooledTemporaryFile

from datacustodian.utility import relpath
from datacustodian.settings import save_overrides, get_overrides

log = logging.getLogger(__name__)

class BufferedTemporarySpooledFile(SpooledTemporaryFile):
    def __init__(self, headers, name, tfile):
        super(BufferedTemporarySpooledFile, self).__dict__.update(tfile.__dict__)
        self.headers = headers
        self.__dict__["name"] = name
    def __len__(self):
        return int(self.headers['Content-Length'])
    def __getitem__(self, index):
        if isinstance(index, slice):
            self.seek(index.start)
            return self.read(index.stop-index.start)

basedirs = {}
"""dict: base directories that files and folders are browsed from; see the
example config file and explanation in `docs/config/cluster.yml`.
"""
cluster = None
"""ipfscluster.Client: HTTP client for interacting with the IPFS cluster API.
"""
agent = None
"""ipfshttpclient.Client: HTTP client to interact with the IPFS agent for
file getting and removal from IPFS.
"""

def _get_abspath(reqpath):
    """Returns the absolute path on the local server given the specified
    request path, which is assumed to originate at a configured root directory.

    Args:
        reqpath (str): relative path to the file/directory to return; must be
            relative to one of the :data:`basedirs`.
    """
    parts = reqpath.split('/')
    base = parts[0]
    return base, path.join(basedirs[base], '/'.join(parts[1:]))

def configure(norun=False, **settings):
    """Configures the local IPFS cluster on this node.

    Args:
        norun (bool): when True, don't try and connect to the agent or cluster.
        settings (dict): key-value pairs defining the basic storage directories,
            agent and cluster ports, etc.
    """
    global basedirs, cluster, agent, override_file
    #First, set the basic parameters that are just strings; then construct
    #the complex objects.
    override_basedirs = get_overrides("ipfs.basedirs")
    settings["basedirs"].update(override_basedirs)
    basedirs.update({k: relpath(path.expanduser(v), '.')
                     for k, v in settings["basedirs"].items()})
    log.info("Basedirs updated to %r", basedirs)
    if not norun:
        cluster = ipfscluster.connect(**settings.get("cluster", {}))
        agent = ipfshttpclient.connect(**settings.get("agent", {}))

def dirlist(reqpath=None, page=0, per_page=25, **kwargs):
    """Lists contents of `reqpath` if it is a directory; otherwise, serves
    the contents of the file.

    Args:
        reqpath (str): relative path to the file/directory to return.
    """
    assert reqpath is not None

    base, target = _get_abspath(reqpath)
    if not path.exists(target):
        return abort(404)

    # Show directory contents
    contents = os.listdir(target)
    files = [f for f in contents if path.isfile(path.join(target, f))]
    folders = [f for f in contents if path.isdir(path.join(target, f))]
    result = folders + files
    i = len(result)//per_page
    n = per_page * page
    m = per_page if len(result)-n >= per_page else len(result)%per_page
    return {
      "page": page,
      "pages": i+1,
      "per_page": per_page,
      "total": len(result),
      "items": [{
        "did": None,
        "url": "/{}/{}".format(base, r),
        "isdir": n + i < len(folders)
      } for i, r in enumerate(result[n:n+m])]
    }

def download(reqpath=None, **kwargs):
    """Sends the file specified by `reqpath` if it exists.

    Args:
        reqpath (str): relative path to the file to return.
    """
    base, target = _get_abspath(reqpath)
    if path.isfile(target):
        return send_file(target)

def _query_to_addopts(params):
    """Converts the query string parameters to an AddOptions object.
    """
    pinattrs = ["name", "shard_size", "replication_factor_min",
                "replication_factor_max"]
    pinopts = {}
    addopts = {}
    for pname, pval in params.items():
        if pname in pinattrs:
            pinopts[pname] = pval
        else:
            addopts[pname] = pval

    addopts["pinopts"] = PinOptions(**pinopts)
    return AddOptions(**addopts)

def add_local(reqpath=None, _request=None, _data=None, **kwargs):
    """Adds the specified *local* file to IPFS.

    Args:
        reqpath (str): for local files.
        _request: the :class:`flask.Request` to process; used to add files sent
            in the request body.
    """
    base, target = _get_abspath(reqpath)
    addopts = _query_to_addopts(_request.args)
    r = cluster.add_files(target, addopts=addopts)
    r["cid"] = json.dumps(r["cid"])
    return r

def add(reqpath=None, _request=None, _data=None, **kwargs):
    """Adds the specified file to IPFS from the octet stream in the request.

    Args:
        reqpath (str): `None` so the files are retrieved from the request body.
        _request: the :class:`flask.Request` to process; used to add files sent
            in the request body.
    """
    response = []
    addopts = _query_to_addopts(_request.args)
    if _request.files is not None:
        #The files are part of the request object; we want to pass them through
        #so that we don't decode and then encode wastefully.
        for formid, file in _request.files.items():
            name = reqpath or formid
            bfile = BufferedTemporarySpooledFile(_request.headers, name, file.stream)
            r = cluster.add_bytes(bfile, name=name, addopts=addopts)
            r["cid"] = json.dumps(r["cid"])
            response.append(r)

    return response

def get(reqpath=None, **kwargs):
    """Returns the specified file from the IPFS cluster.

    Args:
        reqpath (str): the IPFS address of the file/folder to return from the
            IPFS cluster.
    """
    assert reqpath is not None
    #Get statistics on the file size so that we can send that in the response
    #headers; that allows the browser to know download %, for example.
    stats = agent.object.stat(reqpath)
    size = stats["DataSize"]
    headers = [
        ('Content-Length', str(size)),
        ('Content-Disposition', 'attachment; filename="/ipfs/%s"' % reqpath),
    ]

    log.debug("Responding with headers=%r for %s.", headers, reqpath)
    obj = agent.cat(reqpath)
    return Response(obj,
                    mimetype='application/octet-stream',
                    headers=headers,
                    direct_passthrough=True)

def rm(reqpath=None, **kwargs):
    """Removes the specified file from the local node. Note that IPFS is the
    *permanent* web, so things never get deleted from IPFS itself. However, you
    can choose to not pin things anymore so that they are deleted locally. If
    nobody is pinning something, it is essentially deleted since a lookup will
    not return any peers that can actually serve the content.

    .. note:: This function is equivalent to calling :func:`unpin` on the cluster.

    Args:
        reqpath (str): the IPFS address of the file/folder to remove from the
            IPFS cluster.
    """
    return unpin(reqpath)

def pin(reqpath=None, **kwargs):
    """Pins the specified file to the local node. This essentially creates a
    cached copy of the local file.

    Args:
        reqpath (str): the IPFS address of the file/folder to cache locally.
    """
    return cluster.pins.add(reqpath)

def unpin(reqpath=None, **kwargs):
    """Pins the specified file to the local node. This essentially creates a
    cached copy of the local file.

    Args:
        reqpath (str): the IPFS address of the file/folder to cache locally.
    """
    return cluster.pins.rm(reqpath)

def ls_pins(**kwargs):
    """Lists pin allocations across the cluster. This is equivalent to listing
    which files in IPFS are pinned locally at each node.
    """
    return {
        "pins": cluster.allocations.ls()
    }

def _basedir_response():
    """Serializes the current state of :data:`basedirs` into a `dict` that
    matches the model configuration of the endpoint.
    """
    return {
        "basedirs": [{
            "key": k,
            "path": v
        } for k, v in basedirs.items()]
    }

def add_basedir(_data=None, **kwargs):
    """Adds a base directory to the list of currently configured
    ones.

    .. note:: If you specify a relative path, it will be taken relative to the
        working directory that the executable was started in. This is set in
        the container docker image using `WORKDIR`.

    Args:
        key (str): key of the base directory to refer to in the paths.
        dirpath (str): absolute or relative path to configure.
    """
    global basedirs
    key, dirpath = _data["key"], _data["path"]
    basedirs[key] = relpath(path.expanduser(dirpath), '.')
    save_overrides("ipfs.basedirs", basedirs)
    return _basedir_response()

def rm_basedir(key=None, **kwargs):
    """Removes the specified `basedir` from the list of currently configured
    ones.

    Args:
        key (str): key of the directory as returned by :func:`ls_basedirs`.
    """
    global basedirs
    if key in basedirs:
        del basedirs[key]

    save_overrides("ipfs.basedirs", basedirs)
    return _basedir_response()

def ls_basedirs(**kwargs):
    """Returns a list of currently configured base-directories that can be used
    in the `download` GET and `files` PUT methods.
    """
    return _basedir_response()
