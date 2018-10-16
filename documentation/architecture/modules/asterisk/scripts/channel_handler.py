#!/usr/bin/env python
 
import ari
import logging
import threading
 
logging.basicConfig(level=logging.ERROR)
 
client = ari.connect('http://10.10.10.109:8088/', 'asterisk', 'asterisk')
 
channel_timers = {}
 
def stasis_end_cb(channel, ev):
    """Handler for StasisEnd event"""
 
    print "Channel %s just left our application" % channel.json.get('name')
 
    # Cancel any pending timers
    timer = channel_timers.get(channel.id)
    if timer:
        timer.cancel()
        del channel_timers[channel.id]
 
def stasis_start_cb(channel_obj, ev):
    """Handler for StasisStart event"""
 
    def answer_channel(channel):
        """Callback that will actually answer the channel"""
        print "Answering channel %s" % channel.json.get('name')
        channel.answer()
        channel.startSilence()
 
        # Hang up the channel in 4 seconds
        timer = threading.Timer(4, hangup_channel, [channel])
        channel_timers[channel.id] = timer
        timer.start()
 
    def hangup_channel(channel):
        """Callback that will actually hangup the channel"""
 
        print "Hanging up channel %s" % channel.json.get('name')
        channel.hangup()
 
    channel = channel_obj.get('channel')
    print "Channel %s has entered the application" % channel.json.get('name')

    for key, value in channel.json.items():
        print "%s: %s" % (key, value)
 
    channel.ring()
    # Answer the channel after 5 seconds
    timer = threading.Timer(5, answer_channel, [channel])
    channel_timers[channel.id] = timer
    timer.start()
 
def channel_state_change_cb(channel, ev):
    """Handler for changes in a channel's state"""
    print "Channel %s is now: %s" % (channel.json.get('name'),
                                     channel.json.get('state'))
 
#Evento en StassisStart => ring, timer, contesto con answer_channel, luego hay event ChannelStateChange
#Una vez que contesto, funcion answer_channel da silencio por 4 segundos y llama a hangup_channel
#Esto genera event en StassisEnd, limpio timers pendientes y muestro informacion en pantalla
client.on_channel_event('StasisStart', stasis_start_cb) 
client.on_channel_event('ChannelStateChange', channel_state_change_cb) #solo muestro informacion del estado del canal
client.on_channel_event('StasisEnd', stasis_end_cb)
 
client.run(apps='channel-state')