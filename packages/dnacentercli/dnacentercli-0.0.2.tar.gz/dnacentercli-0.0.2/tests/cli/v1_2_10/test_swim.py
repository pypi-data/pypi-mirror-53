import click
import pytest
from json import loads
from tests.environment import DNA_CENTER_VERSION
from tests.models.schema_validator import json_schema_validate
from dnacentersdk import mydict_data_factory
from tests.config import LOCAL_SOFTWARE_IMAGE_PATH, LOCAL_SOFTWARE_IMAGE_NAME
from tests.config import DEFAULT_BASE_URL
from .test_file import get_list_of_files
from .test_devices import get_device_list


pytestmark = pytest.mark.skipif(DNA_CENTER_VERSION != '1.2.10', reason='version does not match')


# @pytest.mark.swim
# def test_get_software_image_details(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'swim', 'get-software-image-details', '''--application_type=None''', '''--created_time=None''', '''--family=None''', '''--image_integrity_status=None''', '''--image_name=None''', '''--image_series=None''', '''--image_size_greater_than=None''', '''--image_size_lesser_than=None''', '''--image_uuid=None''', '''--is_cco_latest=None''', '''--is_cco_recommended=None''', '''--is_tagged_golden=None''', '''--limit=None''', '''--name=None''', '''--offset=None''', '''--sort_by=None''', '''--sort_order='asc'''', '''--version=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_0c8f7a0b49b9aedd_v1_2_10').validate(obj) is None


# @pytest.mark.skipif(not all([LOCAL_SOFTWARE_IMAGE_PATH, LOCAL_SOFTWARE_IMAGE_PATH]) is True,
#                     reason="tests.config values required not present")
# @pytest.mark.swim
# def test_import_local_software_image(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'swim', 'import-local-software-image', '''--is_third_party=None''', '''--third_party_application_type=None''', '''--third_party_image_family=None''', '''--third_party_vendor=None''', '''--multipart_fields={'file': (LOCAL_SOFTWARE_IMAGE_NAME,
#                                    open(LOCAL_SOFTWARE_IMAGE_PATH''', '''--'rb'))}''', '''--multipart_monitor_callback=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_4dbe3bc743a891bc_v1_2_10').validate(obj) is None


# @pytest.mark.skipif(not all([DEFAULT_BASE_URL]) is True,
#                     reason="tests.config values required not present")
# @pytest.mark.swim
# def test_import_software_image_via_url(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'swim', 'import-software-image-via-url', '''--schedule_at=None''', '''--schedule_desc=None''', '''--schedule_origin=None''', '''--payload=[{
#             'applicationType': image_details.applicationType,
#             'vendor': image_details.vendor,
#             'imageFamily': image_details.family,
#             'sourceURL': DEFAULT_BASE_URL + '/dna/intent/api/v1/' + files
#         }]''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_bc8aab4746ca883d_v1_2_10').validate(obj) is None


# @pytest.mark.swim
# def test_trigger_software_image_activation(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'swim', 'trigger-software-image-activation', '''--schedule_validate=None''', '''--payload=[{
#             'activateLowerImageVersion': True,
#             'deviceUuid': get_device_list(api).response[0].id,
#             'distributeIfNeeded': True,
#             'imageUuidList': [get_software_image_details(api).response[0].imageUuid],
#         }]''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_fb9beb664f2aba4c_v1_2_10').validate(obj) is None


# @pytest.mark.swim
# def test_trigger_software_image_distribution(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'swim', 'trigger-software-image-distribution', '''--payload=[{
#             'deviceUuid': get_device_list(api).response[0].id,
#             'imageUuid': get_software_image_details(api).response[0].imageUuid
#         }]''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_8cb6783b4faba1f4_v1_2_10').validate(obj) is None
