"""Auto-generated testing file by datacustodian; make sure to define request data
for each of the test functions created below.
"""
import pytest
from datacustodian.testing import urlsub
from urllib.parse import urlencode

{%- for nspec in namespaces %}
{%- for espec in nspec.endpoints %}
def test_{{ espec.name }}(client):
    {%- for route in espec.routes if route in testing[nspec.name]["endpoints"][espec.name].get("routes", espec.routes) %}
        {%- for sattr in espec if sattr in ["put", "get", "post", "delete"] %}
    {%- if nspec.name not in testing or espec.name not in testing[nspec.name]["endpoints"] %}
    raise NotImplementedError("Define the request arguments for this test!")
    {{ sattr }}_params = None
    {{ sattr }}_data = None
    {{ sattr }}_url = '/{{ name }}/{{ nspec.name }}{{ route }}'
    {%- else %}
    {%- if sattr in testing[nspec.name]["endpoints"][espec.name] %}
        {%- if testing[nspec.name]["endpoints"][espec.name][sattr]["url"] %}
    {{ sattr }}_url = urlsub('/{{ name }}/{{ nspec.name }}{{ route }}', {{ testing[nspec.name]["endpoints"][espec.name][sattr]["url"] }})
        {%- else %}
    {{ sattr }}_url = '/{{ name }}/{{ nspec.name }}{{ route }}'
        {%- endif %}
        {%- if testing[nspec.name]["endpoints"][espec.name][sattr]["params"] %}
    {{ sattr }}_params = {{ testing[nspec.name]["endpoints"][espec.name][sattr]["params"] }}
        {%- else %}
    {{ sattr }}_params = None
        {%- endif %}
        {%- if testing[nspec.name]["endpoints"][espec.name][sattr]["data"] %}
    {{ sattr }}_data = {{ testing[nspec.name]["endpoints"][espec.name][sattr]["data"] }}
        {%- else %}
    {{ sattr }}_data = None
        {%- endif %}
        {%- if testing[nspec.name]["endpoints"][espec.name][sattr]["preamble"] %}

    {{ testing[nspec.name]["endpoints"][espec.name][sattr]["preamble"]|wordwrap(80,wrapstring='\n    ') }}
    
        {%- endif %}
    {%- else %}
    {{ sattr }}_data = None
    {{ sattr }}_params = None
    {{ sattr }}_url = '/{{ name }}/{{ nspec.name }}{{ route }}'
    {%- endif %}
    {%- endif %}
    {%- if sattr in testing[nspec.name]["endpoints"][espec.name] and testing[nspec.name]["endpoints"][espec.name][sattr]["file"] %}
    {{ sattr }}_file = open('{{ testing[nspec.name]["endpoints"][espec.name][sattr]["file"] }}', 'rb')
    rv_{{ sattr }} = client.{{ sattr }}({{ sattr }}_url, query_string={{ sattr }}_params, data={{ sattr }}_file)
    {%- else %}
    rv_{{ sattr }} = client.{{ sattr }}({{ sattr }}_url, query_string={{ sattr }}_params, json={{sattr}}_data)
    {%- endif %}
    {%- if sattr in testing[nspec.name]["endpoints"][espec.name] and testing[nspec.name]["endpoints"][espec.name][sattr]["code"] %}
    assert rv_{{ sattr }}.status_code == {{ testing[nspec.name]["endpoints"][espec.name][sattr]["code"] }}
    {%- endif %}
        {% endfor %}
    {%- endfor %}

{%- endfor %}
{% endfor %}
