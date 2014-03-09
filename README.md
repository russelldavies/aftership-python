aftership-python
================

Python package for AfterShip API.

This package helps developers to integrate with AfterShip easily.


About AfterShip
==============

AfterShip provides an automated way for online merchants to track packages and
send their customers delivery status notifications. Customers no longer need to
deal with tracking numbers and track packages on their own. With AfterShip,
online merchants extend their customer service after the point of purchase by
keeping their customers actively informed, while saving time and money by
reducing customers’ questions about the status of their purchase delivery.


Installation
============

Install using pip or easy_install:

    $ pip install aftership-python
    or
    $ easy_install aftership-python

If you want to install it from source, grab the git repository from GitHub and run setup.py:

    $ git clone https://github.com/russelldavies/aftership-python.git
    $ cd aftership-python
    $ python setup.py install


Configuration
=============
###1. Before you begin

You'll need to have a AfterShip account [http://www.aftership.com](http://www.aftership.com).

###2. Setup the API Key

You can retrieve your api key at [https://www.aftership.com/connect/api](https://www.aftership.com/connect/api)


Usage
=====
###1. Setup
Before using API, please include the package in your script

	import aftership

You should set you API key before making any request to AfterShip.

	aftership.config.api_key = "YOUR_API_KEY"
Replace "YOUR_API_KEY" to your AfterShip api key.

Optionally, you can specify the API version:

    aftership.config.api_version = '3'

###1. Courier

####1. Get Courier list
You can retrive the list of supported couriers:

	aftership.Courier.all()

Result (truncated for ease of reading):

	{
        "total": 3,
        "couriers": [
            {
                "slug": "dhl",
                "name": "DHL",
                "phone": "+1 800 225 5345",
                "other_name": "DHL Express",
                "web_url": "http://www.dhl.com/"
            },
            {
                "slug": "china-post",
                "name": "China Post",
                "phone": "+86 20 11185",
                "other_name": "中国邮政",
                "web_url": "http://www.chinapost.com.cn/"
            },
            {
                "slug": "tnt",
                "name": "TNT",
                "phone": "+1 800 558 5555",
                "other_name": "TNT Express",
                "web_url": "http://www.tnt.com/"
            }
        ]
    }

####1. Detect Courier
Get a list of matched couriers for a tracking number based on the tracking
number format:

    aftership.Courier.detect('1Z1896X70305267337')

Result:

    {
        "total": 2,
        "tracking_number": "1234567890",
        "couriers": [
            {
                "slug": "dhl",
                "name": "DHL",
                "phone": "+1 800 225 5345",
                "other_name": "DHL Express",
                "web_url": "http://www.dhl.com/"
            },
            {
                "slug": "yrc",
                "name": "YRC",
                "phone": "+1 800-468-5739",
                "other_name": "YRC Freight",
                "web_url": "http://www.yrc.com/"
            }
        ]
    }


###1. Tracking

For each of these examples, the first parameter is the tracking number and the
second is the carrier slug. They can also be specified as keyword arguments:
`tracking_number` and `slug`, respectively.

Some calls take extra optional parameters. The parameters have the same name as
documented in the API.

####1. Create a tracking
You can add tracking number to AfterShip by calling

	aftership.Tracking.create("218501627271", "toll-global-express")

Optionally, you can pass extra paramaters, for example, customer name:

	aftership.Tracking.create("218501627271", "toll-global-express", customer_name="John Doe")

For extra parameters list, please consult the API.

####1. Get tracking result
To get the tracking results of multiple trackings:

    aftership.Tracking.get()

To get the tracking results of a single tracking:

	aftership.Tracking.get("218501627271", "toll-global-express")

####1. Update a tracking

To update a tracking:

	aftership.Tracking.update("218501627271", "toll-global-express",
                              title="Computer parts",
                              customer_name="John Doe")

The keyword arguments are optional parameters and none or all may be specified.


####1. Reactivate a tracking

To reactive an expired tracking:

	aftership.Tracking.reactivate("218501627271", "toll-global-express")

####1. Last Checkpoint

Get tracking information of the last checkpoint of a tracking:

    aftership.Tracking.last_checkpoint('218501627271', 'toll-global-express')

Optional parameters may be specified:

    aftership.Tracking.last_checkpoint('218501627271', 'toll-global-express',
                                       fields='title,order_id,tag',
                                       lang='en')


Documentation
=============
You can view the API documentation at: https://www.aftership.com/docs/api
