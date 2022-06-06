from django.db import connection
from .serializer import *
import tensorflow as tf
import numpy as np
import unicodedata
def SelectView(request):
    try:
        cursor = connection.cursor()
        strSql = r"SELECT content FROM app_matchimage where title='{}'".format(request)
        result = cursor.execute(strSql)
        content = cursor.fetchall()
        connection.commit()
        connection.close()

    except Exception as e:
        connection.rollback()
        return e

    return content

class Model:

    def __init__(self):
        self.class_names = ['오짬', '신라면', '오뚜기참깨라면(컵)', '컵누들매콤', '풀무원백면4개입', '정면', '새우탕면', '진라면 매운맛', '열라면', '컵누들우동', '짜파게티 큰사발', '우동', '삼양)치즈불닭볶음면큰컵', '오뚜기진라면순한맛', '농심생생우동봉지', '농심안성탕면', '팔도왕뚜껑', '피피이씨음성생면 홍면', '농심 신라면큰사발면', '피피이씨 직화짜장', '피피이씨 생면식감순한맛', '농심 신라면블랙', '오뚜기크림진짬뽕', '오뚜기부대찌개라면', '농심)사리곰탕컵', '농심짜왕큰사발면', '팔도비빔면컵', '키다리식품세이면잔치국수', '농심사리곰탕큰사발', '오뚜기 쇠고기미역국라면', '멸치맛쌀국수', '농심새우탕큰사발', '오뚜기 컵누들베트남쌀국수컵', '농심짜파게티범벅', '농심 앵그리 짜파구리큰사발', '오뚜기육개장용기면', '농심튀김우동컵', '농심사천짜파게티', '팔도비빔면', '농심시원한메밀소바', '농심튀김우동컵', '농심 감자면', '농심 무파마큰사발', '농심 육개장 큰사발', '오뚜기 참깨라면 용기', '농심 오징어짬뽕큰사발', '오뚜기진짬뽕(큰컵)', '삼양 까르보불닭볶음면(낱개)', '농심김치큰사발면', '농심쌀국수']
        self.model = tf.keras.models.load_model(r'D:\nullwehang\djreact\mypj\app\try-45.ckpt')
        
    def predict_img(self,img):
        img = img.resize((256,256))

        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array,0)
        
        predictions = self.model.predict(img_array[:,:,:,:3])
        
        score = tf.nn.softmax(predictions[0])
        
        prediction, acc = self.class_names[np.argmax(score)],100*np.max(score)
        prediction = unicodedata.normalize('NFC',prediction)
        print(prediction)
        return prediction,acc
