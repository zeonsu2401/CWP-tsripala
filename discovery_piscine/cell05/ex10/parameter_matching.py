#!/usr/bin/env python3
import sys

def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print("none")
        return

    secret = args[0]
    guess = input("What was the parameter? ")
    
    response = "Good job!" if guess == secret else "Nope, sorry..."
    print(response)

if __name__ == "__main__":
    main()
