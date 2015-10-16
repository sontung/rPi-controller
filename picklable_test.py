import copy
import voice_recognition
import voice_speak
import event_handler
import gui
import pyttsx

s = voice_speak.Speaker("name", None, None)
r = voice_recognition.VoiceRecognition()
e = event_handler.EventLogic(None, None)
g = gui.GUI(None)
c = copy.deepcopy(pyttsx.init())
