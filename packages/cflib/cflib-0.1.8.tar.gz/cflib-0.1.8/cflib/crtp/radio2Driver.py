#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2011-2013 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
"""
Crazyradio CRTP link driver.

This driver is used to communicate with the Crazyflie using the Crazyradio
USB dongle.

Version 2 of the driver solving scalability issues
"""
import array
import binascii
import collections
import logging
import re
import struct
import sys
import threading

from .crtpstack import CRTPPacket
from .exceptions import WrongUriType
from cflib.crtp.crtpdriver import CRTPDriver
from cflib.drivers.crazyradio import Crazyradio

if sys.version_info < (3,):
    import Queue as queue  # pylint: disable=E0401
else:
    import queue


__author__ = 'Bitcraze AB'
__all__ = ['Radio2Driver']

logger = logging.getLogger(__name__)

_nr_of_retries = 100
_nr_of_arc_retries = 3

DEFAULT_ADDR_A = [0xe7, 0xe7, 0xe7, 0xe7, 0xe7]
DEFAULT_ADDR = 0xE7E7E7E7E7

class Radio2Driver(CRTPDriver):
    """ Crazyradio link driver """

    def __init__(self):
        """ Create the link driver """
        CRTPDriver.__init__(self)


    def connect(self, uri, link_quality_callback, link_error_callback):
        """
        Connect the link driver to a specified URI of the format:
        radio://<dongle nbr>/<radio channel>/[250K,1M,2M]

        The callback for linkQuality can be called at any moment from the
        driver to report back the link quality in percentage. The
        callback from linkError will be called when a error occurs with
        an error message.
        """

        # check if the URI is a radio URI
        if not re.search('^radio2://', uri):
            raise WrongUriType('Not a radio URI')

        # Open the USB dongle
        if not re.search('^radio2://([0-9]+)((/([0-9]+))'
                         '((/(250K|1M|2M))?(/([A-F0-9]+))?)?)?$', uri):
            raise WrongUriType('Wrong radio URI format!')

        uri_data = re.search('^radio2://([0-9]+)((/([0-9]+))'
                             '((/(250K|1M|2M))?(/([A-F0-9]+))?)?)?$', uri)

        self.uri = uri

        channel = 2
        if uri_data.group(4):
            channel = int(uri_data.group(4))

        datarate = Crazyradio.DR_2MPS
        if uri_data.group(7) == '250K':
            datarate = Crazyradio.DR_250KPS
        if uri_data.group(7) == '1M':
            datarate = Crazyradio.DR_1MPS
        if uri_data.group(7) == '2M':
            datarate = Crazyradio.DR_2MPS

        address = DEFAULT_ADDR_A
        if uri_data.group(9):
            addr = str(uri_data.group(9))
            new_addr = struct.unpack('<BBBBB', binascii.unhexlify(addr))
            address = new_addr
    
        # self._crtpQeue = 



    def receive_packet(self, time=0):
        """
        Receive a packet though the link. This call is blocking but will
        timeout and return None if a timeout is supplied.
        """
        pass

    def send_packet(self, pk):
        """ Send the packet pk though the link """
        pass

    def close(self):
        """ Close the link. """
        pass

    def _scan_radio_channels(self, cradio, start=0, stop=125):
        """ Scan for Crazyflies between the supplied channels. """
        return []

    def scan_selected(self, links):
        return []

    def scan_interface(self, address):
        """ Scan interface for Crazyflies """
        return []

    def get_status(self):
        return 'plop'

    def get_name(self):
        return 'radio2'

#### Multiple crazyradio handling ####
radioEngines = []

class _CrtpQueue():
    """
    Encapsulate tx and rx crtp/event queues to a radio communication engine
    close must be called to terminate the connection
    """
    def __init__(self, sendQueue, receiveQueue):
        self.sendQueue = sendQueue
        self.receiveQueue = receiveQueue

def _create_crtp_queue(radio_id, channel, address):
    """
    Create a connection to radio_id, channel, address and returns a radio queue to it
    """
    pass

class _RadioEngine():
    """
    Handles communication of one Crazyradio to one to many Crazyflies
    Communicates with the rest of the firmware using data queues
    """
    def __init__(self, deviceId):
        self._radio = None
        self._configurations = []
        self._configLock = threading.Lock()
        self._thread = None
        self._deviceId = deviceId

        self.ncycle = 0

    def add_connection(self, channel, datarate, address):
        sendQueue = queue.Queue()
        receiveQueue = queue.Queue()

        crtpQueue = _CrtpQueue(sendQueue, receiveQueue)

        config = {
            "type": "connection",
            "channel": channel,
            "datarate": datarate,
            "address": address,
            "queues": crtpQueue
        }

        with self._configLock:
            self._configurations.append(config)

            if not self._thread or not self._thread.is_alive():
                self._thread = threading.Thread(target=self._communicationLoop, daemon=True)
                self._thread.start()
        
        return crtpQueue
    
    def remove_connection(self, channel, datarate, address):
        with self._configLock:
            for c in self._configurations:
                if c["type"] == "connection" and \
                   c["channel"] == channel and \
                   c["datarate"] == datarate and \
                   c["address"] == address:
                   self._configurations.remove(c)

                   return True

        return False

    def _communicationLoop(self):
        self._radio = Crazyradio(devid=self._deviceId)
        self._radio.set_arc(0)

        while len(self._configurations) > 0:
            with self._configLock:
                for c in self._configurations:
                    if c["type"] == "connection":
                        self._connection_cycle(c)
                    elif c["type"] == "scann" and not c["done"]:
                        self._scann_cycle(c)
                        c["done"] = True
        
        self._radio.close()
        self._radio = None
    
    def _connection_cycle(self, config):
        self.ncycle += 1

        """ Runs one connection cycle on one configuration """
        self._radio.set_channel(config["channel"])
        self._radio.set_address(config["address"])
        self._radio.set_data_rate(config["datarate"])

        try:
            packet = config["queues"].sendQueue.get(block = False)
        except queue.Empty:
            packet = [0xff]
        
        ack = self._radio.send_packet(packet)

        if ack and ack.ack and len(ack.data) > 0:
            config["queues"].receiveQueue.put(ack.data, block=False)
            
    
    def _scann_cycle(self, config):
        """ Scann for Crazyflies """
        pass
