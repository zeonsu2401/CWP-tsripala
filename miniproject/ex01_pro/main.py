import sys
import os
import copy

def render_board(board_2d):
    n = len(board_2d)
    print("\n  " + "".join([f" {c} " for c in range(n)]))
    for r in range(n):
        line = f"{r} "
        for c in range(n):
            bg = '\033[47m' if (r + c) % 2 == 0 else '\033[100m'
            char = board_2d[r][c]
            if char == 'K': fg = '\033[38;5;196m' 
            elif char in 'PBRQN': fg = '\033[1;34m'
            else: fg = '\033[1;30m'; char = '.'
            line += f"{bg}{fg} {char} \033[0m"
        print(line)
    print()


def validate_board(board_str):
    lines = board_str.strip().split('\n')
    if not lines: 
        return False
        
    n = len(lines)
    k_count = 0
    valid_chars = set('KPBRQN. ') # อนุญาตแค่ตัวอักษรเหล่านี้
    
    for line in lines:
        if len(line) != n: 
            return False # เช็คความยาวแต่ละบรรทัดต้องเท่ากับจำนวนบรรทัด (N x N)
            
        for char in line:
            if char not in valid_chars: 
                return False # เจอตัวอักษรแปลกปลอม
            if char == 'K': 
                k_count += 1
                
    return k_count == 1 # ต้องมี King ตัวเดียวเป๊ะๆ

def get_king_pos(board_2d):
    for r in range(len(board_2d)):
        for c in range(len(board_2d)):
            if board_2d[r][c] == 'K': return r, c
    return None, None

def is_in_check(board_2d, kr, kc):
    if kr is None or kc is None: return False
    n = len(board_2d)
    dirs = [(-1,0,['R','Q']), (1,0,['R','Q']), (0,-1,['R','Q']), (0,1,['R','Q']),
            (-1,-1,['B','Q']), (-1,1,['B','Q']), (1,-1,['B','Q']), (1,1,['B','Q'])]
    for dr, dc, pieces in dirs:
        r, c = kr + dr, kc + dc
        while 0 <= r < n and 0 <= c < n:
            if board_2d[r][c] != '.':
                if board_2d[r][c] in pieces: return True
                break
            r += dr; c += dc
    for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
        if 0 <= kr+dr < n and 0 <= kc+dc < n and board_2d[kr+dr][kc+dc] == 'N': return True
    if kr+1 < n and kc-1 >= 0 and board_2d[kr+1][kc-1] == 'P': return True
    if kr+1 < n and kc+1 < n and board_2d[kr+1][kc+1] == 'P': return True
    return False

def get_king_legal_moves(board_2d, kr, kc):
    if kr is None or kc is None: return []
    n = len(board_2d)
    moves = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0: continue
            nr, nc = kr + dr, kc + dc
            if 0 <= nr < n and 0 <= nc < n:
                if board_2d[nr][nc] == '.' or board_2d[nr][nc] in 'PBRQN':
                    sim_board = copy.deepcopy(board_2d)
                    sim_board[kr][kc] = '.'
                    sim_board[nr][nc] = 'K'
                    if not is_in_check(sim_board, nr, nc):
                        moves.append((nr, nc))
    return moves

def generate_moves(board_2d, r, c, piece, n):
    moves = []
    if piece == 'P':
        if r+1 < n and board_2d[r+1][c] == '.': moves.append((r+1, c))
        if r+1 < n and c-1 >= 0 and board_2d[r+1][c-1] == 'K': moves.append((r+1, c-1))
        if r+1 < n and c+1 < n and board_2d[r+1][c+1] == 'K': moves.append((r+1, c+1))
    elif piece == 'N':
        for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            if 0 <= r+dr < n and 0 <= c+dc < n and board_2d[r+dr][c+dc] in ['.', 'K']: moves.append((r+dr, c+dc))
    else:
        dirs = []
        if piece in ['R', 'Q']: dirs += [(-1,0), (1,0), (0,-1), (0,1)]
        if piece in ['B', 'Q']: dirs += [(-1,-1), (-1,1), (1,-1), (1,1)]
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            while 0 <= nr < n and 0 <= nc < n:
                if board_2d[nr][nc] == '.': moves.append((nr, nc))
                elif board_2d[nr][nc] == 'K': moves.append((nr, nc)); break
                else: break
                nr += dr; nc += dc
    return moves

