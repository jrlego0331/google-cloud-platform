#라이브러리 import
from google.cloud import vision
from google.cloud.vision import types
import os
from PIL import Image, ImageDraw
import io
import cv2

#GCP Settings
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "WithGoogle/key.json"
googleClient = vision.ImageAnnotatorClient()

#Open CV Settings
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    #image reading and displaying
    ret, crntIMG = capture.read()

    #image saving
    filename = 'WithGoogle/Camstuff/textRecognition.png'
    cv2.imwrite(filename, crntIMG)
    with io.open(filename, 'rb') as tt:
        content = tt.read()

    #send to GCP and save result
    image = types.Image(content=content)
    check = googleClient.text_detection(image=image)
    Result = check.text_annotations

    for num in Result:
        vertices = (['({},{})'.format(vertex.x, vertex.y) for vertex in num.bounding_poly.vertices])
        print('\nRecognized: {}'.format(num.description) )

    #view result
    squres = []
    the = Image.open(filename)
    for num in Result:
        squres.append(num.bounding_poly)
    draw = ImageDraw.Draw(the)

    for lines in squres:
        draw.polygon([lines.vertices[0].x, lines.vertices[0].y, lines.vertices[1].x, lines.vertices[1].y, lines.vertices[2].x, lines.vertices[2].y, lines.vertices[3].x, lines.vertices[3].y], None, 'red')
    the.save(filename)

    final = cv2.imread(filename)
    cv2.imshow("Facial Recognition", final)


    #exit
    if cv2.waitKey(1) > 0: break


capture.release()
cv2.destroyAllWindows()