from crypt import methods
import os

from cairo import Content
from numpy import True_
from gerber import load_layer
from gerber.render import RenderSettings, theme
from gerber.render.cairo_backend import GerberCairoContext
from display import display_on_lcd

# Scale corespond to number of pixels per inch - display property 
display_scale = 300

#positive or negative photoresist
positive_photoresist = False

GERBER_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'examples/gerbers'))

# Open the gerber files

loaded_layer = load_layer(os.path.join(GERBER_FOLDER, 'copper.GTL'))

# Create a new drawing context
ctx = GerberCairoContext(scale = display_scale)

display_bounds = display_on_lcd.calculate_bounds(loaded_layer, display_scale = display_scale)

white_settings = RenderSettings(color=theme.COLORS['white'], alpha=1)
black_settings = RenderSettings(color=theme.COLORS['black'], alpha=1)

if(False):
    display_on_lcd.move_xy(display_bounds, -2, 1.2)

def render():
    if(positive_photoresist):
        ctx.render_layer(loaded_layer, settings=white_settings, bgsettings=black_settings, bounds=display_bounds)
    else:
        ctx.render_layer(loaded_layer, settings=black_settings, bgsettings=white_settings, bounds=display_bounds)

    ctx.dump(os.path.join(os.path.dirname(__file__), 'to_display.png'))

    return

display_on_lcd.show_on_LCD()

