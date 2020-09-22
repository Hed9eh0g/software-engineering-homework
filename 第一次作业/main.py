#python 3.7
import jieba
import gensim
import re


def get_file_contents(path):
    str = ''
    f = open(path, 'r', encoding='UTF-8')
    line = f.readline()
    while line:
        str = str + line
        line = f.readline()
    f.close()
    return str


def filter(str):
    pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    str = pattern.sub("", str)
    result = jieba.lcut(str)
    return result


def calc_similarity(text1, text2):
    texts = [text1, text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    test_corpus_1 = dictionary.doc2bow(text1)
    cosine_sim = similarity[test_corpus_1][1]
    return cosine_sim


if __name__ == '__main__':
    path1 = "./test/orig.txt"
    path2 = "./test/orig_0.8_dis_15.txt"
    save_path="./save.txt"
    str1 = get_file_contents(path1)
    str2 = get_file_contents(path2)
    text1 = filter(str1)
    text2 = filter(str2)
    similarity = calc_similarity(text1, text2)
    print("文章相似度： %.4f" % similarity)
    #将相似度结果写入指定文件
    f = open(save_path, 'w', encoding="utf-8")
    f.write("文章相似度： %.4f"%similarity)
    f.close()
