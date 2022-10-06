from flask import Flask, request
from flask import send_from_directory
from flask import render_template

app = Flask(__name__, )

FLUTTER_WEB_APP = 'templates'

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

# @app.route('/web/display', methods = ['POST'])
# def display_to_lcd():
#     display_on_lcd.show_on_LCD()
#     print("Motif visible on display")
#     return "Motif visible on display"

#@app.route('/web/move', methods = ['POST'])
# def move_xy():
#     print(request.is_json)
#     package = request.get_json()
#     print(package['move_x'])
#     print(package['move_y'])
#     display_on_lcd.move_xy(display_bounds, move_x=float(package['move_x'])/display_scale, move_y=float(package['move_y'])/display_scale)
#     print('display on lcd move xy succesful')
#     render()
#     print('rener succesful')
#     display_on_lcd.update_on_LCD()
#     print('display on lcd show on lcd succesfull')
#     return 'Jason posted'


if __name__ == '__main__':
    app.run(debug=True)