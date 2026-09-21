#!/usr/bin/env python3
import sys

if len(sys.argv) < 3:
    print("none")
else:
    word = sys.argv[1]
    text = sys.argv[2]
    words = text.split()
    count = words.count(word)
    print(count)
