import logging, threading
from werkzeug.serving import make_server
from flask_restplus import Api, reqparse, fields
from flask_restful.utils import cors
from attrdict import AttrDict

__version__ = "0.0"

log = logging.getLogger(__name__)
apis = AttrDict()
"""AttrDict: keys are application names; values are flask_restplus.Api configured
for that app.
"""

_runmsg = '>>>>> Starting server at http://{}:{} <<<<<'
class ServerThread(threading.Thread):
    """Thread to start an application server for the REST API.

    Args:
        app (flask.Flask): application that provides the context to serve.
        servername (str): IP address and port to serve the application at.
    """
    def __init__(self, app, servername, ssl_context=None):
        threading.Thread.__init__(self)
        self.ip, self.port = servername.split(':')
        self.port = int(self.port)
        log.debug(f"Making werkzeug server at {self.ip}:{self.port}.")
        self.srv = make_server(self.ip, self.port, app, ssl_context=ssl_context)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        log.info(_runmsg.format(self.ip, self.port))
        self.srv.serve_forever()

    def shutdown(self): # pragma: no cover
        #This is actually called, but somehow the coverage isn't picking up.
        try:
            log.debug("Stopping API server with :meth:`shutdown`.")
            self.srv.shutdown()
        except:
            log.error("Shutdown error for main API server.")

def create_api(appspec, compspec):
    """Creates a :class:`flask_restplus.Api` for the given set of application and
    API settings.

    Args:
        appspec (AttrDict): specification for the overall application, which
            includes path information for the generated component.
        compspec (AttrDict): component specification to create an API for.
    """
    global apis
    appname = compspec.name
    api = Api(version=__version__, title=compspec.title,
              description=compspec.description)
    apis[appname] = api

    @api.errorhandler
    def default_error_handler(e):
        message = 'An unhandled exception occurred.'
        log.exception(message)

        if not appspec.debug:
            return ({'message': message}, 500)

    return api

def create_parsers(spec):
    """Creates all parser definitions from the specification dictionary.

    Args:
        spec (dict): keys are parser names; values are lists of parameter definitions
            for the request.

    Returns:
        dict: keys are parser names; values are :class:`flask_restplus.reqparse.RequestParser`.

    Examples:

        For the most part, allowable attributes are those that are accepted by
        the well-known :mod:`argparse` package.

        .. code-block:: yaml

            parsers:
              Pagination:
                - name: page
                  type: int
                  required: False
                  default: 1
                  help: 'Page number.'
                - name: per-page
                  type: int
                  required: False
                  choices: [2, 5, 10, 25, 50]
                  default: 10
                  help: 'Number of records to display in each page.'
    """
    parsers = {}
    for sname, sparams in spec.items():
        p = reqparse.RequestParser()
        for args in sparams:
            cargs = args.copy()
            name = cargs.pop("name")
            p.add_argument(name, **cargs)
        parsers[name] = p

    return parsers

class Schema(dict):
    """Represents a collection of model schema specifications for the REST API that
    facilitates serialization.
    """
    def create_model(self, compname, spec):
        """Calls :meth:`flask_restplus.Api.model` from the specifications dict to create
        a serialization model.

        Args:
            compname (str): name of the component to generate the model for.
            spec (dict): key-value pairs defining the schema of the model.

        Examples:
            The following shows an example that defines a paginated collection of
            records:

            .. code-block:: yaml

                name: Record
                properties:
                  id:
                    type: String
                    readOnly: True
                    description: 'The unique identifier of the record.'

            Here we see that each model needs a name and fields. Each key in the fields
            `dict` becomes the name of a field. The special keyword type is one of the
            types contained in :class:`flask_restplus.fields`. All additional arguments
            are passed as keyword arguments to the model constructor. Next, we define the
            paginator fields:

            .. code-block:: yaml

                name: Pagination
                properties:
                  page:
                    type: Integer
                    description: 'Number of this page of results.'
                  pages:
                    type: Integer
                    description: 'Total number of pages of results.'
                  per_page:
                    type: Integer
                    description: 'Number of items per page of results.'
                  total:
                    type: Integer
                    description: 'Total number of results.'

            Finally, in order to support inheritance and nested types, we introduce
            two additional special keywords: "inherit" (at the model level), and
            "nest" at the field level.

            .. code-block:: yaml

                name: Collection
                inherit: [Pagination]
                properties:
                  items:
                    type: List
                    nest: Record

            This demonstrates how `Collection` inherits fields from `Pagination`. In
            addition, it defines an additional field `items`, that is a list of
            nested `Record` models.
        """
        _name, _fields = spec["name"], spec["properties"]
        if _name in self:
            log.warning("A spec for %s already exists, overwriting.", _name)

        mfields = {}
        for fname, fspec in _fields.items():
            #Make a shallow copy so that we can mutate the dictionary without
            #messing around with the caller dict.
            cspec = fspec.copy()
            _type = cspec.pop("type")
            _nest = cspec.pop("nest", None)
            typecls = getattr(fields, _type)

            if _nest is not None:
                if _nest in self:
                    target = self[_nest]
                    if _type in ["List"]:
                        mfields[fname] = typecls(fields.Nested(target), **cspec)
                    else:
                        mfields[fname] = typecls(target, **cspec)
                else:
                    target = getattr(fields, _nest)
                    mfields[fname] = typecls(target, **cspec)
            else:
                mfields[fname] = typecls(**cspec)

        #Now, construct the model object using this set of fields, and then add it
        #to the models cache.
        if "inherit" in spec:
            ancestry = [self.get(s) for s in spec["inherit"]]
            result = apis[compname].inherit(_name, *ancestry, mfields)
        else:
            result = apis[compname].model(_name, mfields)

        self[_name] = result
        return result

    def load(self, compname, modelspec):
        """Creates models for all specifications.

        Args:
            compname (str): name of the component to create the models for.
            modelspec (list): list of models to generate.
        """
        for spec in modelspec:
            self.create_model(compname, spec)
