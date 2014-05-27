==================
OpenTok Python SDK
==================

.. image:: https://travis-ci.org/opentok/Opentok-Python-SDK.svg
   :target: https://travis-ci.org/opentok/Opentok-Python-SDK

The OpenTok Python SDK lets you generate
`sessions <http://tokbox.com/opentok/tutorials/create-session/>`_ and
`tokens <http://tokbox.com/opentok/tutorials/create-token/>`_ for `OpenTok <http://www.tokbox.com/>`_
applications, and `archive <http://www.tokbox.com/platform/archiving>`_ Opentok 2.0 sessions.

If you are updating from a previous version of this SDK, see
`Important changes in v2.2 <#important-changes-in-v22>`_.

Installation using Pip (recommended):
-------------------------------------

Pip helps manage dependencies for Python projects using the PyPI index. Find more info here:
http://www.pip-installer.org/en/latest/

Add the ``opentok`` package as a dependency in your project. The most common way is to add it to your
``requirements.txt`` file::

  opentok>=2.2.0

Next, install the dependencies::

  $ pip install -r requirements.txt


Usage
-----

Initializing
~~~~~~~~~~~~

Import the package at the top of any file where you will use it. At the very least you will need the
``OpenTok`` class. Then initialize an OpenTok instance with your own API Key and API Secret.

.. code:: python

  from opentok import OpenTok

  opentok = OpenTok(api_key, api_secret)

Creating Sessions
~~~~~~~~~~~~~~~~~

The create an OpenTok Session, use the ``opentok.create_session()`` method. There are two optional
keyword parameters for this method: ``location`` which can be set to a string containing an IP
address, and ``media_mode`` which is a String (defined by the MediaModes class). This method returns
a ``Session`` object. Its ``session_id`` attribute is useful when saving to a persistent store (such
as a database).

.. code:: python

  # Just a plain Session:
  session = opentok.create_session()
  # A Session that attempts to send streams directly between clients (falling back
  # to use the OpenTok TURN server to relay streams if the clients cannot connect):
  session = opentok.create_session(media_mode=MediaModes.relayed)
  # A Session with a location hint
  session = opentok.create_session(location=u'12.34.56.78')

  # Store this session ID in the database
  session_id = session.session_id

Generating Tokens
~~~~~~~~~~~~~~~~~

Once a Session is created, you can start generating Tokens for clients to use when connecting to it.
You can generate a token either by calling the ``opentok.generate_token(session_id)`` method or by
calling the ``session.generate_token()`` method on a ``Session`` instance after creating it. There
is a set of optional keyword parameters: ``role``, ``expire_time``, and ``data``.

.. code:: python

  # Generate a Token from just a session_id (fetched from a database)
  token = opentok.generate_token(session_id)
  # Generate a Token by calling the method on the Session (returned from create_session)
  token = session.generate_token()

  from opentok import Roles
  # Set some options in a token
  token = session.generate_token(role=Roles.moderator,
                                 expire_time=int(time.time()) + 10,
                                 data=u'name=Johnny')

Working with Archives
~~~~~~~~~~~~~~~~~~~~~

You can start the recording of an OpenTok Session using the ``opentok.start_archive(session_id)``
method. This method takes an optional keyword argument ``name`` to assign a name to the archive.
This method will return an ``Archive`` instance. Note that you can only start an Archive on
a Session that has clients connection.

.. code:: python

  archive = opentok.start_archive(session_id, name=u'Important Presentation')

  # Store this archive_id in the database
  archive_id = archive.id

You can stop the recording of a started Archive using the ``opentok.stop_archive(archive_id)``
method. You can also do this using the ``archive.stop()`` method of an ``Archive`` instance.

.. code:: python

  # Stop an Archive from an archive_id (fetched from database)
  opentok.stop_archive(archive_id)
  # Stop an Archive from an instance (returned from opentok.start_archive)
  archive.stop()

To get an ``Archive`` instance (and all the information about it) from an archive ID, use the
``opentok.get_archive(archive_id)`` method.

.. code:: python

  archive = opentok.get_archive(archive_id)

To delete an Archive, you can call the ``opentok.delete_archive(archive_id)`` method or the
``archive.delete()`` method of an ``Archive`` instance.

.. code:: python

  # Delete an Archive from an archive ID (fetched from database)
  opentok.delete_archive(archive_id)
  # Delete an Archive from an Archive instance (returned from opentok.start_archive or
  opentok.get_archive)
  archive.delete()

You can also get a list of all the Archives you've created (up to 1000) with your API Key. This is
done using the ``opentok.list_archives()`` method. There are two optional keyword parameters:
``count`` and ``offset``; they can help you paginate through the results. This method returns an
instance of the ``ArchiveList`` class.

.. code:: python

  archive_list = opentok.list_archive()

  # Get a specific Archive from the list
  archive = archive_list.items[i]

  # Iterate over items
  for archive in iter(archive_list):
    pass

  # Get the total number of Archives for this API Key
  total = archive_list.total

Samples
-------

There are two sample applications included in this repository. To get going as fast as possible, clone the whole
repository and follow the Walkthroughs:

- `HelloWorld <sample/HelloWorld/README.md>`_
- `Archiving <sample/Archiving/README.md>`_

Documentation
-------------

Reference documentation is available at <http://www.tokbox.com/opentok/libraries/server/python/reference/index.html> and in the
docs directory of the SDK.

Requirements
------------

You need an OpenTok API key and API secret, which you can obtain at https://dashboard.tokbox.com/

The OpenTok Python SDK requires Python 2.6, 2.7, 3.2, 3.3, or 3.4

Release Notes
-------------

See the `Releases <https://github.com/opentok/Opentok-Python-SDK/releases>`_ page for details about
each release.

Important changes in v2.2
-------------------------

This version of the SDK includes support for working with OpenTok 2.0 archives. (This API does not
work with OpenTok 1.0 archives.)

The OpenTok.create_session() method now includes a media_mode parameter, instead of a p2p parameter.

For details, see the reference documentation at
<http://www.tokbox.com/opentok/libraries/server/python/reference/index.html>.

Development and Contributing
----------------------------

Interested in contributing? We :heart: pull requests! See the `Development <DEVELOPING.md>`_ and
`Contribution <CONTRIBUTING.md>`_ guidelines.

Support
-------

See http://tokbox.com/opentok/support/ for all our support options.

Find a bug? File it on the `Issues <https://github.com/opentok/opentok-python-sdk/issues>`_ page.
Hint: test cases are really helpful!
