import time
import sys

BG_W = '\033[47m'; BG_B = '\033[100m'; BG_PATH = '\033[43m'; BG_ATK = '\033[45m'; BG_HIT = '\033[41m'
FG_K = '\033[38;5;196m'; FG_P = '\033[1;34m'; FG_DOT = '\033[1;30m'; RESET = '\033[0m'

is_first_frame = True

def draw_frame(board, highlight_path, attacker_pos, msg, is_hit=False):
    global is_first_frame
    
    if not is_first_frame:
        sys.stdout.write('\033[11A')
    else:
        is_first_frame = False
        
    n = len(board)
    sys.stdout.write(f"\033[K\n")
    sys.stdout.write(f"\033[K {msg}\n")
    sys.stdout.write(f"\033[K  " + "".join([f" {c} " for c in range(n)]) + "\n")
    
    for r in range(n):
        line = f"{r} "
        for c in range(n):
            bg = BG_W if (r + c) % 2 == 0 else BG_B
            char = board[r][c]
            
            # ย้อมสีพื้นหลัง
            if (r, c) == attacker_pos: 
                bg = BG_ATK
            elif (r, c) in highlight_path: 
                # ถ้าจุดนี้คือ King และโดนรุก ให้ย้อมสีแดง ถ้าไม่ใช่ให้ย้อมสีเหลือง(รัศมี)
                bg = BG_HIT if (char == 'K' and is_hit) else BG_PATH
                
            if char == 'K': fg = FG_K
            elif char in 'PNRBQ': fg = FG_P
            else: fg = FG_DOT; char = '.'
            line += f"{bg}{fg} {char} {RESET}"
            
        sys.stdout.write(f"\033[K{line}\n")
        
    sys.stdout.flush()
    # จังหวะหน่วงเวลาโชว์รัศมี "ปึ้ง!"
    time.sleep(0.5)

def animate_check(board_str, test_name):
    global is_first_frame
    is_first_frame = True 
    
    board = [list(line) for line in board_str.strip().split('\n')]
    n = len(board)
    pieces = {'P':[], 'N':[], 'R':[], 'B':[], 'Q':[]}
    
    for r in range(n):
        for c in range(n):
            if board[r][c] in pieces: pieces[board[r][c]].append((r,c))
            
    dirs = {'R': [(-1,0), (1,0), (0,-1), (0,1)], 'B': [(-1,-1), (-1,1), (1,-1), (1,1)], 'Q': [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]}
    
    draw_frame(board, [], None, f"=== {test_name} ===")
    time.sleep(0.5)
    
    for ptype in ['P', 'N', 'R', 'B', 'Q']:
        for pr, pc in pieces[ptype]:
            attack_squares = []
            
            # 1. คำนวณรัศมีโจมตีทั้งหมดของหมากตัวนี้
            if ptype == 'P':
                for tr, tc in [(pr+1, pc-1), (pr+1, pc+1)]:
                    if 0 <= tr < n and 0 <= tc < n:
                        attack_squares.append((tr, tc))
                        
            elif ptype == 'N':
                for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
                    tr, tc = pr+dr, pc+dc
                    if 0 <= tr < n and 0 <= tc < n:
                        attack_squares.append((tr, tc))
                        
            else:
                for dr, dc in dirs[ptype]:
                    tr, tc = pr+dr, pc+dc
                    while 0 <= tr < n and 0 <= tc < n:
                        attack_squares.append((tr, tc))
                        if board[tr][tc] != '.': 
                            break # ชนหมากตัวอื่น (รวมถึง King) หยุดยิงแสงทิศนี้
                        tr += dr; tc += dc
            
            if not attack_squares:
                continue
                
            # 2. เช็คว่ามี King อยู่ในรัศมีไหม
            is_hit = any(board[tr][tc] == 'K' for tr, tc in attack_squares)
            
            # 3. เฟรมที่ 1: สาดสีรัศมีทั้งหมดพร้อมกัน (AoE)
            draw_frame(board, attack_squares, (pr,pc), f"⚡ {ptype} at ({pr},{pc}) casts attack range!")
            
            if is_hit:
                # 4. เฟรมที่ 2: ถ้าโดน King จะกระพริบแดงทันที
                draw_frame(board, attack_squares, (pr,pc), f"💥 {ptype} at ({pr},{pc}) CHECKMATE!", is_hit=True)
                return True
                
    return False

def main():
    board_success = "R...B..Q\n...P....\n..N.....\n........\n....K...\n........\n........\n........"
    board_fail = "R...B..Q\n...P....\n..N.....\n........\n........\n........\n........\n.......K"
    
    if animate_check(board_success, "TEST CASE 1: SUCCESS (CHECK)"): 
        print("\n RESULT: SUCCESS! King is in check.\n")
        
    time.sleep(1.5)
    
    if animate_check(board_fail, "TEST CASE 2: FAIL (SAFE)"): 
        print("\n RESULT: SUCCESS! King is in check.\n")
    else: 
        print("\n RESULT: FAIL! King is safe.\n")

if __name__ == "__main__": 
    main()
