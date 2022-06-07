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
        self.class1_names = ['농심 감자면', '농심 김치면', '농심 무파마', '농심 사리곰탕', '농심 사천 짜파게티', '농심 새우탕면', '농심 생생우동', '농심 시원한 메밀소바', '농심 신라면', '농심 쌀국수']
        self.class2_names = ['농심 사리곰탕', '농심 새우탕', '농심 생생우동', '농심 신라면 블랙', '농심 안성탕면', '농심 앵그리 짜파구리', '농심 오징어짬뽕', '농심 육개장', '농심 튀김우동', '키다리식품 세이면 잔치국수']
        self.class3_names = ['농심 신라면', '농심 오징어짬뽕', '농심 짜파게티', '농심 튀김우동', '백제 멸치맛 쌀국수', '삼양 치즈 불닭볶음면', '오뚜기 부대찌개 라면', '오뚜기 쇠고기 미역국 라면', '오뚜기 열라면', '오뚜기 육개장']
        self.class4_names=['농심 짜파게티 범벅', '삼양 까르보 불닭볶음면', '오뚜기 진라면 순한맛', '오뚜기 진짬뽕', '오뚜기 참깨라면', '오뚜기 컵누들 베트남 쌀국수', '오뚜기 크림 진짬뽕', '팔도 비빔면', '팔도 왕뚜껑', '풀무원 백면']
        self.class5_names=['농심 짜왕', '오뚜기 진라면 매운맛', '오뚜기 참깨라면', '오뚜기 컵누들 매콤', '오뚜기 컵누들 우동맛', '팔도 비빔면', '풀무원 생면식감 순한맛', '풀무원 정면', '풀무원 직화짜장', '풀무원 홍면']
        self.class1_model = tf.keras.models.load_model(r'D:\nullwehang\Model\djreact\mypj\app\class1.ckpt')
        self.class2_model = tf.keras.models.load_model(r'D:\nullwehang\Model\djreact\mypj\app\class2.ckpt')
        self.class3_model = tf.keras.models.load_model(r'D:\nullwehang\Model\djreact\mypj\app\class3.ckpt')
        self.class4_model = tf.keras.models.load_model(r'D:\nullwehang\Model\djreact\mypj\app\class4.ckpt')
        self.class5_model = tf.keras.models.load_model(r'D:\nullwehang\Model\djreact\mypj\app\class5.ckpt')
        self.total_class = [self.class1_names,self.class2_names,self.class3_names,self.class4_names,self.class5_names]
        self.model_list = [self.class1_model,self.class2_model,self.class3_model,self.class4_model,self.class5_model]
        
    def predict(self,img,index):
        img = img.resize((256,256))

        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array,0)
        
        predictions = self.model_list[index].predict(img_array)
        score = tf.nn.softmax(predictions[0])

        prediction, acc = self.total_class[index][np.argmax(score)], 100 * np.max(score)
        return prediction, acc
    
    def predict_img(self,img):
        max = 0
        last_prediction = ''
        for i in range(5):
            prediction, acc = self.predict(img, i)
            if acc >= max:
                max = acc
                last_prediction = prediction
        return last_prediction,max
