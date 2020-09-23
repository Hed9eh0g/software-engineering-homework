
# 前言



本文涉及代码已上传[个人GitHub](https://github.com/Hed9eh0g/software-engineering-homework/blob/master/%E7%AC%AC%E4%B8%80%E6%AC%A1%E4%BD%9C%E4%B8%9A)

> 题目：论文查重
>
> 描述如下：
> 
> 设计一个论文查重算法，给出一个原文文件和一个在这份原文上经过了增删改的抄袭版论文的文件，在答案文件中输出其重复率。
>
> 原文示例：今天是星期天，天气晴，今天晚上我要去看电影。
> 抄袭版示例：今天是周天，天气晴朗，我晚上要去看电影。
> 要求输入输出采用文件输入输出，规范如下：
> 
> 从命令行参数给出：论文原文的文件的绝对路径。
> 从命令行参数给出：抄袭版论文的文件的绝对路径。
> 从命令行参数给出：输出的答案文件的绝对路径。
> 我们提供一份样例，课堂上下发，上传到班级群，使用方法是：orig.txt是原文，其他orig_add.txt等均为抄袭版论文。
>
> 注意：答案文件中输出的答案为浮点型，精确到小数点后两位

查询网上文章，总结出实现思路：

- 先将待处理的数据（中文文章）进行分词，得到一个存储若干个词汇的列表
- 接着计算并记录出列表中词汇对应出现的次数，将这些次数列出来即可认为我们得到了一个向量
- 将两个数据对应的向量代入夹角余弦定理
- 计算的值意义为两向量的偏移度，这里也即对应两个数据的相似度

除了余弦定理求相似度，还可以使用欧氏距离、海明距离等

# 所用接口

## jieba.cut

用于对中文句子进行分词，功能非常强大，详细功能见[GitHub](https://github.com/fxsjy/jieba)

该方法提供多种分词模式供选择，这里只需用到默认最简单的“精确模式”。

代码：

```python
seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
print(", ".join(seg_list))
```

运行结果：

```
他, 来到, 了, 网易, 杭研, 大厦
```



## re.match

由于对比对象为中文或英文单词，因此应该对读取到的文件数据中存在的换行符`\n`、标点符号过滤掉，这里选择用正则表达式来匹配符合的数据。

代码：

```python
def filter(str):
    str = jieba.lcut(str)
    result = []
    for tags in str:
        if (re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]", tags)):
            result.append(tags)
        else:
            pass
    return result
```

这里正则表达式为`u"[a-zA-Z0-9\u4e00-\u9fa5]"`，也即对`jieba.cut`分词之后的列表中的值，只保留英文`a-zA-z`、数字`0-9`和中文`\u4e00-\u9fa5`的结果。



## gensim.dictionary.doc2bow

Doc2Bow是gensim中封装的一个方法，主要用于实现Bow模型。

> Bag-of-words model (BoW model) 最早出现在自然语言处理（Natural Language Processing）和信息检索（Information Retrieval）领域.。该模型忽略掉文本的语法和语序等要素，将其仅仅看作是若干个词汇的集合，文档中每个单词的出现都是独立的。

例如：

```python
text1='John likes to watch movies. Mary likes too.'
text2='John also likes to watch football games.'
```

基于上述两个文档中出现的单词，构建如下一个词典 (dictionary)：

```
 {"John": 1, "likes": 2,"to": 3, "watch": 4, "movies": 5,"also": 6, "football": 7, "games": 8,"Mary": 9, "too": 10}
```

上面的词典中包含10个单词, 每个单词有唯一的索引, 那么每个文本我们可以使用一个10维的向量来表示。如下：

```
[1, 2, 1, 1, 1, 0, 0, 0, 1, 1]
[1, 1, 1, 1, 0, 1, 1, 1, 0, 0]
```

该向量与原来文本中单词出现的顺序没有关系，而是词典中每个单词在文本中出现的频率。

代码：

```python
def convert_corpus(text1,text2):
    texts=[text1,text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    return corpus
```



## gensim.similarities.Similarity

该方法可以用计算余弦相似度，但具体的实现方式[官网](https://tedboy.github.io/nlps/generated/generated/gensim.similarities.Similarity.html)似乎并未说清楚，这是我查找大量文章得到的一种实现方式：

```python
def calc_similarity(text1,text2):
    corpus=convert_corpus(text1,text2)
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    test_corpus_1 = dictionary.doc2bow(text1)
    cosine_sim = similarity[test_corpus_1][1]
    return cosine_sim
```

当然也可以根据余弦公式实现计算余弦相似度：

```python
from math import sqrt
def similarity_with_2_sents(vec1, vec2):
    inner_product = 0
    square_length_vec1 = 0
    square_length_vec2 = 0
    for tup1, tup2 in zip(vec1, vec2):
        inner_product += tup1[1]*tup2[1]
        square_length_vec1 += tup1[1]**2
        square_length_vec2 += tup2[1]**2

    return (inner_product/sqrt(square_length_vec1*square_length_vec2))


cosine_sim = similarity_with_2_sents(vec1, vec2)
print('两个句子的余弦相似度为： %.4f。'%cosine_sim)
```



# 代码实现

将上述方法汇总应用，得到代码：

```python
import jieba
import gensim
import re

#获取指定路径的文件内容
def get_file_contents(path):
    str = ''
    f = open(path, 'r', encoding='UTF-8')
    line = f.readline()
    while line:
        str = str + line
        line = f.readline()
    f.close()
    return str

#将读取到的文件内容先进行jieba分词，然后再把标点符号、转义符号等特殊符号过滤掉
def filter(str):
    str = jieba.lcut(str)
    result = []
    for tags in str:
        if (re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]", tags)):
            result.append(tags)
        else:
            pass
    return result

#传入过滤之后的数据，通过调用gensim.similarities.Similarity计算余弦相似度
def calc_similarity(text1,text2):
    texts=[text1,text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    test_corpus_1 = dictionary.doc2bow(text1)
    cosine_sim = similarity[test_corpus_1][1]
    return cosine_sim

if __name__ == '__main__':
    path1 = "E:\pythonProject1\test\orig_0.8_dis_10.txt"  #论文原文的文件的绝对路径（作业要求）
    path2 = "E:\pythonProject1\test\orig_0.8_dis_15.txt"  #抄袭版论文的文件的绝对路径
    save_path = "E:\pythonProject1\save.txt"   #输出结果绝对路径
    str1 = get_file_contents(path1)
    str2 = get_file_contents(path2)
    text1 = filter(str1)
    text2 = filter(str2)
    similarity = calc_similarity(text1, text2)
    print("文章相似度： %.4f"%similarity)
    #将相似度结果写入指定文件
    f = open(save_path, 'w', encoding="utf-8")
    f.write("文章相似度： %.4f"%similarity)
    f.close()

```
可以看出两篇文章相似度很大：

![](https://img2020.cnblogs.com/blog/2147920/202009/2147920-20200922195205856-1533931868.png)


![](https://img2020.cnblogs.com/blog/2147920/202009/2147920-20200922194944707-243636993.png)

运行结果：

![](https://img2020.cnblogs.com/blog/2147920/202009/2147920-20200922194739389-1962324918.png)

更改路径，

```python
path1 = "E:\pythonProject1\test\orig.txt"   ##论文原文的文件的绝对路径
path2 = "E:\pythonProject1\test\orig_0.8_dis_15.txt"   #抄袭版论文的文件的绝对路径
```

可以看出两篇文章相似度较小：

![](https://img2020.cnblogs.com/blog/2147920/202009/2147920-20200922194906953-713078168.png)

![](https://img2020.cnblogs.com/blog/2147920/202009/2147920-20200922194944707-243636993.png)

运行结果：

![](https://img2020.cnblogs.com/blog/2147920/202009/2147920-20200922194807147-1940080997.png)


综上，该程序基本符合判断相似度的要求


# 性能分析

## 时间耗费

利用pycharm的插件可以得到耗费时间的几个主要函数排名：

![](https://img2020.cnblogs.com/blog/2147920/202009/2147920-20200922200937014-1736737410.png)

关注到`filter`函数：由于`cut`和`lcut`暂时找不到可提到的其他方法（jieba库已经算很强大了），暂时没办法进行改进，因此考虑对正则表达式匹配改进。

**这里是先用`lcut`处理后再进行匹配过滤，这样做显得过于臃肿，可以考虑先匹配过滤之后再用`lcut`来处理**

改进代码：

```python
def filter(string):
    pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    string = pattern.sub("", string)
    result = jieba.lcut(string)
    return result
```

再做一次运行时间统计：

![](https://img2020.cnblogs.com/blog/2147920/202009/2147920-20200922210326060-215207646.png)

可以看到总耗时快了0.5s，提升了时间效率

## 代码覆盖率

代码覆盖率100%，满足要求：

![](https://img2020.cnblogs.com/blog/2147920/202009/2147920-20200922212751815-1196767001.png)

# 单元测试

这里需要用到python的unittest单元测试框架，详见[官网介绍](https://docs.python.org/zh-cn/3/library/unittest.html)



为了方便进行单元测试，源码的`main()`应该修改一下：

```python
import jieba
import gensim
import re

#获取指定路径的文件内容
def get_file_contents(path):
    string = ''
    f = open(path, 'r', encoding='UTF-8')
    line = f.readline()
    while line:
        string = string + line
        line = f.readline()
    f.close()
    return string

#将读取到的文件内容先把标点符号、转义符号等特殊符号过滤掉，然后再进行结巴分词
def filter(string):
    pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    string = pattern.sub("", string)
    result = jieba.lcut(string)
    return result

#传入过滤之后的数据，通过调用gensim.similarities.Similarity计算余弦相似度
def calc_similarity(text1, text2):
    texts = [text1, text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    test_corpus_1 = dictionary.doc2bow(text1)
    cosine_sim = similarity[test_corpus_1][1]
    return cosine_sim


def main_test():
    path1 = input("输入论文原文的文件的绝对路径：")
    path2 = input("输入抄袭版论文的文件的绝对路径：")
    str1 = get_file_contents(path1)
    str2 = get_file_contents(path2)
    text1 = filter(str1)
    text2 = filter(str2)
    similarity = calc_similarity(text1, text2)   #生成的similarity变量类型为<class 'numpy.float32'>
    result=round(similarity.item(),2)  #借助similarity.item()转化为<class 'float'>，然后再取小数点后两位
    return result


if __name__ == '__main__':
    main_test()
```

为了使预期值更好确定，这里考虑只取返回的相似度值的前两位，借助round(float,2)即可处理，由于生成的similarity类型为<class 'numpy.float32'>，因此应当先转化为<class 'float'>，查找[对应解决方法](https://stackoverflow.com/questions/9452775/converting-numpy-dtypes-to-native-python-types)：通过`xxx.item()`即可转化。

再新建单元测试文件unit_test.py：

```python
import unittest
from main import main_test


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(main_test(),0.99)   #首先假设预测的是前面第一组运行的测试数据


if __name__ == '__main__':
    unittest.main()

```

可以发现预测值为0.99正确：

![](https://img2020.cnblogs.com/blog/2147920/202009/2147920-20200923215021710-274165704.png)

![](https://img2020.cnblogs.com/blog/2147920/202009/2147920-20200923215100303-922870715.png)

相似度仍然预测为0.99，但路径更改为之前测试的第二组数据：

![](https://img2020.cnblogs.com/blog/2147920/202009/2147920-20200923215302158-1202301996.png)

可以发现预测失败。

# 异常处理说明

在读取指定文件路径时，如果文件路径不存在，程序将会出现异常，因此可以在读取指定文件内容之前先判断文件是否存在，若不存在则做出响应并且结束程序。

这里引入`os.path.exists()`方法用于检验文件是否存在：

```python

def main_test():
    path1 = input("输入论文原文的文件的绝对路径：")
    path2 = input("输入抄袭版论文的文件的绝对路径：")
    if not os.path.exists(path1) :
        print("论文原文文件不存在！")
        exit()
    if not os.path.exists(path2):
        print("抄袭版论文文件不存在！")
        exit()
    ······
```



# PSP表格记录


| ***PSP***                               | ***Personal Software Process Stages***  | ***预估耗时（分钟）*** | ***实际耗时（分钟）*** |
| --------------------------------------- | --------------------------------------- | ---------------------- | ---------------------- |
| Planning                                | 计划                                    | 120                    | 150                    |
| · Estimate                              | · 估计这个任务需要多少时间              | 120                    | 150                    |
| Development                             | 开发                                    | 480                    | 300                    |
| · Analysis                              | · 需求分析 (包括学习新技术)             | 120                    | 100                    |
| · Design Spec                           | · 生成设计文档                          | 30                     | 10                     |
| · Design Review                         | · 设计复审                              | 30                     | 10                     |
| · Coding Standard                       | · 代码规范 (为目前的开发制定合适的规范) | 20                     | 5                      |
| · Design                                | · 具体设计                              | 10                     | 5                      |
| · Coding                                | · 具体编码                              | 120                    | 120                    |
| · Code Review                           | · 代码复审                              | 20                     | 5                      |
| · Test                                  | · 测试（自我测试，修改代码，提交修改）  | 20                     | 20                     |
| Reporting                               | 报告                                    | 30                     | 20                     |
| · Test Repor                            | · 测试报告                              | 20                     | 10                     |
| · Size Measurement                      | · 计算工作量                            | 5                      | 5                      |
| · Postmortem & Process Improvement Plan | · 事后总结, 并提出过程改进计划          | 5                      | 5                      |
| Total                                   | 总计                                  |  1150                  | 915                    |


# 参考文章

https://titanwolf.org/Network/Articles/Article?AID=26627f5e-1ce9-40cb-a091-b771ae91d69d

http://www.ruanyifeng.com/blog/2013/03/cosine_similarity.html

https://blog.csdn.net/qq_40938678/article/details/105354002
