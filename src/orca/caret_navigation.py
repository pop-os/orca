# Orca
#
# Copyright 2013-2015 Igalia, S.L.
# Author: Joanmarie Diggs <jdiggs@igalia.com>
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

"""Provides an Orca-controlled caret for text content."""

__id__ = "$Id$"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2013-2015 Igalia, S.L."
__license__ = "LGPL"

from . import cmdnames
from . import debug
from . import input_event
from . import keybindings
from . import messages
from . import settings_manager


class CaretNavigation:
    """Implements the caret navigation support available to scripts."""

    def __init__(self, script):
        if not (script and script.app):
            msg = "CARET NAVIGATION: Caret navigation requires a script and app."
            debug.printMessage(debug.LEVEL_INFO, msg)

        self._script = script

        # To make it possible for focus mode to suspend this navigation without
        # changing the user's preferred setting.
        self._suspended = False

        self._handlers = self.get_handlers(True)
        self._bindings = self.get_bindings(True)

    def handles_navigation(self, handler):
        """Returns True if handler is a navigation command."""

        if handler not in self._handlers.values():
            return False

        if handler.function == self.toggle_enabled:
            return False

        return True

    def get_bindings(self, refresh=False, is_desktop=True):
        """Returns the caret-navigation keybindings."""

        if refresh:
            msg = "CARET NAVIGATION: Refreshing bindings."
            debug.printMessage(debug.LEVEL_INFO, msg, True)
            self._setup_bindings()

        return self._bindings

    def get_handlers(self, refresh=False):
        """Returns the caret-navigation handlers."""

        if refresh:
            msg = "CARET NAVIGATION: Refreshing handlers."
            debug.printMessage(debug.LEVEL_INFO, msg, True)
            self._setup_handlers()

        return self._handlers

    def _setup_handlers(self):
        """Sets up the caret-navigation input event handlers."""

        self._handlers = {}
        if not (self._script and self._script.app):
            return

        self._handlers["toggle_enabled"] = \
            input_event.InputEventHandler(
                self.toggle_enabled,
                cmdnames.CARET_NAVIGATION_TOGGLE,
                enabled = not self._suspended)

        enabled = settings_manager.getManager().getSetting('caretNavigationEnabled') \
            and not self._suspended

        self._handlers["next_character"] = \
            input_event.InputEventHandler(
                self._next_character,
                cmdnames.CARET_NAVIGATION_NEXT_CHAR,
                enabled = enabled)

        self._handlers["previous_character"] = \
            input_event.InputEventHandler(
                self._previous_character,
                cmdnames.CARET_NAVIGATION_PREV_CHAR,
                enabled = enabled)

        self._handlers["next_word"] = \
            input_event.InputEventHandler(
                self._next_word,
                cmdnames.CARET_NAVIGATION_NEXT_WORD,
                enabled = enabled)

        self._handlers["previous_word"] = \
            input_event.InputEventHandler(
                self._previous_word,
                cmdnames.CARET_NAVIGATION_PREV_WORD,
                enabled = enabled)

        self._handlers["next_line"] = \
            input_event.InputEventHandler(
                self._next_line,
                cmdnames.CARET_NAVIGATION_NEXT_LINE,
                enabled = enabled)

        self._handlers["previous_line"] = \
            input_event.InputEventHandler(
                self._previous_line,
                cmdnames.CARET_NAVIGATION_PREV_LINE,
                enabled = enabled)

        self._handlers["start_of_file"] = \
            input_event.InputEventHandler(
                self._start_of_file,
                cmdnames.CARET_NAVIGATION_FILE_START,
                enabled = enabled)

        self._handlers["end_of_file"] = \
            input_event.InputEventHandler(
                self._end_of_file,
                cmdnames.CARET_NAVIGATION_FILE_END,
                enabled = enabled)

        self._handlers["start_of_line"] = \
            input_event.InputEventHandler(
                self._start_of_line,
                cmdnames.CARET_NAVIGATION_LINE_START,
                enabled = enabled)

        self._handlers["end_of_line"] = \
            input_event.InputEventHandler(
                self._end_of_line,
                cmdnames.CARET_NAVIGATION_LINE_END,
                enabled = enabled)

        msg = "CARET NAVIGATION: Handlers set up."
        debug.printMessage(debug.LEVEL_INFO, msg, True)

    def _setup_bindings(self):
        """Sets up the caret-navigation key bindings."""

        self._bindings = keybindings.KeyBindings()
        if not (self._script and self._script.app):
            return

        self._bindings.add(
            keybindings.KeyBinding(
                "F12",
                keybindings.defaultModifierMask,
                keybindings.ORCA_MODIFIER_MASK,
                self._handlers.get("toggle_enabled"),
                1,
                not self._suspended))

        enabled = settings_manager.getManager().getSetting('caretNavigationEnabled') \
            and not self._suspended

        self._bindings.add(
            keybindings.KeyBinding(
                "Right",
                keybindings.defaultModifierMask,
                keybindings.NO_MODIFIER_MASK,
                self._handlers.get("next_character"),
                1,
                enabled))

        self._bindings.add(
            keybindings.KeyBinding(
                "Left",
                keybindings.defaultModifierMask,
                keybindings.NO_MODIFIER_MASK,
                self._handlers.get("previous_character"),
                1,
                enabled))

        self._bindings.add(
            keybindings.KeyBinding(
                "Right",
                keybindings.defaultModifierMask,
                keybindings.CTRL_MODIFIER_MASK,
                self._handlers.get("next_word"),
                1,
                enabled))

        self._bindings.add(
            keybindings.KeyBinding(
                "Left",
                keybindings.defaultModifierMask,
                keybindings.CTRL_MODIFIER_MASK,
                self._handlers.get("previous_word"),
                1,
                enabled))

        self._bindings.add(
            keybindings.KeyBinding(
                "Down",
                keybindings.defaultModifierMask,
                keybindings.NO_MODIFIER_MASK,
                self._handlers.get("next_line"),
                1,
                enabled))

        self._bindings.add(
            keybindings.KeyBinding(
                "Up",
                keybindings.defaultModifierMask,
                keybindings.NO_MODIFIER_MASK,
                self._handlers.get("previous_line"),
                1,
                enabled))

        self._bindings.add(
            keybindings.KeyBinding(
                "End",
                keybindings.defaultModifierMask,
                keybindings.NO_MODIFIER_MASK,
                self._handlers.get("end_of_line"),
                1,
                enabled))

        self._bindings.add(
            keybindings.KeyBinding(
                "Home",
                keybindings.defaultModifierMask,
                keybindings.NO_MODIFIER_MASK,
                self._handlers.get("start_of_line"),
                1,
                enabled))

        self._bindings.add(
            keybindings.KeyBinding(
                "End",
                keybindings.defaultModifierMask,
                keybindings.CTRL_MODIFIER_MASK,
                self._handlers.get("end_of_file"),
                1,
                enabled))

        self._bindings.add(
            keybindings.KeyBinding(
                "Home",
                keybindings.defaultModifierMask,
                keybindings.CTRL_MODIFIER_MASK,
                self._handlers.get("start_of_file"),
                1,
                enabled))

        msg = "CARET NAVIGATION: Bindings set up."
        debug.printMessage(debug.LEVEL_INFO, msg, True)

    @staticmethod
    def toggle_enabled(script, event):
        """Toggles caret navigation."""

        if not event:
            return False

        _settings_manager = settings_manager.getManager()
        enabled = not _settings_manager.getSetting('caretNavigationEnabled')
        if enabled:
            string = messages.CARET_CONTROL_ORCA
        else:
            string = messages.CARET_CONTROL_APP

        script.presentMessage(string)
        _settings_manager.setSetting('caretNavigationEnabled', enabled)
        script.refreshKeyGrabs("toggling caret navigation")
        return True

    def suspend_commands(self, suspended):
        """Suspends caret navigation independent of the enabled setting."""

        if suspended == self._suspended:
            return

        msg = f"CARET NAVIGATION: Suspended: {suspended}"
        debug.printMessage(debug.LEVEL_INFO, msg, True)
        self._suspended = suspended

        self._handlers = self.get_handlers(True)
        self._bindings = self.get_bindings(True)

    @staticmethod
    def _next_character(script, event):
        """Moves to the next character."""

        if not event:
            return False

        obj, offset = script.utilities.nextContext()
        if not obj:
            return False

        script.utilities.setCaretPosition(obj, offset)
        script.updateBraille(obj)
        script.sayCharacter(obj)
        return True

    @staticmethod
    def _previous_character(script, event):
        """Moves to the previous character."""

        if not event:
            return False

        obj, offset = script.utilities.previousContext()
        if not obj:
            return False

        script.utilities.setCaretPosition(obj, offset)
        script.updateBraille(obj)
        script.sayCharacter(obj)
        return True

    @staticmethod
    def _next_word(script, event):
        """Moves to the next word."""

        if not event:
            return False

        obj, offset = script.utilities.nextContext(skipSpace=True)
        contents = script.utilities.getWordContentsAtOffset(obj, offset)
        if not contents:
            return False

        obj, end, string = contents[-1][0], contents[-1][2], contents[-1][3]
        if string and string[-1].isspace():
            end -= 1

        script.utilities.setCaretPosition(obj, end)
        script.updateBraille(obj)
        script.sayWord(obj)
        return True

    @staticmethod
    def _previous_word(script, event):
        """Moves to the previous word."""

        if not event:
            return False

        obj, offset = script.utilities.previousContext(skipSpace=True)
        contents = script.utilities.getWordContentsAtOffset(obj, offset)
        if not contents:
            return False

        obj, start = contents[0][0], contents[0][1]
        script.utilities.setCaretPosition(obj, start)
        script.updateBraille(obj)
        script.sayWord(obj)
        return True

    @staticmethod
    def _next_line(script, event):
        """Moves to the next line."""

        if not event:
            return False

        if script.inSayAll():
            _settings_manager = settings_manager.getManager()
            if _settings_manager.getSetting('rewindAndFastForwardInSayAll'):
                msg = "CARET NAVIGATION: inSayAll and rewindAndFastforwardInSayAll is enabled"
                debug.printMessage(debug.LEVEL_INFO, msg)
                return True

        obj, offset = script.utilities.getCaretContext()
        line = script.utilities.getLineContentsAtOffset(obj, offset)
        if not (line and line[0]):
            return False

        contents = script.utilities.getNextLineContents()
        if not contents:
            return False

        obj, start = contents[0][0], contents[0][1]
        script.utilities.setCaretPosition(obj, start)
        script.speakContents(contents, priorObj=line[-1][0])
        script.displayContents(contents)
        return True

    @staticmethod
    def _previous_line(script, event):
        """Moves to the previous line."""

        if not event:
            return False

        if script.inSayAll():
            _settings_manager = settings_manager.getManager()
            if _settings_manager.getSetting('rewindAndFastForwardInSayAll'):
                msg = "CARET NAVIGATION: inSayAll and rewindAndFastforwardInSayAll is enabled"
                debug.printMessage(debug.LEVEL_INFO, msg)
                return True


        contents = script.utilities.getPreviousLineContents()
        if not contents:
            return False

        obj, start = contents[0][0], contents[0][1]
        script.utilities.setCaretPosition(obj, start)
        script.speakContents(contents)
        script.displayContents(contents)
        return True

    @staticmethod
    def _start_of_line(script, event):
        """Moves to the start of the line."""

        if not event:
            return False

        obj, offset = script.utilities.getCaretContext()
        line = script.utilities.getLineContentsAtOffset(obj, offset)
        if not (line and line[0]):
            return False

        obj, start = line[0][0], line[0][1]
        script.utilities.setCaretPosition(obj, start)
        script.sayCharacter(obj)
        script.displayContents(line)
        return True

    @staticmethod
    def _end_of_line(script, event):
        """Moves to the end of the line."""

        if not event:
            return False

        obj, offset = script.utilities.getCaretContext()
        line = script.utilities.getLineContentsAtOffset(obj, offset)
        if not (line and line[0]):
            return False

        obj, end, string = line[-1][0], line[-1][2], line[-1][3]
        if string.strip() and string[-1].isspace():
            end -= 1

        script.utilities.setCaretPosition(obj, end)
        script.sayCharacter(obj)
        script.displayContents(line)
        return True

    @staticmethod
    def _start_of_file(script, event):
        """Moves to the start of the file."""

        if not event:
            return False

        document = script.utilities.documentFrame()
        obj, offset = script.utilities.findFirstCaretContext(document, 0)
        contents = script.utilities.getLineContentsAtOffset(obj, offset)
        if not contents:
            return False

        obj, offset = contents[0][0], contents[0][1]
        script.utilities.setCaretPosition(obj, offset)
        script.speakContents(contents)
        script.displayContents(contents)
        return True

    @staticmethod
    def _end_of_file(script, event):
        """Moves to the end of the file."""

        if not event:
            return False

        document = script.utilities.documentFrame()
        tokens = ["CARET NAVIGATION: Go to end of", document]
        debug.printTokens(debug.LEVEL_INFO, tokens, True)

        obj = script.utilities.getLastObjectInDocument(document)
        tokens = ["CARET NAVIGATION: Last object in", document, "is", obj]
        debug.printTokens(debug.LEVEL_INFO, tokens, True)

        offset = 0
        text = script.utilities.queryNonEmptyText(obj)
        if text:
            offset = text.characterCount - 1

        while obj:
            lastobj, lastoffset = script.utilities.nextContext(obj, offset)
            if not lastobj:
                break
            obj, offset = lastobj, lastoffset

        contents = script.utilities.getLineContentsAtOffset(obj, offset)
        if not contents:
            return False

        obj, offset = contents[-1][0], contents[-1][2]
        script.utilities.setCaretPosition(obj, offset)
        script.speakContents(contents)
        script.displayContents(contents)
        return True
