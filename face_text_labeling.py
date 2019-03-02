#라이브러리 불러오기
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
import os
import io
import cv2

#GCP Settings
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "WithGoogle/key.json"
googleClient = vision.ImageAnnotatorClient()

#Open CV Settings
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    #image reading
    ret, crntIMG = capture.read()

    #image saving
    filename = 'WithGoogle/Camstuff/face_Text_Labeling.png'
    cv2.imwrite(filename, crntIMG)
    with io.open(filename, 'rb') as tt:
        content = tt.read()

    #send to GCP and save result
    image = types.Image(content=content)
    labelResult = googleClient.label_detection(image=image)
    txtDetect = googleClient.text_detection(image=image)
    textResult = txtDetect.text_annotations
    faceDetect = googleClient.face_detection(image=image)
    facialResult = faceDetect.face_annotations

    #receiving facial boundaries and determind color
    for num in facialResult:
        vertices = (['({},{})'.format(vertex.x, vertex.y) for vertex in num.bounding_poly.vertices])

        if num.anger_likelihood > 2:
            COL = 'red'
        if num.joy_likelihood > 2:
            COL = 'green'
        if num.surprise_likelihood > 2:
            COL = 'yellow'
        else:
            COL = 'blue'

    #drawing face line
    squres = []
    the = Image.open(filename)
    for num in facialResult:
        squres.append(num.fd_bounding_poly)
    draw = ImageDraw.Draw(the)
    for lines in squres:
        draw.polygon([lines.vertices[0].x, lines.vertices[0].y, lines.vertices[1].x, lines.vertices[1].y, lines.vertices[2].x, lines.vertices[2].y, lines.vertices[3].x, lines.vertices[3].y], None, COL)

    for num in textResult:
        vertices = (['({},{})'.format(vertex.x, vertex.y) for vertex in num.bounding_poly.vertices])
        print('\nRecognized: {}'.format(num.description) )

    #drawing txt line
    txtsqures = []
    for num in textResult:
        txtsqures.append(num.bounding_poly)
    for lines in txtsqures:
        draw.polygon([lines.vertices[0].x, lines.vertices[0].y, lines.vertices[1].x, lines.vertices[1].y, lines.vertices[2].x, lines.vertices[2].y, lines.vertices[3].x, lines.vertices[3].y], None, 'red')
    
    #file save
    the.save(filename)
    final = cv2.imread(filename)
    cv2.imshow("Facial Recognition", final)
    
    #receiving emotions to determind color
    for labels in labelResult.label_annotations:
        likeness = round(labels.score, 2) * 100
        print('\nLable: ', labels.description, '\nPercentage: ', likeness, '%')

    #exit
    if cv2.waitKey(1) > 0: break


capture.release()
cv2.destroyAllWindows()