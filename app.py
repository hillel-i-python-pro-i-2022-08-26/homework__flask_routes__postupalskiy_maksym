from flask import Flask, Response
from faker import Faker
from pathlib import Path
from _collections_abc import Generator
from typing import Any
import json
import requests
import csv
from webargs import fields
from webargs.flaskparser import use_args


from application.services.db_table import create_table
from application.services.db_connection import DBConnection

app = Flask(__name__)
fake = Faker()

file_path = Path("test_for_route")


# Main page
@app.route("/")
def main_page() -> str:
    return (
        "<h1> Welcome to the home page!</h1>"
        "<h3><li><a href='/requirements/'>requirements</a></li></h3>"
        "<h3><li><a href='/generate-users/'>generate-users</a></li></h3>"
        "<h3><li><a href='/space/'>space</a></li></h3>"
        "<h3><li><a href='/mean/'>mean</a></li></h3>"
        "<h3><li><a href='/phones/create'>create table</a></li></h3>"
        "<h3><li><a href='/phones/read-all'>read all</a></li></h3>"
        "<h3><li><a href='/phones/read/'>read for id</a></li></h3>"
        "<h3><li><a href='/phones/update/'>update</a></li></h3>"
        "<h3><li><a href='/phones/delete/'>delete</a></li></h3>"
    )


# Requirements
@app.route("/requirements/")
def txt_reader() -> str:
    return "".join(f"<p>{i}</p>" for i in file_path.read_text().splitlines())


# Name generator
def name_generator() -> str:
    name = fake.first_name()
    email = f"{name}@{fake.domain_name()}"
    return f"{name} - {email}"


# Users generator
@app.route("/generate-users/")
@app.route("/generate-users/<int:amount>")
def generate_users(amount: int = 100) -> Generator[str, Any, None]:
    for index in range(amount):
        yield f"<p>{index + 1}. {name_generator()}<p>"


# Space(json reader)
@app.route("/space/")
def json_reader() -> str:
    url = "http://api.open-notify.org/astros.json"
    response = requests.get(url)
    text = response.text
    json_file = json.loads(text)
    return f"На данный в момент в космосе прибывает столько космонавтов: {json_file['number']}"


# Mean calculator
@app.route("/mean/")
def mean() -> str:
    total_height = 0
    total_weight = 0
    total_index = 0
    cvs_url = "https://drive.google.com/uc?export=download&id=1yM0a4CSf0iuAGOGEljdb7qcWyz82RBxl"
    with requests.Session() as s:
        download = s.get(cvs_url)
    decoded_content = download.content.decode("utf-8")
    reader = csv.DictReader(decoded_content.splitlines())
    for row in reader:
        total_height += float(list(row.values())[1]) * 2.54
        total_weight += float(list(row.values())[2]) * 0.45
        total_index += 1
    average_height = total_height / total_index
    average_weight = total_weight / total_index
    return (
        f"<p>Average height: {round(average_height, 2)} cm.</p>"
        f"<p>Average weigh: {round(average_weight, 2)} kg.</p>"
        f"<p>Number of participants: {total_index}."
    )


@app.route("/phones/create")
@use_args(
    {"contactName": fields.Str(required=True), "phoneValue": fields.Int(required=True)},
    location="query",
)
def phones_create(args):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                """INSERT INTO phones (contactName, phoneValue)
                VALUES (:contactName, :phoneValue);""",
                {"contactName": args["contactName"], "phoneValue": args["phoneValue"]},
            )
    return "OK"


@app.route("/phones/read-all")
def phones__read_all():
    with DBConnection() as connection:
        phones = connection.execute(
            """
            SELECT * FROM phones;
        """
        ).fetchall()
    return "<br>".join(
        [
            f'{value["phoneID"]}: {value["contactName"]} - {value["phoneValue"]}'
            for value in phones
        ]
    )


@app.route("/phones/read/<int:phone_id>")
def users__read(phone_id: int):
    with DBConnection() as connection:
        value = connection.execute(
            """
            SELECT * FROM phones
            WHERE (phoneID=:phone_id);
            """,
            {
                "phone_id": phone_id,
            },
        ).fetchone()

    return f'{value["phoneID"]}: {value["contactName"]} - {value["phoneValue"]}'


@app.route("/phones/update/<int:phone_id>")
@use_args({"phoneValue": fields.Int(), "contactName": fields.Str()}, location="query")
def phones__update(
    args,
    phone_id: int,
):
    with DBConnection() as connection:
        with connection:
            name = args.get("contactName")
            phone = args.get("phoneValue")
            if name is None and phone is None:
                return Response(
                    "Need to provide at least one argument",
                    status=400,
                )

            args_for_request = []
            if name is not None:
                args_for_request.append("contactName=:name")
            if phone is not None:
                args_for_request.append("phoneValue=:phone")

            args_2 = ", ".join(args_for_request)

            connection.execute(
                "UPDATE phones "
                f'SET {", ".join(args_for_request)} '
                "WHERE phoneID=:phone_id;",
                {
                    "phone_id": phone_id,
                    "phone": phone,
                    "name": name,
                },
            )

    return "Ok"


@app.route("/phones/delete/<int:phone_id>")
def users__delete(phone_id):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "DELETE " "FROM phones " "WHERE (phoneID=:phone_id);",
                {
                    "phone_id": phone_id,
                },
            )

    return "Ok"


create_table()

if __name__ == "__main__":
    app.run(debug=True)
