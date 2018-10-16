#!/usr/bin/env python
 
import logging
import requests
import ari
import threading
 
channel_timers = {}
CAC_THRESHOLD = 2
total_channels = 0
connectedChannels = {}
currentBridge = None
 
def getTotalChannels():
    ''' Count current connected channels '''
    localChannels = 0
    for connectedChannel in connectedChannels:
        if connectedChannels[connectedChannel]:
            localChannels = localChannels + 1

    totalChannels = localChannels
    return totalChannels

def safe_hangup(channel, bridge, frontClient):
    """Safely hang up the specified channel"""
    try:
        connectedChannels[ bridge.id ] = False
        channel.hangup()
        bridge.destroy()

        total_channels
        frontClient.broadcast("closeChannel", {
            "totalChannels": getTotalChannels()
        })

        print "Hung up {}".format(channel.json.get('name'))
    except requests.HTTPError as e:
        if e.response.status_code != requests.codes.not_found:
            raise e
 
 
def stasis_start_cb(channel_obj, ev, localClient, frontClient, ryuApi):
    """Handler for StasisStart"""
 
    client = localClient
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
        outgoing = client.channels.originate(endpoint=args[1],
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
 
        bridge = client.bridges.create(type='mixing')
        bridge.addChannel(channel=[channel.id, outgoing.id])

        connectedChannels[ bridge.id ] = True
        totalChannels = getTotalChannels()

        channel.on_event('StasisEnd', lambda *args: safe_hangup(outgoing, bridge, frontClient))
        outgoing.on_event('StasisEnd', lambda *args: safe_hangup(channel, bridge, frontClient))

        frontClient.broadcast("newChannel", {
            "currentNewChannel": channel.json.items(),
            "totalChannels": totalChannels
        })

        response = ryuApi.queryForGetPorts()
        frontClient.broadcast("queryForGetPorts", {
          "queryForGetPorts": response
        })

        # Hang up the channel in 4 seconds
        if totalChannels >= CAC_THRESHOLD:
            timer = threading.Timer(4, hangup_channel, [channel, frontClient])
            channel_timers[channel.id] = timer
            timer.start()
 
    def hangup_channel(channel, frontClient):
        """Callback that will actually hangup the channel"""
 
        print "Hanging up channel %s" % channel.json.get('name')
        channel.hangup()
        frontClient.broadcast("cacTrigger", {
            "data": 1
        })

    outgoing.on_event('StasisStart', outgoing_start_cb)
