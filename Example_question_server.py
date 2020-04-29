# Used only to test, real question manager server could use several ways
# to create and distribute the questions to the users

from random import randint
import flask
from flask import request, jsonify

import test_manage_questions


def main():
    # Server confguration
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True

    @app.route('/question_server/', methods=["GET", "POST"])
    def send_question():
        # Select a random question
        qid = randint(100, 110)
        question = test_manage_questions.find_question(qid)
        return jsonify(question)

    @app.route('/new_answer/', methods=["GET", "POST"])
    def add_new_answer():
        # Receive the answer from the user POST and save
        if request.method == "POST":
            answer = request.get_json()
            test_manage_questions.save_answer(answer)
            return "answer saved"
        return "Error"

    app.run(port=8080)

if __name__ == "__main__":
    main()
