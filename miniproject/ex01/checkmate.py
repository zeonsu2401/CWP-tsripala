def checkmate(board):
    try:
        lines = board.strip().split('\n')
        if not lines:
            return
            
        n = len(lines)
        for line in lines:
            if len(line) != n:
                print("Error")
                return
                
        k_pos = None
        k_count = 0
        for r in range(n):
            for c in range(n):
                if lines[r][c] == 'K':
                    k_pos = (r, c)
                    k_count += 1
                    
        if k_count != 1:
            print("Error")
            return
            
        kr, kc = k_pos
        
        directions = [
            (-1, 0, ['R', 'Q']),
            (1, 0, ['R', 'Q']),
            (0, -1, ['R', 'Q']),
            (0, 1, ['R', 'Q']),
            (-1, -1, ['B', 'Q']),
            (-1, 1, ['B', 'Q']),
            (1, -1, ['B', 'Q']),
            (1, 1, ['B', 'Q'])
        ]
        
        for dr, dc, pieces in directions:
            r, c = kr + dr, kc + dc
            while 0 <= r < n and 0 <= c < n:
                char = lines[r][c]
                if char != '.' and char != ' ':
                    if char in pieces:
                        print("Success")
                        return
                    else:
                        break
                r += dr
                c += dc
                
        if kr + 1 < n and kc - 1 >= 0 and lines[kr + 1][kc - 1] == 'P':
            print("Success")
            return
        if kr + 1 < n and kc + 1 < n and lines[kr + 1][kc + 1] == 'P':
            print("Success")
            return
            
        print("Fail")
        
    except Exception:
        print("Error")
