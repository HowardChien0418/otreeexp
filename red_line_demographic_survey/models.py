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
                              label="What is your age?")
    gender = models.StringField(widget=widgets.RadioSelect,
                                label="What is your gender?",
                                choices=['Female', 'Male', 'Other', 'Prefer not to respond'])
    nationality = models.StringField(label="What is your nationality?")
    race = models.StringField(widget=widgets.RadioSelect,
                              label="What is your race?",
                              choices=['White', 'Asian', 'Black/African', 'Other', 'Prefer not to respond'])

    # Education & Occupation
    is_student = models.BooleanField(widget=widgets.RadioSelect,
                                     label="Are you a student?")
    student_semesters = models.IntegerField(min=0, max=10,
                                            label="How many semesters did you study so far in total?")
    student_program = models.StringField(label="What do you study (program/course)?")
    highest_degree = models.StringField(widget=widgets.RadioSelect,
                                        label="What is your highest educational degree?",
                                        choices=['High School Diploma or equivalent', 'Bachelor', 'Master', 'PhD'])
    current_occupation = models.StringField(label="What is your current occupation?")

    # Experiment
    similar_experiment_before = models.BooleanField(widget=widgets.RadioSelect,
                                                    label="Have you been part of a similar experiment before?")
    find_instructions_clear = models.StringField(widget=widgets.RadioSelectHorizontal,
                                                 label="Do you find the experiment instruction clear?",
                                                 choices=['Strongly disagree', 'Disagree', 'Neutral',
                                                          'Agree', 'Strongly agree'])
    comments = models.LongStringField(label="Comments about this experiment",
                                      blank=True)
