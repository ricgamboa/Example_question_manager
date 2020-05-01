# Used only to test decrypt request

import sqlite3
import json
import requests


def find_question(qid):
    # Find and return question from the database
    connection = sqlite3.connect("question_answer_database.sqlite")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM question WHERE global_question_id = ?", (qid,))
    question_find = cursor.fetchone()
    connection.commit()
    cursor.close()
    if question_find is None:
        return "Not found"
    question = {"question_id": question_find[1], "number_letters": question_find[2],
                "icons_lists": json.loads(question_find[3]), "positions_lists": json.loads(question_find[4])}
    return question

def find_answer(question_id, user_id):
    # Find answer in database and convert to list

    connection = sqlite3.connect("question_answer_database.sqlite")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM answer WHERE question_id=? AND user_id=?", (question_id, user_id))
    answer_find = cursor.fetchone()
    connection.commit()
    cursor.close()
    if answer_find is None:
        return "Not found"

    answer = {"user_id": answer_find[1], "answer": answer_find[2], "question_id": answer_find[3]}
    return answer


def send_answer(url, answer_send):

    try:
        response = requests.post(url=url, json=answer_send)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    print("Status code: ", response.status_code)


def send_question(url, question_send):

    try:
        response = requests.post(url=url, json=question_send)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    print("Status code: ", response.status_code)


def request_decription(user_id, question_id, url):

    params = {"user": user_id, "question": question_id}
    try:
        response = requests.get(url=url, params=params)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    decription = response.json()
    print(decription)


def main():
    user_id = input("Enter user global id: ")
    question_id = input("Enter questtion global id: ")

    answer = json.dumps(find_answer(question_id, user_id))

    question = json.dumps(find_question(question_id))

    url_send_answer = "http://localhost:8080/new_answer/"
    url_send_question = "http://localhost:8080/new_question/"
    url_request = "http://localhost:8080/solve_answer/"


    send_answer(url_send_answer, answer)
    send_question(url_send_question, question)
    request_decription(user_id, question_id,  url_request)

if __name__ == "__main__":
    main()