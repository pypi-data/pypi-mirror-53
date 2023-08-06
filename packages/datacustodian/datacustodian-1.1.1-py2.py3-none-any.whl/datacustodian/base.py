class SectionProperty(object):
	def __init__(self, cls):
		self.__prop_cls__ = cls

	def __get__(self, client_object, type=None):
		if client_object is not None:  # We are invoked on object
			try:
				return client_object.__prop_objs__[self]
			except AttributeError:
				client_object.__prop_objs__ = {
					self: self.__prop_cls__(client_object)
				}
				return client_object.__prop_objs__[self]
			except KeyError:
				client_object.__prop_objs__[self] = self.__prop_cls__(client_object)
				return client_object.__prop_objs__[self]
		else:  # We are invoked on class
			return self.__prop_cls__


class AgentSectionBase(object):
	# Accept parent object from property descriptor
	def __init__(self, parent):
		self.__parent = parent

	# Proxy the parent's properties
	@property
	def _client(self):
		return self.__parent.client_session

	async def request(self, method, path, data=None, as_text=False,
					  params=None, **kwargs):
		"""Performs an asynchronous HTTP request to the admin endpoint for
		the given method and arguments.

		Args:
		    method (str): one of the HTTP methods to use.
		    path (str): relative path in the OpenAPI to send the request to.
		    data (dict): payload to send with the request in the `json` argument.
		    as_text (bool): when True, return the response as a `str`; otherwise,
		        return the deserialized JSON `dict`.
		"""
		return await self.__parent.admin_request(method, path, data, as_text, params, **kwargs)


class ClientSectionBase(object):
	# Accept parent object from property descriptor
	def __init__(self, parent):
		self.__parent = parent
		self.request = self.__parent.request

	# Proxy the parent's properties
	@property
	def _client(self):
		return self.__parent.client_session


def exhandler(function, parser):
    """If --examples was specified in 'args', the specified function
    is called and the application exits.
    :arg function: the function that prints the examples.
    :arg parser: the initialized instance of the parser that has the
      additional, script-specific parameters.
    """
    args = vars(bparser.parse_known_args()[0])
    if args["examples"]:
        function()
        return
    if args["verbose"]:
        from .msg import set_verbosity
        set_verbosity(args["verbose"])

    args.update(vars(parser.parse_known_args()[0]))
    return args

def _common_parser():
    """Returns a parser with common command-line options for all the scripts
    in the matdb suite.
    """
    import argparse
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--examples", action="store_true",
                        help="See detailed help and examples for this script.")
    parser.add_argument("--verbose", default=0, type=int,
                        help="See verbose output as the script runs.")
    parser.add_argument("--debug", action="store_true",
                        help="Print verbose calculation information for debugging.")

    return parser

bparser = _common_parser()
testmode = False
"""bool: when True, the package is operating in unit test mode, which changes
how plotting is handled.
"""
def set_testmode(testing):
    """Sets the package testing mode.
    """
    global testmode
    testmode = testing

debug = False
"""bool: when True, loggers throughout the `datacustodian` system are set to debug level
to produce more verbose logging output. Can also be `int` corresponding to level
in :mod:`logging`.
"""
def set_debug(debugging):
    """Sets the package testing mode.
    """
    global debug
    debug = debugging
