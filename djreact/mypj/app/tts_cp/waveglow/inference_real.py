## 기본 라이브러리 Import
import sys
import numpy as np
import torch
import os
import argparse
import soundfile as sf

## WaveGlow 프로젝트 위치 설정
sys.path.append('C:/Users/금정산1_PC15/Desktop/workspace/waveglow/')
## Tacontron2 프로젝트 위치 설정
sys.path.append('C:/Users/금정산1_PC15/Desktop/workspace/waveglow/tacotron2/')

## 프로젝트 라이브러리 Import
from hparams import defaults
from model import Tacotron2
from layers import TacotronSTFT, STFT
from audio_processing import griffin_lim
from tacotron2.train import load_model
from text import text_to_sequence
from scipy.io.wavfile import write
import IPython.display as ipd
import json
import sys
from glow import WaveGlow
from denoiser import Denoiser
from tqdm.notebook import tqdm

## dict->object 변환용
class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        
def load_checkpoint(checkpoint_path, model):
    assert os.path.isfile(checkpoint_path)
    checkpoint_dict = torch.load(checkpoint_path, map_location='cpu')
    model_for_loading = checkpoint_dict['model']
    model.load_state_dict(model_for_loading.state_dict())
    return model
        
class Synthesizer:
    def __init__(self, tacotron_check, waveglow_check):
        hparams = Struct(**defaults)
        hparams.n_mel_channels=80
        hparams.sampling_rate = 22050
        
        self.hparams = hparams
        
        model = load_model(hparams)
        model.load_state_dict(torch.load(tacotron_check)['state_dict'])
        model.cuda().eval()#.half()
        
        self.tacotron = model
        
        with open('C:/Users/금정산1_PC15/Desktop/workspace/waveglow/config.json',encoding='UTF-8') as f:
            data = f.read()
        config = json.loads(data)
        waveglow_config = config["waveglow_config"]
        
        waveglow = WaveGlow(**waveglow_config)
        waveglow = load_checkpoint(waveglow_check, waveglow)
        waveglow.cuda().eval()
        
        self.denoiser = Denoiser(waveglow)
        self.waveglow = waveglow
        
        
    def inference(self, text):
        assert type(text)==str, "텍스트 하나만 지원합니다."
        sequence = np.array(text_to_sequence(text, ['korean_cleaners']))[None, :]
        sequence = torch.autograd.Variable(torch.from_numpy(sequence)).cuda().long()

        mel_outputs, mel_outputs_postnet, _, alignments = self.tacotron.inference(sequence)
        
        
        with torch.no_grad():
            audio = self.waveglow.infer(mel_outputs_postnet, sigma=0.666)
        audio = audio[0].data.cpu().numpy()
        return audio, self.hparams.sampling_rate
    
    ## \n으로 구성된 여러개의 문장 inference 하는 코드
    def inference_phrase(self, phrase, sep_length=4000):
        texts = phrase.split('\n')
        audios = []
        for text in texts:
            if text == '':
                audios.append(np.array([0]*sep_length))
                continue
            audio, sampling_rate = self.inference(text)
            audios.append(audio)
            audios.append(np.array([0]*sep_length))
        return np.hstack(audios[:-1]), sampling_rate
            
    
    def denoise_inference(self, text, sigma=0.666):
        assert type(text)==str, "텍스트 하나만 지원합니다."
        sequence = np.array(text_to_sequence(text, ['korean_cleaners']))[None, :]
        sequence = torch.autograd.Variable(torch.from_numpy(sequence)).cuda().long()

        mel_outputs, mel_outputs_postnet, _, alignments = self.tacotron.inference(sequence)
               
        with torch.no_grad():
            audio = self.waveglow.infer(mel_outputs_postnet, sigma=0.666)
            
        
        audio_denoised = self.denoiser(audio, strength=0.01)[:, 0].cpu().numpy()
        return audio_denoised.reshape(-1), self.hparams.sampling_rate

## 체크포인트 설정
tacotron2_checkpoint = 'C:/Users/금정산1_PC15/Desktop/workspace/waveglow/tacotron2/output/HJ_checkpoint_360000'
waveglow_checkpoint = 'C:/Users/금정산1_PC15/Desktop/workspace/waveglow/checkpoints/HJ_waveglow_390000'

## 음성 합성 모듈 생성
synthesizer = Synthesizer(tacotron2_checkpoint, waveglow_checkpoint)

