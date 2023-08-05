import logging
import datetime
import csv
from termcolor import colored 

def test():
	print(colored('this logger is 🔥', 'white', 'on_grey', attrs=['bold', 'underline']))

def write_to_csv(display_message, message_level, message):
    with open(r'log.csv', 'a') as csv_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%s")
        writer = csv.writer(csv_file)
        writer.writerow([timestamp, message_level, message])
        print('%s  %s | %s' % (display_message, colored(timestamp, 'green'), message))

def debug(message):
    format_message = colored(' 🤬   DEBUG    ', 'white', 'on_grey', attrs=['bold'])
    write_to_csv(format_message, 'DEBUG', message)

def info(message):
    format_message = colored(' 💁  INFO     ', 'white', 'on_green', attrs=['bold'])
    write_to_csv(format_message, 'INFO', message)

def warning(message):
    format_message = colored(' ⚠️   WARNING  ', 'white', 'on_yellow', attrs=['bold'])
    write_to_csv(format_message, 'WARNING', message)

def error(message):
    format_message = colored(' 💩  ERROR    ', 'white', 'on_red', attrs=['bold'])
    write_to_csv(format_message, 'ERROR', message)

def critical(message):
    format_message = colored(' 🖕  CRITICAL ', 'white', 'on_cyan', attrs=['bold', 'blink'])
    write_to_csv(format_message, 'CRITICAL', message)

