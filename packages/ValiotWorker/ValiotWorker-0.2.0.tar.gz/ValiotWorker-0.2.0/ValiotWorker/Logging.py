# terminal styles for better logging
import sys
from enum import Enum
from colorama import Fore, Back, Style, init as init_term, AnsiToWin32
from termcolor import colored
# colorful terminal initializacion
init_term(wrap=True, autoreset=True)
stream = AnsiToWin32(sys.stderr).stream

class LogLevel(Enum):
  DEBUG = 'DEBUG' # Blue
  ERROR = 'ERROR' # Red
  INFO = 'INFO'   # White
  WARNING = 'WARNING' # Yellow
  SUCCESS = 'SUCCESS' # ! Green, Non-standard with Eliot (might not care)

# print wrappers
def log(level, message):
  if(level == LogLevel.INFO):
    log_info(message)
  if(level == LogLevel.SUCCESS):
    log_success(message)
  if(level == LogLevel.WARNING):
    log_warning(message)
  if(level == LogLevel.ERROR):
    log_error(message)
  if(level == LogLevel.DEBUG):
    log_debug(message)

def log_info(message):
  print(colored(message, 'white'))

def log_success(message):
  print(colored(message, 'green'))

def log_warning(message):
  print(colored(message, 'yellow'))

def log_error(message):
  print(colored(message, 'red'))

def log_debug(message):
  print(colored(message, 'blue'))