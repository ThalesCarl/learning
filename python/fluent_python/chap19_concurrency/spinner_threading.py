# Concurrent hello world

# This program will display a character spinning in the terminal while processing other characters

import itertools
import time
from threading import Thread, Event

def spin(msg: str, done: Event) -> None:
    for char in itertools.cycle(r'\|/-'): # infinite loop
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)
        if done.wait(.1):
            break
        blanks = ' ' * len(status)
        print(f'\r{blanks}\r', end='')

def slow() -> int:
    time.sleep(2)
    return 42

def supervisor() -> int:
    done = Event()
    spinner = Thread(target=spin, args=('thinking!', done))
    print(f'spinner object: {spinner}')
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result

def main() -> None:
    result = supervisor()
    print(f'Answer: {result}')

if __name__ == '__main__':
    main()