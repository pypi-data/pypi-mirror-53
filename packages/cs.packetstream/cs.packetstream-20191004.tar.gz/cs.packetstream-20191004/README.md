general purpose bidirectional packet stream connection


*Latest release 20191004*:
PacketConnection: new optional parameter `packet_grace` to tune the send delay for additional packets before a flush, default DEFAULT_PACKET_GRACE (0.01s), 0 for no delay.
Add a crude packet level activity ticker.

A general purpose bidirectional packet stream connection.

## Class `Packet`

MRO: `cs.binary.PacketField`, `abc.ABC`  
A protocol packet.

## Class `PacketConnection`

A bidirectional binary connection for exchanging requests and responses.

### Method `PacketConnection.__init__(self, recv, send, request_handler=None, name=None, packet_grace=None, tick=None)`

Initialise the PacketConnection.

Parameters:
* `recv`: inbound binary stream.
  If this is an `int` it is taken to be an OS file descriptor,
  otherwise it should be a `cs.buffer.CornuCopyBuffer`
  or a file like object with a `read1` or `read` method.
* `send`: outbound binary stream.
  If this is an `int` it is taken to be an OS file descriptor,
  otherwise it should be a file like object with `.write(bytes)`
  and `.flush()` methods.
  For a file descriptor sending is done via an os.dup() of
  the supplied descriptor, so the caller remains responsible
  for closing the original descriptor.
* `packet_grace`:
  default pause in the packet sending worker
  to allow another packet to be queued
  before flushing the output stream.
  Default: `DEFAULT_PACKET_GRACE`s.
  A value of `0` will flush immediately if the queue is empty.
* `request_handler`: an optional callable accepting
  (`rq_type`, `flags`, `payload`).
  The request_handler may return one of 5 values on success:
  * `None`: response will be 0 flags and an empty payload.
  * `int`: flags only. Response will be the flags and an empty payload.
  * `bytes`: payload only. Response will be 0 flags and the payload.
  * `str`: payload only. Response will be 0 flags and the str
          encoded as bytes using UTF-8.
  * `(int, bytes)`: Specify flags and payload for response.
  An unsuccessful request should raise an exception, which
  will cause a failure response packet.
* `tick`: optional tick parameter, default `None`.
  If `None`, do nothing.
  If a Boolean, call `tick_fd_2` if true, otherwise do nothing.
  Otherwise `tick` should be a callable accepting a byteslike value.

## Class `Request_State`

MRO: `builtins.tuple`  
RequestState(decode_response, result)

## Function `tick_fd_2(bs)`

A low level tick function to write a short binary tick
to the standard error file descriptor.

This may be called by the send and receive workers to give
an indication of activity type.



# Release Log

*Release 20191004*:
PacketConnection: new optional parameter `packet_grace` to tune the send delay for additional packets before a flush, default DEFAULT_PACKET_GRACE (0.01s), 0 for no delay.
Add a crude packet level activity ticker.

*Release 20190221*:
DISTINFO requirement updates.

*Release 20181228*:
Initial PyPI release.
