import click
import pytest
from json import loads
from tests.environment import DNA_CENTER_VERSION
from tests.models.schema_validator import json_schema_validate
from dnacentersdk import mydict_data_factory


pytestmark = pytest.mark.skipif(DNA_CENTER_VERSION != '1.2.10', reason='version does not match')


# @pytest.mark.tag
# def test_create_tag(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'tag', 'create-tag', '''--description=None''', '''--dynamicRules=None''', '''--id=None''', '''--instanceTenantId=None''', '''--name='InterestingTool01'''', '''--systemTag=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_1399891c42a8be64_v1_2_10').validate(obj) is None


# @pytest.mark.tag
# def test_get_tag(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'tag', 'get-tag', '''--additional_info_attributes=None''', '''--additional_info_name_space=None''', '''--field=None''', '''--level=None''', '''--limit=None''', '''--name=None''', '''--offset=None''', '''--order='des'''', '''--size=None''', '''--sort_by='name'''', '''--system_tag=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_ee9aab01487a8896_v1_2_10').validate(obj) is None


# @pytest.mark.tag
# def test_get_tag_created(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'tag', 'get-tag-created', '''--additional_info_attributes=None''', '''--additional_info_name_space=None''', '''--field=None''', '''--level=None''', '''--limit=None''', '''--name='InterestingTool01'''', '''--offset=None''', '''--order=None''', '''--size=None''', '''--sort_by=None''', '''--system_tag=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_ee9aab01487a8896_v1_2_10').validate(obj) is None


# @pytest.mark.tag
# def test_get_tag_by_id(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'tag', 'get-tag-by-id', '''--id=get_tag(api).response[0].id''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_c1a359b14c89b573_v1_2_10').validate(obj) is None


# @pytest.mark.tag
# def test_get_tag_by_id_created(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'tag', 'get-tag-by-id-created', '''--id=get_tag_created(api).response[0].id''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_c1a359b14c89b573_v1_2_10').validate(obj) is None


# @pytest.mark.tag
# def test_get_tag_count(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'tag', 'get-tag-count', '''--attribute_name=None''', '''--level=None''', '''--name=None''', '''--name_space=None''', '''--size=None''', '''--system_tag=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_8091a9b84bfba53b_v1_2_10').validate(obj) is None


# @pytest.mark.tag
# def test_get_tag_resource_types(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'tag', 'get-tag-resource-types', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_4695090d403b8eaa_v1_2_10').validate(obj) is None


# @pytest.mark.tag
# def test_get_tag_member_count(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'tag', 'get-tag-member-count', '''--id=get_tag(api).response[0].id''', '''--member_type=get_tag_resource_types(api).response[0]''', '''--level='0'''', '''--member_association_type=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_2e9db85840fbb1cf_v1_2_10').validate(obj) is None


# @pytest.mark.tag
# def test_updates_tag_membership(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'tag', 'updates-tag-membership', '''--memberToTags={key: [tag]}''', '''--memberType='networkdevice'''', '''--payload=None''', '''--active_validation=False'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_45bc7a8344a8bc1e_v1_2_10').validate(obj) is None


# @pytest.mark.tag
# def test_add_members_to_the_tag(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'tag', 'add-members-to-the-tag', '''--id=get_tag_created(api).response[0].id''', '''--payload={
#            "networkdevice": [api.devices.get_device_list().response[0].id]
#        }''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_00a2fa6146089317_v1_2_10').validate(obj) is None


# @pytest.mark.tag
# def test_get_tag_members_by_id(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'tag', 'get-tag-members-by-id', '''--id=get_tag_created(api).response[0].id''', '''--member_type=get_tag_resource_types(api).response[0]''', '''--level='0'''', '''--limit=None''', '''--member_association_type=None''', '''--offset=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_eab7abe048fb99ad_v1_2_10').validate(obj) is None


# @pytest.mark.tag
# def test_update_tag(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'tag', 'update-tag', '''--description=None''', '''--dynamicRules=None''', '''--id=tag.id''', '''--instanceTenantId=None''', '''--name='{} Updated'.format(tag.name)''', '''--systemTag=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_4d86a993469a9da9_v1_2_10').validate(obj) is None


# @pytest.mark.tag
# def test_remove_tag_member(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'tag', 'remove-tag-member', '''--id=tag.id''', '''--member_id=device.id''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_caa3ea704d78b37e_v1_2_10').validate(obj) is None


# @pytest.mark.tag
# def test_delete_tag(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'tag', 'delete-tag', '''--id=tag.id''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_429c28154bdaa13d_v1_2_10').validate(obj) is None
