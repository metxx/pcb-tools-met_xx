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
from display import display_on_lcd, show_on_LCD

GERBER_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'examples/gerbers'))

# Open the gerber files
copper = load_layer(os.path.join(GERBER_FOLDER, 'copper.GTL'))
#mask = load_layer(os.path.join(GERBER_FOLDER, 'soldermask.GTS'))
#silk = load_layer(os.path.join(GERBER_FOLDER, 'silkscreen.GTO'))
#drill = load_layer(os.path.join(GERBER_FOLDER, 'ncdrill.DRD'))

# Create a new drawing context
ctx = GerberCairoContext(scale=300)

display_bounds = display_on_lcd.calculate_bounds(copper)


white_settings = RenderSettings(color=theme.COLORS['white'], alpha=1)
black_settings = RenderSettings(color=theme.COLORS['black'], alpha=1)

# Draw the copper layer. render_layer() uses the default color scheme for the
# layer, based on the layer type. Copper layers are rendered as
ctx.render_layer(copper, settings=white_settings, bgsettings=black_settings, bounds=display_bounds)

# Write output to png file
ctx.dump(os.path.join(os.path.dirname(__file__), 'to_display.png'))

show_on_LCD()