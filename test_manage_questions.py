# Used only to test, real question manager server could use several ways
# to create and distribute the questions to the users

import sqlite3
import json

import me_question_creator_pkg


def find_question(qid):
    # Find and return question from the database
    connection = sqlite3.connect("question_database.sqlite")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM question WHERE global_question_id = ?", (qid,))
    question_find = cursor.fetchone()
    if question_find == None:
        return "Not found"
    else:
        question = {"question_id":question_find[1], "number_letters":question_find[2], "icons_lists":question_find[3],
                    "icons_lists":question_find[3], "positions_lists":question_find[4]}
        return question

def create_ten_questions(number_of_letters):
    # Only for test, create ten questions
    connection = sqlite3.connect("question_database.sqlite")
    cursor = connection.cursor()

    # Erase current database and create some new questions
    cursor.executescript("DROP TABLE IF EXISTS question")
    for qid in range(100, 111):
        me_question_creator_pkg.me_question_create(qid, number_of_letters)
    connection.commit()
    cursor.close()

def save_answer(answer):
    # Save answer to database
    connection = sqlite3.connect("answer_database.sqlite")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS answer("
                     "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,"
                     "user_id INTEGER,"
                     "answer TEXT,"
                     "question_id INTEGER)")
    cursor.execute("INSERT INTO answer (user_id,answer,question_id) VALUES (?,?,?)",
                   (answer["user_id"],json.dumps(answer["answer"]),answer["question_id"]))
    connection.commit()
    cursor.close()

def main():
    create = input("Do you want to create some questions [Y/N]: ")
    if create.lower() == "y" or create == "yes":
        create_ten_questions(2)

if __name__ == "__main__":
    main()