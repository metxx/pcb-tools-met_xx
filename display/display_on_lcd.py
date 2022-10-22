import cv2
from screeninfo import get_monitors

screen = get_monitors()[0]
window_name = 'PCB_Printer'
    

def calculate_bounds(layer, display_scale):

    print(screen)
    width_screen, height_screen = screen.width, screen.height

    width_screen_inch = width_screen/display_scale
    height_screen_inch = height_screen/display_scale

    height_pic = layer.bounds[1][1]
    width_pic = layer.bounds[0][1]

    width_delta = (width_screen_inch-width_pic)/2
    height_delta = (height_screen_inch-height_pic)/2

    display_bounds = [[0,0],[0,0]]

    display_bounds[0][0] = (-width_delta)
    display_bounds[1][0] = (-height_delta)
    display_bounds[0][1] = (width_pic+width_delta)
    display_bounds[1][1] = (height_pic+height_delta)

    return display_bounds

def show_on_LCD(time):
    print('in show_on_lcd function')
    exposure_layer = cv2.imread('./to_display.png')
    print('im read succesfull')
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    print('named window succesfull')
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    print('move window succesfull')
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    print('set window property')
    cv2.imshow(window_name, exposure_layer)
    print('imshow succesfull')
    cv2.waitKey(time)
    cv2.destroyAllWindows()
    print('destroyed all windows')
    return

def hide_on_LCD():
    cv2.destroyAllWindows()
    cv2.waitKey(200)
    print('destroyed all windows')
    return

def move_xy(bounds, move_x, move_y):

    bounds[0][0] = (bounds[0][0] + move_x)
    bounds[1][0] = (bounds[1][0] + move_y)
    bounds[0][1] = (bounds[0][1] + move_x)
    bounds[1][1] = (bounds[1][1] + move_y)

    return bounds