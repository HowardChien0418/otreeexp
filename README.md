# otree_redlink
Decision Making Experiment on oTree

## Usage

1. Install oTree, for instructions see https://otree.readthedocs.io/en/latest/install.html.

2. Clone this repository.

3. Run the `./run.sh` script which will launch the otree server.
3.1 (Troubeshooting) If the command does not work you may have to run `chmod +x ./run.sh` before.

4. Open the mentioned IP address.

5. You can launch demo for the experiment by clicking `Red Line Experiment` link, or proceed to the `Sessions` tab to create real experiment. 

## Structure

oTree experiments contain sequence of oTree applications, which are launched one after another. This project includes the following applications:

 * `red_line_instruction_questionnaire` - questionnaire about the instructions
 
 * `red_line_experiment` - the main experiment (50 rounds)
 
 * `red_line_lottery` - lottery choice task (10 rounds)
 
 * `red_line_demographic_survey` - final survey

Other folders in the repository contain sample games provided by oTree, which can be removed if not needed.

## Parameters

A list of parameters of the experiment is presented below. Parameters are grouped by application they belong 
to, proceed to the `Constants` class in the `models.py` in the corresponding folder to change anything.

### red_line_instruction_questionnaire
 
 * `questions_per_role` - questions for the participants, use the following format:

    ```
        {
            'S': [
                (question1, expected_answer1 [True/False]),
                ...
            ]
            'R': [
                (question1, expected_answer1 [True/False]),
                ...
            ]
        }
    ```
   
   **Note:** you can use HTML tags in questions, formatting will be displayed. Also you can add/remove questions.

 * `instruction_time_seconds` - time that participants have to examine the instructions (in seconds).
 
### red_line_experiment

 * `num_rounds` - number of game rounds.
 
 * `decision_time_seconds` - time that participants have to make a decision (in seconds).
 
    **Note:** during the experiment, timeout is soft, and user is only asked to proceed further. It is implemented
    this way in order to avoid answers that are auto-submitted in case of hard timeout and to give people an opportunity to answer themselves.

 * `w0` - value of W<sub>0</sub>.
 
 * `v_choices, x_choices, eps_choices` - lists of values, which are used to generate V, X, and &epsilon;, respectively.
 
 * `bucket_probabilities` - probability of having a golden bucket for each round for each sequence, format:
 
   ```
   bucket_probabilities = {
       1: [0.3, ..., 0.3, 0.5, ..., 0.5, 0.3, ..., 0.3],   # sequence 1
       2: [0.5, ..., 0.5, 0.3, ..., 0.3, 0.5, ..., 0.5]   # sequence 2
   }
   ```
   
 * `total_balls` - the amount of balls in buckets.
 
 * `golden_balls_golden_bucket` - a list of options for the amount of golden balls in the golden bucket.
 
 * `golden_balls_silver_bucket` - the amount of golden balls in the silver bucket.

### red_line_lottery

 * `outcomes` - dictionary of possible prizes for options, format:
 
   ```
   outcomes = {
      'A': [20, 16],
      'B': [38.5, 1]
   } 
   ```
   
 * `outcome_probability_percent` - a list of probabilities of the first outcome in each lottery choice.
 
### red_line_demographic_survey

Everything is described in the fields of the `Player` class.