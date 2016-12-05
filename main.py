from __future__ import print_function
import matplotlib as mpl
from matplotlib.colors import LogNorm
mpl.use("Agg")
import numpy as np
import pandas as pd 
import matplotlib.backends.backend_agg as agg
import matplotlib.pylab as plt
import pygame
import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

#mpl.rc('font', family='serif', size=28, serif="Times New Roman")



red = (200,0,0)
green = (0,200,0)
green = (0,0,220)

bright_red = (255,0,0)
bright_green = (0,255,0)
bright_green = (0,0,255)

black = (0,0,0)
white = (255,255,255)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

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


def askbutton(s,screen,msg,x,y,w,h,ic,ac):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1:
        	command_str= ask(screen,msg,x,y,w,h,ic,ac)
		command_list = command_str.split(" ")
		acceptable_command = False
		#if len(command_list)==4 and (command_list[0]=="x" or command_list[0]=="y") and (command_list[1] in s.df.columns.values.tolist()) and is_number(command_list[2]) and is_number(command_list[3]) :
		if command_list[0]=="x" and  len(command_list)==4:
			if (command_list[1] in s.df.columns.values.tolist() and is_number(command_list[2]) and is_number(command_list[3])):   
				s.set_x(command_list[1],[float(command_list[2]),float(command_list[3])] )	 
				print("s.range_x : ", s.range_x)
				acceptable_command = True
                if command_list[0]=="y"and  len(command_list)==4:
			if (command_list[1] in s.df.columns.values.tolist() and is_number(command_list[2]) and is_number(command_list[3])):
                                s.set_y(command_list[1],[float(command_list[2]),float(command_list[3])] )	
				acceptable_command = True
		if command_list[0]=="z"and  len(command_list)==3:
			if (command_list[1] in s.df.columns.values.tolist() and is_number(command_list[2])):
				s.set_z(command_list[1], command_list[2])
				acceptable_command = True

		if acceptable_command:
			s.make_plot()
			s.pygame_update()
		else:
			smallText = pygame.font.SysFont("comicsansms",20) 
			textSurf, textRect = text_objects("Unrecognised command", smallText)
			textRect.topleft = (500,275)
			s.screen.blit(textSurf, textRect)
			print("Unrecognised command")
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

