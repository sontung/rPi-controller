import pyttsx


class Speaker:
    def __init__(self, name, talk, _game_gui):
        self.name = name
        self.talk = talk
        self._game_gui = _game_gui
        self.already_introduced = False
        self.engine = pyttsx.init()
        self.engine.setProperty('volume', 1.0)
        self.engine.setProperty('voice',
                                "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_10.0")

    def __getstate__(self):
        odict = self.__dict__.copy()
        del odict["engine"]
        return odict

    def __setstate__(self, d):
        self.__dict__.update(d)
        self.engine = pyttsx.init()

    def introduce(self):
        if not self.already_introduced:
            self.already_introduced = True
            self.say('Hello, my name is %s. I\'m your assistant in our smart home '
                     'programme. To get started, press Space bar to give me a command.' % self.name)
        else:
            self.say('Hello again, how can I help you? Press Space bar so I can hear you')

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def react(self, text):
        if text == "hi" or text == "hello":
            self.introduce()
            return None
        elif text == "green":
            #self.talk.command("echo switchGreen >/tmp/commandPipe")
            self.say("green light is on as you commanded")
            return "green"
        elif text == "red":
            #self.talk.command("echo switchRed >/tmp/commandPipe")
            self.say("red light is on as you commanded")
            return "red"
        elif text == "yellow":
            #self.talk.command("echo switchYellow >/tmp/commandPipe")
            self.say("yellow light is on as you commanded")
            return "yellow"
        else:
            pass
