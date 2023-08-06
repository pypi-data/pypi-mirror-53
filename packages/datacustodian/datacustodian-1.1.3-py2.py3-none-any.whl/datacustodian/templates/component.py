"""Auto-generated module for the datacustodian package that creates a customized
component for a flask app.
"""
{%- macro model_to_params(model, location="query") -%}
    {%- for entry, data in model.properties.items() %}
    @api.param('{{ entry }}', """{{ data.get('description', '') }}""", __in="{{ location }}",
               required={{ data.get("required", False)}}, default='{{ data.get("default", None) }}')
    {%- endfor %}
{%- endmacro %}
import sys
import logging
from flask import Blueprint, request, abort
from flask_restplus import Resource
from asyncio import iscoroutinefunction, run_coroutine_threadsafe
from werkzeug.exceptions import Forbidden

from datacustodian.utility import import_fqn, decode_request_data
from datacustodian.api import create_parsers, Schema, apis
from datacustodian.settings import specs
from datacustodian.consent.auth import auth_endpoint_roles

log = logging.getLogger(__name__)

blueprint = Blueprint('{{ name }}',
                      '{{ package.name }}.{{ name }}',
                      url_prefix='{{ url_prefix }}')
"""Blueprint: component-level modularization of component for a global flask app.
"""
api = apis["{{ name }}"]
"""flask_restplus.Api: api object to handle the blueprint for this component.
"""
api.init_app(blueprint)

model_specs = specs["{{ name }}"]["models"]
"""list: of model spec `dict` instances with raw model schemas"""
models = Schema()
"""Schema: model schema definitions for the component.
"""
models.load("{{ name }}", model_specs)

parsers = create_parsers(specs["{{ name }}"].parsers)
"""dict: keys are parser names, values are :class:`flask_restplus.RequestParser`.
"""

ns_specs = specs["{{ name }}"].namespaces
"""dict: keys are namespace names; values are the raw specification `dict` for
that namespace.
"""
namespaces = {}
"""dict: keys are namespace names, values are :class:`flask_restplus.Namespace`
objects.
"""
event_loop = None
"""asyncio.AbstractEventLoop: the event loop running the main program on the
main thread. Used to schedule threadsafe execution of asynchronous functions
from these endpoints.
"""

def set_event_loop(loop):
    """Sets a reference to the event loop of the main thread for this component
    to use in calling asynchronous coroutines.

    Args:
        loop (asyncio.AbstractEventLoop): the event loop running the main
            program on the main thread.
    """
    global event_loop
    event_loop = loop

def _run(f, timeout=10.):
    """Runs the specified coroutine in a threadsafe call on the global event_loop.
    """
    future = run_coroutine_threadsafe(f, event_loop)
    return future.result(timeout)

for nspec in ns_specs:
    namespaces[nspec.name] = api.namespace(nspec.name)
{% for nspec in namespaces %}
ns_{{ nspec.name }} = namespaces["{{ nspec.name }}"]
{% endfor %}
#Reinitialize the keyword arguments for the namespace; these just affect
#attributes on the namespace object, which will retain its pointer.
_nspeclookup = {s.name: s for s in ns_specs}
for nsname, ns in namespaces.items():
    nspec = _nspeclookup[nsname]
    ns.description = nspec.get("description", None)
    ns._path = nspec.get("path", None)
    ns._validate = nspec.get("validate", None)
    ns.decorators = nspec.get("decorators", [])
    ns.authorizations = nspec.get("authorizations", None)
    ns.ordered = nspec.get("ordered", False)

def _get_expectant(name):
    """Returns a parser with the given name, if it exists. If it doesn't,
    attempts to get a *model* with that name. If no model exists, an error
    is raised.
    """
    return parsers.get(name, models.get(name))
{% for nspec in namespaces %}
{%- for espec in nspec.endpoints %}
{%- if espec.agent %}
{{ espec.name }}_agent = '{{ espec.agent }}'
{%- else %}
{{ espec.name }}_agent = None
{%- endif %}
@ns_{{ nspec.name }}.route(*{{ espec.routes }})
class {{ espec.name|title }}(Resource):
    {%- for sattr in espec if sattr in ["put", "get", "post", "delete"] %}
    {%- if espec[sattr].expect %}
    @api.expect(_get_expectant("{{ espec[sattr].expect.object }}"),
                validate={{"True" if espec[sattr].expect.validate else "False"}})
    {%- endif %}
    {%- if espec[sattr].params %}
    {{ model_to_params(espec[sattr].params.object, espec[sattr].params.get("location", "query")) }}
    {%- endif %}
    {%- if espec[sattr].marshal %}
    @api.marshal_with(models["{{ espec[sattr].marshal.object }}"],
                      {%- if espec[sattr].marshal.envelope %}
                      envelope="{{ espec[sattr].marshal.envelope }}",
                      {%- endif %}
                      skip_none={{"True" if espec[sattr].marshal.skip_none else "False"}})
    {%- endif %}
    {%- if espec[sattr].response %}
    @api.response({{ espec[sattr].response.code }}, "{{ espec[sattr].response.message }}")
    {%- endif %}
    def {{ sattr }}(ns, *args, **kwargs):
        """{{ espec[sattr].docstring }}
        """
        {%- set rolelist = espec[sattr].get("roles", espec.get("roles", [])) %}
        {%- set credlist = espec[sattr].get("credentials", espec.get("credentials", [])) %}
        {%- set didauth = espec[sattr].get("didauth", espec.get("didauth", False)) %}
        {%- if rolelist|length > 0 or credlist|length > 0 or didauth %}
        if not _run(auth_endpoint_roles({{ rolelist }},
                                        request.headers, request.method, request.path, {{espec.name}}_agent,
                                        {{ credlist }})):
            raise Forbidden("Signature or DID-auth role verification failed; cannot execute endpoint.")
        {%- endif %}

        {%-if espec[sattr].expect %}
        if "{{ espec[sattr].expect.object }}" in parsers: #pragma: no cover
            kwargs = parsers["{{ espec[sattr].expect.object }}"].parse_args(request)
        {%- else %}
        kwargs.update({{ espec[sattr].function.get("kwargs", {}) }})
        {%- endif %}
        if request.json is not None:
            kwargs["_data"] = request.json
        else:
            kwargs["_data"] = request.data
        kwargs["_data"] = decode_request_data(kwargs["_data"])
        kwargs["_request"] = request
        kwargs["_agent"] = {{ espec.name }}_agent

        mod, call = import_fqn("{{ espec[sattr].function.fqn }}")
        if iscoroutinefunction(call):
            results = _run(call(*args, **kwargs), {{ espec[sattr].function.get("timeout", 10) }})
        else:
            results = call(*args, **kwargs)
        {%- if espec[sattr].response %}
        return results, {{ espec[sattr].response.code }}
        {% else %}
        return results
        {%- endif %}
    {% endfor %}
{%- endfor %}
{% endfor %}

for nspec in ns_specs:
    api.add_namespace(namespaces[nspec.name])
