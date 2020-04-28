# Main program that create a new question

import json
from pathlib import Path

from . import me_question_db
from . import me_components


def me_question_create(question_id, num_answer_letters):
    # Function used to create a new question and save in the database
    # Input: Question ID, Number of letters the answer must have

    # Check configuration values
    config_file_path = Path.cwd().joinpath("me_question_creator_pkg", "config_file")
    with open(config_file_path, "r") as config:
        config_info = json.load(config)
    collection_size = config_info["COLLECTION_SIZE"]
    num_icons_sender = config_info["NUM_ICONS_SENDER"]
    position_list_size = config_info["POSITION_LIST_SIZE"]

    current_question = me_question_db.QuestionDB(question_id, num_answer_letters)

    # create one set of icons with random order for each letter
    icons = me_components.Icons(collection_size)
    for count_sets in range(current_question.num_answer_letters):
        current_question.append_icon_set(icons.random_order())

    #create one list with random positions for each letter
    for count_pos in range(current_question.num_answer_letters):
        position = me_components.PositionList(position_list_size, num_icons_sender)
        current_question.append_position_list(position.list)

    #save question to database
    current_question.save_info()
