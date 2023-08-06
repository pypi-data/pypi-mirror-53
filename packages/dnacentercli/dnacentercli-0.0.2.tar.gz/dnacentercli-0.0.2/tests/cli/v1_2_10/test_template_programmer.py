import click
import pytest
from json import loads
from tests.environment import DNA_CENTER_VERSION
from tests.models.schema_validator import json_schema_validate
from dnacentersdk import mydict_data_factory


pytestmark = pytest.mark.skipif(DNA_CENTER_VERSION != '1.2.10', reason='version does not match')


# @pytest.mark.template_programmer
# def test_gets_the_templates_available(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'template-programmer', 'gets-the-templates-available', '''--filter_conflicting_templates=None''', '''--product_family=None''', '''--product_series=None''', '''--product_type=None''', '''--project_id=None''', '''--software_type=None''', '''--software_version=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_01b09a254b9ab259_v1_2_10').validate(obj) is None


# @pytest.mark.template_programmer
# def test_get_projects(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'template-programmer', 'get-projects', '''--name=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_109d1b4f4289aecd_v1_2_10').validate(obj) is None


# @pytest.mark.template_programmer
# def test_get_template_details(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'template-programmer', 'get-template-details', '''--template_id=templateID''', '''--latest_version=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_83a3b9404cb88787_v1_2_10').validate(obj) is None


# @pytest.mark.template_programmer
# def test_get_template_versions(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'template-programmer', 'get-template-versions', '''--template_id=templateID''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_c8bf6b65414a9bc7_v1_2_10').validate(obj) is None


# @pytest.mark.template_programmer
# def test_create_project(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'template-programmer', 'create-project', '''--createTime=None''', '''--description=None''', '''--id=None''', '''--lastUpdateTime=None''', '''--name='test_project'''', '''--tags=None''', '''--templates=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_00aec9b1422ab27e_v1_2_10').validate(obj) is None


# @pytest.mark.template_programmer
# def test_create_template(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'template-programmer', 'create-template', '''--project_id=filtered_project[0].id''', '''--author=None''', '''--composite=False''', '''--containingTemplates=[]''', '''--createTime=None''', '''--description=None''', '''--deviceTypes=[
#             {
#                 "productFamily": "Switches and Hubs",
#                 # "productSeries": "Cisco Catalyst 9300 Series Switches",
#                 # "productType": "Cisco Catalyst 9300 Switch"
#             }
#         ]''', '''--failurePolicy=None''', '''--id=None''', '''--lastUpdateTime=None''', '''--name='test_template'''', '''--parentTemplateId=None''', '''--projectId=None''', '''--projectName=None''', '''--rollbackTemplateContent=''''', '''--rollbackTemplateParams=[]''', '''--softwareType='IOS-XE'''', '''--softwareVariant='XE'''', '''--softwareVersion=None''', '''--tags=None''', '''--templateContent='show version\n'''', '''--templateParams=[]''', '''--version=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_f6b119ad4d4aaf16_v1_2_10').validate(obj) is None


# @pytest.mark.template_programmer
# def test_update_template(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'template-programmer', 'update-template', '''--author=None''', '''--composite=template.composite''', '''--containingTemplates=template.containingTemplates''', '''--createTime=None''', '''--description=None''', '''--deviceTypes=template.deviceTypes''', '''--failurePolicy=None''', '''--id=template.id''', '''--lastUpdateTime=None''', '''--name=template.name + '_updated'''', '''--parentTemplateId=None''', '''--projectId=template.projectId''', '''--projectName=None''', '''--rollbackTemplateContent=template.rollbackTemplateContent''', '''--rollbackTemplateParams=template.rollbackTemplateParams''', '''--softwareType=template.softwareType''', '''--softwareVariant=template.softwareVariant''', '''--softwareVersion=None''', '''--tags=None''', '''--templateContent=template.templateContent''', '''--templateParams=template.templateParams''', '''--version=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_7781fa0548a98342_v1_2_10').validate(obj) is None


# @pytest.mark.template_programmer
# def test_update_project(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'template-programmer', 'update-project', '''--createTime=None''', '''--description=None''', '''--id=filtered_project[0].id''', '''--lastUpdateTime=None''', '''--name=filtered_project[0].name + '_updated'''', '''--tags=None''', '''--templates=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_9480fa1f47ca9254_v1_2_10').validate(obj) is None


# @pytest.mark.template_programmer
# def test_version_template(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'template-programmer', 'version-template', '''--comments=None''', '''--templateId=template.id''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_62b05b2c40a9b216_v1_2_10').validate(obj) is None


# @pytest.mark.template_programmer
# def test_preview_template(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'template-programmer', 'preview-template', '''--params=None''', '''--templateId=template.id''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_f393abe84989bb48_v1_2_10').validate(obj) is None


# @pytest.mark.template_programmer
# def test_deploy_template(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'template-programmer', 'deploy-template', '''--forcePushTemplate=True''', '''--isComposite=template.composite''', '''--mainTemplateId=template.parentTemplateId''', '''--memberTemplateDeploymentInfo=None''', '''--targetInfo=[{'id': t.managementIpAddress,
#                    'type': 'MANAGED_DEVICE_IP'''', '''--'params': {}} for t in target]''', '''--templateId=template.id''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_6099da82477b858a_v1_2_10').validate(obj) is None


# @pytest.mark.template_programmer
# def test_get_template_deployment_status(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'template-programmer', 'get-template-deployment-status', '''--deployment_id=deploymentID''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_9c9a785741cbb41f_v1_2_10').validate(obj) is None


# @pytest.mark.template_programmer
# def test_delete_template(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'template-programmer', 'delete-template', '''--template_id=template.id''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_a7b42836408a8e74_v1_2_10').validate(obj) is None


# @pytest.mark.template_programmer
# def test_delete_project(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'template-programmer', 'delete-project', '''--project_id=filtered_project[0].id''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_d0a1abfa435b841d_v1_2_10').validate(obj) is None
