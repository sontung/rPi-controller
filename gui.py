import pygame
import sys
import time


class GUI:
    def __init__(self, _game_state):
        pygame.init()
        self.handler = None
        self.state = _game_state
        self.font_size = 30
        self.window_height = 600
        self.window_width = 600
        self.colors = {"white": (255, 255, 255),
                       "black": (41, 36, 33),
                       "navy": (0, 0, 128),
                       "red": (139, 0, 0),
                       "blue": (0, 0, 255),
                       "dark": (3, 54, 73),
                       "yellow": (255, 255, 0),
                       "turquoise blue": (0, 199, 140),
                       "green": (0, 128, 0),
                       "light green": (118, 238, 0),
                       "turquoise": (0, 229, 238),
                       "gray": (152, 152, 152),
                       "toolbar": (100,221,23),
                       "main_background": (118,255,3)}
        self.text_color = self.colors["red"]
        self.bg_color = self.colors["main_background"]
        self.tile_color = None
        self.tb_color = self.colors["toolbar"]
        self.shadow_color = (236,239,241)
        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Light Controlling Interface")
        self.button_sprites = pygame.image.load("assets\\images\\buttons.png")
        self.light_sprites = pygame.image.load("assets\\images\\leds.png")
        self.bg_sprites = pygame.image.load("assets\\images\\bg3.jpg")
        self.typing_tag = False
        self.recording = False
        self.time_recording = None  # the moment the user records
        self.set_time_recording = True

        # states of the lights
        self.red = False
        self.green = False
        self.yellow = False

        self.light_to_string = dict(red=self.red, green=self.green, yellow=self.yellow)
        self.bool_to_text = dict(True="on", False="off")

        # for setting up information for communication
        self.host_prompt = Prompt((self.window_width/4, self.window_height/3), self, "host")
        self.user_prompt = Prompt((self.window_width/4, self.window_height/3+100), self, "username")
        self.password_prompt = Prompt((self.window_width/4, self.window_height/3+200), self, "password")

    def add_handler(self, handler):
        self.handler = handler

    def reset_prompts(self):
        self.host_prompt.reset()
        self.user_prompt.reset()
        self.password_prompt.reset()

    def update_states_lights(self):
        result = self.handler.get_states_lights()
        self.red = bool(int(result[0][0]))
        self.yellow = bool(int(result[0][1]))
        self.green = bool(int(result[0][2]))

    def blit_lights(self):
        """
        Make changes to the GUI according to the states
        of the lights
        :return:
        """
        self.display_surface.blit(self.red_light.get_img(), self.red_light.get_pos())
        self.display_surface.blit(self.green_light.get_img(), self.green_light.get_pos())
        self.display_surface.blit(self.yellow_light.get_img(), self.yellow_light.get_pos())

    def make_text(self, text, color, bg_color, center, topleft=None):
        """
        Make a text object for drawing
        """
        font = pygame.font.Font("assets\\fonts\Cutie Patootie Skinny.ttf", self.font_size)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect()
        if center:
            text_rect.center = center
        else:
            text_rect.topleft = topleft
        return text_surf, text_rect

    def set_typing_tag(self, val):
        """
        Decide whether you want to type or not.
        """
        self.typing_tag = val

    def indicate_saying(self):
        if self.time_recording is None:
            return self.make_text("recording ...", self.text_color, self.tile_color, (120, self.window_height/4))
        elif time.time() - self.time_recording >= 1:
            return self.make_text("say something ...", self.text_color, self.tile_color, (120, self.window_height/4))
        else:
            return self.make_text("recording ...", self.text_color, self.tile_color, (120, self.window_height/4))

    def draw_toolbar(self, title=True):
        pygame.draw.rect(self.display_surface, self.colors["toolbar"], pygame.Rect(0, 0, self.window_width,
                                                                                   self.window_height/6))
        self.display_surface.blit(self.bg_sprites, (0, 0))
        if title:
            title_sur, title_rect = self.make_text(self.state.get_state(), self.colors["blue"], self.tb_color, None,
                                                   (30, self.window_height/15))
            self.display_surface.blit(title_sur, title_rect)

    def draw(self, state):
        """
        Draw the scene.
        """
        self.display_surface.fill(self.bg_color)
        if state == "welcome":
            start_point = 60
            self.setting = Button('Settings', self.text_color, self.tile_color,
                                  (self.window_width/2, start_point+120), self)
            self.new = Button('New Session', self.text_color, self.tile_color,
                              (self.window_width/2, start_point), self)
            self.quit = Button('Quit', self.text_color, self.tile_color,
                               (self.window_width/2, start_point+120*4), self)
            self.help = Button('How to use this app', self.text_color, self.tile_color,
                               (self.window_width/2, start_point+120*2), self)
            self.author = Button('About the author', self.text_color, self.tile_color,
                                 (self.window_width/2, start_point+120*3), self)
            self.buttons = [self.new, self.setting, self.quit, self.help, self.author]
            self.display_surface.blit(self.setting.get_sr()[0], self.setting.get_sr()[1])
            self.display_surface.blit(self.new.get_sr()[0], self.new.get_sr()[1])
            self.display_surface.blit(self.quit.get_sr()[0], self.quit.get_sr()[1])
            self.display_surface.blit(self.help.get_sr()[0], self.help.get_sr()[1])
            self.display_surface.blit(self.author.get_sr()[0], self.author.get_sr()[1])

        elif state == "help":
            self.draw_toolbar()
            sys.stdin = open("assets/texts/instruction.txt")
            for i in range(9):
                instructions = sys.stdin.readline().strip()
                self.instructions_sur, self.instructions_rect = self.make_text(instructions, self.colors["black"],
                                                                               self.tile_color,
                                                                               (self.window_width/2,
                                                                                self.window_height/2-120+i*35))
                self.display_surface.blit(self.instructions_sur, self.instructions_rect)
            self.back = Button("Back", self.text_color, self.tb_color, None, self,
                               (self.window_width-30, self.window_height/15))
            self.buttons = [self.back]
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])

        elif state == "author":
            self.draw_toolbar()
            sys.stdin = open("assets/texts/author.txt")
            for i in range(8):
                instructions = sys.stdin.readline().strip()
                self.instructions_sur, self.instructions_rect = self.make_text(instructions, self.colors["black"],
                                                                               self.tile_color,
                                                                               (self.window_width/2,
                                                                                self.window_height/2-120+i*35))
                self.display_surface.blit(self.instructions_sur, self.instructions_rect)
            self.back = Button("Back", self.text_color, self.tb_color, None, self,
                               (self.window_width-30, self.window_height/15))
            self.buttons = [self.back]
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])

        elif state == "new session":
            self.draw_toolbar()
            self.back = Button("Back", self.text_color, self.tb_color, None, self,
                               (self.window_width-30, self.window_height/15))
            choose_sur, choose_rect = self.make_text("Choose your pref communication", self.colors["green"], self.tile_color,
                                                     (self.window_width/2, self.window_height/4))
            self.ssh_button = Button("SSH connection", self.text_color, self.tile_color,
                                     (self.window_width/4, self.window_height/2), self)
            self.web_button = Button("Web connection", self.text_color, self.tile_color,
                                     (self.window_width*3/4, self.window_height/2), self)
            self.buttons = [self.ssh_button, self.back, self.web_button]
            self.display_surface.blit(choose_sur, choose_rect)
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])
            self.display_surface.blit(self.ssh_button.get_sr()[0], self.ssh_button.get_sr()[1])
            self.display_surface.blit(self.web_button.get_sr()[0], self.web_button.get_sr()[1])

        elif state == "settings":
            self.draw_toolbar()
            self.host_prompt.draw_rect()
            self.user_prompt.draw_rect()
            self.password_prompt.draw_rect()

            guide_sur, guide_rect = self.make_text("Specify essential information below:",
                                                   self.colors["green"], self.tile_color,
                                                   (self.window_width/2, self.window_height/4))
            self.save = Button("Save", self.text_color, self.tile_color, (4.5*self.window_width/5, self.window_height/4), self)
            self.back = Button("Back", self.text_color, self.tb_color, None, self,
                               (self.window_width-30, self.window_height/15))
            self.buttons = [self.back, self.save]
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])
            self.display_surface.blit(self.save.get_sr()[0], self.save.get_sr()[1])
            self.display_surface.blit(guide_sur, guide_rect)
            if self.typing_tag:
                self.display_surface.blit(self.host_prompt.output()[1], self.host_prompt.output()[2])
                self.display_surface.blit(self.user_prompt.output()[1], self.user_prompt.output()[2])
                self.display_surface.blit(self.password_prompt.output()[1], self.password_prompt.output()[2])
            self.display_surface.blit(self.host_prompt.output_title()[0], self.host_prompt.output_title()[1])
            self.display_surface.blit(self.user_prompt.output_title()[0], self.user_prompt.output_title()[1])
            self.display_surface.blit(self.password_prompt.output_title()[0], self.password_prompt.output_title()[1])

        elif state in ["SSH season", "Web season"]:
            self.draw_toolbar(False)
            self.update_states_lights()
            title_sur, title_rect = self.make_text("CONTROL BOARD", self.colors["green"], self.tb_color,
                                                   (self.window_width/2, self.window_height/15))
            self.back = Button("Back", self.text_color, self.tb_color, None, self,
                               (self.window_width-30, self.window_height/15))
            self.voice_mode = Button("Voice mode", self.text_color, self.tb_color, None, self, (130, self.window_height/15))
            self.red_light = LightSprite((self.window_width*3/8, self.window_height/4), self.light_sprites,
                                         {"on": (105, 0), "normal": (0, 0)}, self, self.red)
            self.green_light = LightSprite((self.window_width*5/8, self.window_height/4), self.light_sprites,
                                           {"on": (35, 0), "normal": (0, 0)}, self, self.green)
            self.yellow_light = LightSprite((self.window_width*7/8, self.window_height/4), self.light_sprites,
                                            {"on": (70, 0), "normal": (0, 0)}, self, self.yellow)
            allOn_indication_sur, allOn_indication_rect = self.make_text("All On", self.text_color, self.tile_color,
                                                                         (self.window_width/8, self.window_height/4+25))
            allOff_indication_sur, allOff_indication_rect = self.make_text("All Off", self.text_color, self.tile_color,
                                                                           (self.window_width/8, self.window_height*7/20+25))
            red_indication_sur, red_indication_rect = self.make_text("Red On/Off", self.text_color, self.tile_color,
                                                                     (self.window_width/8, self.window_height*9/20+25))
            green_indication_sur, green_indication_rect = self.make_text("Green On/Off", self.text_color,
                                                                         self.tile_color,
                                                                         (self.window_width/8, self.window_height*11/20+25))
            yellow_indication_sur, yellow_indication_rect = self.make_text("Yellow On/Off", self.text_color,
                                                                           self.tile_color,
                                                                           (self.window_width/8, self.window_height*13/20+25))
            flash_indication_sur, flash_indication_rect = self.make_text("Flash", self.text_color, self.tile_color,
                                                                         (self.window_width/8, self.window_height*15/20+25))
            self.allOn_switch = ButtonSprite((self.window_width/4, self.window_height/4), self.button_sprites,
                                             {"normal": (0, 0), "hover": (50, 0), "pressed": (100, 0)}, self)
            self.allOff_switch = ButtonSprite((self.window_width/4, self.window_height*7/20), self.button_sprites,
                                             {"normal": (0, 0), "hover": (50, 0), "pressed": (100, 0)}, self)
            self.red_switch = ButtonSprite((self.window_width/4, self.window_height*9/20), self.button_sprites,
                                           {"normal": (0, 0), "hover": (50, 0), "pressed": (100, 0)}, self)
            self.green_switch = ButtonSprite((self.window_width/4, self.window_height*11/20), self.button_sprites,
                                             {"normal": (0, 0), "hover": (50, 0), "pressed": (100, 0)}, self)
            self.yellow_switch = ButtonSprite((self.window_width/4, self.window_height*13/20), self.button_sprites,
                                              {"normal": (0, 0), "hover": (50, 0), "pressed": (100, 0)}, self)
            self.flash_switch = ButtonSprite((self.window_width/4, self.window_height*15/20), self.button_sprites,
                                             {"normal": (0, 0), "hover": (50, 0), "pressed": (100, 0)}, self)
            self.buttons = [self.allOn_switch, self.allOff_switch, self.back, self.red_switch, self.green_switch,
                            self.yellow_switch, self.flash_switch, self.voice_mode]
            self.display_surface.blit(title_sur, title_rect)

            # Texts
            self.display_surface.blit(allOn_indication_sur, allOn_indication_rect)
            self.display_surface.blit(allOff_indication_sur, allOff_indication_rect)
            self.display_surface.blit(red_indication_sur, red_indication_rect)
            self.display_surface.blit(green_indication_sur, green_indication_rect)
            self.display_surface.blit(yellow_indication_sur, yellow_indication_rect)
            self.display_surface.blit(flash_indication_sur, flash_indication_rect)

            # Switches
            self.display_surface.blit(self.allOn_switch.get_img(), self.allOn_switch.get_pos())
            self.display_surface.blit(self.allOff_switch.get_img(), self.allOff_switch.get_pos())
            self.display_surface.blit(self.red_switch.get_img(), self.red_switch.get_pos())
            self.display_surface.blit(self.green_switch.get_img(), self.green_switch.get_pos())
            self.display_surface.blit(self.yellow_switch.get_img(), self.yellow_switch.get_pos())
            self.display_surface.blit(self.flash_switch.get_img(), self.flash_switch.get_pos())
            self.blit_lights()
            self.display_surface.blit(self.voice_mode.get_sr()[0], self.voice_mode.get_sr()[1])
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])

        elif state in ["Web season voice mode", "SSH season voice mode"]:
            self.update_states_lights()
            self.draw_toolbar(False)
            title_sur, title_rect = self.make_text("CONTROL BOARD", self.colors["green"], self.tb_color,
                                                   (self.window_width/2, self.window_height/15))
            recording_sur, recording_rect = self.indicate_saying()
            self.back = Button("Back", self.text_color, self.tb_color, None, self,
                               (self.window_width-30, self.window_height/15))
            self.button_mode = Button("Button mode", self.text_color, self.tb_color, None, self, (130, self.window_height/15))
            self.red_light = LightSprite((self.window_width*3/8, self.window_height/4), self.light_sprites,
                                         {"on": (105, 0), "normal": (0, 0)}, self, self.red)
            self.green_light = LightSprite((self.window_width*5/8, self.window_height/4), self.light_sprites,
                                           {"on": (35, 0), "normal": (0, 0)}, self, self.green)
            self.yellow_light = LightSprite((self.window_width*7/8, self.window_height/4), self.light_sprites,
                                            {"on": (70, 0), "normal": (0, 0)}, self, self.yellow)
            self.buttons = [self.back, self.button_mode]
            self.display_surface.blit(title_sur, title_rect)
            if self.recording:
                if self.set_time_recording:
                    self.time_recording = time.time()
                    self.set_time_recording = False
                self.display_surface.blit(recording_sur, recording_rect)
            else:
                self.set_time_recording = True
            self.blit_lights()
            self.display_surface.blit(self.button_mode.get_sr()[0], self.button_mode.get_sr()[1])
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])

        elif state.find("error") != -1:
            self.draw_toolbar()
            sys.stdin = open("assets/texts/error_help.txt")
            for i in range(9):
                instructions = sys.stdin.readline().strip()
                self.instructions_sur, self.instructions_rect = self.make_text(instructions, self.colors["black"],
                                                                               self.tile_color,
                                                                               (self.window_width/2,
                                                                                self.window_height/2-120+i*35))
                self.display_surface.blit(self.instructions_sur, self.instructions_rect)
            if state == "error cannot connect":
                error_sur, error_rect = self.make_text("Cannot connect", self.colors["red"], self.tile_color,
                                                       (self.window_width/2, self.window_height*2.5/4))
            elif state == "error authentication":
                error_sur, error_rect = self.make_text("Wrong credentials", self.colors["red"], self.tile_color,
                                                       (self.window_width/2, self.window_height*2.5/4))
            self.back = Button("Back", self.text_color, self.tb_color,
                               (self.window_width-30, self.window_height/10), self)
            self.buttons = [self.back]
            self.display_surface.blit(error_sur, error_rect)
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])


