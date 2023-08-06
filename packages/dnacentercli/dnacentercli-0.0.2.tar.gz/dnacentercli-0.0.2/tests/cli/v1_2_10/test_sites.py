import click
import pytest
from json import loads
from tests.environment import DNA_CENTER_VERSION
from tests.models.schema_validator import json_schema_validate
from dnacentersdk import mydict_data_factory


pytestmark = pytest.mark.skipif(DNA_CENTER_VERSION != '1.2.10', reason='version does not match')


# @pytest.mark.sites
# def test_get_site_health(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'sites', 'get-site-health', '''--timestamp=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_17a82ac94cf99ab0_v1_2_10').validate(obj) is None


# @pytest.mark.sites
# def test_create_site(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'sites', 'create-site', '''--site=None''', '''--type=None''', '''--payload={
#             'type': 'building',
#             'site': {
#                 'building': {
#                     'name': 'Test_Building',
#                     'address': '10.10.22.70'
#                 }
#             }
#         }''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_50b589fd4c7a930a_v1_2_10').validate(obj) is None


# @pytest.mark.sites
# def test_assign_device_to_site(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'sites', 'assign-device-to-site', '''--site_id=siteId''', '''--device=[{'ip': device.managementIpAddress}]''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_eeb168eb41988e07_v1_2_10').validate(obj) is None