## 문장 생성
sample_text = '돌고래는 지능이 발달했다.'
audio, sampling_rate = synthesizer.inference(sample_text)
## 음성 저장하기
sf.write('HJ_문장_0531_돌고래.wav', audio, sampling_rate)
#돌고래 : 돌고래는 지능이 발달했다.
#용돈 : 용돈을 아껴 써라.
## 구문 생성
sample_phrase = """
타코트론 모델은 음성 생성 길이가 제한되어 있습니다.
즉 구문을 구성하려면 여러개의 문장을 생성한 후 합쳐야 합니다.
"""
# audio, sampling_rate = synthesizer.inference_phrase(sample_phrase)
## 음성 저장하기
# sf.write('v100_sample_phrase.wav', audio, sampling_rate)
## 문장 생성
# sample_text = '용돈을 아껴 써라.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_문장_0531_용돈.wav', audio, sampling_rate)
# #돌고래 : 돌고래는 지능이 발달했다.
# #용돈 : 용돈을 아껴 써라.
# sample_text = '하이 빅스비.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_빅스비.wav', audio, sampling_rate)
# ## 구문 생성
# sample_phrase = """
# 타코트론 모델은 음성 생성 길이가 제한되어 있습니다.
# 즉 구문을 구성하려면 여러개의 문장을 생성한 후 합쳐야 합니다.
# """
# audio, sampling_rate = synthesizer.inference_phrase(sample_phrase)
# ## 음성 저장하기
# # sf.write('구문_0523_용돈.wav', audio, sampling_rate)
# sample_text = '해당 제품은 농심 김치사발면 입니다.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_김치사발면.wav', audio, sampling_rate)

# sample_text = '해당 제품은 팔도의 비빔면 입니다.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_비빔면.wav', audio, sampling_rate)

# sample_text = '오십'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_50.wav', audio, sampling_rate)

# sample_text = '학교 다녀왔어요.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_학교.wav', audio, sampling_rate)


# sample_text = '해당 제품은 테스트를 위한 것입니다.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_믹스.wav', audio, sampling_rate)

# sample_text = '학교 다녀와서 제품 테스트를 했다.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_학교 믹스.wav', audio, sampling_rate)

# sample_text = '돌고래는 김치사발면을 좋아한다.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_돌고래김치사발면.wav', audio, sampling_rate)

# sample_text = '해당 제품은 돌고래는 지능이 발달했다 입니다.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_돌고래제품.wav', audio, sampling_rate)

# sample_text = '해당 제품은 제 말 듣고 계세요? 입니다.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_해당제품은.wav', audio, sampling_rate)

# sample_text = '해당 제품은 내이름은 최재무 입니다.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_최재무.wav', audio, sampling_rate)

# sample_text = '해당 최재무 입니다.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_최재무2.wav', audio, sampling_rate)

# sample_text = '최재무입니다. 안녕하세요.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_최재무3.wav', audio, sampling_rate)

# sample_text = '사진을 다시 촬영하던가 말던가.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_다시 촬영하던가2.wav', audio, sampling_rate)

# sample_text = '해당 제품은 집에 가고 싶은 현진님 입니다.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_고잉홈.wav', audio, sampling_rate)


# sample_text = '해당 제품은 타코트론은 끝났다! 더러웠고 다시 보자!'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_taco is done.wav', audio, sampling_rate)

# sample_text = '타코트론은 끝났다! 더러웠고 다시 보자!'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_taco is done!.wav', audio, sampling_rate)

# sample_text = '재무님 태경님 현진님 우린님 정식님 그리고 나 너무 고생했어요.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_goodbye.wav', audio, sampling_rate)

# sample_text = '이 발표는 타코트론이 대신 진행합니다.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('HJ_만능타코.wav', audio, sampling_rate)

sample_text = '오십 퍼센트'
audio, sampling_rate = synthesizer.inference(sample_text)
## 음성 저장하기
sf.write('HJ_50퍼센트.wav', audio, sampling_rate)

# sample_text = '정식님 배고파요.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('v100_정식.wav', audio, sampling_rate)

# sample_text = '정식님 배고파요?'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('v100_정식정식.wav', audio, sampling_rate)

# sample_text = '무성님 너무 무서워요.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('v100_창민님이하고싶은말.wav', audio, sampling_rate)

# sample_text = '옛날옛날에 토끼와 호랑이가 살고있었어요.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('v100_토끼호랑이.wav', audio, sampling_rate)

# sample_text = '어흥.'
# audio, sampling_rate = synthesizer.inference(sample_text)
# ## 음성 저장하기
# sf.write('v100_ESTJ.wav', audio, sampling_rate)


