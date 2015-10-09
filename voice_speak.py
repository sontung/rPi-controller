import pyttsx


class Speaker:
    def __init__(self, name):
        self.name = name
        self.already_introduced = False
        self.engine = pyttsx.init()
        self.engine.setProperty('volume', 1.0)
        self.engine.setProperty('voice',
                                "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_10.0")

    def introduce(self):
        if not self.already_introduced:
            self.already_introduced = True
            self.say('Hello, my name is %s. I\'m your assistant in our smart home '
                     'programme. To get started, please give me a command.' % self.name)
        else:
            self.say('Hello again, how can I help you?')

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def react(self, text):
        if text == "hi" or text == "hello":
            self.introduce()
        else:
            self.say(text)