import speech_recognition


class VoiceRcognition:
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()

    def listen(self):
        with speech_recognition.Microphone() as source:
            print("Say something!")
            self.audio = self.recognizer.listen(source)

    def process(self):
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

