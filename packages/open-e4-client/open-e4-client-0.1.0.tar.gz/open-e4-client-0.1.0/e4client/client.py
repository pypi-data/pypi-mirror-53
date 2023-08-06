from __future__ import annotations

import logging
import queue
import socket
import threading
import time
from contextlib import AbstractContextManager
from typing import Any, Callable, Tuple, Union

from e4client.exceptions import BTLEConnectionError, DeviceNotFoundError, \
    ServerRequestError
from e4client.protocol import E4DataStreamID, E4Device, _CmdID, _CmdStatus, \
    _ServerMessageType, _ServerReply, _gen_command_string, _parse_device_list, \
    _parse_incoming_message


# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


class E4StreamingClient(AbstractContextManager):
    """Empatica E4 streaming server full-duplex TCP client.

    Implements a client for the Empatica E4 streaming server, providing
    convenience methods for commands. Note that this object instantiates two
    additional internal threads, one for full duplex communication and one
    for callback execution.

    Attributes:

    is_connected (bool): flag indicating whether the client is currently
    connected to the server.

    Can be used as a context manager.
    """

    _delim = b'\n'

    def __init__(self, server_ip: str,
                 server_port: int,
                 max_conn_attempts: int = 20):
        """
        Instantiate a new E4StreamingClient. Note that the client will
        immediately attempt to connect on instantiation.

        :param server_ip: IP address of the Streaming Server.
        :param server_port: TCP port of the Streaming Server.
        :param max_conn_attempts: maximum number of connection attempts.

        :raises OSError: in case of connection failure.
        """
        super().__init__()

        self._logger = logging.getLogger(self.__class__.__name__)

        # set up buffers for responses and subscriptions
        self._resp_q = queue.Queue(maxsize=1)
        self._sub_callbacks = {}
        self._callback_lock = threading.RLock()
        self._callback_q = queue.Queue()

        self._shutdown = threading.Event()
        self._shutdown.clear()

        self._logger.info(f'Connecting to {server_ip}:{server_port}...')

        # immediately try to connect
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        attempts = 0
        while True:
            try:
                self._logger.info(f'Connection attempt {attempts + 1}.')
                self._socket.connect((server_ip, server_port))
                self._logger.info('Connection success.')
                break
            except OSError:
                self._logger.info('Connection failed.')
                if attempts < max_conn_attempts:
                    self._logger.info('Reattempting connection...')
                    attempts += 1
                    time.sleep(0.01)
                    continue
                else:
                    self._logger.error('Too many connection attempts!')
                    self._socket.close()
                    raise

        self._connected = True

        self._recv_thread = threading.Thread(target=self._recv_loop)
        self._callback_thread = threading.Thread(target=self._callback_loop)
        self._recv_thread.start()
        self._callback_thread.start()

    @property
    def is_connected(self) -> bool:
        """
        Flag indicating the connection status of the client.
        """
        return self._connected

    def _try_callback_for_stream_sample(self,
                                        stream: E4DataStreamID,
                                        *sample) -> None:
        """
        Helper method to execute callbacks for individual samples.

        :param stream: Stream to which sample belongs.
        :param sample: Data sample.
        """
        with self._callback_lock:
            callback = self._sub_callbacks.get(stream, None)

        if callback:
            try:
                callback(stream, *sample)
            except Exception as e:
                self._logger.error(f'Callback for stream '
                                   f'{stream.name} failed with '
                                   f'exception.', e)
        else:
            self._logger.error(f'Got sample for stream {stream.name} '
                               f'without an active callback!')

    def _callback_loop(self):
        """
        Callback handler thread loop.
        """
        self._logger.debug('Starting callback handler thread...')

        while not self._shutdown.is_set():
            try:
                # TODO: fix magic number
                stream, *sample = self._callback_q.get(block=True, timeout=0.01)
                self._try_callback_for_stream_sample(stream, *sample)
                self._callback_q.task_done()
            except queue.Empty:
                pass

        self._logger.debug('Shutting down callback handler thread, executing '
                           'callbacks for remaining items in queue.')

        while not self._callback_q.empty():
            stream, *sample = self._callback_q.get(block=False)
            self._try_callback_for_stream_sample(stream, *sample)
            self._callback_q.task_done()

        self._logger.debug('Shut down callback handler thread.')

    def _recv_loop(self):
        """
        Socket read loop.
        """
        self._logger.debug('Starting receiving thread...')

        data = b''
        while not self._shutdown.is_set():
            try:
                # small block size since messages are short
                data += self._socket.recv(64)

                # split up responses and process them
                while True:
                    raw_msg, lim, rest = \
                        data.partition(E4StreamingClient._delim)
                    if len(lim) == len(rest) == 0:
                        # no remaining complete messages, read again from socket
                        break

                    data = rest  # save the remaining data for further
                    # processing

                    # parse the first extracted response
                    message = raw_msg.decode('utf-8')
                    self._logger.debug(f'Raw incoming message: {message}')

                    msg_type, parsed_msg = _parse_incoming_message(message)
                    self._logger.debug(f'Parsed message: {parsed_msg}')

                    if msg_type == _ServerMessageType.STREAM_DATA:
                        # TODO: FIX TIMESTAMPS
                        self._logger.debug(
                            f'Got sample for {parsed_msg.stream}, putting '
                            f'into callback queue...')
                        self._callback_q.put((parsed_msg.stream,
                                              parsed_msg.timestamp,
                                              *parsed_msg.data))
                    else:
                        while True:
                            try:
                                self._resp_q.get_nowait()
                            except queue.Empty:
                                self._resp_q.put_nowait(parsed_msg)
                                break

            except socket.error as e:
                self._logger.debug('Socket error.')
                self._logger.debug(e)
                break

        self._logger.debug('Shut down receiving thread...')

    def _send(self, cmd: str) -> None:
        """
        Send a raw string to the server.

        :param cmd: Raw string to send.
        """
        self._logger.debug(f'Sending \'{cmd.encode("utf-8")}\' to server.')
        self._socket.sendall(cmd.encode('utf-8'))

    def _send_command(self, cmd_id: _CmdID, **kwargs) \
            -> _ServerReply:
        """
        Send a command to the server.

        :param cmd_id: Command ID.
        :param kwargs: Arguments associated with the command.
        :return: Reply from the server.
        """
        self._send(_gen_command_string(cmd_id, **kwargs))
        resp = self._resp_q.get(block=True)

        assert resp.command == cmd_id
        return resp

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Closes this client. See E4StreamingClient.close().
        """
        self.close()

    # public convenience methods follow:
    def BTLE_discover_devices(self) -> Tuple[E4Device]:
        """
        Discover active, but not yet connected, E4 devices in the vicinity of
        the streaming server.

        :return: A tuple containing the discovered E4s.
        """
        resp = self._send_command(_CmdID.DEV_DISCOVER)
        return _parse_device_list(resp.data)

    def BTLE_connect_device(self,
                            device: Union[E4Device, str],
                            timeout: int = 200) -> None:
        """
        Connect a previously discovered E4 to the Streaming Server.

        :param device: Device to connect to.
        :param timeout: Timeout before giving up on connection.
        """
        device = device.uid if isinstance(device, E4Device) else device
        resp = self._send_command(_CmdID.DEV_CONNECT_BTLE,
                                  dev=device, timeout=timeout)

        if resp.status != _CmdStatus.SUCCESS:
            raise BTLEConnectionError(device)

    def BTLE_disconnect_device(self,
                               device: Union[E4Device, str]) -> None:
        """
        Disconnect a connected E4 device from the Streaming Server.

        :param device: The device to disconnect.
        """
        device = device.uid if isinstance(device, E4Device) else device
        resp = self._send_command(_CmdID.DEV_DISCONNECT_BTLE, dev=device)

        if resp.status != _CmdStatus.SUCCESS:
            raise BTLEConnectionError(device)

    def list_connected_devices(self) -> Tuple[E4Device]:
        """
        List the devices currently connected to the Streaming Server.

        :return: A tuple containing the currently connected devices.
        """
        resp = self._send_command(_CmdID.DEV_LIST)
        return _parse_device_list(resp.data)

    def connect_to_device(self,
                          device: Union[E4Device, str]) -> E4DeviceConnection:
        """
        Connect the client to a specific E4 for sensor data streaming.
        Returns an E4DeviceConnection for interacting directly with the
        specific device.

        Note that E4DeviceConnection is a context manager, and this method is
        intended to be used inside a 'with ... as' statement as follows:

        with client.connect_to_device(...) as client_conn: ...

        This ensures proper cleanup after finishing interacting with the device.

        :param device: The device to connect to.
        :return: An E4DeviceConnection context manager.
        """
        device = device.uid if isinstance(device, E4Device) else device
        resp = self._send_command(_CmdID.DEV_CONNECT, dev=device)

        if resp.status == _CmdStatus.SUCCESS:
            return E4DeviceConnection(client=self, dev_uid=device)
        else:
            raise DeviceNotFoundError(device)

    def disconnect_from_device(self) -> None:
        """
        Disconnect from the currently connected E4 device.

        Note: this method is automatically called by the corresponding
        E4ConnectionDevice context manager if used with the 'with ... as'
        statement.
        """
        resp = self._send_command(_CmdID.DEV_DISCONNECT)
        if resp.status != _CmdStatus.SUCCESS:
            raise ServerRequestError(resp.data)

    def subscribe_to_stream(self,
                            stream: E4DataStreamID,
                            callback: Callable[..., Any]) -> None:
        """
        Subscribes to the specified stream on the currently connected E4.

        :param stream: Stream to subscribe to.
        :param callback: Callback to execute for each received sample in the
        subscribed stream.
        """
        with self._callback_lock:
            if stream in self._sub_callbacks.keys():
                self._logger.error(f'Already subscribed to {stream.name}, '
                                   f'need to unsubscribe first to change '
                                   f'callback.')
                return
            else:
                self._sub_callbacks[stream] = callback

        resp = self._send_command(_CmdID.DEV_SUBSCRIBE,
                                  stream=stream, on=True)

        if resp.status != _CmdStatus.SUCCESS:
            with self._callback_lock:
                del self._sub_callbacks[stream]
            raise ServerRequestError(resp.data)

    def unsubscribe_from_stream(self, stream: E4DataStreamID) -> None:
        """
        Unsubscribes from the specified stream on the currently connected E4.

        :param stream: Stream to unsubscribe from.
        """
        resp = self._send_command(_CmdID.DEV_SUBSCRIBE,
                                  stream=stream, on=False)

        if resp.status != _CmdStatus.SUCCESS:
            raise ServerRequestError(resp.data)
        else:
            try:
                with self._callback_lock:
                    del self._sub_callbacks[stream]
            except KeyError:
                pass

    def pause(self) -> None:
        """
        Pause the streaming of sensor data from the currently connected E4.
        """
        resp = self._send_command(_CmdID.DEV_PAUSE, on=True)
        if resp.status != _CmdStatus.SUCCESS:
            raise ServerRequestError(resp.data)

    def resume(self) -> None:
        """
        Resume streaming of sensor data from the currently connected E4.
        """
        resp = self._send_command(_CmdID.DEV_PAUSE, on=False)
        if resp.status != _CmdStatus.SUCCESS:
            raise ServerRequestError(resp.data)

    def close(self) -> None:
        """
        Closes the connection to the server and shuts down the receiving and
        callback threads. Note that the client is left in an unusable state
        after this and cannot be reconnected to the server.

        Multiple calls to close() have no effect.
        """
        if self._connected:
            self._shutdown.set()
            self._socket.shutdown(socket.SHUT_RDWR)
            self._socket.close()
            self._callback_q.join()
            self._recv_thread.join()
            self._callback_thread.join()
            self._connected = False


class E4DeviceConnection(AbstractContextManager):
    """Context manager for device connections.

    Provides a simple interface to manage single device connections and
    subscriptions. Implemented as a context manager to automatize the
    clearing of subscriptions and disconnecting.
    """

    def __init__(self,
                 client: E4StreamingClient,
                 dev_uid: str):
        """
        Instantiates a new device connection. Not intended for external use,
        and should only be called by the E4StreamingClient.connect_to_device()
        method.

        :param client: underlying E4StreamingClient
        :param dev_uid: device currently connected to the streaming server.
        """
        self._client = client
        self._dev = dev_uid
        self._subscriptions = set()

        self._logger = logging.getLogger(self.__class__.__name__)
        self._paused = False

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Closes this device connection. See E4DeviceConnection.disconnect().
        """
        self.disconnect()

    @property
    def is_paused(self) -> bool:
        return self._paused

    @property
    def uid(self) -> str:
        """
        Unique ID of the currently connected device.
        """
        return self._dev

    def subscribe_to_stream(self,
                            stream: E4DataStreamID,
                            callback: Callable[..., Any]) -> None:
        """
        Subscribes to the specified stream on the currently connected E4 device.
        Each sample received for the stream will then be passed on to the
        specified callback. Note that the callback will be executed on a
        separate thread and should have a signature of the form:


        def callback(<stream id>, <timestamp>, <payload 1>, <payload 2>, ...)


        :param stream: stream to subscribe to.
        :param callback: Callback for the subscribed stream.
        """
        self._logger.debug(f'Subscribing to {stream}.')
        self._client.subscribe_to_stream(stream, callback)
        self._subscriptions.add(stream)

    def toggle_pause(self) -> None:
        """
        Pause/resume streaming of sensor data from this client connection.
        """
        if self._paused:
            self._client.resume()
        else:
            self._client.pause()

    def unsubscribe_from_stream(self, stream: E4DataStreamID) -> None:
        """
        Unsubscribes from a pre-established subscription.

        :param stream: Stream to unsubscribe from.
        """
        self._logger.debug(f'Unsubscribing from {stream}.')
        self._client.unsubscribe_from_stream(stream)
        self._subscriptions.remove(stream)

    def disconnect(self) -> None:
        """
        Disconnects from the current device.

        Note: should not be called directly, as it will automatically be
        called when exiting the current context if E4DeviceConnection is used
        as a context manager.
        """
        self._logger.debug(f'Disconnecting device {self._dev}.')
        for sub in self._subscriptions:
            self._client.unsubscribe_from_stream(sub)

        self._client.disconnect_from_device()
