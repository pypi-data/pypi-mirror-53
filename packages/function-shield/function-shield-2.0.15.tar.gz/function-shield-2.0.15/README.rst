
FunctionShield
--------------

   Serverless Security Library for Developers. Regain Control over Your
   Serverless Runtime.

How FunctionShield helps With Serverless Security?
--------------------------------------------------

-  By monitoring (or blocking) outbound network traffic from your
   function, you can be certain that your data is never leaked
-  By disabling read/write operations on the /tmp/ directory, you can
   make your function truly ephemeral
-  By disabling the ability to launch child processes, you can make sure
   that no rogue processes are spawned without your knowledge by
   potentially malicious packages
-  By disabling the ability to read the function's (handler) source code
   through the file system, you can prevent handler source code leakage,
   which is oftentimes the first step in a serverless attack

Supports AWS Lambda and Google Cloud Functions

Get a free token
----------------

Please visit: https://www.puresec.io/function-shield-token-form

Install
-------

.. code:: sh

   $ pip install function-shield

Super simple to use
-------------------

.. code:: python

   import function_shield

   function_shield.configure({
       "policy": {
           # "block" mode => active blocking
           # "alert" mode => log only
           # "allow" mode => allowed, implicitly occurs if key does not exist
           "outbound_connectivity": "block",
           "read_write_tmp": "block",
           "create_child_process": "block",
           "read_handler": "block"
       },
       "token": os.environ["FUNCTION_SHIELD_TOKEN"]
   })

   def handler(event, context):
       # Your Code Here #

Logging & Security Visibility
-----------------------------

FunctionShield logs are sent directly to your function's AWS CloudWatch
log group. Here are a few sample logs, demonstrating the log format you
should expect:

.. code:: js

    // Log example #1:
    {
        "details": {
            "host": "microsoft.com",
            "ip": "13.77.161.179"
        },
        "function_shield": true,
        "timestamp": "2019-06-19T09:08:00.455144Z",
        "policy": "outbound_connectivity",
        "mode": "block"
    }

    // Log example #2:
    {
        "details": {
            "path": "/tmp/block"
        },
        "function_shield": true,
        "timestamp": "2019-06-19T09:08:00.422553Z",
        "policy": "read_write_tmp",
        "mode": "block"
    }

    // Log example #3:
    {
        "details": {
            "arguments": [
                "uname",
                "-a"
            ],
            "path": "/bin/uname"
        },
        "function_shield": true,
        "timestamp": "2019-06-19T09:08:00.469822Z",
        "policy": "create_child_process",
        "mode": "block"
    }

    // Log example #4:
    {
        "details": {
            "path": "/var/task/handler.py"
        },
        "function_shield": true,
        "timestamp": "2019-06-19T09:08:00.433942Z",
        "policy": "read_handler",
        "mode": "block"
    }

Reconfiguring FunctionShield
-----------------------------
``function_shield.configure`` can be called multiple time to temporary disable one of the policies.

Note that you need to add an additional parameter ``cookie`` to any subsequent call to ``function_shield.configure``.

.. code:: python

   import function_shield
   import requests

   cookie = function_shield.configure({
       "policy": {
           "outbound_connectivity": "block",
           "read_write_tmp": "block",
           "create_child_process": "block",
           "read_handler": "block"
       },
       "token": os.environ["FUNCTION_SHIELD_TOKEN"]
   })

   def handler(event, context):
       ...
       function_shield.configure({
           "cookie": cookie,
           "policy": {
               "outbound_connectivity": "allow"
           }
       })

       r = requests.get("https://api.company.com/users")

       function_shield.configure({
           "cookie": cookie,
           "policy": {
               "outbound_connectivity": "block"
           }
       })
       ...
       

Custom Security Policy (whitelisting)
-------------------------------------

Custom security policy is only supported with the PureSec SSP full
product.

`Get PureSec`_

.. _Get PureSec: https://www.puresec.io/product
