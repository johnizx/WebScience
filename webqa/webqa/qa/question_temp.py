# encoding=utf-8

"""
@desc:
问题模板 → SPARQL语句
"""
from refo import finditer, Predicate, Star, Any
import re

# SPARQL前缀和模板
SPARQL_PREFIX = u"""
PREFIX : <http://www.war.com#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

SPARQL_SELECT_TEM = u"{prefix}\n" + \
                    u"SELECT DISTINCT {select} WHERE {{\n" + \
                    u"{expression}\n" + \
                    u"}}\n"

SPARQL_COUNT_TEM = u"{prefix}\n" + \
                   u"SELECT COUNT({select}) WHERE {{\n" + \
                   u"{expression}\n" + \
                   u"}}\n"

SPARQL_ASK_TEM = u"{prefix}\n" + \
                 u"ASK {{\n" + \
                 u"{expression}\n" + \
                 u"}}\n"


class W(Predicate):
    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token)
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition_num, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action
        self.condition_num = condition_num

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])

        return self.action(matches), self.condition_num


class KeywordRule(object):
    def __init__(self, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])
        if len(matches) == 0:
            return None
        else:
            return self.action()


class QuestionSet:
    def __init__(self):
        pass

    @staticmethod
    def participate_war(word_objects):
        """
        某国（组织）打赢了什么战争？
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_combatant:
                e = u'?s :combatantName "{combatant}".' \
                    u"?s :wonIn ?w." \
                    u"?w :warName ?x".format(combatant=w.token.decode('utf-8'))

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def combatant_participate(word_objects):
        """
        某场战争有哪些参战者？
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_war:
                e = u'?w :warName "{war}".' \
                    u"{{?c :wonIn ?w}} UNION" \
                    u"{{?c :failedIn ?w}}." \
                    u"?c :combatantName ?x".format(war=w.token.decode('utf-8'))

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def count_participated_wars(word_objects):
        """
        某国参加了多少场战争？
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_combatant:
                e = u'?c :combatantName "{combatant}".' \
                    u"{{?c :wonIn ?x}} UNION" \
                    u"{{?c :failedIn ?x}}.".format(combatant=w.token.decode('utf-8'))

                sparql = SPARQL_COUNT_TEM.format(prefix=SPARQL_PREFIX, select=select, expression=e)
                break

        return sparql

    @staticmethod
    def war_take_place(word_objects):
        """
        某场战争在何时开始？
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_war:
                e = u'?s :warName "{war}".' \
                    u"?s :warStartDate ?x".format(war=w.token.decode('utf-8'))

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def war_death_number(word_objects):
        """
        某场战争的死亡人数
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_war:
                e = u'?s :warName "{war}".' \
                    u"?s :warDeathNumber ?x".format(war=w.token.decode('utf-8'))

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql


# TODO 定义关键词
pos_combatant = "@@nt"
pos_war = "@@nz"
pos_location = "@@ns"

combatant_entity = (W(pos=pos_combatant))
war_entity = (W(pos=pos_war))
location_entity = (W(pos=pos_location))

war = (W("战斗") | W("战役") | W("战争"))
combatant = (W("参战方") | W("参战国") | W("国家") | W("组织"))
several = (W("多少") | W("几场"))

war_name = (W("冲突名称") | W("战役名称"))
war_death = (W("战损") | W("死亡人数"))

when = (W("哪个地方") | W("何时") | W("什么时候"))
where = (W("在哪里") | W("哪儿") | W("何地") | W("何处") | W("在") + W("哪"))

# TODO 问题模板/匹配规则
"""
1. 某个国家打赢了什么战争
2. 某场战争有哪些参战者
3. 某国参加了多少战争
4. 某场战争在何时发生
5. 某场战争的战损是多少
"""
rules = [
    Rule(condition_num=2, condition=combatant_entity + Star(Any(), greedy=False) + war + Star(Any(), greedy=False), action=QuestionSet.participate_war),
    Rule(condition_num=2, condition=(war_entity + Star(Any(), greedy=False) + combatant + Star(Any(), greedy=False)) | (combatant + Star(Any(), greedy=False) + war_entity + Star(Any(), greedy=False)), action=QuestionSet.combatant_participate),
    Rule(condition_num=3, condition=combatant_entity + Star(Any(), greedy=False) + several + Star(Any(), greedy=False) + (war | Star(Any(), greedy=False)), action=QuestionSet.count_participated_wars),
    Rule(condition_num=2, condition=war_entity + Star(Any(), greedy=False) + when, action=QuestionSet.war_take_place),
    Rule(condition_num=2, condition=war_entity + Star(Any(), greedy=False) + war_death + Star(Any(), greedy=False), action=QuestionSet.war_death_number),
]
