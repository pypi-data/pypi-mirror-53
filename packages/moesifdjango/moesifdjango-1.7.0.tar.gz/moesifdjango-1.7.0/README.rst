Moesif Middleware for Python Django
===================================

|Built For| |Latest Version| |Language Versions| |Software License|
|Source Code|

Django middleware to capture *incoming* or *outgoing* API calls and send
to the Moesif API Analytics platform.

`Source Code on GitHub <https://github.com/moesif/moesifdjango>`__

This SDK uses the Requests library and will work for Python 2.7 — 3.5.

How to install
--------------

.. code:: shell

   pip install moesifdjango

How to use
----------

In your ``settings.py`` file in your Django project directory, please
add ``moesifdjango.middleware.moesif_middleware`` to the MIDDLEWARE
array. If you plan to use celery as the backend of asynchronous
delivered logged requests, you also need to add ``moesifdjango`` to your
``INSTALLED_APPS``.

Because of middleware execution order, it is best to add moesifdjango
middleware **below** SessionMiddleware and AuthenticationMiddleware,
because they add useful session data that enables deeper error analysis.
On the other hand, if you have other middleware that modified response
before going out, you may choose to place Moesif middleware **above**
the middleware modifying response. This allows Moesif to see the
modifications to the response data and see closer to what is going over
the wire.

Changes in Django 1.10
~~~~~~~~~~~~~~~~~~~~~~

Django middleware style and setup was refactored in version 1.10. You
need need to import the correct version of Moesif middleware depending
on your Django version. If you’re using Django 1.10 or greater, use
``moesifdjango.middleware.moesif_middleware``. However, if you’re using
Django 1.9 or older, you need to follow the legacy style for importing
middleware and use
``moesifdjango.middleware_pre19.MoesifMiddlewarePre19`` instead.

You can find your current Django version via
``python -c "import django; print(django.get_version())"`` {:
.notice–info}

Django 1.10 or newer
~~~~~~~~~~~~~~~~~~~~

Add the middleware to your application:

Django 1.10 renamed ``MIDDLEWARE_CLASSES`` to ``MIDDLEWARE.`` If you’re
using 1.10 or newer and still using the legacy MIDDLEWARE_CLASSES, the
Moesif middleware will not run. {: .notice–danger}

::

   MIDDLEWARE = [
       ...
       'django.contrib.sessions.middleware.SessionMiddleware',
       'django.middleware.common.CommonMiddleware',
       'django.contrib.auth.middleware.AuthenticationMiddleware',
       'moesifdjango.middleware.moesif_middleware'
       ...
   ]

Django 1.9 or older
~~~~~~~~~~~~~~~~~~~

Add the middleware to your application:

::

   MIDDLEWARE_CLASSES = [
       ...
       'moesifdjango.middleware_pre19.MoesifMiddlewarePre19',
       ...
       # other middlewares
   ]

Also, add ``MOESIF_MIDDLEWARE`` to your ``settings.py`` file,

::


   MOESIF_MIDDLEWARE = {
       'APPLICATION_ID': 'Your Application ID Found in Settings on Moesif',
       ...
       # other options see below.
   }

You can find your Application Id from `Moesif
Dashboard <https://www.moesif.com/>`__ -> *Top Right Menu* -> *App
Setup*

Configuration options
---------------------

**``APPLICATION_ID``**
^^^^^^^^^^^^^^^^^^^^^^

(**required**), *string*, is obtained via your Moesif Account, this is
required.

**``SKIP``**
^^^^^^^^^^^^

(optional) *(request, response) => boolean*, a function that takes a
request and a response, and returns true if you want to skip this
particular event.

**``IDENTIFY_USER``**
^^^^^^^^^^^^^^^^^^^^^

(optional) *(request, response) => string*, a function that takes a
request and a response, and returns a string that is the user id used by
your system. While Moesif identify users automatically, and this
middleware try to use the standard Django request.user.username, if your
set up is very different from the standard implementations, it would be
helpful to provide this function.

**``GET_SESSION_TOKEN``**
^^^^^^^^^^^^^^^^^^^^^^^^^

(optional) *(request, response) => string*, a function that takes a
request and a response, and returns a string that is the session token
for this event. Again, Moesif tries to get the session token
automatically, but if you setup is very different from standard, this
function will be very help for tying events together, and help you
replay the events.

**``GET_METADATA``**
^^^^^^^^^^^^^^^^^^^^

(optional) *(request, response) => dictionary*, getMetadata is a
function that returns an object that allows you to add custom metadata
that will be associated with the event. The metadata must be a
dictionary that can be converted to JSON. For example, you may want to
save a VM instance_id, a trace_id, or a tenant_id with the request.

