from os import listdir
import subprocess
import shlex
from itertools import zip_longest
import argparse

parser = argparse.ArgumentParser(description='Testing utility')
parser.add_argument('-r', nargs='*', dest="files", action="store_true",
                    help='if set recaculates the correct output for all tests', required=False)

for test in listdir('testcases'):
    botfiles = ' '.join(f'"filebot.py testcases/{test}/{i}"' for i in range(2))
    rng_file = f"testcases/{test}/rng"
    prompt = f"python simulation.py -v -d --bots {botfiles} --rng {rng_file}"
    proc = subprocess.run(shlex.split(prompt), capture_output=True, encoding="utf-8", check=True)

    with open(f"testcases/{test}/out", 'r') as f:
        out = proc.stdout
        data = f.read()
        for i,(l1,l2) in enumerate(zip_longest(out.split('\n'), data.split('\n')), start=1):
            if l1!=l2:
                print(f"blad w linii {i}: {l1!r} {l2!r}")

print('wszystko OK')