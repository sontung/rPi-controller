import pyttsx


class Speaker:
    def __init__(self, name, ssh_talk, web_talk, _game_gui):
        self.name = name
        self.state = ""
        self.ssh_talk = ssh_talk
        self.web_talk = web_talk
        self._game_gui = _game_gui
        self.already_introduced = False
        self.engine = pyttsx.init()
        self.engine.setProperty('volume', 1.0)
        self.engine.setProperty('voice',
                                "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_10.0")

    def __getstate__(self):
        odict = self.__dict__.copy()
        if self.state == "ssh":
            self.ssh_talk.disconnect()
        del odict["engine"]
        return odict

    def __setstate__(self, d):
        self.__dict__.update(d)
        if self.state == "ssh":
            self.ssh_talk.connect()
        self.engine = pyttsx.init()
        self.engine.setProperty('volume', 1.0)
        self.engine.setProperty('voice',
                                "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_10.0")

    def update_state(self, val):
        self.state = val

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
        """
        Return proper command according to what is
        heard, also return proper indication if necessary
        :param text:
        :return:
        """
        if text == "hi" or text == "hello":
            self.introduce()
            return None
        elif text == "green":
            if self.state == "ssh":
                self.ssh_talk.command("echo switchGreen >/tmp/commandPipe")
            elif self.state == "web":
                self.web_talk.command("put", "green")
            return "green light is %s as you commanded"
        elif text == "red":
            if self.state == "ssh":
                self.ssh_talk.command("echo switchRed >/tmp/commandPipe")
            elif self.state == "web":
                self.web_talk.command("put", "red")
            return "red light is %s as you commanded"
        elif text == "yellow":
            if self.state == "ssh":
                self.ssh_talk.command("echo switchYellow >/tmp/commandPipe")
            elif self.state == "web":
                self.web_talk.command("put", "yellow")
            return "yellow light is %s as you commanded"
        elif text.lower() == "flash":
            if self.state == "ssh":
                self.ssh_talk.command("echo flash >/tmp/commandPipe")
            elif self.state == "web":
                self.web_talk.command("put", "flash")
            self.say("the lights are flashing")
            return "nothing"
        elif text.lower() == "all on":
            if self.state == "ssh":
                self.ssh_talk.command("echo turnOn >/tmp/commandPipe")
            elif self.state == "web":
                self.web_talk.command("put", "all on")
            self.say("all the lights are on")
            return "nothing"
        elif text.lower() == "all off":
            if self.state == "ssh":
                self.ssh_talk.command("echo turnOff >/tmp/commandPipe")
            elif self.state == "web":
                self.web_talk.command("put", "all off")
            self.say("all the lights are off")
            return "nothing"
        else:
            pass
