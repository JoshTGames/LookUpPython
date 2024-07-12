# Made by Joshua Thompson (https://joshgames.co.uk)
# REQURES 'SpeechRecognition' module

import os, sys
from importlib.machinery import SourceFileLoader
import speech_recognition as sr
import json_manager as json
import socket as s

r = sr.Recognizer()
recognitionService = r.recognize_google
settings = json.ReadFile(os.getcwd() + '/settings.json')
Clear = lambda: os.system(settings['ClearCommand'])
dataFolder = os.getcwd() + '/__data__'
id = s.gethostname()
ip = s.gethostbyname(id)
mic = sr.Microphone(device_index=1)
commands = {}

# Add commands to the system path for module import
commands_location = os.getcwd()+ '/__commands__/'
if commands_location not in sys.path:
    sys.path.append(commands_location)

# Iterate through all the commands in the commands folder
def get_commands(): 
    for file in os.listdir(commands_location):
        name = os.fsdecode(file)
        if(name.endswith('.py')):
            mod = SourceFileLoader(file, commands_location+file).load_module()
            commands[name.split('.py')[0].lower()] = mod

# Calls the command
def process_command(cmd):
    if(cmd == None): return
    for x in commands:
        if(not x in cmd): continue

        data = cmd[len(x) + 1:]
        return commands[x].run(data)

# Reads the microphone
def get_speech():
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        said = ''
        try:
            said = recognitionService(audio)
        except sr.UnknownValueError:
            Clear()
            print(f'Unable to listen... Try again!')
        except sr.RequestError as e:
            Clear()
            print(f'Could not request results:\n{e}')
    return said.lower()

# Main loop
print(f'ID: {id} // IP: {ip}\n\n')
get_commands()
while True:
    print("Listening")
    text = get_speech()
    wakePhrase = settings['WakePhrase'].lower()
    print(text)
    if(text.count(wakePhrase)):
        command = text[len(wakePhrase) + 1:]
        print(f'{process_command(command)}\n')