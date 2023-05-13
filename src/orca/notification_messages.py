# Orca
#
# Copyright 2010 Informal Informatica LTDA.
# Author: Jose Vilmar <vilmar@informal.com.br>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., Franklin Street, Fifth Floor,
# Boston MA  02110-1301 USA.

"""Module for notification messages"""
__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2010 Informal Informatica LTDA."
__license__   = "LGPL"

import gi
gi.require_version("Atspi", "2.0")
from gi.repository import Atspi

from . import cmdnames
from . import debug
from . import input_event
from . import messages
from . import orca_state

# to store  the messages generated by the notification daemon
notificationMessages = []

# max size of the list
maxSizeList = 55

# a index to walk in the list of messages
indexNotificationMessages = 0

# number of keys invalid while in when in list notification mode.
# if > 3, call _help()
invalidKeys = 0

# input event handlers
inputEventHandlers = {}

def repeatLastNotificationMessage(script, inputEvent=None):
    """ Repeats the last notification message. """

    _showNotificationMessage(script, 1)
    return True

def repeatPreviousNotificationMessage(script, inputEvent=None):
    """ Repeats the previous notification message. """

    _showNotificationMessage(script, 2)
    return True

def enableNotificationMessageListMode(script, inputEvent=None):
    """ Enables the list of notification message. """

    _listModeEnable(script)
    return True

inputEventHandlers["repeatLastNotificationMessageHandler"] = \
        input_event.InputEventHandler(
            repeatLastNotificationMessage,
            cmdnames.NOTIFICATION_MESSAGES_LAST)

inputEventHandlers["repeatPreviousNotificationMessageHandler"] = \
        input_event.InputEventHandler(
            repeatPreviousNotificationMessage,
            cmdnames.NOTIFICATION_MESSAGES_PREVIOUS)

inputEventHandlers["enableNotificationMessageListModeHandler"] = \
        input_event.InputEventHandler(
            enableNotificationMessageListMode,
            cmdnames.NOTIFICATION_MESSAGES_LIST)

def _showMessage(script, msg):
    script.presentMessage(msg)

def saveMessage(msg):
    """save the message in a list to be presented later"""

    while size() >= maxSizeList:
        del notificationMessages[0]

    notificationMessages.append(msg)

    debug.println(debug.LEVEL_FINEST, \
                   "saveMessage (queue length: %s)"\
                   % (size()))

def size():
    """ return the size of the queue messages """

    return len(notificationMessages)

def _messagesPresent(script):

    if size() <= 0:
        _showMessage(script, messages.NOTIFICATION_NO_MESSAGES)
        return False

    return True

def _listModeEnable(script):
    """ enable the list mode if the queue is not empty """

    global indexNotificationMessages
    global invalidKeys
    if _messagesPresent(script):
        indexNotificationMessages = 1
        invalidKeys = 0
        orca_state.listNotificationsModeEnabled = True
        _help(script, True)
        _showNotificationMessage(script, indexNotificationMessages)

    return True

def _showNotificationMessage(script, index):
    global indexNotificationMessages
    if not _messagesPresent(script):
        return

    if index < 1:
        index = 1
        _showMessage(script, messages.NOTIFICATION_LIST_TOP)
    elif index > size():
        index = size()
        _showMessage(script, messages.NOTIFICATION_LIST_BOTTOM)

    indexNotificationMessages = index
    index = size() - index
    debug.println(debug.LEVEL_FINEST, \
                   "_showNotificationMessage (queue length: %s, index: %s)"\
                   % (size(), index))
    if index >= 0 and index < size():
        msg = notificationMessages[index]
        _showMessage(script, msg)

def exitListNotificationMessagesMode(script):
    """ Turns list notification messages mode off. """

    orca_state.listNotificationsModeEnabled = False
    _showMessage(script, messages.NOTIFICATION_LIST_EXIT)

def listNotificationMessages(script, event):
    """ When list notification messages  mode is enabled, this function
    provides a means by which users can navigate through the list the
    notification messages. User can use the navigation keys or press
    the number of the message. Pressing escape key disable the mode.
    """

    global indexNotificationMessages
    global invalidKeys
    consumed = True
    speak = True

    if event.type != Atspi.EventType.KEY_PRESSED_EVENT:
        return False
    script.presentationInterrupt()
    if event.event_string == "Escape":
        exitListNotificationMessagesMode(script)
        speak = False
    elif event.event_string == "Home":
        indexNotificationMessages = 1
    elif event.event_string == "End":
        indexNotificationMessages = size()
    elif event.event_string == "Up":
        indexNotificationMessages -= 1
    elif event.event_string == "Down":
        indexNotificationMessages += 1
    elif event.event_string in\
                   [ '1', '2', '3', '4', '5', '6', '7', '8', '9' ]:
        indexNotificationMessages = int(event.event_string)
    elif event.event_string in [ 'h', 'H']:
        _help(script, True)
        speak = False
    elif event.event_string == "space":
        pass
    else:
        speak = False
        invalidKeys += 1
        if invalidKeys > 2:
            _help(script)
            invalidKeys = 0

    if speak:
        _showNotificationMessage(script, indexNotificationMessages)
        invalidKeys = 0

    return consumed

def _help(script, longHelp = False):
    msg = messages.messagesCount(size())
    msg += messages.NOTIFICATION_LIST_HELP
    if longHelp:
        msg += messages.NOTIFICATION_LIST_TUTORIAL

    _showMessage(script, msg)
