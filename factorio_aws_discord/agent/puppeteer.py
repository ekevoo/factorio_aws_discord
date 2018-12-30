#!/usr/bin/python3

import asyncio
import pathlib
import signal
import sys

import pexpect
import pexpect.popen_spawn
from unsync import Unfuture, unsync


class Puppeteer:
    """
    This class is a low-level handler of the game. It also transparently passes its input/output, except that stderr
    gets redirected into stdout due to a limitation of pexpect.
    """

    def __init__(self, base_path: str):
        command = ['bin/x64/factorio', '--start-server', 'saves/world.zip']
        self.process = pexpect.popen_spawn.PopenSpawn(command, timeout=31557600, cwd=base_path)
        self._std_in: Unfuture = self._run_std_in()
        self._std_out: Unfuture = self._run_std_out()

    @unsync
    def _run_std_in(self):
        line = sys.stdin.readline()
        while line:
            self.process.write(line)
            line = sys.stdin.readline()
        print('Input ended! Exiting.')
        self.process.kill(signal.SIGTERM)
        self.process.wait()
        print('Exited.')

    @unsync
    def _run_std_out(self):
        line = self.process.readline()
        while line:
            print(line.decode(), end='')
            line = self.process.readline()
        print('stdout exited')

    def __await__(self):
        return asyncio.gather(self._std_in, self._std_out).__await__()


@unsync
async def main():
    here = pathlib.Path(__file__).resolve().parent
    await Puppeteer(str(here / 'game'))
    print('All done!')


if __name__ == '__main__':
    main().result()
