import pygame
import sys


class GUI:
    def __init__(self, _game_state):
        pygame.init()
        self.state = _game_state
        self.font_size = 40
        self.window_height = 800
        self.window_width = 800
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
                       "gray": (152, 152, 152)}
        self.text_color = self.colors["red"]
        self.bg_color = self.colors["turquoise blue"]
        self.tile_color = self.bg_color
        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Pipi Controlling Interface")
        self.font = pygame.font.Font("assets\\fonts\Cutie Patootie Skinny.ttf", self.font_size)
        self.font_bold = pygame.font.Font("assets\\fonts\Cutie Patootie.ttf", self.font_size)
        self.typing_tag = False
        self.prompt = Prompt((self.window_width/2-27, self.window_height/2-57), self)
        self.pos_pad_modify_command = {
            0: (90, 340),
            2: (90, 390),
            8: (90, 290),
            4: (40, 340),
            6: (140, 340)
        }
        self.pos_pad_modify_indication = {
            0: "",
            2: "moving backward",
            8: "moving forward",
            4: "moving to the left",
            6: "moving to the right"
        }
        self.pos_pad_indication = ""  # Default indication for the position of game pad
        self.pos_pad = (90, 340)  # Default position for the game pad

    def make_text(self, text, color, bg_color, center):
        """
        Make a text object for drawing
        """
        text_surf = self.font.render(text, True, color, bg_color)
        text_rect = text_surf.get_rect()
        text_rect.center = center
        return text_surf, text_rect

    def set_typing_tag(self, val):
        """
        Decide whether you want to type or not.
        """
        self.typing_tag = val

    def modify_pos_pad(self, command):
        """
        Modify the position of the pad according to movement.
        :return:
        """
        self.pos_pad_indication = self.pos_pad_modify_indication[command]
        self.pos_pad = self.pos_pad_modify_command[command]

    def draw(self, state):
        """
        Draw the scene.
        """
        self.display_surface.fill(self.bg_color)
        if state == "welcome":
            start_point = 160
            self.setting = Button('Settings', self.text_color, self.tile_color,
                                  (self.window_width/2, start_point+120), self)
            self.new = Button('New Season', self.text_color, self.tile_color,
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
            sys.stdin = open("instruction.txt")
            for i in range(9):
                instructions = sys.stdin.readline().strip()
                self.instructions_sur, self.instructions_rect = self.make_text(instructions, self.colors["black"],
                                                                               self.tile_color,
                                                                               (self.window_width/2,
                                                                                self.window_height/2-120+i*35))
                self.display_surface.blit(self.instructions_sur, self.instructions_rect)
            self.back = Button("Back", self.text_color, self.tile_color,
                               (self.window_width-60, self.window_height/8), self)
            self.buttons = [self.back]
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])

        elif state == "author":
            sys.stdin = open("author.txt")
            for i in range(8):
                if i == 0:
                    instructions = sys.stdin.readline().strip()
                    self.instructions_sur, self.instructions_rect = self.make_text(instructions, self.colors["green"],
                                                                                   self.tile_color,
                                                                                   (self.window_width/2,
                                                                                    self.window_height/2-180+i*35))
                    self.display_surface.blit(self.instructions_sur, self.instructions_rect)
                else:
                    instructions = sys.stdin.readline().strip()
                    self.instructions_sur, self.instructions_rect = self.make_text(instructions, self.colors["black"],
                                                                                   self.tile_color,
                                                                                   (self.window_width/2,
                                                                                    self.window_height/2-120+i*35))
                    self.display_surface.blit(self.instructions_sur, self.instructions_rect)
            self.back = Button("Back", self.text_color, self.tile_color, (self.window_width-60, self.window_height/8), self)
            self.buttons = [self.back]
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])

        elif state == "new season":
            self.back = Button("Back", self.text_color, self.tile_color, (self.window_width-60, self.window_height/8), self)
            indi_sur, indi_rect = self.make_text(self.pos_pad_indication, self.text_color, self.tile_color,
                                                 (self.window_width/2, self.window_height/2))
            self.buttons = [self.back]
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])
            self.display_surface.blit(indi_sur, indi_rect)
            pygame.draw.circle(self.display_surface, self.colors["white"], (90, 340), 50, 6)
            pygame.draw.circle(self.display_surface, self.colors["gray"], self.pos_pad, 30, 30)

        elif state == "setting":
            self.prompt_rect = pygame.Rect(self.window_width/2-30, self.window_height/2-60, 60, 50)
            pygame.draw.rect(self.display_surface, self.colors["white"], self.prompt_rect)
            self.guide_sur, self.guide_rect = self.make_text("Specify your Bluetooth COM port below:",
                                                             self.colors["green"], self.tile_color,
                                                             (self.window_width/2, self.window_height/4))
            self.save = Button("Save", self.text_color, self.tile_color, (self.window_width/2+90, self.window_height//2-45), self)
            self.back = Button("Back", self.text_color, self.tile_color, (self.window_width-60, self.window_height/8), self)
            self.buttons = [self.back, self.save]
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])
            self.display_surface.blit(self.save.get_sr()[0], self.save.get_sr()[1])
            self.display_surface.blit(self.guide_sur, self.guide_rect)
            if self.typing_tag:
                pygame.draw.line(self.display_surface, self.colors["black"],
                                 (self.window_width/2-27, self.window_height/2-57),
                                 (self.window_width/2-27, self.window_height/2-33), 2)
            self.display_surface.blit(self.prompt.output()[1], self.prompt.output()[2])

        elif state == "error":
            sys.stdin = open("error_help.txt")
            for i in range(9):
                instructions = sys.stdin.readline().strip()
                self.instructions_sur, self.instructions_rect = self.make_text(instructions, self.colors["black"],
                                                                               self.tile_color,
                                                                               (self.window_width/2,
                                                                                self.window_height/2-120+i*35))
                self.display_surface.blit(self.instructions_sur, self.instructions_rect)
            self.back = Button("Back", self.text_color, self.tile_color,
                               (self.window_width-60, self.window_height/8), self)
            self.buttons = [self.back]
            self.display_surface.blit(self.back.get_sr()[0], self.back.get_sr()[1])


