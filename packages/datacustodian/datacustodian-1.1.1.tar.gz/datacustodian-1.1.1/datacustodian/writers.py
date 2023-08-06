from os import path, mkdir
import sys
import logging
from glob import glob
from jinja2 import Environment, PackageLoader
import re

from datacustodian.settings import load, specs
from datacustodian.utility import relpath
from datacustodian.testing import url_params

log = logging.getLogger(__name__)

rx = re.compile(r"(\<[\w\d:]+\>)", re.I)
"""re.MatchObject: with the pattern to replace route variable names.
"""
def convert_route_to_function(route):
    """Converts a route to a function name.
    """
    return rx.sub("", route).replace('/', '_')

def route_to_vars(routes):
    """Returns a list of variables encoded in the route.
    """
    result = []
    for r in routes:
        result.extend(url_params(r).keys())
    return set(result)

def package_init(appspecs, packspec, reset=False, compspecs=None):
    """Initializes the generated package folder structure, if it doesn't already
    exist.

    Args:
        appspecs (list): of `str` paths to application specifications.
        packspec (AttrDict): specification for the overall application, which
            includes path information for the generated component.
        reset (bool): when True, reset the package files like setup.py,
            __init__.py, conftest.py to auto-generated status. This nukes the
            local changes made manually.
        compspecs (dict): of all component specifications for the whole app.

    Returns:
        tuple: `(root, coderoot, testroot, client_root)`, where root is the repository root folder,
        and `coderoot` is the sub-directory where python code is stored. `testroot`
        is the directory to the `tests` directory for unit testing. `client_root` is
        the directory that the HTTP client sub-package is generated in.
    """
    root = path.abspath(path.expanduser(packspec.root))
    #Make sure that the repository root path is in the python path for dynamic
    #imports of the generated package.
    if root not in sys.path:
        sys.path.insert(0, root)
    coderoot = path.join(root, packspec.name)
    testroot = path.join(root, "tests")
    client_root = path.join(coderoot, "client")

    if not path.isdir(root): # pragma: no cover
        mkdir(root)
    if not path.isdir(coderoot): # pragma: no cover
        mkdir(coderoot)
    if not path.isdir(testroot): # pragma: no cover
        mkdir(testroot)
    if not path.isdir(client_root): # pragma: no cover
        mkdir(client_root)

    setup = path.join(root, "setup.py")
    init = path.join(coderoot, "__init__.py")
    wsgi = path.join(coderoot, f"{packspec.name}_app.py")
    client_init = path.join(client_root, "__init__.py")
    conftest = path.join(testroot, "conftest.py")

    env = Environment(loader=PackageLoader('datacustodian', 'templates'))
    t_setup = env.get_template("setup.py")
    t_init = env.get_template("init.py")
    c_init = env.get_template("client_init.py")
    t_tests = env.get_template("_conftest.py")
    t_wsgi = env.get_template("wsgi.py")
    cpspec = packspec.copy()
    cpspec["appspecs"] = appspecs
    cpspec["compspecs"] = compspecs

    if not path.isfile(setup) or reset:
        with open(setup, 'w') as f:
            f.write(t_setup.render(**cpspec))
    if not path.isfile(init) or reset:
        with open(init, 'w') as f:
            f.write(t_init.render(**cpspec))
    if not path.isfile(client_init) or reset:
        with open(client_init, 'w') as f:
            f.write(c_init.render(**cpspec))
    if not path.isfile(conftest) or reset:
        with open(conftest, 'w') as f:
            f.write(t_tests.render(**cpspec))
    if not path.isfile(wsgi) or reset:
        with open(wsgi, 'w') as f:
            f.write(t_wsgi.render(**cpspec))

    return root, coderoot, testroot, client_root

def component_write(appspecs, packspec, compspec, overwrite=False, reset=False,
                    allspecs=None):
    """Writes the python code file for the specified component specification so
    that a :class:`flask.Blueprint` can be created via direct import.

    Args:
        appspecs (list): of `str` paths to application specifications.
        packspec (AttrDict): specification for the derived package, which
            includes path information for the generated component.
        compspec (AttrDict): component specification to create.
        overwrite (bool): when True, overwrite the module file if it already
            exists.
        reset (bool): when True, reset the package files like setup.py,
            __init__.py, conftest.py to auto-generated status. This nukes the
            local changes made manually.
        allspecs (dict): of all component specifications for the whole app.
    """
    root, coderoot, testroot, client_root = package_init(appspecs, packspec, reset=reset, compspecs=allspecs)
    target = path.join(coderoot, "{}.py".format(compspec.name))

    #Look for pre-defined testing data for auto-generated unit tests.
    if "testdata" in packspec:
        testspecroot = relpath(packspec.testdata, '.')
    else: # pragma: no cover
        testspecroot = path.join(testroot, "specs")

    tests = None
    log.debug("Looking for testing specifications in %s.", testspecroot)
    if path.isdir(testspecroot):
        ctestspec = path.join(testspecroot, "{}.yml".format(compspec.name))
        if path.isfile(ctestspec):
            log.debug("Found specs for %s at %s.", compspec.name, ctestspec)
            tests = load(ctestspec, asattr=False)

    testspec = {}
    #Merge the test specification with the namespaces one.
    cspec = specs[compspec.name]
    for nspec in cspec.namespaces:
        testspec[nspec.name] = {}
        testspec[nspec.name]["endpoints"] = {}
        try:
            tn = None
            if tests is not None:
                tn = [t for t in tests if t["name"] == nspec.name][0]

            for espec in nspec.endpoints:
                en = []
                if tn is not None:
                    en = [e for e in tn["endpoints"] if e["name"] == espec.name]

                if len(en) > 0:
                    testspec[nspec.name]["endpoints"][espec.name] = en[0]
                else:
                    testspec[nspec.name]["endpoints"][espec.name] = {}

        except IndexError:
            for espec in nspec.endpoints:
                testspec[nspec.name]["endpoints"][espec.name] = {}

    env = Environment(loader=PackageLoader('datacustodian', 'templates'))
    template = env.get_template("component.py")
    cpspec = compspec.copy()
    cpspec["package"] = packspec
    cpspec["testing"] = testspec

    if not path.isfile(target) or overwrite:
        with open(target, 'w') as f:
            f.write(template.render(**cpspec))
    else:
        log.info("%s exists and no-overwrite enabled. Skipping.",
                 target)

    #Also create the unit tests for this component with all specified HTTP
    #methods already coded (albeit without the data to make them work).
    testfile = path.join(testroot, "test_{}.py".format(compspec.name))
    t_test = env.get_template("t_component.py")
    if not path.isfile(testfile) or overwrite:
        with open(testfile, 'w') as f:
            f.write(t_test.render(**cpspec))
    else:
        log.info("%s exists and no-overwrite enabled. Skipping.",
                 testfile)

    # Next, write the client HTTP library for this component.
    env.filters.update({
        'route2fun': convert_route_to_function,
        'route2vars': route_to_vars
    })
    clientfile = path.join(client_root, f"{compspec.name}.py")
    client_template = env.get_template("client_component.py")
    cpspec = compspec.copy()
    cpspec["package"] = packspec
    cpspec["model_dict"] = {m["name"]: m for m in cpspec["models"]}

    if not path.isfile(clientfile) or overwrite:
        with open(clientfile, 'w') as f:
            f.write(client_template.render(**cpspec))
    else:
        log.info("Client file %s exists and no-overwrite enabled. Skipping.",
                 clientfile)
