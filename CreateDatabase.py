#!/usr/bin/env python3

import sqlite3
import time
import os


def create_database():
    if os.path.exists("RFIDcards.db"):
        os.remove("RFIDcards.db")
        print("An old database removed.")
    connection = sqlite3.connect("RFIDcards.db")
    cursor = connection.cursor()
    cursor.execute(""" CREATE TABLE RFIDcards(
        uid text primary key,
        room text,
        endDate text,
        guestId text
    )""")
    connection.commit()
    connection.close()
    print("The new database created.")


if __name__ == "__main__":
    create_database()