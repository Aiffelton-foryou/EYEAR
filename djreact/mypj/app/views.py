from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from .utils import *
from django.views.generic import TemplateView
from django.http import HttpResponse,FileResponse
import json
import os
from PIL import Image 
import numpy as np
import uuid
from .tts_cp.inference_real import sound_infer
import soundfile as sf
# Create your views here.

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
class ImgListApi(APIView):
    # 리스트 확인
    def get(self,request):
        queryset = MatchImage.objects.all()
        serializer = ImgSerializer(queryset,many = True)
        return Response(serializer.data)

    # 데이터 전송
    def post(self, request):
        print("kk",request)
        serializer = ImgSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)



class ImgDetail(APIView):
    # 개체 가져오기
    def get_object(self,pk):
        try:
            return MatchImage.objects.get(pk=pk)
        except MatchImage.DoesNotExist:
            raise Http404
    
    # detail 보기
    def get(self,request,pk,format=None):
        img = self.get_object(pk)
        serializer = ImgSerializer(img)
        return Response(serializer.data)

    # detail 수정
    def put(self,request,pk,format=None):
        img = self.get_object(pk)
        serializer = ImgSerializer(img,data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        
    # detail 삭제
    def delete(self,request,pk,format=None):
        img = self.get_object(pk)
        img.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

model_ = Model()

class infer(APIView):

    def SelectView(request):
        try:
            print('start')
            cursor = connection.cursor()
            print('second')
            strSql = r"SELECT * FROM app_matchimage WHERE title = {}".format(request)
            print(strSql)
            result = cursor.execute(strSql)
            content = cursor.fetchall()
            print(content)
            connection.commit()
            connection.close()

        except Exception as e:
            connection.rollback()
            return e

        return content
    
    def post(self,request):
        # try:
            '''frontend로부터 받은 image 저장'''
            rowimg = request.data
            img = Image.open(rowimg['img'])
            # img.show()

            unique_filename = str(uuid.uuid4())
            print("SAVE :",unique_filename)
            rgb_img = img.convert('RGB')
            rgb_img.save(f'./image/{unique_filename}.jpg')
            img = Image.open(f'./image/{unique_filename}.jpg')
            '''image inference 수행'''
            pred,acc = model_.predict_img(img)

            print('예측결과',pred,acc)
            '''결과로 db 검색''' 
            # result = SelectView(qr)
            
            

            '''검색결과 tts로 response'''
            audio,sampling_rate = sound_infer(pred) # inferenced name
            sf.write(f'./app/sound/HJ_{pred}.wav', audio, sampling_rate)
            f = open(f"./app/sound/HJ_{pred}.wav","rb")
            response = HttpResponse()
            
            response.write(f.read())
            response['content-type'] = 'audio/wav'
            response['content-length'] = os.path.getsize(f'./app/sound/HJ_{pred}.wav')

            return response
        # except:
        #     return Response(dict(result = -1,b = "입력 형식이 잘못되었습니다."))