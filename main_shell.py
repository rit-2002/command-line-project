import os # For file and directory operations 
import sys # For system-specific parameters and functions
import logging as log  # For logging errors and info
from datetime import datetime # For date and time functions
import socket # For network-related functions
import random # For random theme selection
from termcolor import colored # For colored terminal output
from shell_app import find_help # Importing help function from shell_app

# Configure logging settings for debugging and error tracking 
log.basicConfig(
    level=log.DEBUG,  # Log all levels DEBUG and above
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[log.FileHandler('rkshell.log')] # Log to file
)

# Shell styling constants and themes 
SHELL_STYLES = {
    'success': '✓',
    'error': '✗',
    'warning': '⚠',
    'info': 'ℹ',
    'prompt': '➜',
    'divider': '─' * 50  # Added divider style
}

# Theme configurations
SHELL_THEMES = {
    'classic': {'border': '┌─┐│└┘', 'colors': ['green', 'blue']},
    'modern': {'border': '╭─╮│╰╯', 'colors': ['cyan', 'magenta']},
    'bold': {'border': '┏━┓┃┗┛', 'colors': ['yellow', 'red']},
}

# Main shell implementation class
class RKShell:
    def __init__(self):
        self.theme = random.choice(list(SHELL_THEMES.keys()))
    
        self.commands = {
            "list": self.list_files,
            "dirs": self.list_dirs,
            "date": self.show_date,
            "time": self.show_time,
            "cat": self.cat_file,
            "head": self.head_file,
            "tail": self.tail_file,
            "copy_file": self.copy_file,
            "remove_file": self.remove_file,
            "empty_file": self.empty_file,
            "ipconfig": self.show_ipconfig,
            "pwd": self.show_pwd,
            "clear": self.clear_screen,
            "exit": self.exit_shell,
            "help": self.help_function
        }

   
    def list_files(self, args):
        """
        List all files in current directory or given directory.
        Added try/except -> return "Error" instead of crash.
        """
        try:
            if len(args) < 1:
                files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f)]
                log.info("list -> %s", files)
                return "\n".join(files)
            else:
                files = os.listdir(args[0])
                return "\n".join(files)
        except Exception as e:
            return f"Error: {str(e)}"

    def list_dirs(self, args):
        """
        List directories in current folder or given path.
        """
        try:
            if len(args) < 1:
                dirs = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d)]
                log.info("dirs -> %s", dirs)
                return "\n".join(dirs)
            else:
                dirs = [d for d in os.listdir(args[0]) if os.path.isdir(os.path.join(args[0], d))]
                return "\n".join(dirs)
        except Exception as e:
            return f"Error: {str(e)}"

    # Time and Date Operations with flags
    def show_date(self, args):
        """
        Show current date in different formats based on flags
        """
        try:
            now = datetime.now()
            
            # Check if args exist
            if args:
                return "Error: Date command doesn't accept any flags. Use 'time' command with -hours, -mins, -secs for time components"
        
            # Default format when no flags are provided
            return now.strftime("%d-%b-%Y").lower()
            
        except Exception as e:
            return f"Error: {str(e)}"

    def show_time(self, args):
        """
        Show time.
        Added validation for invalid flags -> return "Error".
        """
        try:
            now = datetime.now()
            hh, mm, ss = now.strftime("%H"), now.strftime("%M"), now.strftime("%S")
            data = ["hours", "mins", "secs"]

            flags = [d for d in args if d.startswith('-') and d[1:] in data]
            if len(args) == 0:
                return f"{hh}:{mm}:{ss}"
            if not flags:
                return "Error: Invalid flag"
            result, form = [], ""
            if "-hours" in flags:
                result.append(hh)
                form += "HH:"
            if "-mins" in flags:
                result.append(mm)
                form += "MM:"
            if "-secs" in flags:
                result.append(ss)
                form += "SS"
            if not result:
                return "Error: Invalid flag for time"
            return form + " -  " + ":".join(result)
        except Exception as e:
            return f"Error: {str(e)}"

    # File Content Operations for cat, head, tail
    def cat_file(self, args):
        """
        Display file contents.
        Added:
          - Better error messages
          - Path validation
          - File existence check with specific messages
        """
        if len(args) != 1:
            return "Error: Usage: cat <filename>"
        
        fname = args[0]
        
        # Check if file exists
        if not os.path.exists(fname):
            # Check if file has correct extension
            if '.' not in fname:
                return f"Error: File '{fname}' not found. Did you forget the file extension?"
            return f"Error: File '{fname}' does not exist in the current directory: {os.getcwd()}"
        
        # Check if it's actually a file (not a directory)
        if not os.path.isfile(fname):
            return f"Error: '{fname}' is a directory, not a file"
        
        try:
            with open(fname, "r") as f:
                content = f.read()
                return content if content else "(Empty file)"
        except PermissionError:
            return f"Error: Permission denied to read '{fname}'"
        except UnicodeDecodeError:
            return f"Error: '{fname}' appears to be a binary file"
        except Exception as e:
            return f"Error: Unable to read '{fname}' - {str(e)}"

    def head_file(self, args):
        """
        Show first N lines of file.
        Added validation for missing args.
        """
        if len(args) != 2:
            return "Error: Usage: head -N <filename>"
        try:
            n = int(args[0].replace("-", ""))
            fname = args[1]
            with open(fname, "r") as f:
                lines = f.readlines()
                return "".join(lines[:n])
        except Exception as e:
            return f"Error: {str(e)}"

    def tail_file(self, args):
        """
        Show last N lines of file.
        Added validation for missing args.
        """
        if len(args) != 2:
            return "Error: Usage: tail -N <filename>"
        try:
            n = int(args[0].replace("-", ""))
            fname = args[1]
            with open(fname, "r") as f:
                lines = f.readlines()
                return "".join(lines[-n:])
        except Exception as e:
            return f"Error: {str(e)}"

    # File Management Operations 
    def copy_file(self, args):
        """
        Copy file content to new file.
        Added:
          - Check for missing args
          - File not found check
        """
        if len(args) != 2:
            return "Error: Usage: copy_file <src> <dest>"
        src, dest = args
        if not os.path.exists(src):
            return f"Error: File not found -> {src}"
        try:
            with open(src, "r") as fsrc:
                data = fsrc.read()
            with open(dest, "w") as fdest:
                fdest.write(data)
            return f"Copied {src} to {dest}"
        except Exception as e:
            return f"Error: {str(e)}"

    def remove_file(self, args):
        """
        Remove file.
        Added validation for args and file not found.
        """
        if len(args) != 1:
            return "Error: Usage: remove_file <filename>"
        fname = args[0]
        if not os.path.exists(fname):
            return f"Error: File not found -> {fname}"
        try:
            os.remove(fname)
            return f"Removed {fname}"
        except Exception as e:
            return f"Error: {str(e)}"

    def empty_file(self, args):
        """
        Empty a file's content (size=0).
        """
        if len(args) != 1:
            return "Error: Usage: empty_file <filename>"
        fname = args[0]
        try:
            open(fname, "w").close()
            return f"Emptied {fname}"
        except Exception as e:
            return f"Error: {str(e)}"

    # System Operations
    def show_ipconfig(self, args):
        """Show system IP address"""
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except Exception as e:
            return f"Error: {str(e)}"

    def show_pwd(self, args):
        """Return current working directory"""
        try:
            return os.getcwd()
        except Exception as e:
            return f"Error: {str(e)}"

    def clear_screen(self, args):
        """Clear terminal screen"""
        try:
            os.system("cls" if os.name == "nt" else "clear")
            return ""
        except Exception as e:
            return f"Error: {str(e)}"

    def exit_shell(self, args):
        """Exit program"""
        print("Exiting shell...")
        sys.exit(0)

    def help_function(self, args):
        """Return help text for commands"""
        try:
            if args:
                return find_help(args[0])  
            else:
                return find_help(None)
        except Exception as e:
            return f"Error: {str(e)}"

    def print_banner(self):    # Ritesh Kunal Grp
        theme_colors = SHELL_THEMES[self.theme]['colors']
        banner = colored("""
    ╔══════════════════════════════════════════════╗
    ║    ____  _  __  _____ _          _ _        ║
    ║   |  _ \\| |/ / / ____| |__   ___| | |       ║
    ║   | |_) | ' /  \\___ \\| '_ \\ / _ \\ | |       ║
    ║   |  _ <| . \\   ___) | | | |  __/ | |       ║
    ║   |_| \\_\\_|\\_\\ |____/|_| |_|\\___|_|_|       ║
    ║                                              ║
    ╚══════════════════════════════════════════════╝
    """, theme_colors[0])
        
        print(banner)
        print(colored(f"{SHELL_STYLES['info']} Type 'help' to see available commands", theme_colors[1]))
        print('─' * 50)

    def format_output(self, output, status='success'):
        """Format command output with indicators and borders"""
        if not output:
            return ""
        theme = SHELL_THEMES[self.theme]
        lines = output.split('\n')
        
        result = []
        result.append(f"{theme['border'][2]} {SHELL_STYLES[status]} Output:")
        for line in lines:
            result.append(f"{theme['border'][2]}  {line}")
        result.append(SHELL_STYLES['divider'])
        
        return '\n'.join(result)

    # Command Execution Handler for run loop
    def run_command(self, line):
        """
        Main command runner.
        Added:
          - Empty input check
          - Invalid command check with logging
        """
        try:
            parts = line.strip().split()
            if not parts:
                log.warning("Empty command entered")
                return self.format_output("Empty command", 'warning')
                
            cmd, args = parts[0], parts[1:]
            if cmd not in self.commands:
                log.error(f"Invalid command attempted: {cmd}")
                return self.format_output(f"Invalid command: {cmd}", 'error')
                
            result = self.commands[cmd](args)
            log.info(f"Command executed successfully: {cmd} with args {args}")
            return self.format_output(result)
        except Exception as e:
            log.error(f"Error executing command '{line}': {str(e)}")
            return self.format_output(f"Error: {str(e)}", 'error')


# ------------------ MAIN LOOP ------------------ #
if __name__ == "__main__":
    try:
        shell = RKShell()
        shell.print_banner()
        
        while True:
            try:
                prompt = colored(f"\n{SHELL_STYLES['prompt']} rkshell> ", 'cyan')
                line = input(prompt)
                output = shell.run_command(line)
                if output:
                    print(output)
            except KeyboardInterrupt:
                print(colored(f"\n{SHELL_STYLES['warning']} Use 'exit' to quit", 'yellow'))
                continue
            except Exception as e:
                log.error(str(e))
                print(colored(f"{SHELL_STYLES['error']} Error: {e}", 'red'))
    except Exception as e:
        log.critical(f"Shell initialization failed: {e}")
        sys.exit(1)
