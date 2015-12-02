#!/usr/bin/python

"""Test of structural navigation amongst 'large objects'."""

from macaroon.playback import *
import utils

sequence = MacroSequence()

#sequence.append(WaitForDocLoad())
sequence.append(PauseAction(5000))
sequence.append(KeyComboAction("<Control>Home"))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("o"))
sequence.append(utils.AssertPresentationAction(
    "1. o to first large chunk", 
    ["BRAILLE LINE:  'I have of late but",
     "wherefore I know not lost all my mirth,",
     "forgone all custom of exercises;",
     "and indeed, it goes so heavily with",
     "my disposition that this goodly frame,",
     "the earth, seems to me a sterile promontory;",
     "this most excellent canopy, the air, look you,",
     "this brave o'erhanging firmament,",
     "this majestical roof fretted with golden fire",
     "why, it appeareth no other thing to me than a foul",
     "and pestilent congregation of vapours.",
     "What a piece of work is a man!",
     "how noble in reason! how infinite in faculties!",
     "in form and moving how express and admirable!",
     "in action how like an angel!",
     "in apprehension how like a god!",
     "the beauty of the world, the paragon of animals!'",
     "     VISIBLE:  'I have of late but",
     "wherefore I k', cursor=1",
     "SPEECH OUTPUT: 'I have of late but",
     "wherefore I know not lost all my mirth,",
     "forgone all custom of exercises;",
     "and indeed, it goes so heavily with",
     "my disposition that this goodly frame,",
     "the earth, seems to me a sterile promontory;",
     "this most excellent canopy, the air, look you,",
     "this brave o'erhanging firmament,",
     "this majestical roof fretted with golden fire",
     "why, it appeareth no other thing to me than a foul",
     "and pestilent congregation of vapours.",
     "What a piece of work is a man!",
     "how noble in reason! how infinite in faculties!",
     "in form and moving how express and admirable!",
     "in action how like an angel!",
     "in apprehension how like a god!",
     "the beauty of the world, the paragon of animals!'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("o"))
sequence.append(utils.AssertPresentationAction(
    "2. o to second large chunk", 
    ["BRAILLE LINE:  'I have of late but",
     "wherefore I know not lost all my mirth,",
     "forgone all custom of exercises;",
     "and indeed, it goes so heavily with",
     "my disposition that this goodly frame,",
     "the earth, seems to me a sterile promontory;",
     "this most excellent canopy, the air, look you,",
     "this brave o'erhanging firmament,",
     "this majestical roof fretted with golden fire",
     "why, it appeareth no other thing to me than a foul",
     "and pestilent congregation of vapours.",
     "What a piece of work is a man!",
     "how noble in reason! how infinite in faculties!",
     "in form and moving how express and admirable!",
     "in action how like an angel!",
     "in apprehension how like a god!",
     "the beauty of the world, the paragon of animals!'",
     "     VISIBLE:  'I have of late but",
     "wherefore I k', cursor=1",
     "SPEECH OUTPUT: 'I have of late but",
     "wherefore I know not lost all my mirth,",
     "forgone all custom of exercises;",
     "and indeed, it goes so heavily with",
     "my disposition that this goodly frame,",
     "the earth, seems to me a sterile promontory;",
     "this most excellent canopy, the air, look you,",
     "this brave o'erhanging firmament,",
     "this majestical roof fretted with golden fire",
     "why, it appeareth no other thing to me than a foul",
     "and pestilent congregation of vapours.",
     "What a piece of work is a man!",
     "how noble in reason! how infinite in faculties!",
     "in form and moving how express and admirable!",
     "in action how like an angel!",
     "in apprehension how like a god!",
     "the beauty of the world, the paragon of animals!'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("o"))
sequence.append(utils.AssertPresentationAction(
    "3. o to third large chunk", 
    ["BRAILLE LINE:  'I have of late but",
     "wherefore I know not lost all my mirth,",
     "forgone all custom of exercises;",
     "and indeed, it goes so heavily with",
     "my disposition that this goodly frame,",
     "the earth, seems to me a sterile promontory;",
     "this most excellent canopy, the air, look you,",
     "this brave o'erhanging firmament,",
     "this majestical roof fretted with golden fire",
     "why, it appeareth no other thing to me than a foul",
     "and pestilent congregation of vapours.",
     "What a piece of work is a man!",
     "how noble in reason! how infinite in faculties!",
     "in form and moving how express and admirable!",
     "in action how like an angel!",
     "in apprehension how like a god!",
     "the beauty of the world, the paragon of animals!'",
     "     VISIBLE:  'I have of late but",
     "wherefore I k', cursor=1",
     "SPEECH OUTPUT: 'I have of late but",
     "wherefore I know not lost all my mirth,",
     "forgone all custom of exercises;",
     "and indeed, it goes so heavily with",
     "my disposition that this goodly frame,",
     "the earth, seems to me a sterile promontory;",
     "this most excellent canopy, the air, look you,",
     "this brave o'erhanging firmament,",
     "this majestical roof fretted with golden fire",
     "why, it appeareth no other thing to me than a foul",
     "and pestilent congregation of vapours.",
     "What a piece of work is a man!",
     "how noble in reason! how infinite in faculties!",
     "in form and moving how express and admirable!",
     "in action how like an angel!",
     "in apprehension how like a god!",
     "the beauty of the world, the paragon of animals!'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("o"))
sequence.append(utils.AssertPresentationAction(
    "4. o to fourth large chunk", 
    ["BRAILLE LINE:  'I am a tranquilizer.",
     "I am effective at home,",
     "I work well at the office,",
     "I take exams,",
     "I appear in court,",
     "I carefully mend broken crockery -",
     "all you need do is take me,",
     "dissolve me under the tongue,",
     "all you need do is swallow me,",
     "just wash me down with water. I know how to cope with misfortune,",
     "how to endure bad news,",
     "take the edge of injustice,",
     "make up for the absence of God,",
     "help pick out your widow's weeds.",
     "What are you waiting for -",
     "have faith in chemistry's compassion. You're still a young man/woman,",
     "you really should settle down somehow.",
     "Who said",
     "life must be lived courageously? Hand your abyss over to me -",
     "I will line it up with soft sleep,",
     "you'll be grateful for",
     "the four-footed landing. Sell me your soul.",
     "There's no other buyer likely to turn up.'",
     "     VISIBLE:  'I am a tranquilizer.",
     "I am effect', cursor=1",
     "SPEECH OUTPUT: 'I am a tranquilizer.",
     "I am effective at home,",
     "I work well at the office,",
     "I take exams,",
     "I appear in court,",
     "I carefully mend broken crockery -",
     "all you need do is take me,",
     "dissolve me under the tongue,",
     "all you need do is swallow me,",
     "just wash me down with water.'",
     "SPEECH OUTPUT: 'I know how to cope with misfortune,",
     "how to endure bad news,",
     "take the edge of injustice,",
     "make up for the absence of God,",
     "help pick out your widow's weeds.",
     "What are you waiting for -",
     "have faith in chemistry's compassion.'",
     "SPEECH OUTPUT: 'You're still a young man/woman,",
     "you really should settle down somehow.",
     "Who said",
     "life must be lived courageously?'",
     "SPEECH OUTPUT: 'Hand your abyss over to me -",
     "I will line it up with soft sleep,",
     "you'll be grateful for",
     "the four-footed landing.'",
     "SPEECH OUTPUT: 'Sell me your soul.",
     "There's no other buyer likely to turn up.'"]))

sequence.append(utils.StartRecordingAction())
sequence.append(KeyComboAction("<Shift>o"))
sequence.append(utils.AssertPresentationAction(
    "5. Shift + o to third large chunk", 
    ["BRAILLE LINE:  'I have of late but",
     "wherefore I know not lost all my mirth,",
     "forgone all custom of exercises;",
     "and indeed, it goes so heavily with",
     "my disposition that this goodly frame,",
     "the earth, seems to me a sterile promontory;",
     "this most excellent canopy, the air, look you,",
     "this brave o'erhanging firmament,",
     "this majestical roof fretted with golden fire",
     "why, it appeareth no other thing to me than a foul",
     "and pestilent congregation of vapours.",
     "What a piece of work is a man!",
     "how noble in reason! how infinite in faculties!",
     "in form and moving how express and admirable!",
     "in action how like an angel!",
     "in apprehension how like a god!",
     "the beauty of the world, the paragon of animals!'",
     "     VISIBLE:  'I have of late but",
     "wherefore I k', cursor=1",
     "SPEECH OUTPUT: 'I have of late but",
     "wherefore I know not lost all my mirth,",
     "forgone all custom of exercises;",
     "and indeed, it goes so heavily with",
     "my disposition that this goodly frame,",
     "the earth, seems to me a sterile promontory;",
     "this most excellent canopy, the air, look you,",
     "this brave o'erhanging firmament,",
     "this majestical roof fretted with golden fire",
     "why, it appeareth no other thing to me than a foul",
     "and pestilent congregation of vapours.",
     "What a piece of work is a man!",
     "how noble in reason! how infinite in faculties!",
     "in form and moving how express and admirable!",
     "in action how like an angel!",
     "in apprehension how like a god!",
     "the beauty of the world, the paragon of animals!'"]))

sequence.append(utils.AssertionSummaryAction())
sequence.start()
