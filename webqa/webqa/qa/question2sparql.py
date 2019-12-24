# encoding=utf-8

"""
@desc: 自然语言 → SPARQL查询语句
"""

import question_temp
import word_tagging


class Question2Sparql:
    def __init__(self, dict_paths):
        self.tw = word_tagging.Tagger(dict_paths)
        self.rules = question_temp.rules

    def get_sparql(self, question):
        """
        语义解析，匹配模板，返回对应的SPARQL查询语句
        :param question:
        :return:
        """
        word_objects = self.tw.get_word_objects(question)
        for i in word_objects:
            print i.token, i.pos
        queries_dict = dict()

        for rule in self.rules:
            query, num = rule.apply(word_objects)

            if query is not None:
                queries_dict[num] = query

        if len(queries_dict) == 0:
            return None
        elif len(queries_dict) == 1:
            return queries_dict.values()[0]
        else:
            # TODO 匹配到多个语句，以匹配关键词最多的句子作为返回结果
            sorted_dict = sorted(queries_dict.iteritems(), key = lambda item: item[0], reverse=True)
            return sorted_dict[0][1]