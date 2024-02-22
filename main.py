import sqlite3
import requests
import selectorlib
import smtplib
import ssl
import time

URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class Event:
    def scrape(self, url):
        """Scrape the page source from the URL"""
        response = requests.get(url, headers=HEADERS)
        source = response.text
        return source

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class Email:
    def send(self, message):
        host = "smtp.gmail.com"
        port = 465

        username = "username"
        password = "password"

        receiver = "receiver"
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, receiver, message)

        print("Email was sent!")


class Database:

    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)

    def store(self, extracted_):
        row_ = extracted_.split(",")
        row_ = [item.strip() for item in row_]
        cursor = self.connection.cursor()
        cursor.execute("insert into events values(?,?,?)", row_)
        self.connection.commit()

    def read(self, extracted_):
        row_ = extracted_.split(",")
        row_ = [item.strip() for item in row_]
        band, city, date = row_
        cursor = self.connection.cursor()
        cursor.execute("select * from events where band=? and city=? and date=?", (band, city, date))
        row_ = cursor.fetchall()
        print(row_)
        return row_


if __name__ == "__main__":
    while True:
        event = Event()
        source = event.scrape(URL)
        extracted = event.extract(source)
        print(extracted)

        if extracted != "No upcoming tours":
            database = Database(database_path="data.db")
            row = database.read(extracted)
            if not row:
                database.store(extracted)
                email = Email()
                email.send(message="Hey new event was found!")
        time.sleep(2)
