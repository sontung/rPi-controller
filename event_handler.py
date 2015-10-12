import paramiko
import pygame
import sys
import core_communication
import voice_speak
import voice_recognition
from pygame.locals import *
from multiprocessing import Process, Queue


class EventLogic:
    def __init__(self, _game_state, _game_gui):
        self._game_state = _game_state
        self._game_gui = _game_gui
        self.ssh_talk = core_communication.SSHCommunication()
        self.pipi = voice_speak.Speaker("Pipi", self.ssh_talk, self._game_gui)
        self.pipi_ear = voice_recognition.VoiceRecognition()
        self.current_prompt = None
        self.recording = False
        self.movement = {
            K_UP: 8,
            K_DOWN: 2,
            K_RIGHT: 6,
            K_LEFT: 4
        }
        self.queue = Queue()

    def quit(self):
        pygame.quit()
        sys.exit()

    def pipi_listen(self):
        print "listening"
        out = self.pipi_ear.listen()
        self.pipi.react(out)

    def event_handler(self):
        print "running handler"
        event = pygame.event.poll()
        if event.type == MOUSEBUTTONDOWN:
            if self._game_gui.buttons:
                for button1 in self._game_gui.buttons:
                    button1.set_pressed(pygame.mouse.get_pos())

            if self._game_state.get_state() == "welcome":
                if self._game_gui.new.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("new season")
                elif self._game_gui.help.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("help")
                elif self._game_gui.author.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("author")
                elif self._game_gui.setting.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("setting")
                elif self._game_gui.quit.get_rect().collidepoint(event.pos):
                    self.quit()

            elif self._game_state.get_state() == "new season":
                if self._game_gui.back.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("welcome")
                elif self._game_gui.ssh_button.get_rect().collidepoint(event.pos):  # connecting to SSH
                    try:
                        self.ssh_talk.connect()
                    except paramiko.AuthenticationException:
                        self._game_state.set_state("error ssh authentication")
                    except RuntimeError:
                        self._game_state.set_state("error cannot connect")
                    else:
                        self._game_state.set_state("SSH season")
                        #self.ssh_talk.command("sudo /home/pi/group12/comm/outputControl.py")
                elif self._game_gui.socket_button.get_rect().collidepoint(event.pos):  # connecting to socket
                    pass

            elif self._game_state.get_state() == "SSH season":
                if self._game_gui.allOff_switch.get_rect().collidepoint(event.pos):
                    self._game_gui.command_switch("all off")
                    self.ssh_talk.command("echo turnOff >/tmp/commandPipe")
                elif self._game_gui.allOn_switch.get_rect().collidepoint(event.pos):
                    self._game_gui.command_switch("all on")
                    self.ssh_talk.command("echo turnOn >/tmp/commandPipe")
                elif self._game_gui.red_switch.get_rect().collidepoint(event.pos):
                    self._game_gui.command_switch("red")
                    self.ssh_talk.command("echo switchRed >/tmp/commandPipe")
                elif self._game_gui.green_switch.get_rect().collidepoint(event.pos):
                    self._game_gui.command_switch("green")
                    self.ssh_talk.command("echo switchGreen >/tmp/commandPipe")
                elif self._game_gui.yellow_switch.get_rect().collidepoint(event.pos):
                    self._game_gui.command_switch("yellow")
                    self.ssh_talk.command("echo switchYellow >/tmp/commandPipe")
                elif self._game_gui.flash_switch.get_rect().collidepoint(event.pos):
                    self._game_gui.command_switch("flash")
                    self.ssh_talk.command("echo flash >/tmp/commandPipe")
                elif self._game_gui.voice_mode.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("SSH season voice mode")
                    self.pipi.introduce()
                elif self._game_gui.back.get_rect().collidepoint(event.pos):
                    self.ssh_talk.disconnect()
                    self._game_state.set_state("welcome")

            elif self._game_state.get_state() == "SSH season voice mode":
                if self._game_gui.button_mode.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("SSH season")
                elif self._game_gui.back.get_rect().collidepoint(event.pos):
                    self.ssh_talk.disconnect()
                    self._game_state.set_state("welcome")

            elif self._game_state.get_state() == "setting":
                if self._game_gui.back.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("welcome")
                elif self._game_gui.host_prompt.rect.collidepoint(event.pos):
                    self._game_gui.set_typing_tag(True)
                    self._game_gui.host_prompt.reset_display_title()
                    self._game_gui.user_prompt.set_display_title()
                    self._game_gui.password_prompt.set_display_title()
                    self.current_prompt = self._game_gui.host_prompt
                elif self._game_gui.user_prompt.rect.collidepoint(event.pos):
                    self._game_gui.set_typing_tag(True)
                    self._game_gui.host_prompt.set_display_title()
                    self._game_gui.user_prompt.reset_display_title()
                    self._game_gui.password_prompt.set_display_title()
                    self.current_prompt = self._game_gui.user_prompt
                elif self._game_gui.password_prompt.rect.collidepoint(event.pos):
                    self._game_gui.set_typing_tag(True)
                    self._game_gui.host_prompt.set_display_title()
                    self._game_gui.user_prompt.set_display_title()
                    self._game_gui.password_prompt.reset_display_title()
                    self.current_prompt = self._game_gui.password_prompt
                elif self._game_gui.save.get_rect().collidepoint(event.pos):
                    self.ssh_talk.specify_information(self._game_gui.host_prompt.output()[0],
                                                      self._game_gui.user_prompt.output()[0],
                                                      self._game_gui.password_prompt.output()[0])
                    self._game_gui.reset_prompts()
                else:
                    self._game_gui.set_typing_tag(False)

            elif self._game_state.get_state().find("error") != -1:
                if self._game_gui.back.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("welcome")

            elif self._game_state.get_state() in ["help", "author", "setting"]:
                if self._game_gui.back.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("welcome")

        elif event.type == MOUSEMOTION or event.type == NOEVENT:
            if self._game_gui.buttons:
                for button in self._game_gui.buttons:
                    button.set_bold(pygame.mouse.get_pos())

        elif event.type == pygame.QUIT:
            self.quit()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.quit()

            elif event.key == K_SPACE:
                if self._game_state.get_state() == "SSH season voice mode":
                    self._game_gui.recording = not self._game_gui.recording
                    self._game_gui.draw(self._game_state.get_state())

            else:
                if self._game_gui.typing_tag:
                    self.current_prompt.take_char(pygame.key.name(event.key))
