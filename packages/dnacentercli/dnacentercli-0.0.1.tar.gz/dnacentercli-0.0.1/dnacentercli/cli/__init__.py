# -*- coding: utf-8 -*-
import click
import urllib3
from dnacentersdk import config, DNACenterAPI
from .utils.spinner import (
    init_spinner,
    start_spinner,
    stop_spinner,
)
from .utils.print import (
    tbprint,
    eprint,
    oprint,
    opprint,
)

from .v1_2_10.clients import \
    clients as v1_2_10_clients
from .v1_2_10.command_runner import \
    command_runner as v1_2_10_command_runner
from .v1_2_10.devices import \
    devices as v1_2_10_devices
from .v1_2_10.fabric_wired import \
    fabric_wired as v1_2_10_fabric_wired
from .v1_2_10.file import \
    file as v1_2_10_file
from .v1_2_10.network_discovery import \
    network_discovery as v1_2_10_network_discovery
from .v1_2_10.networks import \
    networks as v1_2_10_networks
from .v1_2_10.non_fabric_wireless import \
    non_fabric_wireless as v1_2_10_non_fabric_wireless
from .v1_2_10.path_trace import \
    path_trace as v1_2_10_path_trace
from .v1_2_10.pnp import \
    pnp as v1_2_10_pnp
from .v1_2_10.swim import \
    swim as v1_2_10_swim
from .v1_2_10.site_profile import \
    site_profile as v1_2_10_site_profile
from .v1_2_10.sites import \
    sites as v1_2_10_sites
from .v1_2_10.tag import \
    tag as v1_2_10_tag
from .v1_2_10.task import \
    task as v1_2_10_task
from .v1_2_10.template_programmer import \
    template_programmer as v1_2_10_template_programmer
from .v1_3_0.clients import \
    clients as v1_3_0_clients
from .v1_3_0.command_runner import \
    command_runner as v1_3_0_command_runner
from .v1_3_0.devices import \
    devices as v1_3_0_devices
from .v1_3_0.fabric_wired import \
    fabric_wired as v1_3_0_fabric_wired
from .v1_3_0.file import \
    file as v1_3_0_file
from .v1_3_0.network_discovery import \
    network_discovery as v1_3_0_network_discovery
from .v1_3_0.networks import \
    networks as v1_3_0_networks
from .v1_3_0.non_fabric_wireless import \
    non_fabric_wireless as v1_3_0_non_fabric_wireless
from .v1_3_0.path_trace import \
    path_trace as v1_3_0_path_trace
from .v1_3_0.pnp import \
    pnp as v1_3_0_pnp
from .v1_3_0.swim import \
    swim as v1_3_0_swim
from .v1_3_0.site_profile import \
    site_profile as v1_3_0_site_profile
from .v1_3_0.sites import \
    sites as v1_3_0_sites
from .v1_3_0.tag import \
    tag as v1_3_0_tag
from .v1_3_0.task import \
    task as v1_3_0_task
from .v1_3_0.template_programmer import \
    template_programmer as v1_3_0_template_programmer


@click.group()
@click.pass_context
def main(ctx):
    """DNA Center API wrapper.

    DNACenterAPI wraps all of the individual DNA Center APIs and represents
    them in a simple hierarchical structure.

    """
    urllib3.disable_warnings()
    pass


@main.group()
@click.option('--username', '-u', envvar='DNA_CENTER_USERNAME',
              default=None,
              help='HTTP Basic Auth username.',
              show_default=True,
              prompt=True)
@click.option('--password', '-p', envvar='DNA_CENTER_PASSWORD',
              default=None,
              help='HTTP Basic Auth password.',
              show_default=True,
              prompt=True, hide_input=True,
              confirmation_prompt=True)
@click.option('--encoded_auth', '-ea', envvar='DNA_CENTER_ENCODED_AUTH',
              default=None,
              help='HTTP Basic Auth base64 encoded string.',
              show_default=True)
@click.option('--base_url', type=str,
              default=config.DEFAULT_BASE_URL,
              help='The base URL to be prefixed to the individual API endpoint suffixes.',
              show_default=True)
@click.option('--single_request_timeout', type=int,
              default=config.DEFAULT_SINGLE_REQUEST_TIMEOUT,
              help='Timeout (in seconds) for RESTful HTTP requests.',
              show_default=True)
@click.option('--wait_on_rate_limit', type=bool,
              default=config.DEFAULT_WAIT_ON_RATE_LIMIT,
              help='Enables or disables automatic rate-limit handling.',
              show_default=True)
@click.option('--verify', type=bool,
              default=config.DEFAULT_VERIFY,
              help="Controls whether to verify the server's TLS certificate.",
              show_default=True)
@click.option('--debug', '-d', type=bool, envvar='DEBUG',
              default=False,
              help="Controls whether to log information about DNA Center APIs' request and response process.",
              show_default=True)
