#입력되는 문자열을 원하는 언어로 번역

#구글 api사용 선언 밑 os 라이브러리 불러오기
from google.cloud import translate
import os

#api 사용을 위한 Key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/kkesu/Desktop/Project_Py/tanslateWithGoogle/key.json"
trans_client = translate.Client()

#텍스트 입력받고 원하는 목적언어 입력받기
text = input("Type your textline\n")
tarLang = input("Input your target language Accoridng to ISO 629-1 codes\n")

#번역 결과 저장
answer = trans_client.translate(text, target_language = tarLang)

#출력
print('Input txt: \n', text)
print('Translation: \n{}'.format(answer['translatedText']))