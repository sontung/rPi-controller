import voice_speak
import voice_recognition

pipi = voice_speak.Speaker("Pipi")
pipi_ear = voice_recognition.VoiceRcognition()

while True:
    pipi_ear.listen()
    out = pipi_ear.process()
    pipi.react(out)