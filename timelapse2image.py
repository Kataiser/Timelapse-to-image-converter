from PIL import Image
import os
import time
from math import floor
import configparser
import ast


def average_images(*arg, do_crop, crop_coords):
    input_num = len(arg)
    print("Averaging", input_num, "images")
    print("From " + arg[0] + " to " + arg[-1])

    if input_num == 1:
        return Image.open(arg[0])

    opened_images = []
    for filename in arg:
        if do_crop:
            opened_images.append(Image.open(filename).crop(crop_coords))
        else:
            opened_images.append(Image.open(filename))

    output = Image.blend(opened_images[0], opened_images[1], 0.5)

    if input_num > 2:
        for inputs in range(2, input_num):
            alpha = 1 / (inputs + 2)
            output = Image.blend(output, opened_images[inputs], alpha)

    return output

config = configparser.ConfigParser()  # load all settings
with open('crop_settings.ini', 'r') as configfile:
    config.read('crop_settings.ini')
    should_crop = ast.literal_eval(config['MAIN']['crop'])
    top_left_x = int(config['MAIN']['top_left_x'])
    top_left_y = int(config['MAIN']['top_left_y'])
    bottom_right_x = int(config['MAIN']['bottom_right_x'])
    bottom_right_y = int(config['MAIN']['bottom_right_y'])

crop = (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
if should_crop:
    width = bottom_right_x - top_left_x
    height = bottom_right_y - top_left_y
else:
    size_ref = Image.open('output/000001.png')
    width = size_ref.size[0]
    height = size_ref.size[1]

every_file = os.listdir('output')
first_file_num = int(every_file[0][0:6]) - 1
total_num = len(every_file)
already_done = len(os.listdir('compressed'))
k = already_done
since_start = 0
step = floor(total_num / width)
if step < 1:
    step = 1
overall_start_time = time.time()

for i in range(already_done * step, total_num, step):
    processing_start_time = time.time()

    k += 1
    since_start += 1
    paths = []

    if k >= width:
        print("Finished")
        break

    for j in range(1, step + 1):
        paths.append('E:\Videos\\timelapse2image\output\\' + str(first_file_num + i + j).zfill(6) + '.png')
    out = average_images(*paths, do_crop=should_crop, crop_coords=crop)
    out.save('E:\Videos\\timelapse2image\compressed\\' + str(k).zfill(6) + '.png')
    to_final = out.load()

    try:
        canvas = Image.open('final.png')
        if canvas.size[0] != width or canvas.size[1] != height:
            raise FileNotFoundError
    except FileNotFoundError:
        blank_final = Image.new('RGB', (width, height), "black")
        blank_final.save('final.png')
        canvas = Image.open('final.png')
    canvas_pix = canvas.load()

    try:
        for y in range(height):
            color = to_final[k, y]
            red = color[0]
            green = color[1]
            blue = color[2]

            canvas_pix[k, y] = (red, green, blue)
        canvas.save('final.png')
    except:
        print("Finished! (Or maybe an error happened but whatever)")

    print("Saved number " + str(k) + " (" + str(int((k / width) * 100)) + "%), "
          "took " + str(time.time() - processing_start_time)[0:3] + " seconds")
    print("Time since started:", round((time.time() - overall_start_time) / 60), "mins"
          + " (" + str(since_start) + " since start)")
    print('\n')
