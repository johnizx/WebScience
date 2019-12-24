# encoding=utf-8

import jieba
import jieba.posseg as pseg


class Word(object):
    def __init__(self, token, pos):
        self.token = token  # 词语
        self.pos = pos  # 词性


class Tagger:
    def __init__(self, dict_paths):
        # 加载外部词典
        for p in dict_paths:
            jieba.load_userdict(p)

    @staticmethod
    def get_word_objects(sentence):
        # 将自然语言转为Word对象
        return [Word(word.encode('utf-8'), tag) for word, tag in pseg.cut(sentence)]


# 测试
if __name__ == '__main__':
    tagger = Tagger(['./external_dict/war.txt', './external_dict/combatant.txt', './external_dict/location.txt'])
    while True:
        s = raw_input()
        for i in tagger.get_word_objects(s):
            print i.token, i.pos
