from __future__ import print_function
import matplotlib
matplotlib.use("Agg")
import numpy as np
import pandas as pd 
import matplotlib.backends.backend_agg as agg
import matplotlib.pylab as plt
import pygame
from pygame.locals import *

class session:
	def __init__(self,df):
		self.df = df
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


 
	def run(self):
		pygame.init()
		window = pygame.display.set_mode((800, 400), DOUBLEBUF)
                self.screen = pygame.display.get_surface()
		self.make_plot()	
		self.pygame_update()
		while True:
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


