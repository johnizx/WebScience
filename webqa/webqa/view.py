# coding=utf-8
from django.shortcuts import render
from webqa.qa import jena_sparql_endpoint, question2sparql
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')


# 接收并处理问题
def process_question(request):
    ctx = {}
    if request.POST:
        fuseki = jena_sparql_endpoint.JenaFuseki()
        # TODO 初始化自然语言到SPARQL查询的模块，参数是外部词典列表。
        q2s = question2sparql.Question2Sparql(
            ['webqa/qa/external_dict/war.txt', 'webqa/qa/external_dict/combatant.txt', 'webqa/qa/external_dict/location.txt'])
        question = request.POST['question']     # 获取前端输入
        ctx['question'] = question  # 保存问题,前端显示
        """
        # 参战者字符处理：去除括号、引号
        en = re.sub(u"([^\u0041-\u005a\u0061-\u007a,\u0020])", "", question)
        ch = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039])", "", question)
        question = "['" + en + "']" + ch
        """
        # print question
        my_query = q2s.get_sparql(question.decode('utf-8'))
        print my_query
        if my_query is not None:
            result = fuseki.get_sparql_result(my_query)
            value = fuseki.get_sparql_result_value(result)
            ctx['result'] = value
            # TODO 判断结果是否是布尔值，是布尔值则提问类型是"ASK"，回答“是”或者“不知道”。
            if isinstance(value, bool):
                if value is True:
                    ctx['result'] = ['Yes', ]
                else:
                    ctx['result'] = ['I don\'t know. ', ]
            else:
                # TODO 查询结果为空,回答“不知道”
                if len(value) == 0:
                    ctx['result'] = ['I don\'t know.(Null Result) ', ]
                else:
                    ctx['result'] = value
        else:
            # TODO 自然语言问题无法匹配到已有的正则模板上，回答“无法理解”
            ctx['result'] = ['I can\'t understand. (No Templates matched)', ]

    return render(request, "index.html", ctx)
