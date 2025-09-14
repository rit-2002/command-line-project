from command_helpers import *
from colorama import init, Fore, Style
import os

# Custom exception for handling unknown commands
class CommandNotFound(Exception):
    pass

# Function to display help information for shell commands
def find_help(subcommand):
    try:
            # Get available commands from helper module
            helper_commands = helper_get_commands()
            help_instance = HelpingCommands()

            command = "help"

            # Handle help with specific subcommand
            if command == "help" and subcommand:
                if subcommand in helper_commands:
                    result = help_instance.help_func(subcommand)
                    if result:
                        print(Fore.CYAN + result)
                        print(Style.RESET_ALL)
                    else:
                        # No help text available for the command
                        print(Fore.YELLOW + f"No detailed help available for '{subcommand}'.")
                        print(Style.RESET_ALL)
                else:
                    # Command not found in helper commands
                    raise CommandNotFound(Fore.RED + f"Unknown Help Command: {subcommand}")
                    
            # Display list of available commands when no subcommand is provided
            elif command == "help" and subcommand is None:
                cmd = """ help <command_name>
    1. list
    2. dirs
    3. date
    4. time
    5. cat
    6. head
    7. tail
    8. copy_file
    9. remove_file
    10. empty_file
    11. ipconfig
    12. pwd
    13. clear
    14. exit
    """
                print(cmd)
            else:
                print("Unknown command")
                
    except Exception as e:
        # Handle and display any errors that occur
        print(e)
        print(Style.RESET_ALL)