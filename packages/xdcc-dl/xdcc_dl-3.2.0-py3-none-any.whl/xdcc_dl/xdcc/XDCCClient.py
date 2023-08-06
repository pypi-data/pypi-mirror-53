"""LICENSE
Copyright 2016 Hermann Krumrey <hermann@krumreyh.com>

This file is part of xdcc-dl.

xdcc-dl is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

xdcc-dl is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with xdcc-dl.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import os
import time
import struct
import shlex
import socket
import irc.events
import irc.client
from threading import Thread
from irc.client import DCCConnection
from colorama import Fore, Back
from typing import Optional, IO, Any, List
from xdcc_dl.entities import User, XDCCPack
from xdcc_dl.logging import Logger
from xdcc_dl.xdcc.exceptions import InvalidCTCPException, \
    AlreadyDownloadedException, DownloadCompleted, DownloadIncomplete, \
    PackAlreadyRequested, UnrecoverableError, Timeout, BotDoesNotExist
from irc.client import SimpleIRCClient, ServerConnection, Event, \
    ip_numstr_to_quad


class XDCCClient(SimpleIRCClient):
    """
    IRC Client that can download an XDCC pack
    """

    download_limit = -1
    """
    Maximum speed of the download in bytes/s
    If set to -1, will be unlimited
    """

    # Create a log command for all events that are printed in debug mode.
    # If methods are overriden manually, these generated methods won't take
    # effect.
    for event in irc.events.all:
        exec(
            "def on_{}(self, c, e):\n"
            "   self.handle_generic_event(\"{}\", c, e)"
            "".format(event, event)
        )

    def handle_generic_event(
            self,
            event_type: str,
            _: ServerConnection,
            event: Event
    ):
        """
        Handles a generic event that isn't handled explicitly
        :param event_type: The event type to handle
        :param _: The connection to use
        :param event: The received event
        :return: None
        """
        self.logger.debug("{}:{} {}".format(
            event_type,
            event.source,
            event.arguments
        ), back=Back.BLUE)

    def __init__(
            self,
            pack: XDCCPack,
            retry: bool = False,
            timeout: int = 120
    ):
        """
        Initializes the XDCC IRC client
        :param pack: The pack to downloadX
        :param retry: Set to true for retried downloads.
        :param timeout: Sets the timeout time for starting downloads
        """
        self.logger = Logger()

        # Save us from decoding errors!
        irc.client.ServerConnection.buffer_class.errors = "replace"

        self.user = User()
        self.pack = pack
        self.server = pack.server
        self.downloading = False
        self.xdcc_timestamp = 0.0
        self.channels = None  # type: Optional[List[str]]
        self.message_sent = False
        self.connect_start_time = 0.0
        self.timeout = timeout
        self.timed_out = False
        self.disconnected = False

        # XDCC state variables
        self.peer_address = ""
        self.peer_port = -1
        self.filesize = -1
        self.progress = 0
        self.xdcc_file = None  # type: Optional[IO[Any]]
        self.xdcc_connection = None  # type: Optional[DCCConnection]
        self.retry = retry

        if not self.retry:
            if self.download_limit == -1:
                limit = "\"unlimited\""
            else:
                limit = str(self.download_limit)
            self.logger.info("Download Limit set to: " + limit)

        super().__init__()

        def timeout_watcher():
            """
            Monitors when the XDCC  message is sent. If it is not sent by the
            timeout time, a ping will be sent and handled by the on_ping method
            :return: None
            """
            self.logger.info("Timeout watcher started")
            while not self.message_sent and not self.disconnected:
                time.sleep(1)
                self.logger.debug("Iterating timeout thread")
                if self.timeout < (time.time() - self.connect_start_time):
                    self.logger.info("Timeout detected")
                    self.connection.ping(self.server.address)
                    time.sleep(2)

        Thread(target=timeout_watcher).start()

    def download(self) -> str:
        """
        Downloads the pack
        :return: The path to the downloaded file
        """
        error = False
        completed = False
        pause = 0
        try:
            self.logger.info("Connecting to " + self.server.address + ":" +
                             str(self.server.port))
            self.connect(
                self.server.address,
                self.server.port,
                self.user.username
            )
            self.connect_start_time = time.time()
            self.start()
        except AlreadyDownloadedException:
            self.logger.error("File already downloaded")
            completed = True
        except DownloadCompleted:
            self.logger.print("File " + self.pack.filename +
                              " downloaded successfully")
            completed = True
        except DownloadIncomplete:
            self.logger.print("File " + self.pack.filename +
                              " not downloaded completely")
            completed = False
        except PackAlreadyRequested:
            self.logger.print("Pack already requested.")
            completed = False
            pause = 60
        except UnrecoverableError:
            error = True
        finally:
            self.logger.info("Disconnecting")
            try:
                self.disconnected = True
                self._disconnect()
            except (DownloadCompleted, ):
                pass

        if error:
            self.logger.info("Aborting because of unrecoverable error")
            return "Failed"

        self.logger.debug("Pausing for {}s".format(pause))
        time.sleep(pause)

        if not completed:
            self.logger.error("Download Incomplete. Retrying.")
            retry_client = XDCCClient(self.pack, True, self.timeout)
            retry_client.download_limit = self.download_limit
            retry_client.download()

        if not self.retry:
            dl_time = str(int(abs(time.time() - self.connect_start_time)))
            self.logger.info("Download completed in " + dl_time + " seconds.")

        return self.pack.get_filepath()

    def on_ping(self, _: ServerConnection, __: Event):
        """
        Handles a ping event.
        Used for timeout checks
        :param _: The IRC connection
        :param __: The received event
        :return: None
        """
        self.logger.debug("PING")
        if not self.message_sent \
                and self.timeout < (time.time() - self.connect_start_time) \
                and not self.timed_out:
            self.logger.error("Timeout")
            self.timed_out = True
            raise Timeout()

    def on_nosuchnick(self, _: ServerConnection, __: Event):
        """
        When a bot does not exist or is not online right now, aborts.
        :param _: The IRC connection
        :param __: The received event
        :return: None
        """
        self.logger.error("This bot does not exist on this server")
        raise BotDoesNotExist()

    def on_welcome(self, conn: ServerConnection, _: Event):
        """
        The 'welcome' event indicates a successful connection to the server
        Sends a whois command to find the bot on the server
        :param conn: The connection
        :param _: The 'welcome' event
        :return: None
        """
        self.logger.info("Connected to server")
        conn.whois(self.pack.bot)

    def on_whoischannels(self, conn: ServerConnection, event: Event):
        """
        The 'whoischannels' event indicates that a whois request has found
        channels that the bot is a part of.
        Channels that the bot has joined will be joined as well.
        :param conn: The connection
        :param event: The 'whoischannels' event
        :return: None
        """
        self.logger.info("WHOIS: " + str(event.arguments))
        channels = event.arguments[1].split("#")
        channels.pop(0)
        channels = list(map(lambda x: "#" + x.split(" ")[0], channels))
        self.channels = channels

        for channel in channels:
            # Join all channels to avoid only joining a members-only channel
            conn.join(channel)

    def on_endofwhois(self, conn: ServerConnection, _: Event):
        """
        The 'endofwhois' event indicates the end of a whois request.
        This manually calls on_join in case the bot
        has not joined any channels.
        :param conn: The connection
        :param _: The 'endofwhois' event
        :return: None
        """
        self.logger.info("WHOIS End")
        if self.channels is None:
            self.on_join(conn, _, True)

    def on_join(
            self,
            conn: ServerConnection,
            event: Event,
            force: bool = False
    ):
        """
        The 'join' event indicates that a channel was successfully joined.
        The first on_join call will send a message to the bot that requests
        the initialization of the XDCC file transfer.
        :param conn: The connection
        :param event: The 'join' event
        :param force: If set to True, will force sending an XDCC message
        :return: None
        """
        # Make sure we were the ones joining
        if not event.source.startswith(self.user.get_name()) and not force:
            return
        if force:
            self.logger.info(
                "Didn't find a channel using WHOIS, "
                "trying to send message anyways"
            )
        else:
            self.logger.info("Joined Channel: " + event.target)

        if not self.message_sent:
            self._send_xdcc_request_message(conn)

    def on_ctcp(self, conn: ServerConnection, event: Event):
        """
        The 'ctcp' event indicates that a CTCP message was received.
        The downloader receives a CTCP from the bot to initialize the
        XDCC file transfer.
        Handles DCC ACCEPT and SEND messages. Other DCC messages will result
        in a raised InvalidCTCP exception.
        DCC ACCEPT will only occur when a resume request was sent successfully.
        DCC SEND will occur when the bot offers a file.
        :param conn: The connection
        :param event: The 'ctcp' event
        :return: None
        :raise InvalidCTCPException: In case no valid DCC message was received
        """

        def start_download(append: bool = False):
            """
            Helper method that starts the download of an XDCC pack
            :param append: If set to True, opens the file in append mode
            :return: None
            """
            self.downloading = True
            self.xdcc_timestamp = time.time()
            mode = "ab" if append else "wb"
            self.logger.info("Starting Download (" + mode + ")")
            self.xdcc_file = open(self.pack.get_filepath(), mode)
            self.xdcc_connection = \
                self.dcc_connect(self.peer_address, self.peer_port, "raw")
            self.xdcc_connection.socket.settimeout(5)

        self.logger.info("CTCP Message: " + str(event.arguments))
        if event.arguments[0] == "DCC":
            payload = shlex.split(event.arguments[1])

            if payload[0] == "SEND":

                filename = payload[1]
                self.peer_address = ip_numstr_to_quad(payload[2])
                self.peer_port = int(payload[3])
                self.filesize = int(payload[4])

                self.pack.set_filename(filename)

                if os.path.isfile(self.pack.get_filepath()):

                    position = os.path.getsize(self.pack.get_filepath())

                    if position >= self.filesize:
                        raise AlreadyDownloadedException(self.pack.filename)

                    self.logger.info("Requesting Resume")
                    self.progress = position
                    bot = event.source.split("!")[0]
                    resume_param = "\"" + filename + "\" " + \
                                   str(self.peer_port) + " " + str(position)
                    conn.ctcp("DCC RESUME", bot, resume_param)

                else:
                    start_download()

            elif payload[0] == "ACCEPT":
                start_download(append=True)

            else:
                raise InvalidCTCPException(payload[0])

    def on_dccmsg(self, _: ServerConnection, event: Event):
        """
        The 'dccmsg' event contains the file data.
        :param _: The connection
        :param event: The 'dccmsg' event
        :return: None
        """
        if self.xdcc_file is None:
            return

        data = event.arguments[0]
        chunk_size = len(data)

        self.xdcc_file.write(data)
        self.progress += chunk_size

        # Limit the download speed
        if self.download_limit != -1:
            delta = abs(time.time() - self.xdcc_timestamp)
            chunk_time = chunk_size / self.download_limit
            sleep_time = chunk_time - delta

            if sleep_time > 0:
                self.logger.debug(
                    "{Throttling for %.2f seconds} " % sleep_time, end=""
                )
                time.sleep(sleep_time)

        percentage = "%.2f" % (100 * (self.progress / self.filesize))
        self.logger.print("[" + self.pack.filename + "]: (" +
                          percentage + "%) |" + str(self.progress) + "|",
                          end="\r", back=Back.LIGHTYELLOW_EX, fore=Fore.BLACK)

        self._ack()
        self.xdcc_timestamp = time.time()

    def on_dcc_disconnect(self, _: ServerConnection, __: Event):
        """
        The 'dccmsg' event contains the file data.
        :param _: The connection
        :param __: The 'dccmsg' event
        :return: None
        """
        self.downloading = False

        if self.xdcc_file is not None:
            self.xdcc_file.close()

        if self.progress >= self.filesize:
            raise DownloadCompleted()
        else:
            raise DownloadIncomplete()

    # noinspection PyMethodMayBeStatic
    def on_privnotice(self, _: ServerConnection, event: Event):
        """
        Handles privnotices. Bots sometimes send privnotices when
        a pack was already requested or the user is put into a queue.

        If the privnotice indicates that a pack was already requested,
        the downloader will pause for 60 seconds

        :param _: The connection
        :param event: The privnotice event
        :return: None
        """
        if "you already requested this pack" in event.arguments[0].lower():
            raise PackAlreadyRequested()
        else:
            self.logger.debug("privnotice: {}:{}".format(
                str(event.source), str(event.arguments), back=Back.BLUE)
            )
        # TODO Handle queues

    def on_error(self, _: ServerConnection, __: Event):
        """
        Sometimes, the connection gives an error which may prove fatal for
        the download process. A possible cause of error events is a banned
        IP address.
        :param _: The connection
        :param __: The error event
        :return: None
        """
        self.logger.error("Unrecoverable Error: Is this IP banned?")
        raise UnrecoverableError()

    def _send_xdcc_request_message(self, conn: ServerConnection):
        """
        Sends an XDCC request message
        :param conn: The connection to use
        :return: None
        """
        msg = self.pack.get_request_message()
        self.logger.info("Send XDCC Message: " + msg)
        self.message_sent = True
        conn.privmsg(self.pack.bot, msg)

    def _ack(self):
        """
        Sends the acknowledgement to the XDCC bot that a
        chunk has been received.
        This process is responsible for the program hanging due to a stuck
        socket.send.
        This is mitigated by completely disconnecting the client and restarting
        the download process with a new XDCC CLient
        :return: None
        """
        try:
            self.xdcc_connection.socket.send(struct.pack(b"!Q", self.progress))
        except socket.error:
            self._disconnect()

    def _disconnect(self):
        """
        Disconnects all connections of the XDCC Client
        :return: None
        """
        self.connection.reactor.disconnect_all()
