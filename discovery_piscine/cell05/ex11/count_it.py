#!/usr/bin/env python3
import sys

def main():
    args = sys.argv[1:]

    if not args:
        print("none")
        return

    print(f"parameters: {len(args)}")
    for word in args:
        print(f"{word}: {len(word)}")

if __name__ == "__main__":
    main()
