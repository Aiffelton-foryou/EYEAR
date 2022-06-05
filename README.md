![header](https://capsule-render.vercel.app/api?type=rect&color=A3DCBE&height=300&section=header&text=프로젝트:EYEAR&fontSize=90)

### 프로젝트 소개
시각장애인(저시력, 색각 이상)의 오프라인 쇼핑을 보조하기 위해 상품명을 읽어주는 서비스

### 팀원 소개 및 역할
- 팀명: 널위한 동행 (널위행)

|이름|구성|역할|
|:---:|:---:|:---:|
|최재무|팀장|프로젝트 총괄, 모델링 구현, Model Tuning|
|임현진|팀원|데이터 수집, 모델링 구현|
|노태경|팀원|환경 구축, 데이터 수집, 전처리|
|서우린|팀원|데이터 수집, Web Service Backend |
|심연진|팀원|데이터 전처리, TTS 모델링|

<div align=center>
<h3>:hammer_and_wrench: 기술 스택 :hammer_and_wrench: </h3>

<img src="https://img.shields.io/badge/React-61DAFB?style=plastic&logo=React&logoColor=white">
<img src="https://img.shields.io/badge/Django-092E20?style=plastic&logo=Django&logoColor=white">
<img src="https://img.shields.io/badge/Python-3776AB?style=plastic&logo=Python&logoColor=white">
<img src="https://img.shields.io/badge/Opencv-5C3EE8?style=plastic&logo=Opencv&logoColor=white">
<img src="https://img.shields.io/badge/Tensorflow-FF6F00?style=plastic&logo=Tensorflow&logoColor=white">
<img src="https://img.shields.io/badge/Pytorch-EE4C2C?style=plastic&logo=Pytorch&logoColor=white">
  <img src="https://img.shields.io/badge/Colab-F9AB00?style=plastic&logo=Colab&logoColor=white">
</div>

### 문제 정의
- 저시력 장애인의 경우 물품을 구매할 때 어떤 제품인지 인식하는 어려움이 있어 마트 직원이나 보조인의 도움이 필요하다. 
- 하지만 코로나로 인해 마트 인력 감축과 무인 계산대의 증가로 인해 일상생활 제춤 자체를 구입하는 것에 대해 어려움을 겪고 있어 쇼핑 과정에 제품을 확안하고 구매할 수 있도록 도와주는 프로젝트를 구성하게 되었다.

### 프로젝트 목표
- 저시력 장애인이 생활용품을 구매할 때 발생하는 문제점들을 최소화하기 위해 Classification을 통해 상품을 인식하고 TTS 기술을 활용하여 음성 안내를 통해 저시력장애인의 쇼핑을 돕는 서비스를 제공한다.


### 프로젝트 구성 
1. 개발 환경 구축
- tensorflow v2 , Pytorch 환경 구축

2.  데이터 수집
- AI Hub 데이터셋 
- 실제 데이터셋 추가 수집

3. 데이터 전처리 및 증강
- random crop, rotate 활용 데이터 증강

4. 모델링 및 Tuning
- Classification 모델링
- Tacotron + Wavwglow 모델링
- Tuning

5. Web Service 개발
- React, Django 환경 구축
- Server 개발 및 ???



### Function
- Classification
  - ResNet101
- TTS
  - Tacotron
  - Waveglow

### Installation
- 프로젝트 사용할 때 version 설정 어떻게 해야 할지 작성


### Web Service 
<img src='https://user-images.githubusercontent.com/58939359/172043495-7b0fa1d5-acc9-4b50-a4bc-e1f8c7f9e637.png' width='500' height='500'>


### 널위행 상품 알리미 서비스 (웹페이지 구동 방식 - 이미지로 표현)
<img src="https://user-images.githubusercontent.com/58939359/172042822-b943ce33-3847-42ed-86f7-b750acf59033.png"  width="500" height="370">

### 상품 인식 단계
1. 카메라로 상품을 촬영하면 해당 상품이 무엇인지 결과가 음성으로 출력된다.


### Reference
https://github.com/melonicedlatte/multi-speaker-tacotron-tensorflow
https://www.tensorflow.org/api_docs/python/tf/keras/applications/resnet?hl=ko
https://qwlake.github.io/django/2020/07/01/apply-https-on-django-server-with-nginx/
https://github.com/danielgatis/rembg

<br>
