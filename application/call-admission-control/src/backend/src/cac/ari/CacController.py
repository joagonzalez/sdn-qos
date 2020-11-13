import os
import sys
import logging
import ari
import requests
import threading

from ...config.settings import config
from .BaseController import BaseController

CAC_VERSION = 'v1'

var = os.getenv('CAC_VERSION')

if var != None:
    CAC_VERSION = var

class CacController(BaseController):
  channel_timers = {}
  CAC_THRESHOLD = 2
  total_channels = 0
  incomingChannels = 0
  connectedChannels = {}
  currentBridge = None
  cacEnable = True
  qosEnable = True

  def __init__(self, ryuApi, frontClient):
    ''' Stasis Program '''
    BaseController.__init__(self, ryuApi, frontClient)
    self.subscribe(self.onStartCallback)

  def getTopologySwitches(self):
    '''
    Get topology open flow switches
    '''
    response = self.ryuApi.getTopologySwitches()
    
    self.frontClient.broadcast("getTopologySwitches", {
            "topologySwitches": response,
        })

  def getTopologyLinks(self):
    '''
    Get topology links
    '''
    response = self.ryuApi.getTopologyLinks()
    
    self.frontClient.broadcast("getTopologyLinks", {
            "topologyLinks": response,
        })

  def onStartCallback(self, channel_obj, ev):
    ''' Handler for StasisStart '''
    channel = channel_obj.get('channel')

    if CAC_VERSION == 'v2':
      if ev.get('args')[0] == "inbound" :
          self.incomingChannels += 1
      print '### Incoming CHANNELS:'
      print self.incomingChannels
      print "CAC Enable: {}".format(self.cacEnable)
      if self.incomingChannels > self.CAC_THRESHOLD and self.cacEnable:
          print "Error: {} Call rejection by CAC mechanism!"
          print "CAC Version: {}".format(CAC_VERSION)
          
          channel.hangup()
          self.incomingChannels -= 1

          self.frontClient.broadcast("cacTrigger", {
            "data": 1
          })
          
          self.frontClient.broadcast("closeChannel", {
              "totalChannels": self.incomingChannels,
              "channelId": channel.json.get('name')
          })

          return 
    
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

    # for key, value in channel.json.items():
    #     print "%s: %s" % (key, value)

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

        if CAC_VERSION == 'v1':
          CacController.connectedChannels[ bridge.id ] = True
          totalChannels = CacController.getTotalChannels()
        else:
          self.incomingChannels += 1
          totalChannels = self.incomingChannels

        channel.on_event('StasisEnd', lambda *args: self.safe_hangup(outgoing, bridge))
        outgoing.on_event('StasisEnd', lambda *args: self.safe_hangup(channel, bridge))

        self.frontClient.broadcast("newChannel", {
            "currentNewChannel": channel.json.items(),
            "totalChannels": totalChannels
        })

        if self.cacEnable and CAC_VERSION == 'v1':
            # Hang up the channel in 0 seconds
            if totalChannels > self.CAC_THRESHOLD:
                print "CAC Version: {}".format(CAC_VERSION)
                timer = threading.Timer(0, hangup_channel, [channel])
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
        if CAC_VERSION == 'v1':
          self.connectedChannels[ bridge.id ] = False
          totalChannels = self.getTotalChannels()
        else:
          self.incomingChannels -= 1
          totalChannels = self.incomingChannels

        channel.hangup()
        bridge.destroy()

        self.frontClient.broadcast("closeChannel", {
            "totalChannels": totalChannels,
            "channelId": channel.json.get('name')
        })

        print "Hung up {}".format(channel.json.get('name'))
    except requests.HTTPError as e:
        if e.response.status_code != requests.codes.not_found:
            raise e
