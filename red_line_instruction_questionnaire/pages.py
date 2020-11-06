from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


#def get_question(role, round_number):
#    return Constants.questions_per_role[role][round_number][0]


class InstructionForAllPage(Page):
    # timeout_seconds = Constants.instruction_time_seconds

    def is_displayed(self) -> bool:
        """
        To be displayed only in the beginning.
        """
        return self.round_number == 1


class InstructionForPlayerPage(InstructionForAllPage):
    pass


class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['answer']

    def vars_for_template(self) -> dict:
        return dict(question=self.group.get_question(self.player.role(), self.round_number))


class Results(Page):
    def is_displayed(self) -> bool:
        """
        To be displayed only after the final question.
        """
        return self.round_number == self.player.num_questions()

    def app_after_this_page(self, upcoming_apps):
        self.setparameters_for_nextapp()
        """
        Go the next app after this page.
        It allows to control number of questions for each player separately.
        """
        return upcoming_apps[0]

    def setparameters_for_nextapp(self):
        self.player.participant.vars['v'] = self.group.v
        self.player.participant.vars['x'] = self.group.x
        self.player.participant.vars['sequence'] = self.group.sequence
        self.player.participant.vars['sequence'] = self.group.sequence


page_sequence = [
    InstructionForAllPage,
    InstructionForPlayerPage,
    Questionnaire,
    Results
]
