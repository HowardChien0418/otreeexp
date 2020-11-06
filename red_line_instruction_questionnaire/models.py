from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = ''

doc = """
This questionnaire is used to ensure that participants have understood the rules of the experiment correctly.
"""

class Constants(BaseConstants):
    instruction_time_seconds = 5 * 60   # 5 minutes
    payoff_template_instructions_new = 'red_line_instruction_questionnaire/payoff_matrices_new.html'
    payoff_template_instructions = 'red_line_instruction_questionnaire/payoff_matrices_colored.html'
    payoff_template = 'red_line_instruction_questionnaire/payoff_matrices_general.html'
    name_in_url = 'red_line_instruction_questionnaire'
    players_per_group = 2
    num_rounds = 8#max(len(questions_per_role['R']), len(questions_per_role['S']))
        # Payoff matrix constants
    w0 = 50
    v_choices = [20, 30]
    x_choices = [5, 10]
    eps_choices = [20, 40]



class Subsession(BaseSubsession):
    def creating_session(self):
        import random
        for gr in self.get_groups():
            gr.eps = random.choice(Constants.eps_choices)
            gr.w1 = random.randint(Constants.w0 - gr.eps, Constants.w0 + gr.eps)
            if gr.round_number == 1:
                gr.v = random.choice(Constants.v_choices)
                gr.x = random.choice(Constants.x_choices)
                gr.sequence = 2 if gr.id_in_subsession % 2 == 0 else 1

            else:
                gr_previous = gr.in_round(1)
                gr.v= gr_previous.v
                gr.x = gr_previous.x
                gr.sequence = gr_previous.sequence


class Group(BaseGroup):
    v = models.IntegerField()
    x = models.IntegerField()
    w1 = models.IntegerField()
    eps = models.IntegerField()
    sequence = models.IntegerField()

    def get_question(self, role,round):
        return self.__getquestion__(role,round)[0]

    def get_answer(self, role,round):
        return self.__getquestion__(role,round)[1]

    def questions_per_role(self,role):
        questions_num = self.__getquestion__(role,-1)#{'S': 7, 'R': 6}
        return questions_num

    def __getquestion__(self, role,round):
        # S palyer has has 8 questionswhich is more than R questions number(7 questions). The Constants.players_per_group shows the max number of questions.
        # In a case of questions list update Constants.players_per_group must be also updated
        questions_per_role = {
            'S': [
            ("As a Player S, if you draw a silver ball from the bucket, you can decide whether to "
             "report the color to Player R. True or False?", True),
            ("As a Player S, if you draw a golden ball from the bucket, you can decide whether to "
             "report the color to Player R. True or False?", False),
            ("If the bucket is Gold, you draw a golden ball from the bucket, and Player R chooses "
             "Silver, your payoff of the round is 0. True or False?", True),
            ("If the bucket is Silver, you draw a silver ball from the bucket, and Player R chooses "
             "Silver, your payoff of the round is "+str(self.v)+". True or False?", True),
            ("If you draw a silver ball from the bucket, you report the color to Player R and he or she "
             "chooses Gold, "+str(self.x)+" points will be deducted from your payoff. True or False?", True),
            ("If the bucket is Gold, you draw a golden ball from the bucket, and Player R chooses Silver, "
             "Player R’s payoff of the round is "+str(Constants.w0)+". True or False?", False),
            ("If the bucket is Silver, you draw a golden ball from the bucket, and Player R chooses "
                "Silver, Player R’s payoff of the round is a value randomly drawn from [30 and 70] or [10 and 90]. True or False?", True),
            ("After the experiment, you will receive a payment consisting of the payoff of a randomly picked "
             "decision-making round plus one of lottery choice outcomes divided by 10, and the participation "
             "fee. True or False?", True)
            ],
            'R': [
                ("If Player S draws a silver ball from the bucket, he or she can decide whether to report "
                "the color to you. True or False?", True),
                ("If Player S draws a golden ball from the bucket, he or she can decide whether to report "
                "the color to you. True or False?", False),
                ("If the bucket is Gold and you choose Silver, your payoff of the round is 0. True or False?", True),
                ("If the bucket is Silver, you choose Silver, your payoff of the round is a value randomly drawn from [30 and 70] or [10 and 90]. You will know the exact value at the beginning of each round. "
                "True or False?", True),
                ("If the bucket is Gold, Player S reports Silver to you, and you choose Gold, Player S’s "
                "payoff of the round is "+str(self.v)+"-"+str(self.x)+". True or False?", True),
                ("If the bucket is Silver, Player S doesn't report the color of the ball he or she drawn to "
                "you, and you choose Gold, Player S’s payoff of the round is 0. True or False?", True),
                ("After the experiment, you will receive a payment consisting of the payoff of a randomly picked "
                "decision-making round plus one of lottery choice outcomes divided by 10, and the participation "
                "fee. True or False?", True)
            ],
        }
        if round == -1:
            return len(questions_per_role[role])
        return questions_per_role[role][round-1]


class Player(BasePlayer):
    answer = models.BooleanField(widget=widgets.RadioSelect,
                                 choices=((True, 'True'), (False, 'False')))

    def answer_error_message(self, answer):
        if answer != self.group.get_answer(self.role(), self.round_number):
            return 'Wrong answer!'

    def role(self):
        if 'role' not in self.participant.vars:
            if self.id_in_subsession % 2 == 1:
                self.participant.vars['role'] = 'S'
            else:
                self.participant.vars['role'] = 'R'
        return self.participant.vars['role']

    def num_questions(self):
        return self.group.questions_per_role(self.role())
