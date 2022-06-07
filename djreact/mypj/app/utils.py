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
        self.class1_names = ['농심감자면', '농심김치큰사발면', '농심무파마', '농심사리곰탕', '농심사천짜파게티', '농심새우탕면작은컵', '농심생생우동', '농심시원한메밀소바', '농심신라면', '농심쌀국수']
        self.class2_names = ['농심사리곰탕작은컵', '농심새우탕', '농심생생우동봉지', '농심신라면블랙', '농심안성탕면', '농심앵그리짜파구리', '농심오징어짬뽕', '농심육개장큰사발', '농심튀김우동', '키다리식품세이면잔치국수']
        self.class3_names = ['농심신라면작은컵', '농심오징어짬뽕작은컵', '농심짜파게티', '농심튀김우동작은컵', '백제멸치맛쌀국수', '삼양치즈불닭볶음면', '오뚜기부대찌개라면', '오뚜기쇠고기미역국라면', '오뚜기열라면', '오뚜기육개장']
        self.class4_names=['농심짜파게티범벅', '삼양까르보불닭볶음면봉지', '오뚜기진라면순한맛', '오뚜기진짬뽕', '오뚜기참깨라면', '오뚜기컵누들베트남쌀국수', '오뚜기크림진짬뽕', '팔도비빔면봉지', '팔도왕뚜껑', '풀무원백면']
        self.class5_names=['농심짜왕', '오뚜기진라면매운맛', '오뚜기참깨라면작은컵', '오뚜기컵누들매콤', '오뚜기컵누들우동맛', '팔도비빔면컵', '풀무원생면식감순한맛', '풀무원정면', '풀무원직화짜장', '풀무원홍면']
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
