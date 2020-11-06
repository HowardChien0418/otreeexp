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
This questionnaire is used to ensure that participants have understood the rules of the experiment correctly.
"""
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
    instruction_time_seconds = 5 * 60   # 5 minutes

    name_in_url = 'red_line_experiment'
    players_per_group = 2
    num_rounds = 50
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
    pass


class Group(BaseGroup):
    v = models.IntegerField()
    x = models.IntegerField()
    w1 = models.IntegerField()
    eps = models.IntegerField()
    sequence = models.IntegerField()
    bucket_is_golden = models.BooleanField()
    player_s_reported = models.BooleanField(initial=False, blank=True)
    bucket_guessed_gold = models.BooleanField()
    ball_is_gold = models.BooleanField()

    paid_round_number = models.IntegerField()
    def payoff_params(self):
        """ Non-trivial parameters of payoff matrices for the round """
        return {
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
            'silver_bucket_probability': round(1 - golden_bucket_probability,2),
            # 'golden_balls_golden_bucket': see Constants.golden_balls_golden_bucket in models.py
            'silver_balls_golden_bucket': Constants.total_balls - Constants.golden_balls_golden_bucket,
            # 'golden_balls_silver_bucket': see Constants.golden_balls_silver_bucket in models.py
            'silver_balls_silver_bucket': Constants.total_balls - Constants.golden_balls_silver_bucket
        }

    def set_payoffs(self):
        payoff_matrix = payoff_gold(self) if self.bucket_is_golden else payoff_silver(self)
        print("payoff matrix:",payoff_matrix)
        for player in self.get_players():

           # player.payoff = payoff_matrix[self.player_s_reported][not self.bucket_is_golden][player.is_player_r()]
            player.payoff = payoff_matrix[self.player_s_reported][not self.bucket_guessed_gold][player.is_player_r()]
            if 'payoffs' not in player.participant.vars:
                player.participant.vars['payoffs'] = []
            player.participant.vars['payoffs'].append(player.payoff)
            print("player payff:",player.payoff)

    def set_round_params(self):
        # Choose round which will be paid
        if self.round_number == Constants.num_rounds:
            self.paid_round_number = random.randint(1, Constants.num_rounds)
            print('Paid round number', self.paid_round_number)

        if self.round_number == 1:
            for player in self.get_players():
                if self.v == None and "v" in player.participant.vars:
                   self.v =  player.participant.vars["v"]
                if self.x == None and "x" in player.participant.vars:
                   self.x =  player.participant.vars["x"]
                if self.sequence == None and "sequence" in player.participant.vars:
                   self.sequence =  player.participant.vars["sequence"]
        else:
           # Reuse constant parameters from previous rounds
            previous = self.in_round(self.round_number - 1)
            self.sequence = previous.sequence
            self.v = previous.v
            self.x = previous.x

            print(f'Reused sequence={self.sequence}, v={self.v}, x={self.x}')

        # Generate parameters that change every round
        self.eps = random.choice(Constants.eps_choices)
        self.w1 = random.randint(Constants.w0 - self.eps, Constants.w0 + self.eps)

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

class Player(BasePlayer):

    def answer_error_message(self, answer):
        if answer != self.group.get_answer(self.role(), self.round_number):
            return 'Wrong answer!'

    def role(self):
        if 'role' not in self.participant.vars:
            raise Exception("Can't get role of player")
        return self.participant.vars['role']

    def is_player_s(self):
        return self.role() == 'S'

    def is_player_r(self):
        return self.role() == 'R'
