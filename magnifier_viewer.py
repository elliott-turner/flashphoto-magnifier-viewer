import re
import random
import argparse
import requests
from PIL import Image
from io import BytesIO

IMAGE_WIDTH = 480
IMAGE_HEIGHT = 631
ZOOM_IMAGE_SIZE = 188
ZOOM_SQUARE_SIZE = 100
PROGRESS_BAR_LENGTH = 50

parser = argparse.ArgumentParser(description="download flashphotography magnifier image")
parser.add_argument("url", help="url of magnifier page")
parser.add_argument("-o", "--output", help="output file name")
args = parser.parse_args()

magnifier_url = args.url

O, R, F, A = re.search(r"http://magnifier.flashphotography.com/Magnify.aspx\?O=([0-9]+)&R=([0-9]+)&F=([0-9]+)&A=([0-9]+)", magnifier_url).groups()

x_coordinates = range(ZOOM_SQUARE_SIZE//2, IMAGE_WIDTH+ZOOM_SQUARE_SIZE//2, ZOOM_SQUARE_SIZE)
y_coordinates = range(ZOOM_SQUARE_SIZE//2, IMAGE_HEIGHT+ZOOM_SQUARE_SIZE//2, ZOOM_SQUARE_SIZE)
num_images = len(x_coordinates)*len(y_coordinates)

final_image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

crop_box = ((ZOOM_IMAGE_SIZE-ZOOM_SQUARE_SIZE)//2, (ZOOM_IMAGE_SIZE-ZOOM_SQUARE_SIZE)//2, (ZOOM_IMAGE_SIZE+ZOOM_SQUARE_SIZE)//2, (ZOOM_IMAGE_SIZE+ZOOM_SQUARE_SIZE)//2)
for i, x in enumerate(x_coordinates):
    for j, y in enumerate(y_coordinates):
        url = f"http://magnifier.flashphotography.com/MagnifyRender.ashx?X={x}&Y={y}&O={O}&R={R}&F={F}&A={A}&rand={random.random()}"
        response = requests.get(url)
        if response.status_code != 200: continue
        image = Image.open(BytesIO(response.content))
        left = (image.width - 100) // 2
        upper = (image.height - 100) // 2
        final_image.paste(image.crop(crop_box), (i * ZOOM_SQUARE_SIZE, j * ZOOM_SQUARE_SIZE))
        progress = (i*len(y_coordinates) + j + 1) / num_images
        print(f"\r[{'='*(int(progress*PROGRESS_BAR_LENGTH)-1)}{'>'}{' '*(PROGRESS_BAR_LENGTH-int(progress*PROGRESS_BAR_LENGTH))}] {progress*100.0:.2f}%", end="")

final_image.save("final_output.jpg" if not args.output else args.output)
