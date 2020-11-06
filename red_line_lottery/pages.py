from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import math


class StartPage(Page):
    def is_displayed(self) -> bool:
        """
        To be displayed only in the beginning.
        """
        return self.round_number == 1


class LotteryRound(Page):
    form_model = 'player'
    form_fields = ['choice_1', 'choice_2', 'choice_3', 'choice_4', 'choice_5',
                   'choice_6', 'choice_7', 'choice_8', 'choice_9', 'choice_10']

    def before_next_page(self):
        self.player.run_lottery()


class Results(Page):
    def is_displayed(self) -> bool:
        """
        To be displayed only after the final question.
        """
        return self.round_number == Constants.num_rounds

    def vars_for_template(self) -> dict:
        return dict(realized_choice_number=self.participant.vars['realized_choice_number'],
                    realized_option=self.participant.vars['realized_option'])

    def before_next_page(self):
        """ Calculate final payoff """
        self.participant.payoff = self.participant.vars['experiment_payoff'] + self.participant.vars['lottery_payoff']


page_sequence = [
    StartPage,
    LotteryRound,
    Results
]