class Sprite:
    """
    Class for handling sprites
    """
    def __init__(self, pos, sheet, loc_in_sheet, _game_gui, dim=None):
        self.sheet = sheet
        self.loc_in_sheet = loc_in_sheet  # a dictionary keeping track of each movement and their sprites
        if dim:
            self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["normal"][0], self.loc_in_sheet["normal"][1], dim[0], dim[1]))
            self.img = self.sheet.subsurface(self.sheet.get_clip())
        else:
            self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["normal"][0], self.loc_in_sheet["normal"][1], 50, 50))
            self.img = self.sheet.subsurface(self.sheet.get_clip())
        self.pos = pos
        self.gui = _game_gui

    def get_img(self):
        return self.img

    def get_pos(self):
        return self.pos


class ButtonSprite(Sprite):
    """
    Child class for handling button sprites specifically
    """
    def __init__(self, pos, sheet, loc_in_sheet, _game_gui):
        Sprite.__init__(self, pos, sheet, loc_in_sheet, _game_gui)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 50, 50)
        self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["hover"][0], self.loc_in_sheet["hover"][1], 50, 50))
        self.img_hover = self.sheet.subsurface(self.sheet.get_clip())
        self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["pressed"][0], self.loc_in_sheet["pressed"][1], 50, 50))
        self.img_pressed = self.sheet.subsurface(self.sheet.get_clip())

    def get_rect(self):
        return self.rect

    def set_pressed(self, pos):
        """
        Highlight the button when the user clicks mouse on
        """
        if self.rect.collidepoint(pos):
            self.gui.display_surface.blit(self.img_pressed, self.pos)

    def set_bold(self, pos):
        """
        Highlight the button when the user hovers mouse over
        """
        if self.rect.collidepoint(pos):
            self.gui.display_surface.blit(self.img_hover, self.pos)


