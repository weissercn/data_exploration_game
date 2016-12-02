from __future__ import print_function
import matplotlib
matplotlib.use("Agg")
import numpy as np
import pandas as pd 
import matplotlib.backends.backend_agg as agg
import matplotlib.pylab as plt
import pygame
import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

black = (0,0,0)
white = (255,255,255)

def button(screen,msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)


def askbutton(screen,msg,x,y,w,h,ic,ac):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1:
            command_str= ask(screen,msg,x,y,w,h,ic,ac)
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

def text_objects(text,font):
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, msg, x,y,w,h, ic,ac):
	"Print a message in a box in the middle of the screen"
	fontobject = pygame.font.Font(None,18)
	pygame.draw.rect(screen, ac,(x,y,w,h))
	if len(msg) != 0:
		smallText = pygame.font.SysFont("comicsansms",20)
		textSurf, textRect = text_objects(msg, smallText)
		textRect.center = ( (x+(w/2)), (y+(h/2)) )
		screen.blit(textSurf, textRect)
	pygame.display.flip()

def ask(screen, question,x,y,w,h, ic,ac):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  display_box(screen, question + ": " + string.join(current_string,""), x,y,w,h,ic,ac)
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey <= 127:
      current_string.append(chr(inkey))
    display_box(screen, question + ": " + string.join(current_string,""), x,y,w,h,ic,ac)
  return string.join(current_string,"")

class session:
	def __init__(self,df):
		self.df = df
		self.df_min = df.min(axis=0)
		self.df_max = df.max(axis=0)	
	def set_all(self,name_a, name_b, range_a, range_b, mode):
		self.name_a, self.name_b, self.range_a, self.range_b, self.mode = name_a, name_b, range_a, range_b, mode

	def make_plot(self):

		fig = plt.figure(figsize=[4, 4], # Inches
				   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
				   )
		ax = fig.gca()
		ax.plot(np.random.randn(5))
		
		#if self.mode == "scatter":
		#	ax.scatter(

		ax.set_xlabel(self.name_a)
		ax.set_ylabel(self.name_b)

		self.fig = fig

        def savefig(self):
                self.fig.savefig("{}_{}_{}_{}_{}_{}_{}.png".format(self.mode,self.name_a, self.range_a[0], self.range_a[1],self.name_b, self.range_b[0], self.range_b[1]))

	def pygame_update(self): 
                canvas = agg.FigureCanvasAgg(self.fig)
                canvas.draw()
                renderer = canvas.get_renderer()
                raw_data = renderer.tostring_rgb()
		 
		size = canvas.get_width_height()
		surf = pygame.image.fromstring(raw_data, size, "RGB")
		self.screen.blit(surf, (0,0))
		#self.screen.blit(surf, (400,0))
		pygame.display.flip()

	def ask(self):
	  screen = self.screen
	  question = "Task"
	  "ask(screen, question) -> answer"
	  pygame.font.init()
	  current_string = []
	  display_box(screen, question + ": " + string.join(current_string,""))
	  while 1:
	    inkey = get_key()
	    if inkey == K_BACKSPACE:
	      current_string = current_string[0:-1]
	    elif inkey == K_RETURN:
	      break
	    elif inkey <= 127:
	      current_string.append(chr(inkey))
	    display_box(screen, question + ": " + string.join(current_string,""))
	  return string.join(current_string,"")

	def run_old(self):
                pygame.init()
                self.clock = pygame.time.Clock()
                window = pygame.display.set_mode((800, 400), DOUBLEBUF)
                self.screen = pygame.display.get_surface()
                self.make_plot()
                self.pygame_update()
                while True:
                        for event in pygame.event.get():
                                #print(event)
                                if event.type == pygame.QUIT:
                                        pygame.quit()
                                        quit()
                        button(self.screen,"Save",500,100,100,50,green,bright_green,self.savefig)
                        pygame.display.flip()
                        #self.clock.tick(3)
                        pass 
	def run(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		window = pygame.display.set_mode((800, 400), DOUBLEBUF)
                self.screen = pygame.display.get_surface()
		self.make_plot()	
		self.pygame_update()
		while True:
			for event in pygame.event.get():
				#print(event)
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
			
			#command_str =ask(self.screen, "Name")
			#print("command_str : ",command_str)
			#button(self.screen,"",500,200,100,50,green,bright_green,self.ask)
			askbutton(self.screen,"Task",500,200,200,50,green,bright_green)
			button(self.screen,"Save",500,100,100,50,green,bright_green,self.savefig)
			pygame.display.flip()
			#self.clock.tick(3)
			pass

	



df = pd.read_csv('gaussian_same_projection_on_each_axis_4D_10000_0.0_0.95_0.95_optimisation_0_named.txt' )
name_a = "a"
name_b = "b"
range_a = [0.0,1.0]
range_b = [0.0,1.0]

#mode = "scatter"
mode = "2Dhist"

s =session(df)
s.set_all(name_a, name_b, range_a, range_b, mode)
s.run()


