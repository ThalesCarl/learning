# Same program, but with coroutines
import itertools
import asyncio
import time

async def spin(msg: str) -> None:
    for char in itertools.cycle(r'\|/-'): # infinite loop
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)
        try:
            await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            break
        blanks = ' ' * len(status)
        print(f'\r{blanks}\r', end='')

async def slow() -> int:
    await asyncio.sleep(2)
    # never use time.sleep in a async coroutine
    # time.sleep(2)
    return 42

def main() -> None:
    result = asyncio.run(supervisor())
    print(f'Answer: {result}')

async def supervisor() -> int:
    spinner = asyncio.create_task(spin('thinking!'))
    print(f'spinner object: {spinner}')
    result = await slow()
    spinner.cancel()
    return result

if __name__ == '__main__':
    main()