class LightSprite(Sprite):
    """
    Child class for handling light sprites specifically
    """
    def __init__(self, pos, sheet, loc_in_sheet, _game_gui, state):
        Sprite.__init__(self, pos, sheet, loc_in_sheet, _game_gui, (35, 35))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 35, 35)
        self.state = state
        self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["on"][0], self.loc_in_sheet["on"][1], 35, 35))
        self.img_on = self.sheet.subsurface(self.sheet.get_clip())

    def get_img(self):
        if self.state:
            return self.img_on
        else:
            return self.img

    def get_rect(self):
        return self.rect


class Button:
    """
    Class for handling buttons
    """
    def __init__(self, text, color, bg_color, center, _game_gui, topright=None):
        self.gui = _game_gui
        self.text = text
        self.topright = topright
        self.center = center
        self.color = color
        self.bg_color = bg_color
        self.bold = False
        self.font_size = 30
        font = pygame.font.Font("assets\\fonts\Cutie Patootie Skinny.ttf", self.font_size)
        self.surf = font.render(text, True, color)
        self.rect = self.surf.get_rect()
        if self.center:
            self.rect.center = self.center
        else:
            self.rect.topright = self.topright

    def make_text(self):
        """
        Make a text object for drawing
        """
        if not self.bold:
            font = pygame.font.Font("assets\\fonts\Cutie Patootie Skinny.ttf", self.font_size)
            text_surf = font.render(self.text, True, self.color, self.bg_color)
        else:
            font_bold = pygame.font.Font("assets\\fonts\Cutie Patootie.ttf", self.font_size)
            text_surf = font_bold.render(self.text, True, self.color)
        text_rect = text_surf.get_rect()
        if self.center:
            text_rect.center = self.center
        else:
            text_rect.topright = self.topright
        return text_surf, text_rect

    def get_rect(self):
        return self.rect

    def get_sr(self):
        return self.surf, self.rect

    def update_sr(self):
        self.surf, self.rect = self.make_text()

    def set_pressed(self, pos):
        pass

    def set_bold(self, pos):
        """
        Highlight the button when the user hovers mouse over
        """
        if self.rect.collidepoint(pos):
            self.bold = True
            self.update_sr()
            self.gui.display_surface.blit(self.surf, self.rect)