**``MASK_EVENT_MODEL``**
^^^^^^^^^^^^^^^^^^^^^^^^

(optional) *(EventModel) => EventModel*, a function that takes an
EventModel and returns an EventModel with desired data removed. Use this
if you prefer to write your own mask function than use the string based
filter options: REQUEST_BODY_MASKS, REQUEST_HEADER_MASKS,
RESPONSE_BODY_MASKS, & RESPONSE_HEADER_MASKS. The return value must be a
valid EventModel required by Moesif data ingestion API. For details
regarding EventModel please see the `Moesif Python API
Documentation <https://www.moesif.com/docs/api?python>`__.

**``LOCAL_DEBUG``**
^^^^^^^^^^^^^^^^^^^

*boolean*, set to True to print internal log messages for debugging SDK
integration issues.

**``USE_CELERY``**
^^^^^^^^^^^^^^^^^^

*boolean*, Default False. Set to True to use Celery for queuing sending
data to Moesif. Check out `Celery
documentation <http://docs.celeryproject.org>`__ for more info.

**``REQUEST_HEADER_MASKS``**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(deprecated), *string[]*, is a list of strings for headers that you want
to hide from Moesif. Will be removed in future version. Replaced by the
function based ‘MASK_EVENT_MODEL’ for additional flexibility.

**``REQUEST_BODY_MASKS``**
^^^^^^^^^^^^^^^^^^^^^^^^^^

(deprecated), *string[]*, is a list of key values in the body that you
want to hide from Moesif. All key values in the body will be recursively
removed before sending to Moesif. Will be removed in future version.
Replaced by the function based ‘MASK_EVENT_MODEL’ for additional
flexibility.

**``RESPONSE_HEADER_MASKS``**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(deprecated), *string[]*, performs the same function for response
headers. Will be removed in future version. Replaced by the function
based ‘MASK_EVENT_MODEL’ for additional flexibility.

**``RESPONSE_BODY_MASKS``**
^^^^^^^^^^^^^^^^^^^^^^^^^^^

(deprecated), *string[]*, performs the same task for response body. Will
be removed in future version. Replaced by the function based
‘MASK_EVENT_MODEL’ for additional flexibility.

**``CAPTURE_OUTGOING_REQUESTS``**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*boolean*, Default False. Set to True to capture all outgoing API calls
from your app to third parties like Stripe or to your own dependencies
while using `Requests <http://docs.python-requests.org/en/master/>`__
library. The options below is applied to outgoing API calls. When the
request is outgoing, for options functions that take request and
response as input arguments, the request and response objects passed in
are `Requests <http://docs.python-requests.org/en/master/api/>`__
request or response objects.

**``SKIP_OUTGOING``**
'''''''''''''''''''''

(optional) *(req, res) => boolean*, a function that takes a
`Requests <http://docs.python-requests.org/en/master/api/>`__ request
and response, and returns true if you want to skip this particular
event.

**``IDENTIFY_USER_OUTGOING``**
''''''''''''''''''''''''''''''

(optional, but highly recommended) *(req, res) => string*, a function
that takes `Requests <http://docs.python-requests.org/en/master/api/>`__
request and response, and returns a string that is the user id used by
your system. While Moesif tries to identify users automatically, but
different frameworks and your implementation might be very different, it
would be helpful and much more accurate to provide this function.

**``GET_METADATA_OUTGOING``**
'''''''''''''''''''''''''''''

(optional) *(req, res) => dictionary*, a function that takes
`Requests <http://docs.python-requests.org/en/master/api/>`__ request
and response, and returns a dictionary (must be able to be encoded into
JSON). This allows to associate this event with custom metadata. For
example, you may want to save a VM instance_id, a trace_id, or a
tenant_id with the request.

