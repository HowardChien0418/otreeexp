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
Lottery Choice Task Application.
"""


def lottery_prize(choice_number, option):
    if option not in ['A', 'B']:
        raise ValueError('Bad option')
    weights = [float(el) / 100 for el in Constants.outcome_probability_percent[choice_number - 1]]
    choices = random.choices(population=Constants.outcomes[option],
                             weights=weights,
                             k=1)
    return choices[0]


def get_option_description(option, choice_number):
    """
    Generates descriptions of possible options.

    :param option: A or B
    :param choice_number: number of choice from 1 to Constants.num_choices (10 currently)
    :return: dictionary with probabilities and prizes that are possible, for example:
        {'prob1': 10, 'prize1': 20, 'prob2': 90, 'prize2': 16}
    """
    if option not in ["A", "B"]:
        raise ValueError("Bad option")
    if choice_number < 1 or choice_number > Constants.num_choices:
        raise ValueError("Bad choice number")
    possible_outcomes = Constants.outcomes[option]
    probabilities = Constants.outcome_probability_percent[choice_number - 1]
    return dict(prob1=probabilities[0],
                prize1=possible_outcomes[0],
                prob2=probabilities[1],
                prize2=possible_outcomes[1])


def make_choice_field(choice_number):
    """
    Creates field for each choice in the lottery.
    Label includes HTML code of the corresponding field, which makes it easier to use in the template.

    :param choice_number: number of choice from 1 to Constants.num_choices (10 currently)
    :return: HTML for table row containing probabilities and prizes for options A and B
    """
    if choice_number < 1 or choice_number > Constants.num_choices:
        raise ValueError("Bad choice number")

    option_a = get_option_description("A", choice_number)
    option_b = get_option_description("B", choice_number)

    label = f"""
        <td>{ option_a["prob1"] }%</td>
        <td>{ option_a["prize1"] }</td>
        <td>{ option_a["prob2"] }%</td>
        <td>{ option_a["prize2"] }</td>
        <td>{ option_b["prob1"] }%</td>
        <td>{ option_b["prize1"] }</td>
        <td>{ option_b["prob2"] }%</td>
        <td>{ option_b["prize2"] }</td>
    """
    return models.BooleanField(widget=widgets.RadioSelectHorizontal,
                               label=label,
                               choices=((True, 'A'), (False, 'B')))


class Constants(BaseConstants):
    # Lottery settings
    outcomes = {
        'A': [20, 16],
        'B': [38.5, 1]
    }
    outcome_probability_percent = [(p, 100 - p) for p in range(10, 101, 10)]
    num_choices = len(outcome_probability_percent)

    name_in_url = 'red_line_lottery'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    """
    Choices are stored in fields from `choice_1` to `choice_10`.
    True (1) or False (0) mean that options A or B were chosen, respectively.
    """

    choice_1 = make_choice_field(choice_number=1)
    choice_2 = make_choice_field(choice_number=2)
    choice_3 = make_choice_field(choice_number=3)
    choice_4 = make_choice_field(choice_number=4)
    choice_5 = make_choice_field(choice_number=5)
    choice_6 = make_choice_field(choice_number=6)
    choice_7 = make_choice_field(choice_number=7)
    choice_8 = make_choice_field(choice_number=8)
    choice_9 = make_choice_field(choice_number=9)
    choice_10 = make_choice_field(choice_number=10)

    def run_lottery(self):
        """
        Runs the lottery and stores the result: realized choice number, realized option and payoff.
        """
        choices = [self.choice_1, self.choice_2, self.choice_3, self.choice_4, self.choice_5,
                   self.choice_6, self.choice_7, self.choice_8, self.choice_9, self.choice_10]

        realized_choice_number = random.randint(1, Constants.num_choices)
        realized_option = 'A' if choices[realized_choice_number - 1] else 'B'
        self.payoff = lottery_prize(realized_choice_number, realized_option)

        # Store the outcomes
        self.participant.vars['realized_choice_number'] = realized_choice_number
        self.participant.vars['realized_option'] = realized_option
        self.participant.vars['lottery_payoff'] = self.payoff

