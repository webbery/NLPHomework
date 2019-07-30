from gensim.models import Word2Vec
import os
import zhconv
import json
import cut_sentence
from gensim.models.word2vec import LineSentence

## 将json格式的wiki数据导出成line sentence格式,数据存为对应文件名.txt
def save_sentence_from_json(rootdir):
    directories = os.listdir(rootdir)
    fw = open(rootdir+'sentences','a',encoding='utf-8')
    for dir in directories:
        class_of_dir = rootdir+dir
        json_files = os.listdir(class_of_dir)
        for file_name in json_files:
            fr=open(class_of_dir+'/'+file_name,'r',encoding='utf-8')
            for line in fr.readlines():
                datum = json.loads(line)
                text = zhconv.convert(datum['text'],'zh-cn')
                sentence = cut_sentence.segment(text)
                fw.write(sentence)
            print(file_name+' finished')
            fr.close()
    fw.close()
    print('save_sentence_from_json ok')

def train_vector(rootdir):
    directories = os.listdir(rootdir)
    fr=open(rootdir+'sentences','r',encoding='utf-8')
    sentences = LineSentence(fr)
    model = Word2Vec(sentences,size=128)
    model.save(rootdir+'wiki.model')
    fr.close()

# save_sentence_from_json("F:/other/py/NLPHomework/Assignment-04/out/")
# train_vector("F:/other/py/NLPHomework/Assignment-04/out/")