=============
dnacentercli
=============

*Command Line Interface for Cisco DNA Center APIs.*

-------------------------------------------------------------------------------

**dnacentercli** is a CLI built for working with the DNA Center APIs.

Installation
============

To install dnacentercli, you will need to have python and pip installed. 
After you can enter the following command:

.. code-block:: bash

    $ pip install dnacentercli


The project has a few dependencies:

- `click`_ >= 7.0
- `dnacentersdk`_ >= 1.3.0.post2

**Note**: dnacentercli works starting from **python 3**

What is DNA Center?
===================

    "A better way to control your network. Cisco DNA Center is the network management and command center for Cisco DNA, your intent-based network for the enterprise."

Visit the official `DNA Center`_ website for more information.


Usage
======

The DNA Center CLI depends and actively uses the `DNA Center SDK`_. 
They, however, have some differences in their usage.


API Version
------------

Cisco DNA Center SDK wraps DNA Center APIs (versions: 1.2.10 and 1.3.0),
using the version parameter to control which API version to use.

DNA Center CLI does it by separating the versions by commands.

.. code-block:: bash
    
    $ dnacentercli --help
    
    Usage: dnacentercli [OPTIONS] COMMAND [ARGS]...

    DNA Center API wrapper.

    DNACenterAPI wraps all of the individual DNA Center APIs and represents
    them in a simple hierarchical structure.

    Options:
     --help  Show this message and exit.

    Commands:
      v1-2-10  DNA Center API v1.2.10
      v1-3-0   DNA Center API v1.3.0


Authenticate
-------------

DNA Center SDK creates a DNACenterAPI "Connection Object" defaults to pulling from environment variables and dnacentersdk.config.
The same happens for the DNA Center CLI, except, of course, the version parameter.

You can ask for help using ``--help`` and see the list of options and commands available on your selected version:

.. code-block:: bash

    $ dnacentercli v1-2-10 --help 


**Note:**

To avoid getting errors like the following:

::

    > HTTPSConnectionPool(host='128.107.71.199', port=443): 
    Max retries exceeded with url: /dna/system/api/v1/auth/token (Caused by SSLError
    (SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate
    verify failed: self signed certificate in certificate chain (_ssl.c:1076)')))


Include the verify option and set it to False: ``--verify False``


Access to DNA Center APIs
--------------------------

You need to authenticate for accessing other DNA Center APIs, such as Clients, Networks or PnP.

You can ask for specific API help using ``--help`` after the previous command options, which will list the endpoints (as commands):

.. code-block:: bash

    $ dnacentercli v1-2-10 --base_url https://128.107.71.199:443 --verify False networks --help


Making API Calls
----------------

Each DNA Center SDK API Call parameter is a DNA Center CLI option.

The following call using the dnacentersdk

.. code-block:: python

    from dnacentersdk import DNACenterAPI
    api = DNACenterAPI(username="devnetuser",
                       password="Cisco123!",
                       base_url="https://sandboxdnac2.cisco.com:443",
                       version='1.2.10',
                       verify=True)

    api.networks.get_overall_network_healt(timestamp='1568008500000', headers={'__runsync': True})

is the same as 

.. code-block:: bash

    $ dnacentercli v1-2-10 --username devnetuser --password Cisco123! \
    > --base_url https://sandboxdnac2.cisco.com:443 --verify True \
    > networks get-overall-network-health \
    > --timestamp "1568008500000" --headers '{"__runsync": true}'


**Note:** 

There are differences across platforms about JSON strings.

On \*nix based systems and command lines, the following is a valid JSON string representation:
    
.. code-block:: bash

    $ dnacentercli v1-2-10 networks get-overall-network-health \
    --timestamp "1568008500000" --headers '{"__runsync": true}'

On Windows and its command lines, the following is the valid JSON string representation:

    
.. code-block:: bash

    dnacentercli v1-2-10 networks get-overall-network-health ^
    --timestamp "1568008500000" --headers '{\"__runsync\": true}'
    
Be careful.


Multiple Options
----------------

There are some cases where the parameter type is a list. To record all the values, you have to provide the parameter multiple times.

For example:

.. code-block:: bash

    $ dnacentercli v1-2-10 devices add-device --ipaddress '10.20.10.1' --ipaddress '10.30.10.1'


Bell
------

To activate the beep when the spinner finishes (or the API call ends), add the ``--beep`` option to your API Call.
The ``--beep`` option is a boolean flag if present is on otherwise is off.


Pretty Print
------------

To pretty-print the JSON response add the option ``-pp`` or ``--pretty_print`` INTEGER to your API Call, where the INTEGER is the indentation.

Both the debug and the JSON response of the API call are streamed to the Standard Output (stdout).

For example:

.. code-block:: bash

    $ dnacentercli v1-2-10 devices get-device-list --family 'Unified AP' --hostname 'T1-9' -pp 2
    {
      "response": [
        {
          "apManagerInterfaceIp": "10.10.20.51",
          "associatedWlcIp": "10.10.20.51",
          "bootDateTime": null,
          "collectionInterval": "NA",
          "collectionStatus": "Managed",
          "errorCode": "null",
          "errorDescription": null,
          "family": "Unified AP",
          "hostname": "T1-9",
          ...
          "memorySize": "NA",
          "platformId": "AIR-AP1141N-A-K9",
          "reachabilityFailureReason": "NA",
          "reachabilityStatus": "Reachable",
          "role": "ACCESS",
          "roleSource": "AUTO",
          "serialNumber": "1140K0009",
          ...
          "snmpContact": "",
          "snmpLocation": "default-location",
          "softwareType": null,
          ...
          "tagCount": "0",
          "tunnelUdpPort": "16666",
          "type": "Cisco 1140 Unified Access Point",
          "upTime": "195days 11:11:32.270",
          "waasDeviceMode": null
        }
      ],
      "version": "1.0"
    }


Exceptions
----------

All DNA Center SDK exceptions are streamed to the Standard Error (stderr).
Before exiting the program, it will print the traceback (limited to 1 element), the exception name and its description.


*Copyright (c) 2019 Cisco and/or its affiliates.*

.. _dnacentersdk: https://dnacentersdk.readthedocs.io/
.. _click: https://click.palletsprojects.com/
.. _DNA Center SDK: https://github.com/cisco-en-programmability/dnacentersdk
.. _DNA Center: https://www.cisco.com/c/en/us/products/cloud-systems-management/dna-center/index.html
