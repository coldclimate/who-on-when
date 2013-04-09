#!/usr/bin/python
import dbus, dbus.glib, dbus.decorators, gobject, redis
from time import gmtime, strftime

bus = dbus.SessionBus() 
obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject") 
purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface") 
r = redis.StrictRedis(host='localhost', port=6379, db=0)
day = strftime("%a", gmtime())
hour = strftime("%H", gmtime())
minute = strftime("%M", gmtime())

protocols = {
    "jabber": "prpl-jabber",
    "facebook": "prpl-jabber",
    "icq": "prpl-icq",
    "msn": "prpl-msn",
    "gtalk": "prpl-jabber",
    "yahoo": "prpl-yahoo",
} # List of protocols: http://developer.pidgin.im/wiki/prpl_id

### Config starts ###
account_name = "therealoliwood@chat.facebook.com" # Must already be logged on.
account_protocol = "facebook" # Change this with the platform
### Config ends ###

account = purple.PurpleAccountsFind(account_name, protocols[account_protocol]) # Get the account information
buddylist = purple.PurpleFindBuddies(account,'') # Get a list of all buddies

for buddy in buddylist: # Sending a message to all online buddies
    if purple.PurpleBuddyIsOnline(buddy): 
        name=purple.PurpleBuddyGetAlias(buddy).replace(" ","_")
	key="%s_%s_%s_%s" % (name,day,hour,minute)
        r.incr(key)

