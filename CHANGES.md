# Release v3.6.0
- Added auto-archive improvements to the `opentok.Client.create_session` method 
to customize automatically created archives:
  - `archive_name` parameter
  - `archive_resolution` parameter
- Added the option to append to the user-agent, which can be done with
```python
opentok.Client.append_to_user_agent('my-appended-string')
```
- Added the option to specify audio-only or video-only broadcasts with the new booleans `hasAudio` and `hasVideo` 
when starting a broadcast or adding new streams to a broadcast.

# Release v3.5.0
- Support for end-to-end encryption (E2EE) that can be specified by a user when creating an OpenTok session.

# Release v3.4.0
- Support for Audio Connector API via `connect_audio_to_websocket` method

# Release v3.3.0

- Support for Experience Composer (Render) API
- Support for multiple archives and broadcasts in the `start_archive` and `start_broadcast` methods
- Support for low latency and DVR modes
- Documented more methods in README
- Updated some out-of-date dependencies

# Release v3.2.0

## Added

- Mute all and mute stream functionality [#192](https://github.com/opentok/Opentok-Python-SDK/pull/192), [#197](https://github.com/opentok/Opentok-Python-SDK/pull/197), [#199](https://github.com/opentok/Opentok-Python-SDK/pull/199)
- Added selective stream feature to `Archive` and `Broadcast` objects. [#196](https://github.com/opentok/Opentok-Python-SDK/pull/196)
- Added PlayDTMF functionality to `SipCall` object [#194](https://github.com/opentok/Opentok-Python-SDK/pull/194)
- Added SIP video outbound flag to `SipCall.dial` method [#194](https://github.com/opentok/Opentok-Python-SDK/pull/194)
- Added the ObserveForceMute flag to `SipCall.dial` method [#193](https://github.com/opentok/Opentok-Python-SDK/pull/193)

# 3.2.0b1

## Added

- Added mute/muteall functionality

# Release v3.1.0

## Added

* #188 - Added support for archive layouts, as well as the new `screenshareType` option for screenshare layouts

# Release v3.0.1

# Changes

- Fixed `readme.rst` not displaying properly on Pypi

Thank you for your support and we are definitely excited to release even more exciting updates!! Stay tuned!!

# Release v3.0.0

# 🎉   Version 3.0 Changes

- Verb to Noun format to make the SDK code more human-readable and maintain consistency with industry standard
- Renamed the Opentok class to Client to ensure compliance with best practice and industry standards
- Improved JWT generation
- Improved error handling
- Fixed Enum34 related issues

# v2.11.0

Fixing issues with Enum34.

# Release v2.10.0

- Add Broadcast APIs
Thanks @normanargueta!

# Release v2.9.0

- Added SIP Dial API
- Added Set Stream Class Lists API

Thanks @normanargueta!

# Release v2.8.0

- List Archives filtration by sessionId (#137 )
- Added Update Archive Layout functionality (#139)

# Release v2.7.0

Added `resolution` parameter for `start_archive`
Added `signal` API
Added `force_disconnect` API
Added `get_stream` API
Added `list_streams` API

Thanks @normanargueta and @maikthomas

# Release v2.6.0

- Add timeout option to opentok constructor (#117, #57 Thanks @tylergould!)

# Release v2.5.1

Changes:

- Exceptions now inherit from `Exception` instead of `BaseException` (#115, thanks @fernandogrd)

As well as:

- Update archive documentation (#80)
- Document the `initial_layout_class_list` param for the `generate_token` function (#112)
- Refactor sample app (#111)

# Release v2.5.0

This updates includes the following changes:

- [Adds support for the `initial_layout_class_list` field in tokens](https://github.com/opentok/Opentok-Python-SDK/pull/77)
- [Adds support for JWT `X-OPENTOK-AUTH` header, replacing the deprecated `X-TB-PARTNER-AUTH` header](https://github.com/opentok/Opentok-Python-SDK/pull/86)
- [Updates the REST API endpoint URL to use `/project/` replacing the deprecated `/partner/`](https://github.com/opentok/Opentok-Python-SDK/pull/105)
- [Only include connection data in generated token if it's been defined](https://github.com/opentok/Opentok-Python-SDK/pull/106)
- [Ensure backwards compatibility with Python 2.6](https://github.com/opentok/Opentok-Python-SDK/pull/91)
- [Removes Python 3.2 from supported version because it's not supported by our dependency](https://github.com/opentok/Opentok-Python-SDK/pull/105)

As well as:

- [Updates JS code in samples to use latest API and best practices](https://github.com/opentok/Opentok-Python-SDK/pull/108)
- [Fix broken image paths in sample](https://github.com/opentok/Opentok-Python-SDK/pull/104)

# Release v2.5.0b1

This update adds support for the `initial_layout_class_list` field in tokens.

# Release v2.4.1

This update adds version information to the User-Agent string for analytics (#78)

# Release v2.4.0

This update adds proxy configuration as a feature of the OpenTok object. (thanks @juandebravo!)

Here is an example of using proxy configuration:

``` python
from opentok import OpenTok

opentok = OpenTok(api_key, api_secret)
opentok.proxies = {
  "http": "http://10.10.1.10:3128",
  "https": "http://10.10.1.10:1080",
}
session = opentok.create_session()
```

The format for the proxy configuration is identical to the format used by the underlying [requests](http://docs.python-requests.org/en/latest/user/advanced/#proxies) library.

# Release v2.3.0

New archiving features:
-  Automatically archived sessions -- See the `archive_mode` parameter of the `opentok.create_session()` method and the `ArchiveModes` class.
-  Audio-only or video-only archives -- See the `has_audio` and `has_video` parameters of the `opentok.start_archive()` method.
-  Individual archiving -- See the `output_mode` parameter of the `opentok.start_archive()` method and the `OutputModes` class.
-  Paused archives -- When no clients are publishing to a session being archived, its status changes to "paused". See `archive.status`.

Other improvements:
-  Adds Python 3.4 support

# Release v2.2.1

The default setting for the `create_session()` method is to create a session with the media mode set
to relayed. In previous versions of the SDK, the default setting was to use the OpenTok Media Router
(media mode set to routed). In a relayed session, clients will attempt to send streams directly
between each other (peer-to-peer); if clients cannot connect due to firewall restrictions, the
session uses the OpenTok TURN server to relay audio-video streams.

# Release v2.2.0

This version of the SDK includes support for working with OpenTok 2.0 archives. (This API does not
work with OpenTok 1.0 archives.)

The `OpenTok.create_session()` method now includes a `media_mode` parameter, instead of a `p2p` parameter.

For details, see the reference documentation at
http://www.tokbox.com/opentok/libraries/server/python/reference/index.html.
