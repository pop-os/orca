# Orca
#
# Copyright 2004-2009 Sun Microsystems Inc.
# Copyright 2010-2011 The Orca Team
# Copyright 2012 Igalia, S.L.
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

"""The main module for the Orca screen reader."""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2004-2009 Sun Microsystems Inc." \
                "Copyright (c) 2010-2011 The Orca Team" \
                "Copyright (c) 2012 Igalia, S.L."
__license__   = "LGPL"


# ruff: noqa: F401
# This unused import keeps Orca working by making pyatspi still available.
# It can only be removed when we have completely eliminated all uses of
# pyatspi API.
import pyatspi

import faulthandler
import gi
import importlib
import os
import re
import signal
import subprocess
import sys

gi.require_version("Atspi", "2.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Atspi
from gi.repository import Gdk

try:
    from gi.repository.Gio import Settings
    a11yAppSettings = Settings(schema_id='org.gnome.desktop.a11y.applications')
except Exception:
    a11yAppSettings = None

from . import braille
from . import debug
from . import event_manager
from . import learn_mode_presenter
from . import logger
from . import messages
from . import mouse_review
from . import orca_state
from . import orca_platform
from . import script_manager
from . import settings
from . import settings_manager
from . import speech
from . import sound
from .ax_object import AXObject
from .ax_utilities import AXUtilities
from .input_event import BrailleEvent

_eventManager = event_manager.getManager()
_scriptManager = script_manager.getManager()
_settingsManager = settings_manager.getManager()
_logger = logger.getLogger()

def onEnabledChanged(gsetting, key):
    try:
        enabled = gsetting.get_boolean(key)
    except Exception:
        return

    if key == 'screen-reader-enabled' and not enabled:
        shutdown()

def getSettingsManager():
    return _settingsManager

def getLogger():
    return _logger

EXIT_CODE_HANG = 50

# The user-settings module (see loadUserSettings).
#
_userSettings = None

# A subset of the original Xmodmap info prior to our stomping on it.
# Right now, this is just for the user's chosen Orca modifier(s).
#
_originalXmodmap = ""
_orcaModifiers = settings.DESKTOP_MODIFIER_KEYS + settings.LAPTOP_MODIFIER_KEYS
_capsLockCleared = False
_restoreOrcaKeys = False

########################################################################
#                                                                      #
# METHODS TO HANDLE APPLICATION LIST AND FOCUSED OBJECTS               #
#                                                                      #
########################################################################

CARET_TRACKING = "caret-tracking"
FOCUS_TRACKING = "focus-tracking"
FLAT_REVIEW = "flat-review"
MOUSE_REVIEW = "mouse-review"
OBJECT_NAVIGATOR = "object-navigator"
SAY_ALL = "say-all"

def getActiveModeAndObjectOfInterest():
    tokens = ["ORCA: Active mode:", orca_state.activeMode,
              "Object of interest:", orca_state.objOfInterest]
    debug.printTokens(debug.LEVEL_INFO, tokens, True)
    return orca_state.activeMode, orca_state.objOfInterest

def emitRegionChanged(obj, startOffset=None, endOffset=None, mode=None):
    """Notifies interested clients that the current region of interest has changed."""

    if startOffset is None:
        startOffset = 0
    if endOffset is None:
        endOffset = startOffset
    if mode is None:
        mode = FOCUS_TRACKING

    try:
        obj.emit("mode-changed::" + mode, 1, "")
    except Exception:
        msg = "ORCA: Exception emitting mode-changed notification"
        debug.printMessage(debug.LEVEL_INFO, msg, True)

    if mode != orca_state.activeMode:
        tokens = ["ORCA: Switching active mode from", orca_state.activeMode, "to", mode]
        debug.printTokens(debug.LEVEL_INFO, tokens, True)
        orca_state.activeMode = mode

    try:
        tokens = ["ORCA: Region of interest:", obj, "(", startOffset, ")", endOffset]
        debug.printTokens(debug.LEVEL_INFO, tokens, True)
        obj.emit("region-changed", startOffset, endOffset)
    except Exception:
        msg = "ORCA: Exception emitting region-changed notification"
        debug.printMessage(debug.LEVEL_INFO, msg, True)

    orca_state.objOfInterest = obj

def setActiveWindow(frame, app=None, alsoSetLocusOfFocus=False, notifyScript=False):
    tokens = ["ORCA: Request to set active window to", frame]
    if app is not None:
        tokens.extend(["in", app])
    debug.printTokens(debug.LEVEL_INFO, tokens, True)

    if frame == orca_state.activeWindow:
        msg = "ORCA: Setting activeWindow to existing activeWindow"
        debug.printMessage(debug.LEVEL_INFO, msg, True)
    elif frame is None:
        orca_state.activeWindow = None
    else:
        real_app, real_frame = AXObject.find_real_app_and_window_for(frame, app)
        if real_frame != frame:
            tokens = ["ORCA: Correcting active window to", real_frame, "in", real_app]
            debug.printTokens(debug.LEVEL_INFO, tokens, True)
            orca_state.activeWindow = real_frame
        else:
            orca_state.activeWindow = frame

    if alsoSetLocusOfFocus:
        setLocusOfFocus(None, orca_state.activeWindow, notifyScript=notifyScript)

def setLocusOfFocus(event, obj, notifyScript=True, force=False):
    """Sets the locus of focus (i.e., the object with visual focus) and
    notifies the script of the change should the script wish to present
    the change to the user.

    Arguments:
    - event: if not None, the Event that caused this to happen
    - obj: the Accessible with the new locus of focus.
    - notifyScript: if True, propagate this event
    - force: if True, don't worry if this is the same object as the
      current locusOfFocus
    """

    if not force and obj == orca_state.locusOfFocus:
        msg = "ORCA: Setting locusOfFocus to existing locusOfFocus"
        debug.printMessage(debug.LEVEL_INFO, msg, True)
        return

    if event and (orca_state.activeScript and not orca_state.activeScript.app):
        app = AXObject.get_application(event.source)
        script = _scriptManager.getScript(app, event.source)
        _scriptManager.setActiveScript(script, "Setting locusOfFocus")

    oldFocus = orca_state.locusOfFocus
    if AXObject.is_dead(oldFocus):
        oldFocus = None

    if obj is None:
        msg = "ORCA: New locusOfFocus is null (being cleared)"
        debug.printMessage(debug.LEVEL_INFO, msg, True)
        orca_state.locusOfFocus = None
        return

    if orca_state.activeScript:
        tokens = ["ORCA: Active script is:", orca_state.activeScript]
        debug.printTokens(debug.LEVEL_INFO, tokens, True)
        if orca_state.activeScript.utilities.isZombie(obj):
            tokens = ["ERROR: New locusOfFocus (", obj, ") is zombie. Not updating."]
            debug.printTokens(debug.LEVEL_INFO, tokens, True)
            return
        if AXObject.is_dead(obj):
            tokens = ["ERROR: New locusOfFocus (", obj, ") is dead. Not updating."]
            debug.printTokens(debug.LEVEL_INFO, tokens, True)
            return

    tokens = ["ORCA: Changing locusOfFocus from", oldFocus, "to", obj, ". Notify:", notifyScript]
    debug.printTokens(debug.LEVEL_INFO, tokens, True)
    orca_state.locusOfFocus = obj

    if not notifyScript:
        return

    if not orca_state.activeScript:
        msg = "ORCA: Cannot notify active script because there isn't one"
        debug.printMessage(debug.LEVEL_INFO, msg, True)
        return

    orca_state.activeScript.locusOfFocusChanged(event, oldFocus, orca_state.locusOfFocus)

########################################################################
#                                                                      #
# METHODS FOR PRE-PROCESSING AND MASSAGING BRAILLE EVENTS.             #
#                                                                      #
########################################################################

def _processBrailleEvent(event):
    """Called whenever a  key is pressed on the Braille display.

    Arguments:
    - command: the BrlAPI event for the key that was pressed.

    Returns True if the event was consumed; otherwise False
    """

    consumed = False

    # Braille key presses always interrupt speech.
    #
    event = BrailleEvent(event)
    if event.event['command'] not in braille.dontInteruptSpeechKeys:
        speech.stop()
    orca_state.lastInputEvent = event

    try:
        consumed = _eventManager.processBrailleEvent(event)
    except Exception:
        debug.printException(debug.LEVEL_SEVERE)

    # TODO - JD: Is this still possible?
    if not consumed and learn_mode_presenter.getPresenter().is_active():
        consumed = True

    return consumed

########################################################################
#                                                                      #
# METHODS FOR HANDLING INITIALIZATION, SHUTDOWN, AND USE.              #
#                                                                      #
########################################################################

def deviceChangeHandler(deviceManager, device):
    """New keyboards being plugged in stomp on our changes to the keymappings,
       so we have to re-apply"""
    source = device.get_source()
    if source == Gdk.InputSource.KEYBOARD:
        msg = "ORCA: Keyboard change detected, re-creating the xmodmap"
        debug.printMessage(debug.LEVEL_INFO, msg, True)
        _createOrcaXmodmap()

def updateKeyMap(keyboardEvent):
    """Unsupported convenience method to call sad hacks which should go away."""

    global _restoreOrcaKeys
    if keyboardEvent.isPressedKey():
        return

    if keyboardEvent.event_string in settings.orcaModifierKeys \
       and orca_state.bypassNextCommand:
        _restoreXmodmap()
        _restoreOrcaKeys = True
        return

    if _restoreOrcaKeys and not orca_state.bypassNextCommand:
        _createOrcaXmodmap()
        _restoreOrcaKeys = False

def _setXmodmap(xkbmap):
    """Set the keyboard map using xkbcomp."""
    p = subprocess.Popen(['xkbcomp', '-w0', '-', os.environ['DISPLAY']],
        stdin=subprocess.PIPE, stdout=None, stderr=None)
    p.communicate(xkbmap)

def _setCapsLockAsOrcaModifier(enable):
    """Enable or disable use of the caps lock key as an Orca modifier key."""
    interpretCapsLineProg = re.compile(
        r'^\s*interpret\s+Caps[_+]Lock[_+]AnyOfOrNone\s*\(all\)\s*{\s*$', re.I)
    normalCapsLineProg = re.compile(
        r'^\s*action\s*=\s*LockMods\s*\(\s*modifiers\s*=\s*Lock\s*\)\s*;\s*$', re.I)
    interpretShiftLineProg = re.compile(
        r'^\s*interpret\s+Shift[_+]Lock[_+]AnyOf\s*\(\s*Shift\s*\+\s*Lock\s*\)\s*{\s*$', re.I)
    normalShiftLineProg = re.compile(
        r'^\s*action\s*=\s*LockMods\s*\(\s*modifiers\s*=\s*Shift\s*\)\s*;\s*$', re.I)
    disabledModLineProg = re.compile(
        r'^\s*action\s*=\s*NoAction\s*\(\s*\)\s*;\s*$', re.I)
    normalCapsLine = '        action= LockMods(modifiers=Lock);'
    normalShiftLine = '        action= LockMods(modifiers=Shift);'
    disabledModLine = '        action= NoAction();'
    lines = _originalXmodmap.decode('UTF-8').split('\n')
    foundCapsInterpretSection = False
    foundShiftInterpretSection = False
    modified = False
    for i, line in enumerate(lines):
        if not foundCapsInterpretSection and not foundShiftInterpretSection:
            if interpretCapsLineProg.match(line):
                foundCapsInterpretSection = True
            elif interpretShiftLineProg.match(line):
                foundShiftInterpretSection = True
        elif foundCapsInterpretSection:
            if enable:
                if normalCapsLineProg.match(line):
                    lines[i] = disabledModLine
                    modified = True
            else:
                if disabledModLineProg.match(line):
                    lines[i] = normalCapsLine
                    modified = True
            if line.find('}'):
                foundCapsInterpretSection = False
        else: # foundShiftInterpretSection
            if enable:
                if normalShiftLineProg.match(line):
                    lines[i] = disabledModLine
                    modified = True
            else:
                if disabledModLineProg.match(line):
                    lines[i] = normalShiftLine
                    modified = True
            if line.find('}'):
                foundShiftInterpretSection = False
    if modified:
        _setXmodmap(bytes('\n'.join(lines), 'UTF-8'))

def _createOrcaXmodmap():
    """Makes an Orca-specific Xmodmap so that the keys behave as we
    need them to do. This is especially the case for the Orca modifier.
    """

    global _capsLockCleared

    if "Caps_Lock" in settings.orcaModifierKeys \
       or "Shift_Lock" in settings.orcaModifierKeys:
        _setCapsLockAsOrcaModifier(True)
        _capsLockCleared = True
    elif _capsLockCleared:
        _setCapsLockAsOrcaModifier(False)
        _capsLockCleared = False

def _storeXmodmap(keyList):
    """Save the original xmodmap for the keys in keyList before we alter it.

    Arguments:
    - keyList: A list of named keys to look for.
    """

    global _originalXmodmap
    _originalXmodmap = subprocess.check_output(['xkbcomp', os.environ['DISPLAY'], '-'])

def _restoreXmodmap(keyList=[]):
    """Restore the original xmodmap values for the keys in keyList.

    Arguments:
    - keyList: A list of named keys to look for. An empty list means
      to restore the entire saved xmodmap.
    """

    msg = "ORCA: Attempting to restore original xmodmap"
    debug.printMessage(debug.LEVEL_INFO, msg, True)

    global _capsLockCleared
    _capsLockCleared = False
    p = subprocess.Popen(['xkbcomp', '-w0', '-', os.environ['DISPLAY']],
        stdin=subprocess.PIPE, stdout=None, stderr=None)
    p.communicate(_originalXmodmap)

    msg = "ORCA: Original xmodmap restored"
    debug.printMessage(debug.LEVEL_INFO, msg, True)

def loadUserSettings(script=None, inputEvent=None, skipReloadMessage=False):
    """Loads (and reloads) the user settings module, reinitializing
    things such as speech if necessary.

    Returns True to indicate the input event has been consumed.
    """

    debug.printMessage(debug.LEVEL_INFO, 'ORCA: Loading User Settings', True)

    global _userSettings

    # Shutdown the output drivers and give them a chance to die.

    player = sound.getPlayer()
    player.shutdown()
    speech.shutdown()
    braille.shutdown()

    _scriptManager.deactivate()

    reloaded = False
    if _userSettings:
        _profile = _settingsManager.getSetting('activeProfile')[1]
        try:
            _userSettings = _settingsManager.getGeneralSettings(_profile)
            _settingsManager.setProfile(_profile)
            reloaded = True
        except ImportError:
            debug.printException(debug.LEVEL_INFO)
        except Exception:
            debug.printException(debug.LEVEL_SEVERE)
    else:
        _profile = _settingsManager.profile
        try:
            _userSettings = _settingsManager.getGeneralSettings(_profile)
        except ImportError:
            debug.printException(debug.LEVEL_INFO)
        except Exception:
            debug.printException(debug.LEVEL_SEVERE)

    if not script:
        script = _scriptManager.getDefaultScript()

    _settingsManager.loadAppSettings(script)

    if _settingsManager.getSetting('enableSpeech'):
        msg = 'ORCA: About to enable speech'
        debug.printMessage(debug.LEVEL_INFO, msg, True)
        try:
            speech.init()
            if reloaded and not skipReloadMessage:
                script.speakMessage(messages.SETTINGS_RELOADED)
        except Exception:
            debug.printException(debug.LEVEL_SEVERE)
    else:
        msg = 'ORCA: Speech is not enabled in settings'
        debug.printMessage(debug.LEVEL_INFO, msg, True)

    if _settingsManager.getSetting('enableBraille'):
        msg = 'ORCA: About to enable braille'
        debug.printMessage(debug.LEVEL_INFO, msg, True)
        try:
            braille.init(_processBrailleEvent)
        except Exception:
            debug.printException(debug.LEVEL_WARNING)
            msg = 'ORCA: Could not initialize connection to braille.'
            debug.printMessage(debug.LEVEL_WARNING, msg, True)
    else:
        msg = 'ORCA: Braille is not enabled in settings'
        debug.printMessage(debug.LEVEL_INFO, msg, True)


    if _settingsManager.getSetting('enableMouseReview'):
        mouse_review.getReviewer().activate()
    else:
        mouse_review.getReviewer().deactivate()

    if _settingsManager.getSetting('enableSound'):
        player.init()

    global _orcaModifiers
    custom = [k for k in settings.orcaModifierKeys if k not in _orcaModifiers]
    _orcaModifiers += custom
    # Handle the case where a change was made in the Orca Preferences dialog.
    #
    if _originalXmodmap:
        _restoreXmodmap(_orcaModifiers)

    _storeXmodmap(_orcaModifiers)
    _createOrcaXmodmap()

    _eventManager.activate()
    _scriptManager.activate()

    debug.printMessage(debug.LEVEL_INFO, 'ORCA: User Settings Loaded', True)

    return True

def _showPreferencesUI(script, prefs):
    if orca_state.orcaOS:
        orca_state.orcaOS.showGUI()
        return

    try:
        module = importlib.import_module('.orca_gui_prefs', 'orca')
    except Exception:
        debug.printException(debug.LEVEL_SEVERE)
        return

    uiFile = os.path.join(orca_platform.datadir,
                          orca_platform.package,
                          "ui",
                          "orca-setup.ui")

    orca_state.orcaOS = module.OrcaSetupGUI(uiFile, "orcaSetupWindow", prefs)
    orca_state.orcaOS.init(script)
    orca_state.orcaOS.showGUI()

def showAppPreferencesGUI(script=None, inputEvent=None):
    """Displays the user interface to configure the settings for a
    specific applications within Orca and set up those app-specific
    user preferences using a GUI.

    Returns True to indicate the input event has been consumed.
    """

    prefs = {}
    for key in settings.userCustomizableSettings:
        prefs[key] = _settingsManager.getSetting(key)

    script = script or orca_state.activeScript
    _showPreferencesUI(script, prefs)

    return True

def showPreferencesGUI(script=None, inputEvent=None):
    """Displays the user interface to configure Orca and set up
    user preferences using a GUI.

    Returns True to indicate the input event has been consumed.
    """

    prefs = _settingsManager.getGeneralSettings(_settingsManager.profile)
    script = _scriptManager.getDefaultScript()
    _showPreferencesUI(script, prefs)

    return True

def addKeyGrab(binding):
    """ Add a key grab for the given key binding."""

    if orca_state.device is None:
        return []

    ret = []
    for kd in binding.keyDefs():
        ret.append(orca_state.device.add_key_grab(kd, None))
    return ret

def removeKeyGrab(id):
    """ Remove the key grab for the given key binding."""

    if orca_state.device is None:
        return

    orca_state.device.remove_key_grab(id)

def quitOrca(script=None, inputEvent=None):
    """Quit Orca. Check if the user wants to confirm this action.
    If so, show the confirmation GUI otherwise just shutdown.

    Returns True to indicate the input event has been consumed.
    """

    shutdown()

    return True

def showFindGUI(script=None, inputEvent=None):
    """Displays the user interface to perform an Orca Find.

    Returns True to indicate the input event has been consumed.
    """

    try:
        module = importlib.import_module('.orca_gui_find', 'orca')
        module.showFindUI()
    except Exception:
        debug.printException(debug.LEVEL_SEVERE)

# If True, this module has been initialized.
#
_initialized = False

def init():
    """Initialize the orca module, which initializes the speech and braille
    modules.  Also builds up the application list, registers for AT-SPI events,
    and creates scripts for all known applications.

    Returns True if the initialization procedure has run, or False if this
    module has already been initialized.
    """

    debug.printMessage(debug.LEVEL_INFO, 'ORCA: Initializing', True)

    global _initialized

    if _initialized and _settingsManager.isScreenReaderServiceEnabled():
        debug.printMessage(debug.LEVEL_INFO, 'ORCA: Already initialized', True)
        return False

    # Do not hang on initialization if we can help it.
    #
    if settings.timeoutCallback and (settings.timeoutTime > 0):
        signal.signal(signal.SIGALRM, settings.timeoutCallback)
        signal.alarm(settings.timeoutTime)

    loadUserSettings()

    if settings.timeoutCallback and (settings.timeoutTime > 0):
        signal.alarm(0)

    _initialized = True
    # In theory, we can do this through dbus. In practice, it fails to
    # work sometimes. Until we know why, we need to leave this as-is
    # so that we respond when gnome-control-center is used to stop Orca.
    if a11yAppSettings:
        a11yAppSettings.connect('changed', onEnabledChanged)

    debug.printMessage(debug.LEVEL_INFO, 'ORCA: Initialized', True)

    return True

def start():
    """Starts Orca."""

    debug.printMessage(debug.LEVEL_INFO, 'ORCA: Starting', True)

    if not _initialized:
        init()

    # Do not hang on startup if we can help it.
    #
    if settings.timeoutCallback and (settings.timeoutTime > 0):
        signal.signal(signal.SIGALRM, settings.timeoutCallback)
        signal.alarm(settings.timeoutTime)

    if settings.timeoutCallback and (settings.timeoutTime > 0):
        signal.alarm(0)

    # Event handlers for input devices being plugged in/unplugged.
    # Used to re-create the Xmodmap when a new keyboard is plugged in.
    # Necessary, because plugging in a new keyboard resets the Xmodmap
    # and stomps our changes
    display = Gdk.Display.get_default()
    devmanager=display.get_device_manager()
    devmanager.connect("device-added", deviceChangeHandler)
    devmanager.connect("device-removed", deviceChangeHandler)

    Gdk.notify_startup_complete()
    msg = 'ORCA: Startup complete notification made'
    debug.printMessage(debug.LEVEL_INFO, msg, True)

    debug.printMessage(debug.LEVEL_INFO, 'ORCA: Starting Atspi main event loop', True)
    Atspi.event_main()

def die(exitCode=1):
    pid = os.getpid()
    if exitCode == EXIT_CODE_HANG:
        # Someting is hung and we wish to abort.
        os.kill(pid, signal.SIGKILL)
        return

    shutdown()
    sys.exit(exitCode)
    if exitCode > 1:
        os.kill(pid, signal.SIGTERM)

def timeout(signum=None, frame=None):
    msg = 'TIMEOUT: something has hung. Aborting.'
    debug.printMessage(debug.LEVEL_SEVERE, msg, True)
    debug.printStack(debug.LEVEL_SEVERE)
    debug.examineProcesses(force=True)
    die(EXIT_CODE_HANG)

def shutdown(script=None, inputEvent=None):
    """Exits Orca.  Unregisters any event listeners and cleans up.

    Returns True if the shutdown procedure ran or False if this module
    was never initialized.
    """

    debug.printMessage(debug.LEVEL_INFO, 'ORCA: Shutting down', True)

    global _initialized

    if not _initialized:
        return False

    # Try to say goodbye, but be defensive if something has hung.
    #
    if settings.timeoutCallback and (settings.timeoutTime > 0):
        signal.signal(signal.SIGALRM, settings.timeoutCallback)
        signal.alarm(settings.timeoutTime)

    orca_state.activeScript.presentationInterrupt()
    orca_state.activeScript.presentMessage(messages.STOP_ORCA, resetStyles=False)

    # Deactivate the event manager first so that it clears its queue and will not
    # accept new events. Then let the script manager unregister script event listeners.
    _eventManager.deactivate()
    _scriptManager.deactivate()

    # Shutdown all the other support.
    #
    if settings.enableSpeech:
        speech.shutdown()
    if settings.enableBraille:
        braille.shutdown()
    if settings.enableSound:
        player = sound.getPlayer()
        player.shutdown()

    if settings.timeoutCallback and (settings.timeoutTime > 0):
        signal.alarm(0)

    _initialized = False
    _restoreXmodmap(_orcaModifiers)

    debug.printMessage(debug.LEVEL_INFO, 'ORCA: Quitting Atspi main event loop', True)
    Atspi.event_quit()
    debug.printMessage(debug.LEVEL_INFO, 'ORCA: Shutdown complete', True)

    return True

exitCount = 0
def shutdownOnSignal(signum, frame):
    global exitCount

    signalString = f'({signal.strsignal(signum)})'
    msg = f"ORCA: Shutting down and exiting due to signal={signum} {signalString}"
    debug.printMessage(debug.LEVEL_INFO, msg, True)

    # Well...we'll try to exit nicely, but if we keep getting called,
    # something bad is happening, so just quit.
    #
    if exitCount:
        die(signum)
    else:
        exitCount += 1

    # Try to do a graceful shutdown if we can.
    #
    if settings.timeoutCallback and (settings.timeoutTime > 0):
        signal.signal(signal.SIGALRM, settings.timeoutCallback)
        signal.alarm(settings.timeoutTime)

    try:
        if _initialized:
            shutdown()
        else:
            # We always want to try to shutdown speech since the
            # speech servers are very persistent about living.
            #
            speech.shutdown()
            shutdown()
        cleanExit = True
    except Exception:
        cleanExit = False

    if settings.timeoutCallback and (settings.timeoutTime > 0):
        signal.alarm(0)

    if not cleanExit:
        die(EXIT_CODE_HANG)

def crashOnSignal(signum, frame):
    signalString = f'({signal.strsignal(signum)})'
    msg = f"ORCA: Shutting down and exiting due to signal={signum} {signalString}"
    debug.printMessage(debug.LEVEL_SEVERE, msg, True)
    debug.printStack(debug.LEVEL_SEVERE)
    _restoreXmodmap(_orcaModifiers)
    try:
        orca_state.activeScript.presentationInterrupt()
        orca_state.activeScript.presentMessage(messages.STOP_ORCA, resetStyles=False)
    except Exception:
        pass
    sys.exit(1)

def main():
    """The main entry point for Orca.  The exit codes for Orca will
    loosely be based on signals, where the exit code will be the
    signal used to terminate Orca (if a signal was used).  Otherwise,
    an exit code of 0 means normal completion and an exit code of 50
    means Orca exited because of a hang."""

    msg = f"ORCA: Launching version {orca_platform.version}"
    if orca_platform.revision:
        msg += f" (rev {orca_platform.revision})"

    sessionType = os.environ.get('XDG_SESSION_TYPE') or ""
    sessionDesktop = os.environ.get('XDG_SESSION_DESKTOP') or ""
    session = "%s %s".strip() % (sessionType, sessionDesktop)
    if session:
        msg += f" session: {session}"
    debug.printMessage(debug.LEVEL_INFO, msg, True)

    if debug.debugFile and os.path.exists(debug.debugFile.name):
        faulthandler.enable(file=debug.debugFile, all_threads=True)
    else:
        faulthandler.enable(all_threads=False)

    # Method to call when we think something might be hung.
    #
    settings.timeoutCallback = timeout

    # Various signal handlers we want to listen for.
    #
    signal.signal(signal.SIGHUP, shutdownOnSignal)
    signal.signal(signal.SIGINT, shutdownOnSignal)
    signal.signal(signal.SIGTERM, shutdownOnSignal)
    signal.signal(signal.SIGQUIT, shutdownOnSignal)
    signal.signal(signal.SIGSEGV, crashOnSignal)

    debug.printMessage(debug.LEVEL_INFO, "ORCA: Enabling accessibility (if needed).", True)
    if not _settingsManager.isAccessibilityEnabled():
        _settingsManager.setAccessibility(True)

    debug.printMessage(debug.LEVEL_INFO, "ORCA: Initializing.", True)
    init()
    debug.printMessage(debug.LEVEL_INFO, "ORCA: Initialized.", True)

    try:
        message = messages.START_ORCA
        script = _scriptManager.getDefaultScript()
        script.presentMessage(message)
    except Exception:
        debug.printException(debug.LEVEL_SEVERE)

    script = orca_state.activeScript
    if script:
        window = script.utilities.activeWindow()

        if window and not orca_state.locusOfFocus:
            app = AXObject.get_application(window)
            setActiveWindow(window, app, alsoSetLocusOfFocus=True, notifyScript=True)

            # setActiveWindow does some corrective work needed thanks to
            # mutter-x11-frames. So retrieve the window just in case.
            window = orca_state.activeWindow
            script = _scriptManager.getScript(app, window)
            _scriptManager.setActiveScript(script, "Launching.")

            focusedObject = AXUtilities.get_focused_object(window)
            tokens = ["ORCA: Focused object is:", focusedObject]
            debug.printTokens(debug.LEVEL_INFO, tokens, True)
            if focusedObject:
                setLocusOfFocus(None, focusedObject)
                script = _scriptManager.getScript(
                    AXObject.get_application(focusedObject), focusedObject)
                _scriptManager.setActiveScript(script, "Found focused object.")

    try:
        msg = "ORCA: Starting ATSPI registry."
        debug.printMessage(debug.LEVEL_INFO, msg, True)
        start() # waits until we stop the registry
    except Exception:
        msg = "ORCA: Exception starting ATSPI registry."
        debug.printMessage(debug.LEVEL_SEVERE, msg, True)
        die(EXIT_CODE_HANG)
    return 0

if __name__ == "__main__":
    sys.exit(main())
