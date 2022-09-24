from flask import Flask
from faker import Faker
from pathlib import Path
from _collections_abc import Generator
from typing import Any
import json
import requests
import csv

app = Flask(__name__)
fake = Faker()

file_path = Path("test_for_route")
UPLOAD_FOLDER = "/path/to/the/uploads"


# Main page
@app.route("/")
def main_page() -> str:
    return (
        "<h1> Welcome to the home page!</h1>"
        "<h3><li><a href='/requirements/'>requirements</a></li></h3>"
        "<h3><li><a href='/generate-users/'>generate-users</a></li></h3>"
        "<h3><li><a href='/space/'>space</a></li></h3>"
        "<h3><li><a href='/mean/'>mean</a></li></h3>"
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


if __name__ == "__main__":
    app.run(debug=True)
