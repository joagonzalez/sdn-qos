import sys
import logging
import ari
import requests
import threading

from ...config.settings import config
from .BaseController import BaseController

class CacController(BaseController):
  channel_timers = {}
  CAC_THRESHOLD = 2
  total_channels = 0
  connectedChannels = {}
  currentBridge = None

  def __init__(self, ryuApi, frontClient):
    ''' Stasis Program '''
    BaseController.__init__(self, ryuApi, frontClient)
    self.subscribe(self.onStartCallback)

  def doSomething(self):
    ''' esto deberia moverse al Facade que expone el metodo '''
    response = self.ryuApi.queryForGetNodes()
    return response

  def doGetPorts(self):
    ''' esto deberia moverse al Facade que expone el metodo '''
    return self.ryuApi.queryForGetPorts()

  def onStartCallback(self, channel_obj, ev):
    ''' Handler for StasisStart '''
    channel = channel_obj.get('channel')
    channel_name = channel.json.get('name')
    args = ev.get('args')
 
    if not args:
        print "Error: {} didn't provide any arguments!".format(channel_name)
        return
 
    if args and args[0] != 'inbound':
        # Only handle inbound channels here
        return
 
    if len(args) != 2:
        print "Error: {} didn't tell us who to dial".format(channel_name)
        channel.hangup()
        return
 
    print "{} entered our application".format(channel_name)

    for key, value in channel.json.items():
        print "%s: %s" % (key, value)

    channel.ring()
 
    try:
        print "Dialing {}".format(args[1])
        outgoing = self.client.channels.originate(endpoint=args[1],
                                             app='cac',
                                             appArgs='dialed')
    except requests.HTTPError:
        print "Whoops, pretty sure %s wasn't valid" % args[1]
        channel.hangup()
        return
 
    def outgoing_start_cb(channel_obj, ev):
        """StasisStart handler for our dialed channel"""   
        print "{} answered; bridging with {}".format(outgoing.json.get('name'),
                                                     channel.json.get('name'))
        channel.answer()
 
        bridge = self.client.bridges.create(type='mixing')
        bridge.addChannel(channel=[channel.id, outgoing.id])

        CacController.connectedChannels[ bridge.id ] = True
        totalChannels = CacController.getTotalChannels()

        channel.on_event('StasisEnd', lambda *args: self.safe_hangup(outgoing, bridge))
        outgoing.on_event('StasisEnd', lambda *args: self.safe_hangup(channel, bridge))

        self.frontClient.broadcast("newChannel", {
            "currentNewChannel": channel.json.items(),
            "totalChannels": totalChannels
        })

        response = self.ryuApi.queryForGetPorts()
        self.frontClient.broadcast("queryForGetPorts", {
          "queryForGetPorts": response
        })

        # Hang up the channel in 4 seconds
        if totalChannels >= self.CAC_THRESHOLD:
            timer = threading.Timer(4, hangup_channel, [channel])
            self.channel_timers[channel.id] = timer
            timer.start()
 
    def hangup_channel(channel):
        """Callback that will actually hangup the channel"""
 
        print "Hanging up channel %s" % channel.json.get('name')
        channel.hangup()
        self.frontClient.broadcast("cacTrigger", {
            "data": 1
        })

    outgoing.on_event('StasisStart', outgoing_start_cb)

  @staticmethod
  def getTotalChannels():
    ''' Count current connected channels '''
    localChannels = 0
    for connectedChannel in CacController.connectedChannels:
        if CacController.connectedChannels[connectedChannel]:
            localChannels = localChannels + 1

    totalChannels = localChannels
    return totalChannels

  def safe_hangup(self, channel, bridge):
    """Safely hang up the specified channel"""
    try:
        self.connectedChannels[ bridge.id ] = False
        channel.hangup()
        bridge.destroy()

        self.frontClient.broadcast("closeChannel", {
            "totalChannels": self.getTotalChannels()
        })

        print "Hung up {}".format(channel.json.get('name'))
    except requests.HTTPError as e:
        if e.response.status_code != requests.codes.not_found:
            raise e
