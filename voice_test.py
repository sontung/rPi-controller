import pyttsx


engine = pyttsx.init()
voices = engine.getProperty('voices')
for voice in voices:
    print voice.id
    if voice.id == "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech Server\v11.0\Voices\Tokens\TTS_MS_en-CA_Heather_11.0":
        main_voice = voice
        main_voice.age = 20
        main_voice.name = "Pipi"
volume = engine.getProperty('volume')
engine.setProperty('volume', 1.0)
engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech Server\v11.0\Voices\Tokens\TTS_MS_en-AU_Hayley_11.0")
engine.say('Hello, my name is %s. I\'m your assistant in our smart home'
           'programme. To get started, please give me a command.' % ("Pipi"))
engine.runAndWait()