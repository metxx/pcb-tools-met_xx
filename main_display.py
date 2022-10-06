from crypt import methods
import os
import threading
import traceback

from cairo import Content
from numpy import True_
from gerber import load_layer
from gerber.render import RenderSettings, theme
from gerber.render.cairo_backend import GerberCairoContext
from display import display_on_lcd
from flask import Flask, request
from flask import send_from_directory
from flask import render_template

app = Flask(__name__, )

FLUTTER_WEB_APP = 'templates'

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

#Flask web server and API

@app.route('/')
def render_page():
    return render_template('index.html')


@app.route('/web/')
def render_page_web():
    return render_template('index.html')


@app.route('/web/<path:name>')
def return_flutter_doc(name):

    datalist = str(name).split('/')
    DIR_NAME = FLUTTER_WEB_APP

    if len(datalist) > 1:
        for i in range(0, len(datalist) - 1):
            DIR_NAME += '/' + datalist[i]

    return send_from_directory(DIR_NAME, datalist[-1])

@app.route('/web/display', methods = ['POST'])
def display_to_lcd():
    display_on_lcd.show_on_LCD()
    print("Motif visible on display")
    return "Motif visible on display"

@app.route('/web/move', methods = ['POST'])
def move_xy():
    print(request.is_json)
    package = request.get_json()
    print(package['move_x'])
    print(package['move_y'])
    display_on_lcd.move_xy(display_bounds, move_x=float(package['move_x'])/display_scale, move_y=float(package['move_y'])/display_scale)
    print('display on lcd move xy succesful')
    render()
    print('render succesful')
    try:
        display_on_lcd.update_on_LCD()
    except Exception as e:
        print(traceback.format_exc())
    print('display on lcd show on lcd succesfull')
    return 'Jason posted'


#if __name__ == '__main__':
app.run(threading=True)
