"""Auto-generated testing file by datacustodian; make sure to define request data
for each of the test functions created below.
"""
import pytest
{% for nspec in namespaces %}
{%- for espec in nspec.endpoints %}
def test_{{ espec.name }}(client):
    {%- for route in espec.routes %}
        {%- for sattr in espec if sattr in ["put", "get", "post", "delete"] %}
    {%- if not espec[sattr].testing %}
    raise NotImplementedError("Define the request arguments for this test!")
    {{ sattr }}_params = None
    {{ sattr }}_data = None    
    {%- else %}
        {%- if espec[sattr].testing.params %}
    {{ sattr }}_params = espec[sattr].testing.params
        {%- else %}
    {{ sattr }}_params = None
        {%- endif %}
        {%- if espec[sattr].testing.data %}
    {{ sattr }}_data = espec[sattr].testing.data
        {%- else %}
    {{ sattr }}_data = None
        {%- endif %}
    {%- endif %}
    rv_{{ sattr }} = client.{{ sattr }}('{{ route }}', params={{sattr}}_params, data={{sattr}}_data)
    assert rv_{{ sattr }}.data
        {% endfor %}
    {%- endfor %}

{%- endfor %}
{% endfor %}
