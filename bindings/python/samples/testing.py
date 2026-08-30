
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import requests
import lxml
import html5lib 
import schedule 
from bs4 import BeautifulSoup as bs
from samplebase import SampleBase
from PIL import Image
from datetime import datetime
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import os
import datetime
from underground import metadata, SubwayFeed

API_KEY = "iKqxWDIi073zUxPKfjiD54lPzAPVa7ra1NLURGJH"
ROUTE = 'L'


class RunText(SampleBase):
	def __init__(self, *args, **kwargs):
		super(RunText, self).__init__(*args, **kwargs)
		self.parser.add_argument("-i1", "--LTrain", help="The image to display", default="ltrain.png")

	def run(self):
		if not 'LTrain' in self.__dict__:
			self.LTrain = Image.open(self.args.LTrain).convert('RGB')

		double_buffer = self.matrix.CreateFrameCanvas()
		img_width, img_height = self.Clear.size
		base_color = graphics.Color(255, 230, 196)
        while True:            
			offscreen_canvas = self.matrix.CreateFrameCanvas()
			font = graphics.Font()
			font.LoadFont("../../../fonts/5x8.bdf")
			pos = offscreen_canvas.width

			#sets timer and sleeptime
			timer = 0
			sleeper = 20

			while True:
				
				now = datetime.now()
				current_time = now.strftime("%-I:%M")
				am_pm = now.strftime("%p")
				current_time1 = float(now.strftime("%H"))
				currentTimeLen = len(str(current_time))
				currentTimePosition = 49 - ((currentTimeLen * 5) -3)
                
				
				if timer >= 600:
					break

					while True:
						
                        feed = SubwayFeed.get(ROUTE, api_key=API_KEY)
                        feed = feed.extract_stop_dict()
                        for (key, value) in feed.items():
                            # Check if key is even then add pair to new dictionary
                            if key == 'L':
                                for (key, value) in value.items():
                                    if key == 'L12N': 
                                        # L12N is the manhattan bound grand st stop (L11N would be graham) 
                                        Manhattan_bound = value
                                    elif key == 'L12S':
                                       # L12S is the brooklyn bound grand st stop (L11S would be graham) 
                                        Brooklyn_bound = value
                        def format_subway_times(n):
                            return n.strftime('%I:%M%p')
                        formatted_manhattan_bound = list(map(format_subway_times, Manhattan_bound))
                        formatted_bk_bound = list(map(format_subway_times, Brooklyn_bound))
                        offscreen_canvas.Clear()
                        offscreen_canvas.SetImage(self.LTrain, 0, 0)
                        offscreen_canvas.SetImage(self.LTrain, 0, 17)
                        line1 = graphics.DrawLine(offscreen_canvas, 18,16,62,16, base_color)
                        temp2 = graphics.DrawText(offscreen_canvas, font, 23, 3, base_color, formatted_manhattan_bound[0])
						temp3 = graphics.DrawText(offscreen_canvas, font, 23, 19, base_color, formatted_manhattan_bound[1])
            			time.sleep(sleeper)
						timer = timer + sleeper            
						offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
						break
