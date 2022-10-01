from curses.textpad import rectangle
from operator import invert
import os
from gerber import load_layer
from gerber.render import RenderSettings, theme
from gerber.render.cairo_backend import GerberCairoContext
from display import display_on_lcd

GERBER_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'examples/gerbers'))

# Open the gerber files
copper = load_layer(os.path.join(GERBER_FOLDER, 'copper.GTL'))
mask = load_layer(os.path.join(GERBER_FOLDER, 'soldermask.GTS'))
silk = load_layer(os.path.join(GERBER_FOLDER, 'silkscreen.GTO'))
drill = load_layer(os.path.join(GERBER_FOLDER, 'ncdrill.DRD'))

# Create a new drawing context
ctx = GerberCairoContext(scale=300)

display_bounds = display_on_lcd.calculate_bounds(copper)

white_settings = RenderSettings(color=theme.COLORS['white'], alpha=1)
black_settings = RenderSettings(color=theme.COLORS['black'], alpha=1)

if(False):
    display_on_lcd.move_xy(display_bounds, 1, 1)

# Draw the copper layer. render_layer() uses the default color scheme for the
# layer, based on the layer type. Copper layers are rendered as
ctx.render_layer(copper, settings=white_settings, bgsettings=black_settings, bounds=display_bounds)

# Write output to png file
ctx.dump(os.path.join(os.path.dirname(__file__), 'to_display.png'))

display_on_lcd.show_on_LCD()