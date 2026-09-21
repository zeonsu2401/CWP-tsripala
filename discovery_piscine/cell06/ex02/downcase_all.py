#!/usr/bin/env python3
import sys

def downcase_it(s):
    return s.lower()

if len(sys.argv) == 1:
    print("none")
else:
    for arg in sys.argv[1:]:
        print(downcase_it(arg))
