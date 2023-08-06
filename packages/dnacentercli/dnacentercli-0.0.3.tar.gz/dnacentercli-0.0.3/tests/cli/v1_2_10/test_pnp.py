import click
import pytest
from json import loads
from tests.environment import DNA_CENTER_VERSION
from tests.models.schema_validator import json_schema_validate
from dnacentersdk import mydict_data_factory
from tests.config import (NEW_VIRTUAL_ACCOUNT_PAYLOAD)


pytestmark = pytest.mark.skipif(DNA_CENTER_VERSION != '1.2.10', reason='version does not match')


# @pytest.mark.pnp
# def test_get_smart_account_list(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'get-smart-account-list', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_3cb24acb486b89d2_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_get_virtual_account_list(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'get-virtual-account-list', '''--domain=get_smart_account_list(api)[0]''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_70a479a6462a9496_v1_2_10').validate(obj) is None


# @pytest.mark.skipif(not all([NEW_VIRTUAL_ACCOUNT_PAYLOAD]) is True,
#                     reason="tests.config values required not present")
# @pytest.mark.pnp
# def test_add_virtual_account(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'add-virtual-account', '''--autoSyncPeriod=None''', '''--ccoUser=None''', '''--expiry=None''', '''--lastSync=None''', '''--profile=None''', '''--smartAccountId=None''', '''--syncResult=None''', '''--syncResultStr=None''', '''--syncStartTime=None''', '''--syncStatus=None''', '''--tenantId=None''', '''--token=None''', '''--virtualAccountId=None''', '''--payload=NEW_VIRTUAL_ACCOUNT_PAYLOAD''', '''--active_validation=False'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_1e962af345b8b59f_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_get_sync_result_for_virtual_account(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'get-sync-result-for-virtual-account', '''--domain=get_smart_account_list(api)[0]''', '''--name=get_virtual_account_list(api)[0]''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_0a9c988445cb91c8_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_update_pnp_server_profile(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'update-pnp-server-profile', '''--autoSyncPeriod=None''', '''--ccoUser=None''', '''--expiry=None''', '''--lastSync=None''', '''--profile=None''', '''--smartAccountId=None''', '''--syncResult=None''', '''--syncResultStr=None''', '''--syncStartTime=None''', '''--syncStatus=None''', '''--tenantId=None''', '''--token=None''', '''--virtualAccountId=None''', '''--payload=get_sync_result_for_virtual_account(api)''', '''--active_validation=False'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_6f9819e84178870c_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_sync_virtual_account_devices(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'sync-virtual-account-devices', '''--autoSyncPeriod=None''', '''--ccoUser=None''', '''--expiry=None''', '''--lastSync=None''', '''--profile=None''', '''--smartAccountId=None''', '''--syncResult=None''', '''--syncResultStr=None''', '''--syncStartTime=None''', '''--syncStatus=None''', '''--tenantId=None''', '''--token=None''', '''--virtualAccountId=None''', '''--payload=get_sync_result_for_virtual_account(api)''', '''--active_validation=False'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_a4b6c87a4ffb9efa_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_deregister_virtual_account(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'deregister-virtual-account', '''--domain=get_smart_account_list(api)[0]''', '''--name=get_virtual_account_list(api)[0]''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_2499e9ad42e8ae5b_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_get_workflow_count(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'get-workflow-count', '''--name=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_7989f86846faaf99_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_get_workflows(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'get-workflows', '''--limit=None''', '''--name=None''', '''--offset=None''', '''--sort='addedOn'''', '''--sort_order='des'''', '''--type=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_aeb4dad04a99bbe3_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_get_pnp_global_settings(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'get-pnp-global-settings', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_7e92f9eb46db8320_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_update_pnp_global_settings(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'update-pnp-global-settings', '''--_id=None''', '''--aaaCredentials=None''', '''--acceptEula=None''', '''--defaultProfile=None''', '''--savaMappingList=None''', '''--taskTimeOuts=None''', '''--tenantId=None''', '''--version=None''', '''--payload=get_pnp_global_settings(api)''', '''--active_validation=False'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_8da0391947088a5a_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_get_device_count(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'get-device-count', '''--cm_state=None''', '''--last_contact=None''', '''--name=None''', '''--onb_state=None''', '''--pid=None''', '''--project_id=None''', '''--project_name=None''', '''--serial_number=None''', '''--smart_account_id=None''', '''--source=None''', '''--state=None''', '''--virtual_account_id=None''', '''--workflow_id=None''', '''--workflow_name=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_d9a1fa9c4068b23c_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_import_devices_in_bulk(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'import-devices-in-bulk', '''--payload=[{
#             "deviceInfo": {
#                 "serialNumber": "c3160d2650",
#                 "name": "Test device c3160d2650"
#             }
#         }]''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_21a6db2540298f55_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_get_device_list(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'get-device-list', '''--cm_state=None''', '''--last_contact=None''', '''--limit=1''', '''--name=None''', '''--offset=None''', '''--onb_state=None''', '''--pid=None''', '''--project_id=None''', '''--project_name=None''', '''--serial_number=None''', '''--smart_account_id=None''', '''--sort=None''', '''--sort_order=None''', '''--source=None''', '''--state=None''', '''--virtual_account_id=None''', '''--workflow_id=None''', '''--workflow_name=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_e6b3db8046c99654_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_get_device_by_id(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'get-device-by-id', '''--id=get_device_list(api)[0].id''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_bab6c9e5440885cc_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_get_device_history(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'get-device-history', '''--serial_number=get_device_list(api)[0].deviceInfo.serialNumber''', '''--sort=None''', '''--sort_order=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_f09319674049a7d4_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_add_device_2(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'add-device-2', '''--_id=None''', '''--deviceInfo={'serialNumber': 'FJC2048D0HX'''', '''--'name': 'catalyst_ap_test'''', '''--'pid': 'ISR4431-SEC/K9'}''', '''--runSummaryList=None''', '''--systemResetWorkflow=None''', '''--systemWorkflow=None''', '''--tenantId=None''', '''--version=None''', '''--workflow=None''', '''--workflowParameters=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_f3b26b5544cabab9_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_preview_config(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'preview-config', '''--deviceId=api.pnp.get_device_list(name='catalyst_ap_test')[0].id''', '''--siteId=siteId''', '''--type='Default'''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_cf9418234d9ab37e_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_claim_a_device_to_a_site(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'claim-a-device-to-a-site', '''--deviceId=None''', '''--siteId=None''', '''--type=None''', '''--payload={
#             "siteId": siteId,
#             "deviceId": deviceId,
#             "type": "Default",
#             "imageInfo": {"imageId": ""''', '''--"skip": False},
#             "configInfo": {"configId": ""''', '''--"configParameters": []}
#         }''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_5889fb844939a13b_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_delete_device_by_id_from_pnp_imported(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'delete-device-by-id-from-pnp-imported', '''--id=api.pnp.get_device_list(name='Test device c3160d2650')[0].id''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_cdab9b474899ae06_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_add_device(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'add-device', '''--_id=None''', '''--deviceInfo={'serialNumber': 'd2650c3160'''', '''--'name': 'Test device d2650c3160'}''', '''--runSummaryList=None''', '''--systemResetWorkflow=None''', '''--systemWorkflow=None''', '''--tenantId=None''', '''--version=None''', '''--workflow=None''', '''--workflowParameters=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_f3b26b5544cabab9_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_update_device(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'update-device', '''--id=api.pnp.get_device_list(name='Test device d2650c3160')[0].id''', '''--_id=None''', '''--deviceInfo={'name': 'Test device d2650c3160-1'}''', '''--runSummaryList=None''', '''--systemResetWorkflow=None''', '''--systemWorkflow=None''', '''--tenantId=None''', '''--version=None''', '''--workflow=None''', '''--workflowParameters=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_09b0f9ce4239ae10_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_add_a_workflow(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'add-a-workflow', '''--_id=None''', '''--addToInventory=None''', '''--addedOn=None''', '''--configId=None''', '''--currTaskIdx=None''', '''--description='test_devnet_1'''', '''--endTime=None''', '''--execTime=None''', '''--imageId=None''', '''--instanceType=None''', '''--lastupdateOn=None''', '''--name='test_devnet_1'''', '''--startTime=None''', '''--state=None''', '''--tasks=[{
#             'taskSeqNo': 0,
#             'name': 'Config Download',
#             'type': 'Config',
#             'startTime': 0,
#             'endTime': 0,
#             'timeTaken': 0,
#             'currWorkItemIdx': 0,
#             'configInfo': {
#                 'configId': template.id,
#                 'configFileUrl': None,
#                 'fileServiceId': None,
#                 'saveToStartUp': True,
#                 'connLossRollBack': True,
#                 'configParameters': None
#             }
#         }]''', '''--tenantId=None''', '''--type='Standard'''', '''--useState='Available'''', '''--version=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_848b5a7b4f9b8c12_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_get_workflow_by_id(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'get-workflow-by-id', '''--id=get_workflows(api)[0].id''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_80acb88e4ac9ac6d_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_update_workflow(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'update-workflow', '''--id=workflow.id''', '''--_id=None''', '''--addToInventory=None''', '''--addedOn=None''', '''--configId=None''', '''--currTaskIdx=None''', '''--description=workflow.description''', '''--endTime=None''', '''--execTime=None''', '''--imageId=None''', '''--instanceType=None''', '''--lastupdateOn=None''', '''--name=workflow.name''', '''--startTime=None''', '''--state=None''', '''--tasks=workflow.tasks''', '''--tenantId=None''', '''--type=workflow.type''', '''--useState=workflow.useState''', '''--version=None''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_3086c9624f498b85_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_claim_device(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'claim-device', '''--configFileUrl=None''', '''--configId=None''', '''--deviceClaimList=[
#             {
#                 "configList": configList,
#                 "deviceId": deviceId
#             }
#         ]''', '''--fileServiceId=None''', '''--imageId=None''', '''--imageUrl=None''', '''--populateInventory=None''', '''--projectId=None''', '''--workflowId=workflow.id''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_d8a619974a8a8c48_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_un_claim_device(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'un-claim-device', '''--deviceIdList=[deviceId]''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_0b836b7b4b6a9fd5_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_reset_device(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'reset-device', '''--deviceResetList=[{"deviceId": deviceId''', '''--"configList": [workflow.tasks[0].configInfo]}]''', '''--projectId=None''', '''--workflowId=workflow.id''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_9e857b5a4a0bbcdb_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_delete_workflow_by_id(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'delete-workflow-by-id', '''--id=api.pnp.get_workflows(name='test_devnet_1')[0].id''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_af8d7b0e470b8ae2_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_delete_device_by_id_from_pnp_added(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'delete-device-by-id-from-pnp-added', '''--id=api.pnp.get_device_list(name='Test device d2650c3160-1')[0].id''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_cdab9b474899ae06_v1_2_10').validate(obj) is None


# @pytest.mark.pnp
# def test_delete_device_by_id_from_pnp_added_2(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'pnp', 'delete-device-by-id-from-pnp-added-2', '''--id=api.pnp.get_device_list(name='catalyst_ap_test')[0].id''', '''--payload=None''', '''--active_validation=True'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_cdab9b474899ae06_v1_2_10').validate(obj) is None
