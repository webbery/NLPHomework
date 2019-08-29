# 分割中文句子
import jieba
import regex as re

def is_chinese(uchar):
    # 判断一个unicode是否是汉字
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False
    
def is_number(uchar):
    # 判断一个unicode是否是数字
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False

def is_alphabet(uchar):
    # 判断一个unicode是否是英文字母
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False

def is_legal(uchar):
    # 判断是否非汉字，数字和英文字符
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return False
    else:
        return True

def cut_chinese_sentences(doc):
    sentences = []
    try:
        for line in doc.splitlines():
            sentences+=re.split("[。?？！!]+",line)
    except:
        print(doc)
    # sentences = [ for line in doc.splitlines()]
    # print(sentences)
    return sentences

def cut_and_segment(doc,lang='zh'):
    sentences = cut_chinese_sentences(doc)
    sentences_of_split=[]
    for sentence in sentences:
        line = segment(sentence)
        if line=="": continue
        sentences_of_split.append(line)
    return sentences_of_split

def segment(sentence,type="str"):
    sentence_seged = jieba.cut(sentence.strip()) 
    stopwords = [",","，","。","?","？","（","）","(",")","《","》","、","/","！","「","」","“","”","：","<",">","－","／"," ","|","-","@","\r","\n","\r\n"]
    if type=="str":
        outstr = ''
        for word in sentence_seged:
            if word not in stopwords:
                if word != '\t':
                    outstr += word
                    outstr += " "
        return outstr
    else:
        outstr = []
        for word in sentence_seged:
            if word not in stopwords:
                if word != '\t':
                    outstr.append(word)
        return outstr

# from sklearn.feature_extraction.text import TfidfVectorizer
# tfidf = TfidfVectorizer()
# line = cut_and_segment("雨后")
# vec = tfidf.fit_transform(line)
# print(line)
