import sys
import os
from checkmate import checkmate

def main():
    if len(sys.argv) < 2:
        return
        
    for file_path in sys.argv[1:]:
        if not os.path.isfile(file_path):
            print("Error")
            continue
            
        try:
            with open(file_path, 'r') as f:
                board = f.read()
            
            print(f"--- Board: {file_path} ---")
            print(board.strip())
            print("Result: ", end="")
            
            checkmate(board)
            print()
            
        except Exception:
            print("Error")

if __name__ == "__main__":
    main()
