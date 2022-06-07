data_train =[]
data_val = []
taco_train = []
taco_val = []
wave = []
with open('HJ_text.txt',encoding='UTF-8') as f:
    for line in f.readlines():
       data_train.append(line.strip())
    for i in data_train:
        array = i.split("|");
        # taco_train.append(array[0] + '|' + array[2])
        wave.append(array[0])
# tacotron2 train을 위한 파일 생성
# with open('train.txt','w',encoding='UTF-8') as f:
#     for name in taco_train:
#         f.write('C:/Users/금정산1_PC15/Desktop/workspace/waveglow/tacotron2/kss_train/'+name+'\n')
#waveglow를 위한 파일 생성(wav파일 위치 알려주는 txt)
with open('wave.txt','w',encoding='UTF-8') as f:
    for name in wave:
        f.write(name+'\n')


# #여기서부터는 text_replacement code
# replace_list = []
# data = []
# #읽어올 파일경로
# with open('wave.txt',encoding='UTF-8') as f:
#     for line in f.readlines():
#        data.append(line.strip())
#     for str in data:
#         #찾아서 바꾸고 싶은 단어 입력(앞->찾을 것, 뒤->바꿀 것)
#         new_str = str.replace('/tacotron2/', '/waveglow/tacotron2/')
#         replace_list.append(new_str)
#         print(new_str)
# #새로 생성할 파일명
# with open('wave_final.txt', 'w', encoding='UTF-8') as f:
#     for new_str in replace_list:
#         f.write(new_str+'\n')


# with open('wave.txt',encoding='UTF-8') as f:
#     for line in f.readlines():
#        data_train.append(line.strip())
#     for i in data_train:
#         array = i.split("|");
#         wave.append(array[0])
# #gcp용 waveglow 위한 파일 생성(wav파일 위치 알려주는 txt)
# with open('wave_final.txt','w',encoding='UTF-8') as f:
#     for name in wave:
#         f.write(name+'\n')

# #tacotron2 val을 위한 파일 생성
# with open('val_text.txt',encoding='UTF-8') as f:
#     for line in f.readlines():
#        data_val.append(line.strip())
#     for i in data_val:
#         array = i.split("|");
#         taco_val.append(array[0] + '|' + array[2])

# with open('val.txt','w',encoding='UTF-8') as f:
#     for name in taco_val:
#         f.write('C:/Users/금정산1_PC15/Desktop/workspace/waveglow/tacotron2/kss_val/'+name+'\n')