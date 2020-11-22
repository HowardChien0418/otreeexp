from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
)


author = ''

doc = """
Demographic Survey Application.
"""


class Constants(BaseConstants):
    name_in_url = 'red_line_demographic_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # General
    age = models.IntegerField(min=18, max=65,
                              label="年齡")
    gender = models.StringField(widget=widgets.RadioSelect,
                                label="性別",
                                choices=['女', '男', '其他', '傾向不告知'])
    nationality = models.StringField(label="國籍")
    race = models.StringField(widget=widgets.RadioSelect,
                              label="What is your race?",
                              choices=['White', 'Asian', 'Black/African', 'Other', 'Prefer not to respond'])

    # Education & Occupation
    is_student = models.BooleanField(widget=widgets.RadioSelect,
                                     label="您是學生嗎")
    student_semesters = models.IntegerField(min=0, max=18,
                                            label="請問您目前共修習多少學期的課程？")
    student_program = models.StringField(label="請問您的主修科系為？")
    highest_degree = models.StringField(widget=widgets.RadioSelect,
                                        label="請問您的最高學歷為",
                                        choices=['高中或等同高中學歷', '學士', '碩士', 'PhD'])
    current_occupation = models.StringField(label="請問您目前的職業是？")

    # Experiment
    similar_experiment_before = models.BooleanField(widget=widgets.RadioSelect,
                                                    label="請問您曾經參加過類似的實驗嗎？")
    find_instructions_clear = models.StringField(widget=widgets.RadioSelectHorizontal,
                                                 label="請問您認為實驗說明夠詳細嗎？",
                                                 choices=['非常不同意', '不同意', '沒意見',
                                                          '同意', '非常同意'])
    comments = models.LongStringField(label="對此實驗，歡迎留下任何建議",
                                      blank=True)
