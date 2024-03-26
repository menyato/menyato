import speech_recognition as sr
import requests
import pyaudio
import sys  # Import sys module for exiting the script
from time import sleep

import wiringpi as wp

in1 = 24 #for the first motor
in2 = 23 #for the first motor 
in3 = 5 #for the second motor
in4 = 6 #for the second motor 
en = 25
temp1 = 1

wp.wiringPiSetup()

wp.pinMode(in1, wp.GPIO.OUTPUT)
wp.pinMode(in2, wp.GPIO.OUTPUT)
wp.pinMode(in3, wp.GPIO.OUTPUT)
wp.pinMode(in4, wp.GPIO.OUTPUT)
wp.pinMode(en, wp.GPIO.OUTPUT)

wp.digitalWrite(in1, wp.GPIO.LOW)
wp.digitalWrite(in2, wp.GPIO.LOW)
wp.digitalWrite(in3, wp.GPIO.LOW)
wp.digitalWrite(in4, wp.GPIO.LOW)

p = wp.softPwmCreate(en, 0, 100)

def speech_to_text(language='en-US'):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(source, timeout=3)
            transcription = recognizer.recognize_google(audio, language=language)
            print("Transcription:", transcription)

            # Send the transcription to the Flask server
            send_transcription(transcription)
            
            if transcription.lower() == "move forward":
                move_motor("f")
                print("Forward")
                
            elif transcription.lower() == "move back":
                move_motor("b")
                print("Backward")
            elif transcription.lower() == "move to the right":
                move_motor("r")
                print("right")
            elif transcription.lower() == "move to the left":
                move_motor("l")
                print("left")
            elif transcription.lower() == "stop the movement right now":
                move_motor("s")
                print("stop")
                
                
            if transcription.lower() == "quit the program":
                print("Exiting the program.")
                sys.exit()  # Exit the script if the user says "quit"

        except sr.UnknownValueError:
            transcription = "Please Repeat I could not understand"
            send_transcription(transcription)
            print("Please Repeat I could not understand.")
        except sr.WaitTimeoutError:
            print("Timeout occurred. No speech detected.")
            
            



def send_transcription(transcription):
    # Define the Flask server URL
    server_url = "http://192.168.1.159:5000/receive_transcription"

    # Send a POST request with the transcription data
    response = requests.post(server_url, json={"transcription": transcription})

    # Print the response from the Flask server
    print("Response from server:", response.text)

def audio_receive():
    # Define the Flask server URL
    server_url = "http://192.168.1.159:5000/static/output.wav"
    response = requests.get(server_url)
    if response.status_code == 200:
        p = pyaudio.PyAudio()

        # Open stream
        stream = p.open(format=p.get_format_from_width(2),  # Adjust based on your audio data
                        channels=1,  # Adjust based on your audio data
                        rate=22050,  # Adjust based on your audio data
                        output=True)

        stream.write(response.content)

        stream.stop_stream()
        stream.close()
        p.terminate()
    else:
        print(f"Failed to fetch audio from {server_url}")
        
def move_motor(movement = "s"):
        if movement == 'f':
            print(f"forward: {movement}")
            wp.digitalWrite(in1, wp.GPIO.HIGH)
            wp.digitalWrite(in2, wp.GPIO.LOW)
            wp.digitalWrite(in3, wp.GPIO.HIGH)
            wp.digitalWrite(in4, wp.GPIO.LOW)
            

        elif movement == 's':
            print(f"stop {movement}")
            wp.digitalWrite(in1, wp.GPIO.LOW)
            wp.digitalWrite(in2, wp.GPIO.LOW)
            wp.digitalWrite(in3, wp.GPIO.LOW)
            wp.digitalWrite(in4, wp.GPIO.LOW)

        elif movement == 'r':
            print(f"right {movement}")
            wp.digitalWrite(in1, wp.GPIO.HIGH)
            wp.digitalWrite(in2, wp.GPIO.LOW)
            wp.digitalWrite(in3, wp.GPIO.LOW)
            wp.digitalWrite(in4, wp.GPIO.HIGH)
            
        elif movement == 'l':
            print(f"left {movement}")
            wp.digitalWrite(in1, wp.GPIO.LOW)
            wp.digitalWrite(in2, wp.GPIO.HIGH)
            wp.digitalWrite(in3, wp.GPIO.HIGH)
            wp.digitalWrite(in4, wp.GPIO.LOW)
            
        elif movement == 'b':
            print(f"backward {movement}")
            wp.digitalWrite(in1, wp.GPIO.LOW)
            wp.digitalWrite(in2, wp.GPIO.HIGH)
            wp.digitalWrite(in3, wp.GPIO.LOW)
            wp.digitalWrite(in4, wp.GPIO.HIGH)
            
        else:
            print(f"This is not a command so stop {movement}")
            wp.digitalWrite(in1, wp.GPIO.LOW)
            wp.digitalWrite(in2, wp.GPIO.LOW)
            wp.digitalWrite(in3, wp.GPIO.LOW)
            wp.digitalWrite(in4, wp.GPIO.LOW)


if __name__ == "__main__":
    while True:
        # For English
        speech_to_text(language='en-US')

        audio_receive()

        # For Arabic
        # speech_to_text(language='ar')
