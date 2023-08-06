import click
import pytest
from json import loads
from tests.environment import DNA_CENTER_VERSION
from tests.models.schema_validator import json_schema_validate
from dnacentersdk import mydict_data_factory
from tests.environment import (
    DNA_CENTER_USERNAME, DNA_CENTER_PASSWORD,
    DNA_CENTER_ENCODED_AUTH
)


pytestmark = pytest.mark.skipif(DNA_CENTER_VERSION != '1.2.10', reason='version does not match')


# @pytest.mark.authentication
# def test_authentication_api(runner, cli, auth_options):
#     result = runner.invoke(cli, ['v1-2-10', *auth_options, 'authentication', 'authentication-api', '''--username=DNA_CENTER_USERNAME''', '''--password=DNA_CENTER_PASSWORD''', '''--encoded_auth=DNA_CENTER_ENCODED_AUTH'''])
#     assert not result.exception
#     if result.output.strip():
#         obj = loads(result.output)
#         assert json_schema_validate('jsd_ac8ae94c4e69a09d_v1_2_10').validate(obj) is None
