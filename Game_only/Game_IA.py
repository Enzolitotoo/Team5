import random
import tkinter as tk
from Min_Max import Tree
from rewrite_alpha import Tree_A
import time



root = tk.Tk()
root.title("The Game Of Division")
root.geometry("600x200+800+300")

main_w = None
end_w = None

def selct(number, score, bank, turn, algo, first, sec, order, visited, visit_total = 0):
    global main_w
    if turn == 1:
        score, bank = 0, 0
        fichier =  open("data.txt", "a")
        fichier.write(f"\nFirst_Number: {number}, ")
        fichier.close()
    else:
        score += 1 if number % 2 == 1 else -1
        if number % 10 in [0, 5]:
            bank += 1
    
    if main_w:
        main_w.destroy()
    
    main_w = tk.Toplevel()
    main_w.title(f"{first} Choose Divider from the possibles one")
    main_w.geometry("600x200+800+300")
    
    dividers = [i for i in range(2, 6) if number % i == 0]
    
    if turn % 2 == 1:
        maxi = True
    else:
        maxi = False
    
    if dividers:
        tk.Label(main_w, text=f"Score= {score}, Bank= {bank}").grid(row=1, column=3)
        
        if first.startswith("AI"):
            start_time = time.time()
            tree = Tree({'number': number, 'score': score, 'Bank': bank, 'MinMax_ana': 0}, None, None, maxi) if algo == 'MinMax' else Tree_A({'number': number, 'score': score, 'Bank': bank, 'MinMax_ana': 0}, None, None, maxi)
            tree.expand()
            visited = tree.count_node()
            visit_total += visited
            best_divider = tree.best_move()
            number //= best_divider
            end_time = time.time()
            tk.Label(main_w, text=f"{first} chose divisor: {best_divider}, New value: {number}, Execution Time: {end_time - start_time:.6f}, Node_visited: {visited}").grid(row=2, column=3)
            tk.Button(main_w, text="Next Turn", command=lambda: selct(number, score, bank, turn + 1, algo, sec, first, order,  0, visit_total )).grid(row=3, column=3)
        else:
            tk.Label(main_w, text=f"The number is: {number}").grid(row=3, column=3)
            
            for col, i in enumerate(dividers):
                tk.Button(main_w, text=str(i), command=lambda i=i: selct(number // i, score, bank, turn + 1, algo, sec, first, order, 0, visit_total)).grid(row=2, column=col)
    else:
        main_w.destroy()
        end(number, score, bank, turn, order, visit_total)

def end(number, score, bank, turn, order, visit_total):
    global end_w
    if end_w:
        end_w.destroy()
    
    end_w = tk.Toplevel()
    end_w.title("This is the End")
    end_w.geometry("600x200+800+300")
    
    # Calcul du score final
    if score % 2 == 1:  # Si le score est impair, c'est le tour de l'AI qui joue avec les points + bank
        Final = score + bank
    else:  # Si le score est pair, c'est le tour de l'humain qui joue avec les points - bank
        Final = score - bank
    
    # Détermination du gagnant
    winner = order[0] if Final % 2 == 1 else order[1]
    
    # Affichage du résultat
    tk.Label(end_w, text=f"Final Number: {number}\nTurns: {turn - 1}\nScore: {score}\nBank: {bank}\nVisited Node:{visit_total}").grid(row=0, column=0)
    tk.Label(end_w, text=f"{winner} Wins! Final Score: {Final}").grid(row=1, column=0)
    
    for i, (txt, cmd) in enumerate([("Close", root.destroy), ("Retry", game)]):
        tk.Button(end_w, text=txt, command=cmd).grid(row=3 + i, column=0)

    fichier =  open("data.txt", "a")
    fichier.write(f"Final Number: {number}, Turns: {turn - 1}, Score: {score}, Bank: {bank}, Final Score: {Final}, Winner: {winner}, Number of Node Visited: {visit_total}")
    fichier.close()
    
def first_p(number, score, bank, turn, algo, p1, p2):
    global main_w
    if main_w:
        main_w.destroy()
    
    main_w = tk.Toplevel()
    main_w.title("Choose the First Player")
    main_w.geometry("600x200+800+300")
    
    for i, player in enumerate([p1, p2]):
        tk.Button(main_w, text=player, command=lambda player=player: selct(number, score, bank, turn, algo, player, p1 if player == p2 else p2, [player, p1 if player == p2 else p2], visited = 0)).grid(row=2 + i, column=0)
def duel(number, score, bank, turn, algo):
    global main_w
    if main_w:
        main_w.destroy()
    
    main_w = tk.Toplevel()
    main_w.title("Choose the Type of Duel")
    main_w.geometry("600x200+800+300")
    
    for i, (txt, p1, p2) in enumerate([("Human VS AI", "Human", "AI"), ("AI VS AI", "AI 1", "AI 2")]):
        tk.Button(main_w, text=txt, command=lambda p1=p1, p2=p2: first_p(number, score, bank, turn, algo, p1, p2)).grid(row=2 + i, column=0)

def algo_c(number, score, bank, turn):
    global main_w
    if main_w:
        main_w.destroy()
    
    main_w = tk.Toplevel()
    main_w.title("Choose the Type of Algorithm")
    main_w.geometry("600x200+800+300")    
    
    for i, algo in enumerate(["MinMax", "Alpha"]):
        tk.Button(main_w, text=f'{algo} Algorithm', command=lambda algo=algo: duel(number, score, bank, turn, algo)).grid(row=3 + i, column=0)

def valid_number(n, min_turns=3): # Check if the number can garentee at least 3 turns
    turns = 0
    while turns < min_turns:
        dividers = [i for i in [2, 3, 4, 5] if n % i == 0]
        if not dividers:
            return False  
        n //= random.choice(dividers)  
        turns += 1
    return True

def game():
    global end_w
    if end_w:
        end_w.destroy()
    
    root.deiconify()
    score, bank, turn = 0, 0, 1
    list_number = []
    
    while len(list_number) < 5:
        num = random.randint(30000, 50000)
        if valid_number(num):
            list_number.append(num)
    for i, num in enumerate(list_number):
        tk.Button(root, text=num, command=lambda num=num: algo_c(num, score, bank, turn)).grid(row=2, column=i+1)
   
game()
root.mainloop()

# Code By Enzo Kerebel
