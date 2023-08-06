# Algomax-Common

A common tools for working with **algomax-cli** and **algomax-engine**.

install the package with bellow command:

`-> pip install algomax-common`

##Logging

Adding logging to your Python program is as easy as this:

`from algomax_common.logger import AMLogger`

###Initiate the logger
add below code on top of your programs file

`AMLogger.init()`

and, use it:

`AMLogger.info('order created successfully', extra=with_this_data)`

`AMLogger.error('order creation failed', extra=order_data_and_error)`

**Note**: extra is a dict

###Explore log files
above code creates a directory named `logs` in your project directory.

log directory structure:

    logs
    |____ error.json    # contains AMLogger.error() records
    |____ info.json     # contains AMLogger.info() records


