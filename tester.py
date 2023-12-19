from os import listdir
import subprocess
import shlex
from itertools import zip_longest
import argparse
from sys import argv

parser = argparse.ArgumentParser(description='Testing utility')
parser.add_argument('-r', dest="recalc", action="store_true",
                    help='if set recaculates the correct output for all tests', required=False)
nspc = parser.parse_args(argv[1:])

error = 0
for test in listdir('testcases'):
    botfiles = ' '.join(f'"filebot.py testcases/{test}/{i}"' for i in range(2))
    rng_file = f"testcases/{test}/rng"
    prompt = f"python simulation.py -v -d --bots {botfiles} --rng {rng_file}"
    proc = subprocess.run(shlex.split(prompt), capture_output=True, encoding="utf-8", check=True)

    out = proc.stdout
    if nspc.recalc:
        with open(f"testcases/{test}/out", 'w') as f:
            f.write(out)

    else:
        with open(f"testcases/{test}/out", 'r') as f:
            data = f.read()

        for i,(l1,l2) in enumerate(zip_longest(out.split('\n'), data.split('\n')), start=1):
            if l1!=l2:
                print(f"blad w teście {test} w linii {i}: {l1!r} {l2!r}")
                error=1

if nspc.recalc:
    print('Pomyślnie zmieniono wynik testów')
elif not error:
    print('wszystko OK')
else:
    print('w trakcie testowania wystąpiły błędy')