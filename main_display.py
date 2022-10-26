#to run this with api: uvicorn main_display:app --reload

#to display api docs go to: http://127.0.0.1:8000/docs#/

from distutils import dir_util
from itertools import count
from multiprocessing.sharedctypes import Value
import os
import shutil
from xml.etree.ElementTree import tostring
import zipfile

from gerber import load_layer
from gerber.render import RenderSettings, theme
from gerber.render.cairo_backend import GerberCairoContext
from display import display_on_lcd
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

# Scale corespond to number of pixels per inch - display property 
display_scale = 300

#positive or negative photoresist
positive_photoresist = True

GERBER_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'examples/gerbers'))

TMP_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp'))

# Open the gerber files

loaded_layer = load_layer(os.path.join(GERBER_FOLDER, 'copper.GTL'))

def load_layer_from_file(file_name):

    global loaded_layer

    loaded_layer = load_layer(os.path.join(TMP_FOLDER, file_name))

    return

# Create a new drawing context
ctx = GerberCairoContext(scale = display_scale)

def render(render_bounds, invert, mirror):

    white_settings = RenderSettings(color=theme.COLORS['white'], alpha=1, invert= invert, mirror=mirror)
    black_settings = RenderSettings(color=theme.COLORS['black'], alpha=1, invert= invert, mirror=mirror)

    ctx.render_layer(loaded_layer, settings=black_settings, bgsettings=white_settings, bounds=render_bounds)

    ctx.dump(os.path.join(os.path.dirname(__file__), 'to_display.png'))

    return

#Input model for show function
class Show_properties (BaseModel):
    move_x: float
    move_y: float
    positive: bool
    mirror: bool
    exp_time: int
    pwm:int
    file_name:str

class Render_properties (BaseModel):
    move_x: float
    move_y: float
    positive: bool
    mirror: bool
    file_name:str

#input model dor files
class Options (BaseModel):
    FileName: str
    FileDesc: str = 'Upload for demonstration'
    #FileType: Optional[str]

@app.post("/destroy")
async def destroy():
    display_on_lcd.hide_on_LCD()
    return 'window destroyed'

@app.get("/serve_layer_for_preview")
async def return_image():
    return FileResponse("to_display.png")

@app.get("/files_on_server")
async def return_file_names():
        dir_list = os.listdir("./tmp/")
        json_dict = {"responseObj":[{"Key": dir_list.index(value),"Value": value} for value in dir_list]}
        print(json_dict)
        return(json_dict)

@app.post("/print")
async def get_data(request: Request, options: Show_properties):
    result = await request.json()

    move_x = float(result['move_x'])
    move_y = float(result['move_y'])
    positive = bool(result['positive'])
    mirror = bool(result['mirror'])
    exp_time = int(result['exp_time'])
    pwm = int(result['pwm'])
    file_name = result['file_name']

    ctx.clear()
    load_layer_from_file(file_name)
    display_bounds = display_on_lcd.calculate_bounds(loaded_layer, display_scale = display_scale)
    render(display_on_lcd.move_xy(display_bounds, move_x, move_y), invert = positive, mirror = mirror)
    display_on_lcd.show_on_LCD(exp_time)
    return

@app.post("/render")
async def get_data(request: Request, options: Render_properties):
    result = await request.json()

    move_x = float(result['move_x'])
    move_y = float(result['move_y'])
    positive = bool(result['positive'])
    mirror = bool(result['mirror'])
    file_name = result['file_name']
    ctx.clear()
    load_layer_from_file(file_name)
    display_bounds = display_on_lcd.calculate_bounds(loaded_layer, display_scale = display_scale)
    render(display_on_lcd.move_xy(display_bounds, move_x, move_y), invert = positive, mirror = mirror)
    return

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    for f in os.listdir("./tmp/"):
        os.remove(os.path.join("./tmp/", f))
    print(file.filename)
    file_object = file.file
    upload_folder = open(os.path.join(TMP_FOLDER, file.filename), 'wb+')
    shutil.copyfileobj(file_object, upload_folder)
    upload_folder.close()
    try:
        with zipfile.ZipFile(os.path.join(TMP_FOLDER, file.filename)) as z:
            z.extractall("./tmp/")
            if os.path.exists(os.path.join(TMP_FOLDER, file.filename)):
                os.remove(os.path.join(TMP_FOLDER, file.filename))
                print('zip removed')
            print("Extracted all")
            dir_list = os.listdir("./tmp/")
            print(dir_list)
            return(dir_list)
    except:
        return {file.filename}
    
    