class Button:
    def __init__(self, text, color, bg_color, center, _game_gui):
        self.gui = _game_gui
        self.text = text
        self.center = center
        self.color = color
        self.bg_color = bg_color
        self.bold = False
        self.font = self.gui.font
        self.font_bold = self.gui.font_bold
        self.surf = self.font.render(text, True, color, bg_color)
        self.rect = self.surf.get_rect()
        self.rect.center = self.center

    def make_text(self):
        """
        Make a text object for drawing
        """
        if not self.bold:
            text_surf = self.font.render(self.text, True, self.color, self.bg_color)
        else:
            text_surf = self.font_bold.render(self.text, True, self.color, self.bg_color)
        text_rect = text_surf.get_rect()
        text_rect.center = self.center
        return text_surf, text_rect

    def get_rect(self):
        return self.rect

    def get_sr(self):
        return self.surf, self.rect

    def update_sr(self):
        self.surf, self.rect = self.make_text()

    def set_bold(self, pos):
        """
        Highlight the button when the user hovers mouse over
        """
        if self.rect.collidepoint(pos):
            self.bold = True
            self.update_sr()
            self.gui.display_surface.blit(self.surf, self.rect)


class Prompt:
    def __init__(self, topleft, _gui):
        self.string = ""
        self.color = _gui.text_color
        self.bg_color = _gui.colors["white"]
        self.topleft = topleft
        self.font = _gui.font

    def make_text(self):
        """
        Make a text object for drawing
        """
        text_surf = self.font.render(self.string, True, self.color, self.bg_color)
        text_rect = text_surf.get_rect()
        text_rect.topleft = self.topleft
        return text_surf, text_rect

    def take_char(self, char):
        """
        Take in character or delete previous one.
        :return:
        """
        if char != "del":
            if len(self.string) <= 3:
                self.string += char
        else:
            self.string = self.string[:-1]

    def output(self):
        """
        Output the string
        :return:
        """
        sur, rect = self.make_text()
        return self.string, sur, rect

    def reset(self):
        """
        Reset the prompt
        :return:
        """
        self.string = ""