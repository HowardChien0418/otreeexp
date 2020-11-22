from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class GroupArrivedPlayersPage(WaitPage):
    body_text = "稍待另一位玩家..."

    def is_displayed(self) -> bool:
        return self.round_number == 1


class SetupRoundParametersPage(WaitPage):
    body_text = "稍待另一位玩家..."
    after_all_players_arrive = 'set_round_params'


class GameStartPage(Page):
    def vars_for_template(self) -> dict:
        vars_for_template = self.group.payoff_params()
        for param, value in self.group.bucket_ball_params().items():
            vars_for_template[param] = value
        return vars_for_template


class GameStartWaitPage(WaitPage):
    body_text = "稍待另一位玩家..."


class PlayerSTurn(Page):
    form_model = 'group'
    form_fields = ['player_s_reported']

    def is_displayed(self) -> bool:
        return self.player.is_player_s()

    def vars_for_template(self) -> dict:
        vars_for_template = self.group.payoff_params()
        for param, value in self.group.bucket_ball_params().items():
            vars_for_template[param] = value
        vars_for_template['ball_type'] = Constants.ball_type[self.group.ball_is_gold]
        return vars_for_template


class PlayerRTurn(Page):
    form_model = 'group'
    form_fields = ['bucket_guessed_gold']

    def is_displayed(self) -> bool:
        return self.player.is_player_r()

    def vars_for_template(self) -> dict:
        vars_for_template = self.group.payoff_params()
        for param, value in self.group.bucket_ball_params().items():
            vars_for_template[param] = value
        return vars_for_template


class WaitPlayerS(WaitPage):
    def vars_for_template(self) -> dict:
        return dict(
            title_text=f"Round {self.round_number}: Please wait",
            body_text="稍待 Player S 做決策..."
        )


class WaitPlayerR(WaitPage):
    after_all_players_arrive = 'set_payoffs'

    def vars_for_template(self) -> dict:
        return dict(
            title_text=f"Round {self.round_number}: Please wait",
            body_text="Player R 正在做決策..."
        )


class Results(Page):
    def vars_for_template(self) -> dict:
        vars_for_template = self.group.payoff_params()
        vars_for_template['bucket_guessed'] = Constants.bucket_type[self.group.bucket_guessed_gold]
        vars_for_template['bucket_type'] = Constants.bucket_type[self.group.bucket_is_golden]
        return vars_for_template

    def before_next_page(self):
        if self.round_number == Constants.num_rounds:
            self.participant.vars['experiment_payoff'] = self.participant.vars['payoffs'][
                self.group.paid_round_number - 1
            ]


page_sequence = [
    GroupArrivedPlayersPage,
    SetupRoundParametersPage,
    GameStartPage,
    GameStartWaitPage,
    PlayerSTurn,
    WaitPlayerS,
    PlayerRTurn,
    WaitPlayerR,
    Results
]
