# Orca
#
# Copyright 2004-2009 Sun Microsystems Inc.
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

"""Each script maintains a set of key bindings, braille bindings, and
AT-SPI event listeners.  The key bindings are an instance of
KeyBindings.  The braille bindings are also a dictionary where the
keys are BrlTTY command integers and the values are instances of
InputEventHandler.  The listeners field is a dictionary where the keys
are AT-SPI event names and the values are function pointers.

Instances of scripts are intended to be created solely by the
script manager.

This Script class is not intended to be instantiated directly.
Instead, it is expected that subclasses of the Script class will be
created in their own module.  The module defining the Script subclass
is also required to have a 'getScript(app)' method that returns an
instance of the Script subclass.  See default.py for an example."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2005-2009 Sun Microsystems Inc."
__license__   = "LGPL"

from . import ax_event_synthesizer
from . import action_presenter
from . import braille_generator
from . import debug
from . import event_manager
from . import flat_review_presenter
from . import formatting
from . import keybindings
from . import label_inference
from . import learn_mode_presenter
from . import mouse_review
from . import notification_presenter
from . import object_navigator
from . import script_utilities
from . import settings_manager
from . import sleep_mode_manager
from . import sound_generator
from . import speech_and_verbosity_manager
from . import speech_generator
from . import structural_navigation
from . import system_information_presenter
from . import table_navigator
from . import bookmarks
from . import where_am_i_presenter
from .ax_object import AXObject


class Script:
    """The specific focus tracking scripts for applications.
    """

    def __init__(self, app):
        """Creates a script for the given application, if necessary.
        This method should not be called by anyone except the
        script manager.

        Arguments:
        - app: the Python Accessible application to create a script for
        """
        self.app = app

        if app:
            self.name = AXObject.get_name(self.app) or "default"
        else:
            self.name = "default"

        self.name += " (module=" + self.__module__ + ")"

        self.listeners = self.getListeners()

        # By default, handle events for non-active applications.
        #
        self.presentIfInactive = True

        self.utilities = self.getUtilities()
        self.labelInference = self.getLabelInference()
        self.structuralNavigation = self.getStructuralNavigation()
        self.caretNavigation = self.getCaretNavigation()
        self.bookmarks = self.getBookmarks()
        self.liveRegionManager = self.getLiveRegionManager()
        self.notificationPresenter = self.getNotificationPresenter()
        self.flatReviewPresenter = self.getFlatReviewPresenter()
        self.speechAndVerbosityManager = self.getSpeechAndVerbosityManager()
        self.systemInformationPresenter = self.getSystemInformationPresenter()
        self.objectNavigator = self.getObjectNavigator()
        self.tableNavigator = self.getTableNavigator()
        self.whereAmIPresenter = self.getWhereAmIPresenter()
        self.learnModePresenter = self.getLearnModePresenter()
        self.mouseReviewer = self.getMouseReviewer()
        self.eventSynthesizer = self.getEventSynthesizer()
        self.actionPresenter = self.getActionPresenter()
        self.sleepModeManager = self.getSleepModeManager()

        self.chat = self.getChat()
        self.inputEventHandlers = {}
        self.pointOfReference = {}
        self.setupInputEventHandlers()
        self.keyBindings = keybindings.KeyBindings()
        self.brailleBindings = self.getBrailleBindings()

        self.formatting = self.getFormatting()
        self.brailleGenerator = self.getBrailleGenerator()
        self.soundGenerator = self.getSoundGenerator()
        self.speechGenerator = self.getSpeechGenerator()
        self.generatorCache = {}
        self.eventCache = {}
        self.spellcheck = self.getSpellCheck()

        self.findCommandRun = False

        msg = f'SCRIPT: {self.name} initialized'
        debug.printMessage(debug.LEVEL_INFO, msg, True)

    def __str__(self):
        return f"{self.name}"

    def getListeners(self):
        """Sets up the AT-SPI event listeners for this script.

        Returns a dictionary where the keys are AT-SPI event names
        and the values are script methods.
        """
        return {}

    def setupInputEventHandlers(self):
        """Defines InputEventHandler fields for this script that can be
        called by the key and braille bindings."""
        pass

    def getKeyBindings(self, enabledOnly=True):
        """Defines the key bindings for this script.

        Returns an instance of keybindings.KeyBindings.
        """
        return keybindings.KeyBindings()

    def getToolkitKeyBindings(self):
        """Returns the toolkit-specific keybindings for this script."""

        return keybindings.KeyBindings()

    def getAppKeyBindings(self):
        """Returns the application-specific keybindings for this script."""

        return keybindings.KeyBindings()

    def getBrailleBindings(self):
        """Defines the braille bindings for this script.

        Returns a dictionary where the keys are BrlTTY commands and the
        values are InputEventHandler instances.
        """
        return {}

    def getFormatting(self):
        """Returns the formatting strings for this script."""
        return formatting.Formatting(self)

    def getBrailleGenerator(self):
        """Returns the braille generator for this script.
        """
        return braille_generator.BrailleGenerator(self)

    def getSoundGenerator(self):
        """Returns the sound generator for this script."""
        return sound_generator.SoundGenerator(self)

    def getSpeechGenerator(self):
        """Returns the speech generator for this script.
        """
        return speech_generator.SpeechGenerator(self)

    def getChat(self):
        """Returns the 'chat' class for this script.
        """
        return None

    def getSpellCheck(self):
        """Returns the spellcheck support for this script."""
        return None

    def getCaretNavigation(self):
        """Returns the caret navigation support for this script."""
        return None

    def getUtilities(self):
        """Returns the utilities for this script."""
        return script_utilities.Utilities(self)

    def getLabelInference(self):
        """Returns the label inference functionality for this script."""
        return label_inference.LabelInference(self)

    def getEnabledStructuralNavigationTypes(self):
        """Returns a list of the structural navigation object types
        enabled in this script.
        """
        return []

    def getStructuralNavigation(self):
        """Returns the 'structural navigation' class for this script."""
        types = self.getEnabledStructuralNavigationTypes()
        enable = settings_manager.getManager().getSetting('structuralNavigationEnabled')
        return structural_navigation.StructuralNavigation(self, types, enable)

    def getLiveRegionManager(self):
        """Returns the live region support for this script."""
        return None

    def getNotificationPresenter(self):
        return notification_presenter.getPresenter()

    def getFlatReviewPresenter(self):
        return flat_review_presenter.getPresenter()

    def getSystemInformationPresenter(self):
        return system_information_presenter.getPresenter()

    def getObjectNavigator(self):
        return object_navigator.getNavigator()

    def getTableNavigator(self):
        return table_navigator.getNavigator()

    def getSpeechAndVerbosityManager(self):
        return speech_and_verbosity_manager.getManager()

    def getWhereAmIPresenter(self):
        return where_am_i_presenter.getPresenter()

    def getLearnModePresenter(self):
        return learn_mode_presenter.getPresenter()

    def getActionPresenter(self):
        return action_presenter.getPresenter()

    def getSleepModeManager(self):
        return sleep_mode_manager.getManager()

    def getMouseReviewer(self):
        return mouse_review.getReviewer()

    def getEventSynthesizer(self):
        return ax_event_synthesizer.getSynthesizer()

    def getBookmarks(self):
        """Returns the "bookmarks" class for this script.
        """
        try:
            return self.bookmarks
        except AttributeError:
            self.bookmarks = bookmarks.Bookmarks(self)
            return self.bookmarks

    def getAppPreferencesGUI(self):
        """Return a GtkGrid containing the application unique configuration
        GUI items for the current application.
        """
        return None

    def getPreferencesFromGUI(self):
        """Returns a dictionary with the app-specific preferences."""

        return {}

    def registerEventListeners(self):
        """Tells the event manager to start listening for all the event types
        of interest to the script.

        Arguments:
        - script: the script.
        """

        event_manager.getManager().registerScriptListeners(self)

    def deregisterEventListeners(self):
        """Tells the event manager to stop listening for all the event types
        of interest to the script.

        Arguments:
        - script: the script.
        """

        event_manager.getManager().deregisterScriptListeners(self)

    def processObjectEvent(self, event):
        """Processes all AT-SPI object events of interest to this
        script.  The interest in events is specified via the
        'listeners' field that was defined during the construction of
        this script.

        Note that this script may be passed events it doesn't care
        about, so it needs to react accordingly.

        Arguments:
        - event: the Event
        """

        if self.skipObjectEvent(event):
            return

        # Clear the generator cache for each event.
        #
        self.generatorCache = {}

        # This calls the first listener it finds whose key *begins with* or is
        # the same as the event.type.  The reason we do this is that the event
        # type in the listeners dictionary may not be as specific as the event
        # type we received (e.g., the listeners dictionary might contain the
        # key "object:state-changed:" and the event.type might be
        # "object:state-changed:focused".  [[[TODO: WDW - the order of the
        # keys is *not* deterministic, and is not guaranteed to be related
        # to the order in which they were added.  So...we need to do something
        # different here.  Logged as bugzilla bug 319781.]]]
        #
        for key in self.listeners.keys():
            if event.type.startswith(key):
                self.listeners[key](event)

    def _getQueuedEvent(self, eventType, detail1=None, detail2=None, any_data=None):
        cachedEvent, eventTime = self.eventCache.get(eventType, [None, 0])
        if not cachedEvent:
            tokens = ["SCRIPT: No queued event of type", eventType]
            debug.printTokens(debug.LEVEL_INFO, tokens, True)
            return None

        if detail1 is not None and detail1 != cachedEvent.detail1:
            tokens = ["SCRIPT: Queued event's detail1 (", cachedEvent.detail1,
                      ") doesn't match", detail1]
            debug.printTokens(debug.LEVEL_INFO, tokens, True)
            return None

        if detail2 is not None and detail2 != cachedEvent.detail2:
            tokens = ["SCRIPT: Queued event's detail2 (", cachedEvent.detail2,
                      ") doesn't match", detail2]
            debug.printTokens(debug.LEVEL_INFO, tokens, True)
            return None

        if any_data is not None and any_data != cachedEvent.any_data:
            tokens = ["SCRIPT: Queued event's any_data (",
                      cachedEvent.any_data, ") doesn't match", any_data]
            debug.printTokens(debug.LEVEL_INFO, tokens, True)
            return None

        tokens = ["SCRIPT: Found matching queued event:", cachedEvent]
        debug.printTokens(debug.LEVEL_INFO, tokens, True)
        return cachedEvent

    def skipObjectEvent(self, event):
        """Gives us, and scripts, the ability to decide an event isn't
        worth taking the time to process under the current circumstances.

        Arguments:
        - event: the Event

        Returns True if we shouldn't bother processing this object event.
        """

        cachedEvent, eventTime = self.eventCache.get(event.type, [None, 0])
        if not cachedEvent or cachedEvent == event:
            return False

        focus    = ["object:state-changed:focused"]
        typing   = ["object:text-changed:insert", "object:text-changed:delete"]
        arrowing = ["object:text-caret-moved", "object:text-selection-changed",
                    "object:selection-changed", "object:active-descendant-changed"]

        skip = False
        if (event.type in arrowing or event.type in typing) \
           and event.source == cachedEvent.source:
            skip = True
            reason = "more recent event of the same type in the same object"
        elif event.type in focus and event.source != cachedEvent.source \
             and event.type == cachedEvent.type \
             and event.detail1 == cachedEvent.detail1:
            skip = True
            reason = "more recent event of the same type in a different object"
        elif event.type.endswith("system") and event.source == cachedEvent.source:
            skip = True
            reason = "more recent system event in the same object"
        elif event.type.startswith("object:state-changed") \
             and event.type == cachedEvent.type \
             and event.source == cachedEvent.source \
             and event.detail1 == cachedEvent.detail1:
            skip = True
            reason = "appears to be duplicate state-changed event"

        if skip:
            tokens = ["SCRIPT: Skipping object event:", reason, cachedEvent]
            debug.printTokens(debug.LEVEL_INFO, tokens, True)

        return skip

    def locusOfFocusChanged(self, event, oldLocusOfFocus, newLocusOfFocus):
        """Updates state and presents changes to the user in response to a
        notification from the FocusManager. Do not call this method outside
        of the FocusManager.

        Arguments:
        - event: if not None, the Event that caused the change
        - oldLocusOfFocus: Accessible that is the old locus of focus
        - newLocusOfFocus: Accessible that is the new locus of focus
        """
        pass

    def isActivatableEvent(self, event):
        """Returns True if the given event is one that should cause this
        script to become the active script.  This is only a hint to
        the focus tracking manager and it is not guaranteed this
        request will be honored.  Note that by the time the focus
        tracking manager calls this method, it thinks the script
        should become active.  This is an opportunity for the script
        to say it shouldn't.
        """
        return True

    def forceScriptActivation(self, event):
        """Allows scripts to insist that they should become active."""

        return False

    def activate(self):
        """Called when this script is activated."""
        pass

    def deactivate(self):
        """Called when this script is deactivated."""
        pass

    def getTransferableAttributes(self):
        return {}
