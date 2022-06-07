data_train =[]
data_val = []
taco_train = []
taco_val = []
wave = []

#tacotron2 train과 waveglow를 위한 txt 파일 생성
with open('train_origin.txt',encoding='UTF-8') as f:
    for line in f.readlines():
       data_train.append(line.strip())
    for i in data_train:
        array = i.split("|");
        taco_train.append(array[0] + '|' + array[2])
        wave.append(array[0])
with open('train.txt','w',encoding='UTF-8') as f:
    for name in taco_train:
        f.write('C:/Users/금정산1_PC15/Desktop/workspace/waveglow/tacotron2/kss_train/'+name+'\n')
with open('wave.txt','w',encoding='UTF-8') as f:
    for name in wave:
        f.write('C:/Users/금정산1_PC15/Desktop/workspace/waveglow/tacotron2/kss_train/'+name+'\n')

#여기서부터는 text_replacement code
replace_list = []
data = []
#읽어올 파일경로
with open('wave.txt',encoding='UTF-8') as f:
    for line in f.readlines():
       data.append(line.strip())
    for str in data:
        #찾아서 바꾸고 싶은 단어 입력(앞->찾을 것, 뒤->바꿀 것)
        new_str = str.replace('/tacotron2/', '/waveglow/tacotron2/')
        replace_list.append(new_str)
        print(new_str)
#새로 생성할 파일명
with open('wave_final.txt', 'w', encoding='UTF-8') as f:
    for new_str in replace_list:
        f.write(new_str+'\n')