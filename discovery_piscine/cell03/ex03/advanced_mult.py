multiplier = 0

while multiplier <= 10:
    print(f"Table de {multiplier}:", end="")
    
    number = 0
    while number <= 10:
        print(f" {multiplier * number}", end="")
        number += 1
        
    print() 
    multiplier += 1
