#!/usr/bin/env python3
import sys

if len(sys.argv) == 2 and 'z' in sys.argv[1]:
    print('z' * sys.argv[1].count('z'))
else:
    print("none")
