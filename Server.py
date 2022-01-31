import paho.mqtt.client as mqtt
import sqlite3
import time
import datetime

broker = "localhost"
port=8883
# The MQTT client.
client = mqtt.Client()

connection = sqlite3.connect("RFIDcards.db", check_same_thread=False)
cursor = connection.cursor()


def reception_process(message_decoded):
    print(message_decoded)
    uid_card = message_decoded[0]
    cursor.execute("SELECT * FROM RFIDcards WHERE uid = " + uid_card)
    card = cursor.fetchall()
    if len(card) == 1:
        cursor.execute("DELETE FROM RFIDcards WHERE uid = " + uid_card)
    
    if len(message_decoded) == 4:
        room = message_decoded[1]
        end_date = message_decoded[2] + " 11:00:00"
        guestId = message_decoded[3]
        cursor.execute("INSERT INTO RFIDcards VALUES(?,?,?,?)", (uid_card, room, end_date, guestId))
    connection.commit()


def rooms_process(message_decoded):
    print(message_decoded)
    uid_card = message_decoded[0]
    current_date = message_decoded[1]
    room_addr = message_decoded[2]

    cursor.execute("SELECT * FROM RFIDcards WHERE uid = " + uid_card)
    card = cursor.fetchall()
    if len(card) == 1:
        card = card[0]
    

    current_date = datetime.datetime.strptime(current_date, '%d/%m/%y %H:%M:%S')
    if len(card) > 2:
        end_date = datetime.datetime.strptime(card[2], '%d/%m/%y %H:%M:%S')

        if current_date <= end_date:        
            if room_addr == card[1]:
               client.publish("rooms/" + room_addr, "1, Drzwi otwarte.") 

            else:
                client.publish("rooms/" + room_addr, "0, Karta do innego pokoju.")
        else:
            client.publish("rooms/" + room_addr, "0, Karta nie jest juz wazna.")
    else:
        client.publish("rooms/" + room_addr, "0, Niepoprawna karta.")    
    connection.commit()



def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8"))).split(",")
    if message.topic == "reception":
        reception_process(message_decoded)
    elif message.topic == "rooms":
        rooms_process(message_decoded)


def connect_to_broker():
    client.username_pw_set(username='server', password='pass')
    client.tls_set('ca.crt')
    client.tls_insecure_set(True)
    client.connect(broker,port)
    client.on_message = process_message
    client.loop_start()
    client.subscribe("rooms")
    client.subscribe("reception")


def disconnect_from_broker():
    client.loop_stop()
    client.disconnect()


def run_receiver():
    connect_to_broker()
    while True:
        pass
    disconnect_from_broker()


if __name__ == "__main__":
    run_receiver()