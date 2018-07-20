### Asteriks posee tres APIs para interactuar: ARI, AGI y AMI

# Asterisk REST Interface (ARI)

- https://wiki.asterisk.org/wiki/pages/viewpage.action?pageId=29395573


- ARI consists of three different pieces that are - for all intents and purposes - interrelated and used together. They are:

        A RESTful interface that a client uses to control resources in Asterisk.
        A WebSocket that conveys events in JSON about the resources in Asterisk to the client.
        The Stasis dialplan application that hands over control of a channel from Asterisk to the client.

        ari = ARI('localhost', ('username', 'password'))
 
        #Hang up all channels
        channels = ari.get('channels')
        for channel in channels:
        ari.delete('channels', channel['id'])


# Asterisk Gateway Interface (AGI)


AGI is analogous to CGI in Apache. AGI provides an interface between the Asterisk dialplan and an external program that wants to manipulate a channel in the dialplan. In general, the interface is synchronous - actions taken on a channel from an AGI block and do not return until the action is completed.


- https://www.voip-info.org/asterisk-agi
- https://wiki.asterisk.org/wiki/pages/viewpage.action?pageId=29395573 - API Asterisk
- https://stackoverflow.com/questions/20043034/how-to-log-a-call-from-asterisk-to-external-web-service
- https://faucet.nz/ - Controlador
- https://www.youtube.com/channel/UChRZ5O2diT7QREazfQX0stQ/videos

## Python

- Fats http://sourceforge.net/projects/fats/ FastAGI & AMI for the Twisted framework, MIT license. Full code test covered, Mock Object pattern examples.
- PyAstre https://pypi.python.org/pypi/pyastre: Asterisk modules using Twisted framework.
- Python AGI http://sourceforge.net/projects/pyst
- Python AGI bindings py-Asterisk

##Manager interface with Plone/Zope atasterisk

- StarPy http://starpy.sourceforge.net/: Asterisk Twisted modules for AMI clients and FastAGI servers

#  Asterisk Manager Interface (AMI)

AMI provides a mechanism to control where channels execute in the dialplan. Unlike AGI, AMI is an asynchronous, event driven interface. For the most part, AMI does not provide mechanisms to control channel execution - rather, it provides information about the state of the channels and controls about where the channels are executing.