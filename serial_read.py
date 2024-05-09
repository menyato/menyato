import serial
import time
import requests

arduino_port = 'COM6'
baud_rate = 9600

arduino = serial.Serial(port=arduino_port, baudrate=baud_rate, timeout=1)

def send_transcription(serial_sent):
    # Define the Flask server URL
    server_url = "http://172.20.10.3:5000/receive_serial"

    # Send a POST request with the transcription data
    response = requests.post(server_url, json={"Serial": serial_sent})

    # Print the response from the Flask server
    print("Response from server:", response.text)


def send_command(command):
    arduino.write(command.encode())  # Encode the command as bytes and send it
    time.sleep(0.1)  # Wait for a short time to let Arduino process the command

def read_command():
    serial_input = arduino.readline().decode().strip()
    return serial_input
    
    
def read_command():
    serial_input = arduino.readline().decode().strip()
    return serial_input

program_started = False

while True:
    command = read_command()
    
    if command == "Start":
        if not program_started:
            print("Program started")
            program_started = True
            
            # Read commands and perform actions until "Start" is received again
            while True:
                command = read_command()
                # Example action based on command
                if command == "OOA":
                    print("On and Off Appliances")
                    send_transcription(command)
                    
                elif command == "LUD":
                    print("Lock and Unlock the door")
                    send_transcription(command)
                # Break the loop if "Start" is received again
                elif command == "OCW":
                    print("Open and Close the window")
                    send_transcription(command)
                # Break the loop if "Start" is received again
                elif command.startswith("Distance: "):
                    print("Serial send:", command)
                    send_transcription(command)
            
                if command == "Start":
                    print("Stopping program...")
                    program_started = False
                    break
        else:
            print("Program already started, stopping...")
            program_started = False
    else:
        print("Can't start the program")

    









