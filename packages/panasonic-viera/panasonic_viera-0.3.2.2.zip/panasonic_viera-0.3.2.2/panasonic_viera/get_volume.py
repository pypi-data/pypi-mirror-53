#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Implementation of https://github.com/florianholzapfel/panasonic-viera.RemoteControl
    using the sample from https://github.com/StevenLooman/async_upnp_client package as base
"""

from enum import Enum
import asyncio
import logging

from async_upnp_client import UpnpFactory
from async_upnp_client.aiohttp import AiohttpRequester

logging.basicConfig(level=logging.INFO)

URN_RENDERING_CONTROL = 'urn:schemas-upnp-org:service:RenderingControl:1'
URN_REMOTE_CONTROL = 'urn:panasonic-com:service:p00NetworkControl:1'
DEFAULT_PORT = 55000

class Keys(Enum):
    """Contains all known keys."""
    thirty_second_skip = 'NRC_30S_SKIP-ONOFF'
    toggle_3d = 'NRC_3D-ONOFF'
    apps = 'NRC_APPS-ONOFF'
    aspect = 'NRC_ASPECT-ONOFF'
    blue = 'NRC_BLUE-ONOFF'
    cancel = 'NRC_CANCEL-ONOFF'
    cc = 'NRC_CC-ONOFF'
    chat_mode = 'NRC_CHAT_MODE-ONOFF'
    ch_down = 'NRC_CH_DOWN-ONOFF'
    input_key = 'NRC_CHG_INPUT-ONOFF'
    network = 'NRC_CHG_NETWORK-ONOFF'
    ch_up = 'NRC_CH_UP-ONOFF'
    num_0 = 'NRC_D0-ONOFF'
    num_1 = 'NRC_D1-ONOFF'
    num_2 = 'NRC_D2-ONOFF'
    num_3 = 'NRC_D3-ONOFF'
    num_4 = 'NRC_D4-ONOFF'
    num_5 = 'NRC_D5-ONOFF'
    num_6 = 'NRC_D6-ONOFF'
    num_7 = 'NRC_D7-ONOFF'
    num_8 = 'NRC_D8-ONOFF'
    num_9 = 'NRC_D9-ONOFF'
    diga_control = 'NRC_DIGA_CTL-ONOFF'
    display = 'NRC_DISP_MODE-ONOFF'
    down = 'NRC_DOWN-ONOFF'
    enter = 'NRC_ENTER-ONOFF'
    epg = 'NRC_EPG-ONOFF'
    ez_sync = 'NRC_EZ_SYNC-ONOFF'
    favorite = 'NRC_FAVORITE-ONOFF'
    fast_forward = 'NRC_FF-ONOFF'
    game = 'NRC_GAME-ONOFF'
    green = 'NRC_GREEN-ONOFF'
    guide = 'NRC_GUIDE-ONOFF'
    hold = 'NRC_HOLD-ONOFF'
    home = 'NRC_HOME-ONOFF'
    index = 'NRC_INDEX-ONOFF'
    info = 'NRC_INFO-ONOFF'
    connect = 'NRC_INTERNET-ONOFF'
    left = 'NRC_LEFT-ONOFF'
    menu = 'NRC_MENU-ONOFF'
    mpx = 'NRC_MPX-ONOFF'
    mute = 'NRC_MUTE-ONOFF'
    net_bs = 'NRC_NET_BS-ONOFF'
    net_cs = 'NRC_NET_CS-ONOFF'
    net_td = 'NRC_NET_TD-ONOFF'
    off_timer = 'NRC_OFFTIMER-ONOFF'
    pause = 'NRC_PAUSE-ONOFF'
    pictai = 'NRC_PICTAI-ONOFF'
    play = 'NRC_PLAY-ONOFF'
    p_nr = 'NRC_P_NR-ONOFF'
    power = 'NRC_POWER-ONOFF'
    program = 'NRC_PROG-ONOFF'
    record = 'NRC_REC-ONOFF'
    red = 'NRC_RED-ONOFF'
    return_key = 'NRC_RETURN-ONOFF'
    rewind = 'NRC_REW-ONOFF'
    right = 'NRC_RIGHT-ONOFF'
    r_screen = 'NRC_R_SCREEN-ONOFF'
    last_view = 'NRC_R_TUNE-ONOFF'
    sap = 'NRC_SAP-ONOFF'
    toggle_sd_card = 'NRC_SD_CARD-ONOFF'
    skip_next = 'NRC_SKIP_NEXT-ONOFF'
    skip_prev = 'NRC_SKIP_PREV-ONOFF'
    split = 'NRC_SPLIT-ONOFF'
    stop = 'NRC_STOP-ONOFF'
    subtitles = 'NRC_STTL-ONOFF'
    option = 'NRC_SUBMENU-ONOFF'
    surround = 'NRC_SURROUND-ONOFF'
    swap = 'NRC_SWAP-ONOFF'
    text = 'NRC_TEXT-ONOFF'
    tv = 'NRC_TV-ONOFF'
    up = 'NRC_UP-ONOFF'
    link = 'NRC_VIERA_LINK-ONOFF'
    volume_down = 'NRC_VOLDOWN-ONOFF'
    volume_up = 'NRC_VOLUP-ONOFF'
    vtools = 'NRC_VTOOLS-ONOFF'
    yellow = 'NRC_YELLOW-ONOFF'

class RemoteControl:
    """This class represents a Panasonic Viera TV Remote Control."""

    @classmethod
    async def create(cls, host, port=DEFAULT_PORT):
        """Creates a remote control."""
        self = RemoteControl(host, port)
        requester = AiohttpRequester()
        factory = UpnpFactory(requester)

        target_dmr = 'http://{}:{}/dmr/ddd.xml'.format(self.host, self.port)
        self.device_dmr = await factory.async_create_device(target_dmr)
        if self.device_dmr.has_service(URN_RENDERING_CONTROL):
            self.service_dmr = self.device_dmr.service(URN_RENDERING_CONTROL)
            self.get_volume_action = self.service_dmr.action('GetVolume')
            self.set_volume_action = self.service_dmr.action('SetVolume')
            self.get_mute_action = self.service_dmr.action('GetMute')
            self.set_mute_action = self.service_dmr.action('SetMute')

        target_nrc = 'http://{}:{}/nrc/ddd.xml'.format(self.host, self.port)
        self.device_nrc = await factory.async_create_device(target_nrc)
        if self.device_nrc.has_service(URN_REMOTE_CONTROL):
            self.service_nrc = self.device_nrc.service(URN_REMOTE_CONTROL)
            self.send_key_action = self.service_nrc.action('X_SendKey')

        return self

    def __init__(self, host, port=DEFAULT_PORT):
        """Initialise the remote control."""
        self._host = host
        self._port = port

    @property
    def host(self) -> str:
        """Get the host of this device."""
        return self._host

    @property
    def port(self) -> int:
        """Get the port of this device."""
        return self._port

    async def get_volume(self):
        """Return the current volume level."""
        result = await self.get_volume_action.async_call(InstanceID=0, Channel='Master')
        return result['CurrentVolume']

    async def set_volume(self, volume):
        """Set a new volume level."""
        if volume > 100 or volume < 0:
            raise Exception('Bad request to volume control. '
                            'Must be between 0 and 100')
        await self.set_volume_action.async_call(InstanceID=0, Channel='Master', DesiredVolume=volume)

    async def get_mute(self):
        """Return if the TV is muted."""
        result = await self.get_mute_action.async_call(InstanceID=0, Channel='Master')
        return result['CurrentMute']

    async def set_mute(self, enable):
        """Mute or unmute the TV."""
        await self.set_mute_action.async_call(InstanceID=0, Channel='Master', DesiredMute=enable)

    async def send_key(self, key):
        """Send a key command to the TV."""
        if isinstance(key, Keys):
            key = key.value
        await self.send_key_action.async_call(X_KeyEvent=key)

    async def turn_off(self):
        """Turn off media player."""
        await self.send_key(Keys.power)

    async def turn_on(self):
        """Turn on media player."""
        await self.send_key(Keys.power)

    async def volume_up(self):
        """Volume up the media player."""
        await self.send_key(Keys.volume_up)

    async def volume_down(self):
        """Volume down media player."""
        await self.send_key(Keys.volume_down)

    async def mute_volume(self):
        """Send mute command."""
        await self.send_key(Keys.mute)

    async def media_play(self):
        """Send play command."""
        await self.send_key(Keys.play)

    async def media_pause(self):
        """Send media pause command to media player."""
        await self.send_key(Keys.pause)

    async def media_next_track(self):
        """Send next track command."""
        await self.send_key(Keys.fast_forward)

    async def media_previous_track(self):
        """Send the previous track command."""
        await self.send_key(Keys.rewind)

async def main():
    rc = await RemoteControl.create('192.168.178.20')
    print('Volume: {}'.format(await rc.get_volume()))
    print('Mute: {}'.format(await rc.get_mute()))

    await rc.set_volume(5)
    print('Volume: {}'.format(await rc.get_volume()))

    await rc.set_volume(10)
    print('Volume: {}'.format(await rc.get_volume()))

    await rc.set_mute(True)
    print('Mute: {}'.format(await rc.get_mute()))

    await rc.set_mute(False)
    print('Mute: {}'.format(await rc.get_mute()))

    await rc.volume_down()
    print('Volume: {}'.format(await rc.get_volume()))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
