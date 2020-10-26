from typing import List

from ._builtin import Page


class GeneralSurvey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'nationality', 'race', 'is_student']


class BackgroundSurvey(Page):
    form_model = 'player'

    def get_form_fields(self) -> List[str]:
        """ Provides relevant form fields depending on whether the player is a student. """
        if self.player.is_student:
            return ['student_semesters', 'student_program']
        else:
            return ['highest_degree', 'current_occupation']


class ExperimentSurvey(Page):
    form_model = 'player'
    form_fields = ['similar_experiment_before', 'find_instructions_clear', 'comments']


class Results(Page):
    def vars_for_template(self) -> dict:
        return dict(
            experiment_payoff_usd=self.participant.vars['experiment_payoff'].to_real_world_currency(self.session),
            lottery_payoff_usd=self.participant.vars['lottery_payoff'].to_real_world_currency(self.session)
        )


page_sequence = [
    GeneralSurvey,
    BackgroundSurvey,
    ExperimentSurvey,
    Results
]
