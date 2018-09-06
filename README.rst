==================
OpenTok Python SDK
==================

.. image:: https://travis-ci.org/opentok/Opentok-Python-SDK.svg
   :target: https://travis-ci.org/opentok/Opentok-Python-SDK

The OpenTok Python SDK lets you generate
`sessions <http://tokbox.com/opentok/tutorials/create-session/>`_ and
`tokens <http://tokbox.com/opentok/tutorials/create-token/>`_ for `OpenTok <http://www.tokbox.com/>`_
applications, and `archive <http://www.tokbox.com/platform/archiving>`_ OpenTok sessions.

Installation using Pip (recommended):
-------------------------------------

Pip helps manage dependencies for Python projects using the PyPI index. Find more info here:
http://www.pip-installer.org/en/latest/

Add the ``opentok`` package as a dependency in your project. The most common way is to add it to your
``requirements.txt`` file::

  opentok>=2.7.0

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

To create an OpenTok Session, use the ``opentok.create_session()`` method. There are three optional
keyword parameters for this method:

* ``location`` which can be set to a string containing an IP address.

* ``media_mode`` which is a String (defined by the MediaModes class).
  This determines whether the session will use the
  `OpenTok Media Router <https://tokbox.com/developer/guides/create-session/#media-mode>`_
  or attempt to send streams directly between clients. A routed session is required for some
  OpenTok features (such as archiving).

* ``archive_mode`` which specifies whether the session will be automatically archived (``always``)
  or not (``manual``).

This method returns a ``Session`` object. Its ``session_id`` attribute is useful when saving to a persistent
store (such as a database).

.. code:: python

  # Create a session that attempts to send streams directly between clients (falling back
  # to use the OpenTok TURN server to relay streams if the clients cannot connect):
  session = opentok.create_session()

  from opentok import MediaModes
  # A session that uses the OpenTok Media Router, which is required for archiving:
  session = opentok.create_session(media_mode=MediaModes.routed)

  # An automatically archived session:
  session = opentok.create_session(media_mode=MediaModes.routed, archive_mode=ArchiveModes.always)

  # A session with a location hint
  session = opentok.create_session(location=u'12.34.56.78')

  # Store this session ID in the database
  session_id = session.session_id

Generating Tokens
~~~~~~~~~~~~~~~~~

Once a Session is created, you can start generating Tokens for clients to use when connecting to it.
You can generate a token either by calling the ``opentok.generate_token(session_id)`` method or by
calling the ``session.generate_token()`` method on a ``Session`` instance after creating it. Both
have a set of optional keyword parameters: ``role``, ``expire_time``, ``data``, and
``initial_layout_class_list``.

.. code:: python

  # Generate a Token from just a session_id (fetched from a database)
  token = opentok.generate_token(session_id)
  # Generate a Token by calling the method on the Session (returned from create_session)
  token = session.generate_token()

  from opentok import Roles
  # Set some options in a token
  token = session.generate_token(role=Roles.moderator,
                                 expire_time=int(time.time()) + 10,
                                 data=u'name=Johnny'
                                 initial_layout_class_list=[u'focus'])

Working with Archives
~~~~~~~~~~~~~~~~~~~~~

You can only archive sessions that use the OpenTok Media
Router (sessions with the media mode set to routed).

You can start the recording of an OpenTok Session using the ``opentok.start_archive(session_id)``
method. This method takes an optional keyword argument ``name`` to assign a name to the archive.
This method will return an ``Archive`` instance. Note that you can only start an Archive on
a Session that has clients connected.

.. code:: python

  archive = opentok.start_archive(session_id, name=u'Important Presentation')

  # Store this archive_id in the database
  archive_id = archive.id

You can also disable audio or video recording by setting the `has_audio` or `has_video` property of
the `options` parameter to `false`:

.. code:: python

  archive = opentok.start_archive(session_id, name=u'Important Presentation', has_video=False)

  # Store this archive_id in the database
  archive_id = archive.id

By default, all streams are recorded to a single (composed) file. You can record the different
streams in the session to individual files (instead of a single composed file) by setting the
``output_mode`` parameter of the ``opentok.start_archive()`` method `OutputModes.individual`.

.. code:: python

  archive = opentok.start_archive(session_id, name=u'Important Presentation', output_mode=OutputModes.individual)

  # Store this archive_id in the database
  archive_id = archive.id

Composed archives (output_mode=OutputModes.composed) have an optional ``resolution`` parameter.
If no value is supplied the opentok platform will use the default resolution "640x480".
You can set this to "1280x720" by setting the
``resolution`` parameter of the ``opentok.start_archive()`` method.

Warning: This value cannot be set for Individual output mode, an error will be thrown.

.. code:: python

  archive = opentok.start_archive(session_id, name=u'Important Presentation', resolution="1280x720")

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
done using the ``opentok.list_archives()`` method. There are three optional keyword parameters:
``count``, ``offset`` and ``session_id``; they can help you paginate through the results and
filter by session ID. This method returns an instance of the ``ArchiveList`` class.

.. code:: python

  archive_list = opentok.list_archive()

  # Get a specific Archive from the list
  archive = archive_list.items[i]

  # Iterate over items
  for archive in iter(archive_list):
    pass

  # Get the total number of Archives for this API Key
  total = archive_list.total

Note that you can also create an automatically archived session, by passing in
``ArchiveModes.always`` as the ``archive_mode`` parameter when you call the
``opentok.create_session()`` method (see "Creating Sessions," above).

