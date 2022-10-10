#to run this with api: uvicorn main_display:app --reload

import os

from numpy import positive

from gerber import load_layer
from gerber.render import RenderSettings, theme
from gerber.render.cairo_backend import GerberCairoContext
from display import display_on_lcd
from fastapi import FastAPI, Request, File, UploadFile, Depends
from pydantic import BaseModel

app = FastAPI()

# Scale corespond to number of pixels per inch - display property 
display_scale = 300

#positive or negative photoresist
positive_photoresist = True

GERBER_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'examples/gerbers'))

# Open the gerber files

loaded_layer = load_layer(os.path.join(GERBER_FOLDER, 'copper.GTL'))

# Create a new drawing context
ctx = GerberCairoContext(scale = display_scale)

def render(render_bounds, invert, mirror):

    white_settings = RenderSettings(color=theme.COLORS['white'], alpha=1, invert= invert, mirror=mirror)
    black_settings = RenderSettings(color=theme.COLORS['black'], alpha=1, invert= invert, mirror=mirror)

    ctx.render_layer(loaded_layer, settings=black_settings, bgsettings=white_settings, bounds=render_bounds)

    ctx.dump(os.path.join(os.path.dirname(__file__), 'to_display.png'))

    return

#Base model
class Show_properties (BaseModel):
    move_x: float
    move_y: float
    positive: bool
    mirror: bool


@app.post("/destroy")
async def destroy():
    display_on_lcd.hide_on_LCD()
    if os.path.exists("to_display.png"):
        os.remove("to_display.png")
        print('file removed')
    return 'window destroyed'

@app.post("/show")
async def get_data(request: Request, options: Show_properties):
    result = await request.json()

    move_x = result['move_x']
    move_y = result['move_y']
    positive = bool(result['positive'])
    mirror = bool(result['mirror'])

    #nevim jestli tady bude muset byt
    if(mirror):
        move_x = move_x * (-1)

    ctx.clear()
    display_bounds = display_on_lcd.calculate_bounds(loaded_layer, display_scale = display_scale)
    render(display_on_lcd.move_xy(display_bounds, move_x, move_y), invert = positive, mirror = mirror)
    display_on_lcd.show_on_LCD()
    return result