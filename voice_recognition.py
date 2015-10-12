import speech_recognition


class VoiceRecognition:
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()

    def listen(self):
        try:
            with speech_recognition.Microphone() as source:
                # listen for 1 second to calibrate the energy threshold for ambient noise levels
                self.recognizer.adjust_for_ambient_noise(source)
                print("Say something!")
                self.audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(self.audio)
                print("Google Speech Recognition thinks you said " + text)
                return text
            except speech_recognition.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                return "What was that again?"
            except speech_recognition.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                return "Sorry, I'm disconnected to the Internet"
        except KeyboardInterrupt:
            pass
