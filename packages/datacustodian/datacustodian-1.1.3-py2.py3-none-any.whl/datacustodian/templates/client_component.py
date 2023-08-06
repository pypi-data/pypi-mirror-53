"""Auto-generated module for the datacustodian package that creates a customized
HTTP client for a component in the endpoint app.
"""
from aiohttp import StreamReader
from contextlib import asynccontextmanager
import logging

from datacustodian.base import ClientSectionBase
from datacustodian.testing import urlsub
{%- macro route_to_signature(routevars) %}
    {%- for entry in routevars %}
                {{ entry }},
    {%- endfor -%}
{%- endmacro %}
{%- macro route_to_subdict(routevars) -%}
    {%- for entry in routevars %}
            '{{ entry }}': {{ entry }},
    {%- endfor -%}
{%- endmacro %}
{%- macro model_to_params(model) -%}
    {%- if model is not string %}
    {%- set m = model %}
    {%- else %}
    {%- set m = model_dict[model] %}
    {%- endif %}
    {%- for entry, data in m.properties.items() %}
            '{{ entry }}' = {{ entry }},
    {%- endfor %}
{%- endmacro %}
{%- macro model_to_subdict(model) -%}
    {%- if model is not string %}
    {%- set m = model %}
    {%- else %}
    {%- set m = model_dict[model] %}
    {%- endif %}
    {%- for entry, data in m.properties.items() %}
            '{{ entry }}': {{ entry }},
    {%- endfor %}
{%- endmacro %}
{%- macro model_to_signature(model, routevars) -%}
    {%- if model is not string %}
    {%- set m = model %}
    {%- else %}
    {%- set m = model_dict[model] %}
    {%- endif %}
    {%- for entry, data in m.properties.items() %}
    {%- if entry not in routevars %}
    {%- if data.get("required", False) %}
                {{ entry }},
    {%- else %}
    {%- set arg = data.get("default", None) %}
    {%- if arg is string %}
                {{ entry }}="{{ arg }}",
    {%- else %}
                {{ entry }}={{ arg }},
    {%- endif %}
    {%- endif %}
    {%- endif %}
    {%- endfor %}
{%- endmacro %}
{%- macro model_to_docstring(model) -%}
    {%- if model is not string %}
    {%- set m = model %}
    {%- else %}
    {%- set m = model_dict[model] %}
    {%- endif %}
    {%- for entry, data in m.properties.items() %}
            {{ entry }}: {{ data.get('description', '') }}
    {%- endfor -%}
{%- endmacro -%}
{%- macro make_signature(routevars, pobject, eobject) %}
    {{ route_to_signature(routevars) }}{%- if pobject|length > 0 -%}
    {{ model_to_signature(pobject.object, routevars) }}
    {%- endif %}
    {%- if eobject|length > 0 -%}
    {{ model_to_signature(eobject.object, routevars) }}
    {%- endif %}
{%- endmacro %}

# from ..{{ name }} import models, parsers, ns_specs, namespaces

log = logging.getLogger(__name__)

{% for nspec in namespaces %}
class {{ nspec.name|title }}Section(ClientSectionBase):
{%- for espec in nspec.endpoints %}
    {%- set routevars = espec.routes | route2vars %}
    {%- set routefun = espec.routes[0]|route2fun %}
    {%- for sattr in espec if sattr in ["put", "get", "post", "delete"] %}
    {%- set pobject = espec[sattr].get("params", {}) %}
    {%- set eobject = espec[sattr].get("expect", {}) %}
    @asynccontextmanager
    async def {{sattr}}{{routefun}}(self,{{ make_signature(routevars, pobject, eobject) }} **kwargs):
        """Queries the `{{ espec.routes[0] }}` endpoint. {{ espec[sattr].docstring }}
        Args:
        {%- if espec[sattr].params -%}
        {{ model_to_docstring(espec[sattr].params.object) }}
        {%- endif -%}
        {%- if espec[sattr].expect -%}
        {{ model_to_docstring(espec[sattr].expect.object) }}
        {%- endif %}
        """
        {%- if espec[sattr].params %}
        params = {
            {{ model_to_subdict(espec[sattr].params.object) }}
        }
        {%- else %}
        params = None
        {%- endif %}
        {%- if espec[sattr].expect %}
        body = {
            {{ model_to_subdict(espec[sattr].expect.object) }}
        }
        {%- else %}
        body = None
        {%- endif %}

        url = urlsub("/{{name}}/{{nspec.name}}{{ espec.routes[0] }}", {
        {{ route_to_subdict(routevars) }}
        })
        didauth = {{ espec[sattr].get("didauth", "False") }}
        async with self.request("{{ sattr|upper }}", url, params=params, data=body, didauth=didauth, **kwargs) as r:
            yield r

    {% endfor %}
{%- endfor %}
{%- endfor %}
