import serial
import time
import threading
import requests
from flask import Flask, request, jsonify

arduino_port = 'COM16'
baud_rate = 9600

arduino = serial.Serial(port=arduino_port, baudrate=baud_rate, timeout=1)

app = Flask(__name__)

def send_command(command):
    arduino.write(command.encode())  # Encode the command as bytes and send it
    time.sleep(0.1)  # Wait for a short time to let Arduino process the command

def send_transcription(serial_sent):
    # Define the Flask server URL
    server_url = "http://192.168.1.12:5000/receive_serial"

    # Send a POST request with the transcription data
    response = requests.post(server_url, json={"Serial": serial_sent})

    # Print the response from the Flask server
    response_json = response.json()
    latest_serial_input = response_json.get("latest_serial_input")
    print("Response from server:", response_json)

@app.route("/send_vibrate", methods=["POST"])
def handle_send_vibrate():
    data = request.get_json()
    command = data.get("command")
    if command == "vibrate":
        send_command("M")
        print("VibMotion")
        return jsonify({"status": "vibration_command_received"})
    elif command == "vibrateA":
        send_command("A")
        print("VibAppliance")
        return jsonify({"status": "unknown_command"})
    elif command == "vibrateD":
        send_command("D")
        print("VibDoor")
        return jsonify({"status": "unknown_command"})
    elif command == "vibrateW":
        send_command("W")
        print("VibWindow")
        return jsonify({"status": "unknown_command"})
def read_command():
    serial_input = arduino.readline().decode().strip()
    return serial_input

def arduino_loop():
    program_started = False
    counter = 0
    counter1 = 0
    counter2 = 0

    while True:
        command = read_command()

        if command == "Start":
            if not program_started:
                print("Program started")
                program_started = True

                # Read commands and perform actions until "Start" is received again
                while program_started:
                    command = read_command()
                    if command:
                        print(f"Received command: {command}")
                        if command == "OOA":
                            if counter1 % 2 == 0:
                                print("ON Appliances")
                                send_transcription("ONA")
                            else:
                                print("Off Appliances")
                                send_transcription("OFA")
                            counter1 += 1
                        elif command == "LUD":
                            if counter % 2 == 0:
                                print("Lock and Unlock the door")
                                send_transcription("Locked")
                            else:
                                print("Lock and Unlock the door")
                                send_transcription("Unlocked")
                            counter += 1
                        elif command == "OCW":
                            if counter2 % 2 == 0:
                                print("Open the window")
                                send_transcription("Open")
                            else:
                                print("Close the window")
                                send_transcription("Close")
                            counter2 += 1
                        elif command.startswith("Distance: "):
                            print("Serial send:", command)
                            send_transcription(command)
                        elif command == "MotionDetected":
                            print("Motion detected")
                            send_transcription("MotionDetected")
                        elif command == "Start":
                            print("Stopping program...")
                            program_started = False
                            break
            else:
                print("Program already started, stopping...")
                program_started = False
        else:
            print("Can't start the program")

def run_flask_app():
    app.run(debug=False, host='0.0.0.0', port=5001)

if __name__ == "__main__":
    # Create a thread for the Arduino loop
    arduino_thread = threading.Thread(target=arduino_loop)
    arduino_thread.daemon = True
    arduino_thread.start()

    # Run the Flask app
    run_flask_app()
    
