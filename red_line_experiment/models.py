import random

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
Red Line Experiment Application
"""

#def get_answer(role, round_number):
#    return Constants.questions_per_role[role][round_number - 1][1]

def payoff_gold(group):
    return [
        [(group.v, Constants.w0), (0, 0)],
        [(group.v - group.x, Constants.w0), (0, 0)]
    ]


def payoff_silver(group):
    return [
        [(0, 0), (group.v, group.w1)],
        [(-group.x, 0), (group.v, group.w1)]
    ]


def draw_boolean_weighted(true_weight):
    weights = [true_weight, 1 - true_weight]
    return random.choices(population=[True, False], weights=weights, k=1)[0]


def get_golden_bucket_probability(sequence, round_number):
    return Constants.golden_bucket_probabilities[sequence][round_number - 1]


class Constants(BaseConstants):
    name_in_url = 'red_line_experiment'
    instruction_time_seconds = 5 * 60   # 5 minutes
    questions_num =  {
            'S': 8,
            'R': 6
        }


    payoff_template_instructions = 'red_line_experiment/payoff_matrices_general.html'
    name_in_url = 'red_line_instruction_questionnaire'
    players_per_group = 2
    num_rounds = 50

    # Payoff matrix constants
    w0 = 50
    v_choices = [20, 30]
    x_choices = [5, 10]
    eps_choices = [20, 40]
    payoff_template = 'red_line_experiment/payoff_matrices.html'
    payoff_gold = 'red_line_experiment/payoff_gold.html'
    payoff_silver = 'red_line_experiment/payoff_silver.html'

    # Sequence constants
    golden_bucket_probabilities = {
        1: [0.7] * 20 + [0.5] * 20 + [0.7] * 10,
        2: [0.5] * 20 + [0.7] * 20 + [0.5] * 10,
    }

    # Bucket constants
    total_balls = 20
    golden_balls_golden_bucket = 14
    golden_balls_silver_bucket = 8
    bucket_ball_template = 'red_line_experiment/bucket_ball_params.html'

    # Descriptions
    bucket_type = {True: 'Gold', False: 'Silver'}
    ball_type = {True: 'Golden', False: 'Silver'}

    # Timer for making a decision
    # Currently this is implemented as a soft constraint, after decision_time_seconds an alert pops up.
    decision_time_seconds = 2 * 60
    timer_template = "red_line_experiment/timer.html"


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


    bucket_is_golden = models.BooleanField()
    player_s_reported = models.BooleanField(initial=False, blank=True)
    bucket_guessed_gold = models.BooleanField()
    ball_is_gold = models.BooleanField()

    sequence = models.IntegerField()
    paid_round_number = models.IntegerField()

    def payoff_params(self):
        """ Non-trivial parameters of payoff matrices for the round """
        print("roud is ", self.round_number)
        return {
            'v': self.v,
            'x': self.x,
            'v_minus_x': self.v - self.x,
            'x_neg': -self.x,
            'w1_lower_bound': Constants.w0 - self.eps,
            'w1_upper_bound': Constants.w0 + self.eps
        }

    def bucket_ball_params(self):
        """ Actual bucket and ball probabilities for the round """
        golden_bucket_probability = get_golden_bucket_probability(self.sequence, self.round_number)
        return {
            'golden_bucket_probability': golden_bucket_probability,
            'silver_bucket_probability': int((1 - golden_bucket_probability)*100)/100,
            # 'golden_balls_golden_bucket': see Constants.golden_balls_golden_bucket in models.py
            'silver_balls_golden_bucket': Constants.total_balls - Constants.golden_balls_golden_bucket,
            # 'golden_balls_silver_bucket': see Constants.golden_balls_silver_bucket in models.py
            'silver_balls_silver_bucket': Constants.total_balls - Constants.golden_balls_silver_bucket
        }

    def vars_for_template(self):
        previous = self.in_round(1)
        return dict(
            sequence = previous.sequence,
            v = previous.v,
            x = previous.x,
            )

    def set_round_params(self):
        print('Setting params for group', self.id_in_subsession, 'round', self.round_number)
        print('Players in the group', self.get_players())
        # Generate parameters that change every round



        # Choose round which will be paid
        if self.round_number == Constants.num_rounds:
            self.paid_round_number = random.randint(1, Constants.num_rounds)
            print('Paid round number', self.paid_round_number)

        if self.round_number == 1:
            # Generate parameters that are constant for the entire experiment
            self.sequence = 2 if self.id_in_subsession % 2 == 0 else 1
            self.x = random.choice(Constants.x_choices)

            print(f'Generated sequence={self.sequence}, v={self.v}, x={self.x}')
    #    else:
    #        # Reuse constant parameters from previous rounds
    #        previous = self.in_round(1)
    #        self.sequence = previous.sequence
    #        self.v = previous.v
    #        self.x = previous.x
    #        self.eps = previous.eps
    #        print(f'Reused sequence={self.sequence}, v={self.v}, x={self.x}')



        # Random bucket
        golden_bucket_probability = get_golden_bucket_probability(self.sequence, self.round_number)
        self.bucket_is_golden = draw_boolean_weighted(golden_bucket_probability)

        # Random ball from the chosen bucket
        if self.bucket_is_golden:
            golden_ball_probability = float(Constants.golden_balls_golden_bucket) / Constants.total_balls
        else:
            golden_ball_probability = float(Constants.golden_balls_silver_bucket) / Constants.total_balls

        self.ball_is_gold = draw_boolean_weighted(golden_ball_probability)

        print(f'Generated eps={self.eps}, w1={self.w1}, bucket_is_golden={self.bucket_is_golden}, '
              f'ball_is_gold={self.ball_is_gold}')

    def set_payoffs(self):

        payoff_matrix = payoff_gold(self) if self.bucket_is_golden else payoff_silver(self)
        for player in self.get_players():
            player.payoff = payoff_matrix[self.player_s_reported][not self.bucket_is_golden][player.is_player_r()]
            if 'payoffs' not in player.participant.vars:
                player.participant.vars['payoffs'] = []
            player.participant.vars['payoffs'].append(player.payoff)


class Player(BasePlayer):
    answer = models.BooleanField(widget=widgets.RadioSelect,
                                 choices=((True, 'True'), (False, 'False')))

    question_page = models.IntegerField(initial=1)

    def get_question_page(self):
        if "question_page" in self.participant.vars:
            return self.participant.vars['question_page']
        else:
            return 1


    def qlabel(self):
        questions_per_role = {
            'S': [
               ("As a Player S, if you draw a silver ball from the bucket, you can decide whether to "
             "report the color to Player R. True or False?", True),
            ("As a Player S, if you draw a golden ball from the bucket, you can decide whether to "
             "report the color to Player R. True or False?", False),
            ("If the bucket is Gold, you drew a golden ball from the bucket, and Player R chose "
             "Silver, your payoff of the round is 0. True or False?", True),
            ("If the bucket is Silver, you drew a silver ball from the bucket, and Player R chose "
             "Silver, your payoff of the round is "+str(self.group.v)+". True or False?", True),
            ("If you drew a silver ball from the bucket, you report the color to Player R and he or she "
             "chose Gold, X points will be deducted from your payoff. True or False?", True),
            ("If the bucket is Gold, you drew a golden ball from the bucket, and Player R chose Silver, "
             "Player R’s payoff of the round is "+str(Constants.w0)+". True or False?", False),
            ("If the bucket is Silver, you draw a golden ball from the bucket, and Player R chooses"
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
            ("If the bucket is Silver, you choose Silver, your payoff of the round is a value randomly"
                "drawn from [30 and 70] or [10 and 90]. You will know the exact value at the beginning"
                "of each round. True or False?", True),
            ("If the bucket is Gold, Player S reported Silver to you, and you chose Gold, Player S’s "
             "payoff of the round is "+str(self.group.v)+"-"+str(self.group.x)+". True or False?", True),
            ("If the bucket is Silver, Player S didn’t report the color of the ball he or she drawn to "
             "you, and you chose Gold, Player S’s payoff of the round is 0. True or False?", True),
            ("After the experiment, you will receive a payment consisting of the payoff of a randomly picked "
            "decision-making round plus one of lottery choice outcomes divided by 10, and the participation "
             "fee. True or False?", True)
            ],
        }
        return questions_per_role[self.role()][(self.get_question_page()-1)][0]

    def answer_error_message(self, value):

        answer_per_role = {
            'S': [(True),(False),(True),(True),(True),(False),(True),(True)],
            'R': [(True),(False),(True),(True),(True),(True)]
            }
        if value == answer_per_role[self.role()][self.get_question_page() -1]:
            if "question_page" in self.participant.vars:
                self.participant.vars['question_page'] = self.participant.vars['question_page'] +1
            else:
                self.participant.vars['question_page'] = 2
        else :
            return 'Wrong answer!'

    def vars_for_template(self):
        question_page = self.question_page
        sequence = self.group.sequence
        return dict(
            question_page=question_page,
            sequence = sequence,
            )


    def is_player_s(self):
        return self.role() == 'S'

    def is_player_r(self):
        return self.role() == 'R'

    def num_questions(self):
        return Constants.questions_num[self.role()]


    def role(self):
        if self.id_in_group == 1:
            self.participant.vars['role'] = 'S'
            return self.participant.vars['role']
        else:
             self.participant.vars['role'] = 'R'
             return self.participant.vars['role']
