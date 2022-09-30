#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2015 Hamilton Kibbe <ham@hamiltonkib.be>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

"""
This example demonstrates the use of pcb-tools with cairo to render a composite
image from a set of gerber files. Each layer is loaded and drawn using a
GerberCairoContext. The color and opacity of each layer can be set individually.
Once all thedesired layers are drawn on the context, the context is written to
a .png file.
"""

from curses.textpad import rectangle
from operator import invert
import os
from gerber import load_layer
from gerber.render import RenderSettings, theme
from gerber.render.cairo_backend import GerberCairoContext

import numpy as np
import cv2
from screeninfo import get_monitors


GERBER_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'examples/gerbers'))

screen_id = 2

screen = get_monitors()[0]
print(screen)
width_screen, height_screen = screen.width, screen.height



# Open the gerber files
copper = load_layer(os.path.join(GERBER_FOLDER, 'copper.GTL'))
#mask = load_layer(os.path.join(GERBER_FOLDER, 'soldermask.GTS'))
#silk = load_layer(os.path.join(GERBER_FOLDER, 'silkscreen.GTO'))
#drill = load_layer(os.path.join(GERBER_FOLDER, 'ncdrill.DRD'))

# Create a new drawing context
ctx = GerberCairoContext(scale=300)

width_screen_inch = width_screen/300
height_screen_inch = height_screen/300

shift_x, shift_y = 100/300, 100/300

height_pic = copper.bounds[1][1]
width_pic = copper.bounds[0][1]

print('widthpic = {}'.format(width_pic))
print('heightpic = {}'.format(height_pic))

width_delta = (width_screen_inch-width_pic)/2
height_delta = (height_screen_inch-height_pic)/2

display_bounds = [[0,0],[0,0]]

display_bounds[0][0] = (-width_delta + shift_x)
display_bounds[1][0] = (-height_delta + shift_y)
display_bounds[0][1] = (width_pic+width_delta + shift_x)
display_bounds[1][1] = (height_pic+height_delta + shift_y)

print('dispaly bounds = {}'.format(display_bounds))

white_settings = RenderSettings(color=theme.COLORS['white'], alpha=1)
black_settings = RenderSettings(color=theme.COLORS['black'], alpha=1)
# Draw the copper layer. render_layer() uses the default color scheme for the
# layer, based on the layer type. Copper layers are rendered as
ctx.render_layer(copper, settings=white_settings, bgsettings=black_settings, bounds=display_bounds)
#ctx.render_layer(copper, settings=white_settings, bgsettings=black_settings)

# Draw the soldermask layer
#ctx.render_layer(mask)


# The default style can be overridden by passing a RenderSettings instance to
# render_layer().
# First, create a settings object:


# Draw the silkscreen layer, and specify the rendering settings to use
#ctx.render_layer(silk, settings=our_settings)

# Draw the drill layer
#ctx.render_layer(drill)


# Write output to png file
ctx.dump(os.path.join(os.path.dirname(__file__), 'to_display.png'))

exposure_layer = cv2.imread('to_display.png')

image = np.ones((height_screen, width_screen, 3), dtype=np.float32)
image[:height_screen, :width_screen] = 0  # black at top-left corner

window_name = 'PCB_Printer'
cv2.destroyAllWindows()
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.imshow(window_name, exposure_layer)
cv2.waitKey(0)
cv2.destroyAllWindows()