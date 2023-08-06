import click
import pytest
from json import loads
from tests.environment import DNA_CENTER_VERSION
from tests.models.schema_validator import json_schema_validate
from dnacentersdk import mydict_data_factory


pytestmark = pytest.mark.skipif(DNA_CENTER_VERSION != '1.2.10', reason='version does not match')


# @pytest.mark.clients
# def test_get_client_detail(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'clients', 'get-client-detail', '''--mac_address=devices.response[0].macAddress''', '''--timestamp=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_e2adba7943bab3e9_v1_2_10').validate(obj) is None


# @pytest.mark.clients
# def test_get_overall_client_health(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'clients', 'get-overall-client-health', '''--timestamp=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_149aa93b4ddb80dd_v1_2_10').validate(obj) is None