For composed archives, you can change the layout dynamically, using the `opentok.set_archive_layout(archive_id, type, stylesheet)` method:

.. code:: python

  opentok.set_archive_layout('ARCHIVEID', 'horizontalPresentation')

Setting the layout of composed archives is optional. By default, composed archives use the `best fit` layout.  Other valid values are: `custom`, `horizontalPresentation`, `pip` and `verticalPresentation`. If you specify a `custom` layout type, set the stylesheet parameter:

.. code:: python

  opentok.set_archive_layout(
      'ARCHIVEID',
      'custom',
      'stream.instructor {position: absolute; width: 100%;  height:50%;}'
  )

For other layout types, do not set the stylesheet property. For more information see
`Customizing the video layout for composed archives <https://tokbox.com/developer/guides/archiving/layout-control.html>`_.

For more information on archiving, see the
`OpenTok archiving <https://tokbox.com/opentok/tutorials/archiving/>`_ programming guide.

Sending Signals
~~~~~~~~~~~~~~~~~~~~~

Once a Session is created, you can send signals to everyone in the session or to a specific connection. You can send a signal by calling the ``signal(session_id, payload)`` method of the ``OpenTok`` class. The ``payload`` parameter is a dictionary used to set the ``type``, ``data`` fields. Ỳou can also call the method with the parameter ``connection_id`` to send a signal to a specific connection ``signal(session_id, data, connection_id)``.

.. code:: python

  # payload structure
  payload = {
      'type': 'type', #optional
      'data': 'signal data' #required
  }

  connection_id = '2a84cd30-3a33-917f-9150-49e454e01572'

  # To send a signal to everyone in the session:
  opentok.signal(session_id, payload)

  # To send a signal to a specific connection in the session:
  opentok.signal(session_id, payload, connection_id)

Working with Streams
~~~~~~~~~~~~~~~~~~~~~

You can get information about a stream by calling the `get_stream(session_id, stream_id)` method of the `OpenTok` class.

The method returns a Stream object that contains information of an OpenTok stream:

* ``id``: The stream ID
* ``videoType``: "camera" or "screen"
* ``name``: The stream name (if one was set when the client published the stream)
* ``layoutClassList``: It's an array of the layout classes for the stream

.. code:: python

  session_id = 'SESSIONID'
  stream_id = '8b732909-0a06-46a2-8ea8-074e64d43422'

  # To get stream info:
  stream = opentok.get_stream(session_id, stream_id)

  # Stream properties:
  print stream.id #8b732909-0a06-46a2-8ea8-074e64d43422
  print stream.videoType #camera
  print stream.name #stream name
  print stream.layoutClassList #['full']

Also, you can get information about all the streams in a session by calling the `list_streams(session_id)` method of the `OpenTok` class.

The method returns a StreamList object that contains a list of all the streams

.. code:: python

  # To get all streams in a session:
  stream_list = opentok.list_streams(session_id)

  # Getting the first stream of the list
  stream = stream_list.items[0]

  # Stream properties:
  print stream.id #8b732909-0a06-46a2-8ea8-074e64d43422
  print stream.videoType #camera
  print stream.name #stream name
  print stream.layoutClassList #['full']

Force Disconnect
~~~~~~~~~~~~~~~~~~~~~

Your application server can disconnect a client from an OpenTok session by calling the force_disconnect(session_id, connection_id) method of the OpenTok class, or the force_disconnect(connection_id) method of the Session class.

.. code:: python

  session_id = 'SESSIONID'
  connection_id = 'CONNECTIONID'

  # To send a request to disconnect a client:
  opentok.force_disconnect(session_id, connection_id)

Samples
-------

There are two sample applications included in this repository. To get going as fast as possible, clone the whole
repository and follow the Walkthroughs:

- `HelloWorld <sample/HelloWorld/README.md>`_
- `Archiving <sample/Archiving/README.md>`_

Documentation
-------------

Reference documentation is available at <http://www.tokbox.com/opentok/libraries/server/python/reference/index.html>.

Requirements
------------

You need an OpenTok API key and API secret, which you can obtain at https://dashboard.tokbox.com/

The OpenTok Python SDK requires Python 2.6, 2.7, 3.3, 3.4, 3.5 or 3.6

Release Notes
-------------

See the `Releases <https://github.com/opentok/Opentok-Python-SDK/releases>`_ page for details about
each release.

Important changes since v2.2
----------------------------

**Changes in v2.2.1:**

The default setting for the create_session() method is to create a session with the media mode set
to relayed. In previous versions of the SDK, the default setting was to use the OpenTok Media Router
(media mode set to routed). In a relayed session, clients will attempt to send streams directly
between each other (peer-to-peer); if clients cannot connect due to firewall restrictions, the
session uses the OpenTok TURN server to relay audio-video streams.

**Changes in v2.2.0:**

This version of the SDK includes support for working with OpenTok archives.

The OpenTok.create_session() method now includes a media_mode parameter, instead of a p2p parameter.

For details, see the reference documentation at
<http://www.tokbox.com/opentok/libraries/server/python/reference/index.html>.

Development and Contributing
----------------------------

Interested in contributing? We :heart: pull requests! See the `Development <DEVELOPING.md>`_ and
`Contribution <CONTRIBUTING.md>`_ guidelines.

Support
-------

See https://support.tokbox.com/ for all our support options.

Find a bug? File it on the `Issues <https://github.com/opentok/opentok-python-sdk/issues>`_ page.
Hint: test cases are really helpful!
