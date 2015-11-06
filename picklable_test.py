import copy
import voice_recognition
import voice_speak
import event_handler
import gui
import pyttsx
import core_communication

s = voice_speak.Speaker("name", None, None)
r = voice_recognition.VoiceRecognition()
e = event_handler.EventLogic(None, None)
g = gui.GUI(None)
t = core_communication.SSHCommunication()
t.specify_information("192.168.43.96", "pi", "raspberry")
t.connect()
t.disconnect()
t.connect()
c = copy.deepcopy(t)
