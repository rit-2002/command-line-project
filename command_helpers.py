import json

def helper_get_commands():
    with open("commands.json", "r") as f:
        helper_commands = json.load(f)
        return helper_commands

class CommandNotFound:
    pass

class HelpingCommands:
    def help_func(self, command):
        helper_commands = helper_get_commands()
        help_result = f"{command} : \n {helper_commands[command]['title']} \nCommand: {helper_commands[command]['command']}"
        return help_result
    