def text_objects(text,font):
	textSurface = font.render(text, True, white)
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
	def set_2D(self,name_x, name_y, range_x, range_y):
		self.name_x, self.name_y, self.range_x, self.range_y = name_x, name_y, range_x, range_y
	def set_3D(self,name_x, name_y, name_z, range_x, range_y, value_z):
		self.name_x, self.name_y, self.name_z, self.range_x, self.range_y, self.value_z = name_x, name_y, name_z, range_x, range_y, value_z
	def set_x(self, name_x, range_x):
		#print("set_x")
		self.name_x, self.range_x = name_x, range_x
		#print(" name_x, range_x : ", name_x, range_x)
        def set_y(self, name_y, range_y):
                #print("set_y") 
		self.name_y, self.range_y = name_y, range_y
	def set_z(self, name_z, range_z):
		self.name_z, self.range_z = name_z, range_z

	def set_mode(self,mode): self.mode = mode

	def make_plot(self):

		fig = plt.figure(figsize=[4, 4], # Inches
				   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
				   )
		ax = fig.gca()
		
		if self.mode == "test":
			ax.plot(np.random.randn(5))

		elif self.mode == "2Dhist":
			cax = ax.hist2d(df[self.name_x],df[self.name_y],norm=LogNorm())
			fig.colorbar(cax[3]) 			
		
		elif self.mode == "scatter":
			df1 = self.df[[self.name_x, self.name_y, self.name_z]]

			if self.value_z >0: 
				#df2 = df1.loc[df1[self.name_z] > self.value_z].sort_values(by=self.name_z,ascending=0)
				df2 = df1.loc[df1[self.name_z] > self.value_z].reindex(np.random.permutation(df1.index))
				df2['dist']= (df2[self.name_z] - self.value_z)
			else:               
				#df2 = df1.loc[df1[self.name_z] < -1.*self.value_z].sort_values(by=self.name_z,ascending=1)
				df2 = df1.loc[df1[self.name_z] < -1.*self.value_z].reindex(np.random.permutation(df1.index))
				df2['dist']= -(df2[self.name_z] + self.value_z)

			ax.scatter(df2[self.name_x],df2[self.name_y], c= df2['dist'], lw = 0 )



		x_min, x_max, y_min, y_max = self.df_min[self.name_x],  self.df_max[self.name_x], self.df_min[self.name_y],  self.df_max[self.name_y]
		x_lims, y_lims = [x_min+(x_max-x_min)*self.range_x[0]/100.,x_min+(x_max-x_min)*self.range_x[1]/100. ], [ y_min+(y_max-y_min)*self.range_y[0]/100.,y_min+(y_max-y_min)*self.range_y[1]/100. ]
		ax.set_xlim(x_lims)
		ax.set_ylim(y_lims)

		ax.set_xlabel(self.name_x)
		ax.set_ylabel(self.name_y)
		plt.tight_layout()
		self.fig = fig

        def savefig(self):
                self.fig.savefig("{}_{}_{}_{}_{}_{}_{}.png".format(self.mode,self.name_x, self.range_x[0], self.range_x[1],self.name_y, self.range_y[0], self.range_y[1]))

	def plot_update(self): 
                canvas = agg.FigureCanvasAgg(self.fig)
                canvas.draw()
                renderer = canvas.get_renderer()
                raw_data = renderer.tostring_rgb()
		 
		size = canvas.get_width_height()
		surf = pygame.image.fromstring(raw_data, size, "RGB")
		self.screen.blit(surf, (0,0))
		#self.screen.blit(surf, (400,0))
		pygame.display.flip()

	def dimensions_update(self):
		smallText = pygame.font.SysFont("comicsansms",20)
                textSurf, textRect = text_objects("Set like: x a 0. 100.", smallText)
                textRect.topleft = (500,25)
                self.screen.blit(textSurf, textRect)

                textSurf, textRect = text_objects(self.name_x, smallText)
                textRect.topleft = (500,125)
		self.screen.blit(textSurf, textRect)
		
		textSurf, textRect = text_objects(str(self.range_x[0])+ "%", smallText)
		textRect.topleft = (500,150)
                self.screen.blit(textSurf, textRect)

                textSurf, textRect = text_objects(str(self.range_x[1]) + "%", smallText)
                textRect.topleft = (550,150)
                self.screen.blit(textSurf, textRect)

                textSurf, textRect = text_objects(self.name_y, smallText) 
                textRect.topleft = (500,175)
                self.screen.blit(textSurf, textRect)

                textSurf, textRect = text_objects(str(self.range_y[0]) + "%", smallText)
                textRect.topleft = (500,200)
                self.screen.blit(textSurf, textRect)

                textSurf, textRect = text_objects(str(self.range_y[1]) + "%", smallText)
                textRect.topleft = (550,200)
                self.screen.blit(textSurf, textRect)
	
		if self.mode =="scatter":
			textSurf, textRect = text_objects(self.name_z, smallText)
			textRect.topleft = (500,225)
			self.screen.blit(textSurf, textRect)

			textSurf, textRect = text_objects(str(self.value_z) + "%", smallText)
			textRect.topleft = (500,250)
			self.screen.blit(textSurf, textRect)

	def pygame_update(self):
		pygame.draw.rect(self.screen, black,(0,0,800,400))
		self.plot_update()
		self.dimensions_update()

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
                self.plot_update()
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
		self.plot_update()
		while True:
			for event in pygame.event.get():
				#print(event)
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
			
			#command_str =ask(self.screen, "Name")
			#print("command_str : ",command_str)
			#button(self.screen,"",500,200,100,50,green,bright_green,self.ask)
			self.dimensions_update()
			askbutton(self,self.screen,"Task",500,75,200,50,green,bright_green)
			button(self.screen,"Save",500,325,100,50,green,bright_green,self.savefig)
			pygame.display.flip()
			#self.clock.tick(3)
			pass

	



df = pd.read_csv('gaussian_same_projection_on_each_axis_4D_10000_0.0_0.95_0.95_optimisation_0_named.txt' )
name_x = "a"
name_y = "b"
name_z = "c"
range_x = [0,50]
range_y = [0,50]
value_z = 0


#mode = "scatter"
mode = "2Dhist"

s =session(df)
#s.set_2D(name_x, name_y, range_x, range_y)
s.set_3D(name_x, name_y, name_z, range_x, range_y, value_z)
s.set_mode(mode)
s.run()


