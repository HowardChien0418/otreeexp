from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

def get_question(group, role, pair_num):
    return Questionnaire.get_question(group,role,pair_num)

class GroupArrivedPlayersPage(WaitPage):
    body_text = "Wait for another participant..."
   # group_by_arrival_time = True

    def is_displayed(self) -> bool:
        return self.round_number == 1


class SetupRoundParametersPage(WaitPage):
    body_text = "Wait for another participant..."
    after_all_players_arrive = 'set_round_params'


class GameStartPage(Page):
    def vars_for_template(self) -> dict:
        vars_for_template = self.group.payoff_params()
        for param, value in self.group.bucket_ball_params().items():
            vars_for_template[param] = value
        return vars_for_template


class GameStartWaitPage(WaitPage):
    body_text = "Wait for another participant..."


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
            body_text="Wait while Player S is making a decision..."
        )


class WaitPlayerR(WaitPage):
    after_all_players_arrive = 'set_payoffs'

    def vars_for_template(self) -> dict:
        return dict(
            title_text=f"Round {self.round_number}: Please wait",
            body_text="Wait while Player R is making a decision..."
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

class InstructoionsEnd(Page):
    def is_displayed(self) -> bool:
        """
        To be displayed only after the final question.
        """
        return self.round_number == self.player.num_questions()

    def app_after_this_page(self, upcoming_apps):
        """
        Go the next app after this page.
        It allows to control number of questions for each player separately.
        """
        return upcoming_apps[0]

class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['answer']

    def is_displayed(self):
        return self.round_number == 1 and self.player.get_question_page() <= Constants.questions_num[self.player.role()]


class InstructionForAllPage(Page):
    # timeout_seconds = Constants.instruction_time_seconds

    def is_displayed(self) -> bool:
        """
        To be displayed only in the beginning.
        """
        return self.round_number == 1



class InstructionForPlayerPage(InstructionForAllPage):
    def is_displayed(self) -> bool:
        """
        To be displayed only in the beginning.
        """
        return self.round_number == 1

    def vars_for_template(self) -> dict:
        vars_for_template = self.group.payoff_params()
        return vars_for_template

page_sequence = [
    InstructionForAllPage,
    InstructionForPlayerPage,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    InstructoionsEnd,
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
