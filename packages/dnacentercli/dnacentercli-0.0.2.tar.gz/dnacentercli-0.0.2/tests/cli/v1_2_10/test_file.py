import click
import pytest
from json import loads
from tests.environment import DNA_CENTER_VERSION
from tests.models.schema_validator import json_schema_validate
from dnacentersdk import mydict_data_factory


pytestmark = pytest.mark.skipif(DNA_CENTER_VERSION != '1.2.10', reason='version does not match')


# @pytest.mark.file
# def test_get_list_of_available_namespaces(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'file', 'get-list-of-available-namespaces', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_3f89bbfc4f6b8b50_v1_2_10').validate(obj) is None


# @pytest.mark.file
# def test_get_list_of_files(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'file', 'get-list-of-files', '''--name_space=get_list_of_available_namespaces(api).response[0]''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_42b6a86e44b8bdfc_v1_2_10').validate(obj) is None


# @pytest.mark.file
# def test_download_a_file_by_fileid(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'file', 'download-a-file-by-fileid', '''--file_id=get_list_of_files(api).response[0].id''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_9698c8ec4a0b8c1a_v1_2_10').validate(obj) is None