class Prompt:
    """
    Prompt which takes input keyboard from user as a string
    """
    def __init__(self, topleft, _gui, title=""):
        self.title = title
        self.string = ""
        self.display_title = True
        self.gui = _gui
        self.colors = _gui.colors
        self.color = _gui.text_color
        self.bg_color = _gui.colors["white"]
        self.topleft = topleft
        self.font_size = 40
        self.rect = pygame.Rect(self.topleft[0], self.topleft[1], 360, 70)

    def draw_rect(self):
        """
        Draw a blank space
        :return:
        """
        if self.display_title:
            pygame.draw.rect(self.gui.display_surface, self.colors["white"], self.rect)
        else:
            pygame.draw.rect(self.gui.display_surface, self.colors["white"], self.rect, 3)

    def make_text(self, text, color=None):
        """
        Make a text object for drawing
        """
        font = pygame.font.Font("assets\\fonts\Cutie Patootie Skinny.ttf", self.font_size)
        if color is None:
            if not self.display_title:
                text_surf = font.render(text, True, self.color)
            else:
                text_surf = font.render(text, True, self.color)
        else:
            text_surf = font.render(text, True, color, self.bg_color)
        text_rect = text_surf.get_rect()
        text_rect.topleft = (self.topleft[0]+1, self.topleft[1]+3)
        return text_surf, text_rect

    def take_char(self, char):
        """
        Take in character or delete previous one.
        :return:
        """
        if char != "backspace":
            self.string += char
        else:
            self.string = self.string[:-1]

    def set_display_title(self):
        self.display_title = True

    def reset_display_title(self):
        self.display_title = False

    def output_title(self):
        """
        Output the title for this prompt
        :return:
        """
        if self.display_title and self.string == "":
            return self.make_text(self.title, self.colors["gray"])
        else:
            return self.make_text("", self.colors["gray"])

    def output(self):
        """
        Output the string
        :return:
        """
        sur, rect = self.make_text(self.string)
        return self.string, sur, rect

    def reset(self):
        """
        Reset the prompt
        :return:
        """
        self.string = ""
