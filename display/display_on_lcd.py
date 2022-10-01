import cv2
from screeninfo import get_monitors

screen = get_monitors()[0]

def calculate_bounds(layer):

    print(screen)
    width_screen, height_screen = screen.width, screen.height

    width_screen_inch = width_screen/300
    height_screen_inch = height_screen/300


    shift_x, shift_y = 0,0

    height_pic = layer.bounds[1][1]
    width_pic = layer.bounds[0][1]

    #print('widthpic = {}'.format(width_pic))
    #print('heightpic = {}'.format(height_pic))

    width_delta = (width_screen_inch-width_pic)/2
    height_delta = (height_screen_inch-height_pic)/2

    display_bounds = [[0,0],[0,0]]

    display_bounds[0][0] = (-width_delta + shift_x)
    display_bounds[1][0] = (-height_delta + shift_y)
    display_bounds[0][1] = (width_pic+width_delta + shift_x)
    display_bounds[1][1] = (height_pic+height_delta + shift_y)

    #print('dispaly bounds = {}'.format(display_bounds))

    return display_bounds

def show_on_LCD():

    exposure_layer = cv2.imread('./to_display.png')

    window_name = 'PCB_Printer'
    cv2.destroyAllWindows()
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(window_name, exposure_layer)
    cv2.waitKey(0)
    cv2.destroyAllWindows()