def minimax_mate(board_2d, depth, is_attacker_turn):
    kr, kc = get_king_pos(board_2d)
    if kr is None: return 0
    in_check = is_in_check(board_2d, kr, kc)
    legal_k_moves = get_king_legal_moves(board_2d, kr, kc)
    if is_attacker_turn and in_check and not legal_k_moves: return 0 
    if depth == 0: return None 
    n = len(board_2d)
    
    if is_attacker_turn:
        best_mate = None
        for r in range(n):
            for c in range(n):
                piece = board_2d[r][c]
                if piece in 'PBRQN':
                    for (nr, nc) in generate_moves(board_2d, r, c, piece, n):
                        sim_board = copy.deepcopy(board_2d)
                        sim_board[r][c] = '.'
                        sim_board[nr][nc] = piece
                        mate_dist = minimax_mate(sim_board, depth - 1, False)
                        if mate_dist is not None:
                            if best_mate is None or mate_dist < best_mate:
                                best_mate = mate_dist
                                if best_mate == 0: return 1 
        return best_mate + 1 if best_mate is not None else None
    else:
        if not legal_k_moves: return None 
        worst_case_for_attacker = -1
        for (nr, nc) in legal_k_moves:
            sim_board = copy.deepcopy(board_2d)
            sim_board[kr][kc] = '.'
            sim_board[nr][nc] = 'K'
            mate_dist = minimax_mate(sim_board, depth - 1, True)
            if mate_dist is None: return None 
            if mate_dist > worst_case_for_attacker: worst_case_for_attacker = mate_dist
        return worst_case_for_attacker

def find_best_move(board_str, search_depth=3):
    if not validate_board(board_str):
        print("Error\n")
        return

    lines = board_str.strip().split('\n')
    n = len(lines)
    board = [list(line) for line in lines]
    print("--- Current Board State ---")
    render_board(board)
    kr, kc = get_king_pos(board)
    
    if kr is not None and is_in_check(board, kr, kc) and not get_king_legal_moves(board, kr, kc):
        print("Verdict: ALREADY CHECKMATE!\n"); return

    print(f"[*] Calculating Minimax up to depth {search_depth} (Wait for it...)")
    best_move = None; best_mate_in = None
    for r in range(n):
        for c in range(n):
            piece = board[r][c]
            if piece in 'PBRQN':
                for (nr, nc) in generate_moves(board, r, c, piece, n):
                    sim_board = copy.deepcopy(board)
                    sim_board[r][c] = '.'
                    sim_board[nr][nc] = piece
                    mate_dist = minimax_mate(sim_board, search_depth - 1, False)
                    if mate_dist is not None:
                        if best_mate_in is None or mate_dist < best_mate_in:
                            best_mate_in = mate_dist
                            best_move = (piece, (r,c), (nr,nc), sim_board)
                            if best_mate_in == 0: break 
                if best_mate_in == 0: break
        if best_mate_in == 0: break
                        
    if best_move:
        p, src, dst, sim_board = best_move
        print(f"INEVITABLE LOSS DETECTED: Mate in {best_mate_in + 1} moves!")
        print(f"Best initial move: {p} at {src} -> {dst}")
        render_board(sim_board)
    else:
        print(f"Verdict: No forced checkmate found within {search_depth} depth.\n")

def main():
    if len(sys.argv) < 2: return
    for file_path in sys.argv[1:]:
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f: board_str = f.read()
            print(f"\n[*] Processing: {file_path}")
            find_best_move(board_str)

if __name__ == "__main__": main()
