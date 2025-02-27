# Orca
#
# Copyright 2016 Igalia, S.L.
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

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2016 Igalia, S.L."
__license__   = "LGPL"

import re

from orca import debug
from orca import focus_manager
from orca import keybindings
from orca import script_utilities
from orca import settings_manager
from orca.ax_text import AXText
from orca.ax_utilities import AXUtilities


class Utilities(script_utilities.Utilities):

    def __init__(self, script):
        super().__init__(script)

    def clearCache(self):
        pass

    def deletedText(self, event):
        match = re.search("\n~", event.any_data)
        if not match:
            return event.any_data

        adjusted = event.any_data[:match.start()]
        tokens = ["TERMINAL: Adjusted deletion: '", adjusted, "'"]
        debug.printTokens(debug.LEVEL_INFO, tokens, True)
        return adjusted

    def insertedText(self, event):
        if len(event.any_data) == 1:
            return event.any_data

        if self.isAutoTextEvent(event):
            return event.any_data

        if self.isClipboardTextChangedEvent(event):
            return event.any_data

        start, end = event.detail1, event.detail1 + len(event.any_data)
        firstLine = AXText.get_line_at_offset(event.source, start)
        tokens = ["TERMINAL: First line of insertion:", firstLine]
        debug.printTokens(debug.LEVEL_INFO, tokens, True)

        lastLine = AXText.get_line_at_offset(event.source, end - 1)
        tokens = ["TERMINAL: Last line of insertion:", lastLine]
        debug.printTokens(debug.LEVEL_INFO, tokens, True)

        if firstLine == lastLine:
            msg = "TERMINAL: Not adjusting single-line insertion."
            debug.printMessage(debug.LEVEL_INFO, msg, True)
            return event.any_data

        currentLine = AXText.get_line_at_offset(event.source, None)
        tokens = ["TERMINAL: Current line:", currentLine]
        debug.printTokens(debug.LEVEL_INFO, tokens, True)

        if firstLine != ("", 0, 0):
            start = firstLine[1]

        if currentLine not in (("", 0, 0), firstLine, lastLine):
            lastLine = currentLine

        if lastLine != ("", 0, 0):
            end = lastLine[2]
            if lastLine[0].endswith("\n"):
                end -= 1

        adjusted = AXText.get_substring(event.source, start, end)
        if adjusted:
            tokens = ["TERMINAL: Adjusted insertion: '", adjusted, "'"]
            debug.printTokens(debug.LEVEL_INFO, tokens, True)
        else:
            msg = "TERMINAL: Adjustment failed. Returning any_data."
            debug.printMessage(debug.LEVEL_INFO, msg, True)
            adjusted = event.any_data

        return adjusted

    def insertionEndsAtCaret(self, event):
        return AXText.get_caret_offset(event.source) == event.detail1 + event.detail2

    def isEditableTextArea(self, obj):
        if AXUtilities.is_terminal(obj):
            return True

        return super().isEditableTextArea(obj)

    def isTextArea(self, obj):
        if AXUtilities.is_terminal(obj):
            return True

        return super().isTextArea(obj)

    def isAutoTextEvent(self, event):
        if not event.type.startswith("object:text-changed:insert"):
            return False

        if not event.any_data or not event.source:
            return False

        if len(event.any_data) <= 1:
            return False

        lastKey, mods = self.lastKeyAndModifiers()
        if lastKey == "Tab":
            return event.any_data != "\t"
        if lastKey == "Return" and event.any_data.startswith("\n"):
            return event.any_data.strip() and not event.any_data.count("\n~")

        return False

    def lastInputEventWasCopy(self):
        keycode, mods = self._lastKeyCodeAndModifiers()
        keynames = self._allNamesForKeyCode(keycode)
        if 'c' not in keynames:
            return False

        if mods & keybindings.CTRL_MODIFIER_MASK:
            return mods & keybindings.SHIFT_MODIFIER_MASK

        return False

    def lastInputEventWasPaste(self):
        keycode, mods = self._lastKeyCodeAndModifiers()
        keynames = self._allNamesForKeyCode(keycode)
        if 'v' not in keynames:
            return False

        if mods & keybindings.CTRL_MODIFIER_MASK:
            return mods & keybindings.SHIFT_MODIFIER_MASK

        return False

    def treatEventAsCommand(self, event):
        if event.source != focus_manager.getManager().get_locus_of_focus():
            return False

        if event.type.startswith("object:text-changed:insert") and event.any_data.strip():
            # To let default script handle presentation.
            if self.lastInputEventWasPaste():
                return False

            if event.any_data.count("\n~"):
                return False

            keyString, mods = self.lastKeyAndModifiers()
            if keyString in ["Return", "Tab", "space", " "]:
                return re.search(r"[^\d\s]", event.any_data)
            if mods & keybindings.ALT_MODIFIER_MASK:
                return True
            if self.lastInputEventWasPrintableKey():
                return len(event.any_data) > 1
            if AXText.get_caret_offset(event.source) == event.detail1 + event.detail2:
                return True

        return False

    def treatEventAsNoise(self, event):
        if self.lastInputEventWasCommand():
            return False

        if event.type.startswith("object:text-changed:delete") and event.any_data.strip():
            keyString, mods = self.lastKeyAndModifiers()
            if keyString in ["Return", "Tab", "space", " "]:
                return True
            if mods & keybindings.ALT_MODIFIER_MASK:
                return True
            if len(event.any_data) > 1 and self.lastInputEventWasPrintableKey():
                return True

        return False

    def willEchoCharacter(self, event):
        if not settings_manager.getManager().getSetting("enableEchoByCharacter"):
            return False

        if len(event.event_string) != 1 \
           or event.modifiers & keybindings.ORCA_CTRL_MODIFIER_MASK:
            return False

        return True