@click.pass_context
def v1_2_10(ctx, username, password, encoded_auth, base_url,
            single_request_timeout,
            wait_on_rate_limit,
            verify,
            debug):
    """DNA Center API v1.2.10

    """
    spinner = init_spinner(beep=False)
    start_spinner(spinner)
    try:
        ctx.obj = DNACenterAPI(username, password, encoded_auth,
                               base_url=base_url,
                               single_request_timeout=single_request_timeout,
                               wait_on_rate_limit=wait_on_rate_limit,
                               verify=verify,
                               version='1.2.10',
                               debug=debug)
        stop_spinner(spinner)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('''Try "dnacentercli v1-2-10 --help" for help.''')
        eprint('Error:', e)
        ctx.exit(-1)


@main.group()
@click.option('--username', '-u', envvar='DNA_CENTER_USERNAME',
              default=None,
              help='HTTP Basic Auth username.',
              show_default=True,
              prompt=True)
@click.option('--password', '-p', envvar='DNA_CENTER_PASSWORD',
              default=None,
              help='HTTP Basic Auth password.',
              show_default=True,
              prompt=True, hide_input=True,
              confirmation_prompt=True)
@click.option('--encoded_auth', '-ea', envvar='DNA_CENTER_ENCODED_AUTH',
              default=None,
              help='HTTP Basic Auth base64 encoded string.',
              show_default=True)
@click.option('--base_url', type=str,
              default=config.DEFAULT_BASE_URL,
              help='The base URL to be prefixed to the individual API endpoint suffixes.',
              show_default=True)
@click.option('--single_request_timeout', type=int,
              default=config.DEFAULT_SINGLE_REQUEST_TIMEOUT,
              help='Timeout (in seconds) for RESTful HTTP requests.',
              show_default=True)
@click.option('--wait_on_rate_limit', type=bool,
              default=config.DEFAULT_WAIT_ON_RATE_LIMIT,
              help='Enables or disables automatic rate-limit handling.',
              show_default=True)
@click.option('--verify', type=bool,
              default=config.DEFAULT_VERIFY,
              help="Controls whether to verify the server's TLS certificate.",
              show_default=True)
@click.option('--debug', '-d', type=bool, envvar='DEBUG',
              default=False,
              help="Controls whether to log information about DNA Center APIs' request and response process.",
              show_default=True)
@click.pass_context
def v1_3_0(ctx, username, password, encoded_auth, base_url,
           single_request_timeout,
           wait_on_rate_limit,
           verify,
           debug):
    """DNA Center API v1.3.0

    """
    spinner = init_spinner(beep=False)
    start_spinner(spinner)
    try:
        ctx.obj = DNACenterAPI(username, password, encoded_auth,
                               base_url=base_url,
                               single_request_timeout=single_request_timeout,
                               wait_on_rate_limit=wait_on_rate_limit,
                               verify=verify,
                               version='1.3.0',
                               debug=debug)
        stop_spinner(spinner)
    except Exception as e:
        stop_spinner(spinner)
        tbprint()
        eprint('''Try "dnacentercli v1-3-0 --help" for help.''')
        eprint('Error:', e)
        ctx.exit(-1)


v1_2_10.add_command(v1_2_10_clients)
v1_2_10.add_command(v1_2_10_command_runner)
v1_2_10.add_command(v1_2_10_devices)
v1_2_10.add_command(v1_2_10_fabric_wired)
v1_2_10.add_command(v1_2_10_file)
v1_2_10.add_command(v1_2_10_network_discovery)
v1_2_10.add_command(v1_2_10_networks)
v1_2_10.add_command(v1_2_10_non_fabric_wireless)
v1_2_10.add_command(v1_2_10_path_trace)
v1_2_10.add_command(v1_2_10_pnp)
v1_2_10.add_command(v1_2_10_swim)
v1_2_10.add_command(v1_2_10_site_profile)
v1_2_10.add_command(v1_2_10_sites)
v1_2_10.add_command(v1_2_10_tag)
v1_2_10.add_command(v1_2_10_task)
v1_2_10.add_command(v1_2_10_template_programmer)
v1_3_0.add_command(v1_3_0_clients)
v1_3_0.add_command(v1_3_0_command_runner)
v1_3_0.add_command(v1_3_0_devices)
v1_3_0.add_command(v1_3_0_fabric_wired)
v1_3_0.add_command(v1_3_0_file)
v1_3_0.add_command(v1_3_0_network_discovery)
v1_3_0.add_command(v1_3_0_networks)
v1_3_0.add_command(v1_3_0_non_fabric_wireless)
v1_3_0.add_command(v1_3_0_path_trace)
v1_3_0.add_command(v1_3_0_pnp)
v1_3_0.add_command(v1_3_0_swim)
v1_3_0.add_command(v1_3_0_site_profile)
v1_3_0.add_command(v1_3_0_sites)
v1_3_0.add_command(v1_3_0_tag)
v1_3_0.add_command(v1_3_0_task)
v1_3_0.add_command(v1_3_0_template_programmer)