**``GET_SESSION_TOKEN_OUTGOING``**
''''''''''''''''''''''''''''''''''

(optional) *(req, res) => string*, a function that takes
`Requests <http://docs.python-requests.org/en/master/api/>`__ request
and response, and returns a string that is the session token for this
event. Again, Moesif tries to get the session token automatically, but
if you setup is very different from standard, this function will be very
help for tying events together, and help you replay the events.

Example:
~~~~~~~~

.. code:: python

   def identifyUser(req, res):
       # if your setup do not use the standard request.user.username
       # return the user id here
       return "user_id_1"

   def should_skip(req, res):
       if "healthprobe" in req.path:
           return True
       else:
           return False

   def get_token(req, res):
       # if your setup do not use the standard Django method for
       # setting session tokens. do it here.
       return "token"

   def mask_event(eventmodel):
       # do something to remove sensitive fields
       # be sure not to remove any required fields.
       return eventmodel

   def get_metadata(req, res):
       return {
           'foo': '12345',
           'bar': '23456',
       }


   MOESIF_MIDDLEWARE = {
       'APPLICATION_ID': 'Your application id',
       'LOCAL_DEBUG': False,
       'IDENTIFY_USER': identifyUser,
       'GET_SESSION_TOKEN': get_token,
       'SKIP': should_skip,
       'MASK_EVENT_MODEL': mask_event,
       'GET_METADATA': get_metadata,
       'USE_CELERY': False
   }

Update User
-----------

update_user method
~~~~~~~~~~~~~~~~~~

A method is attached to the moesif middleware object to update the user
profile or metadata. The metadata field can be any custom data you want
to set on the user. The ``user_id`` field is required.

.. code:: python

   middleware = MoesifMiddleware(None)
   update_user = middleware.update_user({
       'user_id': 'testpythonapiuser',
       'session_token': 'jkj9324-23489y5324-ksndf8-d9syf8',
       'metadata': {'email': 'abc@email.com', 'name': 'abcde', 'image': '1234'}
       })

update_users_batch method
~~~~~~~~~~~~~~~~~~~~~~~~~

A method is attached to the moesif middleware object to update the users
profile or metadata in batch. The metadata field can be any custom data
you want to set on the user. The ``user_id`` field is required.

.. code:: python

   middleware = MoesifMiddleware(None)
   update_users = middleware.update_users_batch([{
           'user_id': 'testpythonapiuser',
           'metadata': {'email': 'abc@email.com', 'name': 'abcdefg', 'image': '123'}
       }, {
           'user_id': 'testpythonapiuser1',
           'metadata': {'email': 'abc@email.com', 'name': 'abcdefg', 'image': '123'}
       }])

Update Company
--------------

update_company method
~~~~~~~~~~~~~~~~~~~~~

A method is attached to the moesif middleware object to update the
company profile or metadata. The metadata field can be any custom data
you want to set on the company. The ``company_id`` field is required.

.. code:: python

   middleware = MoesifMiddleware(None)
   update_company = middleware.update_company({
       'company_id': '1',
       'metadata': {'email': 'abc@email.com', 'name': 'abcde', 'image': '1234'}
       })

update_companies_batch method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A method is attached to the moesif middleware object to update the
companies profile or metadata in batch. The metadata field can be any
custom data you want to set on the company. The ``company_id`` field is
required.

.. code:: python

   middleware = MoesifMiddleware(None)
   update_companies = middleware.update_companies_batch([{
           'company_id': '1',
           'metadata': {'email': 'abc@email.com', 'name': 'abcdefg', 'image': '123'}
       }, {
           'company_id': '2',
           'metadata': {'email': 'abc@email.com', 'name': 'abcdefg', 'image': '123'}
       }])

How to test
-----------

1. Manually clone the git repo
2. Invoke ``pip install Django`` if you haven’t done so.
3. Invoke ``pip install moesifdjango``
4. Add your own application id to ‘tests/settings.py’. You can find your
   Application Id from `Moesif Dashboard <https://www.moesif.com/>`__ ->
   *Top Right Menu* -> *Installation*
5. From terminal/cmd navigate to the root directory of the middleware
   tests.
6. Invoke ``python manage.py test`` if you are using Django 1.10 or
   newer.
7. Invoke ``python manage.py test middleware_pre19_tests`` if you are
   using Django 1.9 or older.

.. _example-1:

Example
-------

An example Moesif integration based on quick start tutorials of Django
and Django Rest Framework: `Moesif Django
Example <https://github.com/Moesif/moesifdjangoexample>`__

Other integrations
------------------

To view more more documentation on integration options, please visit
`the Integration Options
Documentation <https://www.moesif.com/docs/getting-started/integration-options/>`__\ **.**

.. |Built For| image:: https://img.shields.io/badge/built%20for-django-blue.svg
   :target: https://www.djangoproject.com/
.. |Latest Version| image:: https://img.shields.io/pypi/v/moesifdjango.svg
   :target: https://pypi.python.org/pypi/moesifdjango
.. |Language Versions| image:: https://img.shields.io/pypi/pyversions/moesifdjango.svg
   :target: https://pypi.python.org/pypi/moesifdjango
.. |Software License| image:: https://img.shields.io/badge/License-Apache%202.0-green.svg
   :target: https://raw.githubusercontent.com/Moesif/moesifdjango/master/LICENSE
.. |Source Code| image:: https://img.shields.io/github/last-commit/moesif/moesifdjango.svg?style=social
   :target: https://github.com/Moesif/moesifdjango
