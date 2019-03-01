#라이브러리 import
import google.cloud.vision
import os
import io
import cv2

#GCP Settings
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "WithGoogle/key.json"
googleClient = google.cloud.vision.ImageAnnotatorClient()

#Open CV Settings
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    #image reading and displaying
    ret, crntIMG = capture.read()

    #image saving
    filename = 'WithGoogle/Camstuff/imgLabeling.png'
    cv2.imwrite(filename, crntIMG)
    with io.open(filename, 'rb') as tt:
        content = tt.read()

    #send to GCP and save result
    image = google.cloud.vision.types.Image(content=content)
    Result = googleClient.label_detection(image=image)
    

    #receiving boundaries and determind color
    for labels in Result.label_annotations:
        print('\nLable: ', labels.description, '\nPercentage: ', labels.score)

    cv2.imshow("Imange Labling", crntIMG)

    #exit
    if cv2.waitKey(1) > 0: break


capture.release()
cv2.destroyAllWindows()