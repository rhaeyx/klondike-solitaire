#!/usr/bin/python3

from pwn import *

# context.log_level = 'DEBUG'

io = process(['python3', 'solitaire.py'])

moves = {
    'move cA from pile 1 to foundation a' : ['1', 'p', '1', 'cA', 'f', 'a'],
    'move HK from pile 7 to pile 1': ['1', 'p', '7', 'HK', 'p', '1'],
    '1 deal stock': ['2'],
    'move sA from stock to foundation b': ['1', 's', 'sA', 'f', 'b'],
    '2 deal stock 4 times': ['2', '2', '2', '2'],
    'move D8 from stock to pile 2': ['1', 's', 'D8', 'p', '2'],
    'move HA from pile 6 to foundation c': ['1', 'p', '6', 'HA', 'f', 'c'],
    '3 deal stock': ['2'],
    'move D2 from stock to pile 3': ['1', 's', 'D2', 'p', '3'],
    '4 deal stock': ['2'],
    'move D9 from stock to pile 6': ['1', 's', 'D9', 'p', '6'],
    'move sT from pile 6 to pile 5 (2 cards)': ['1', 'p', '6', 'sT', 'p', '5'],
    '1 save': ['3']
}

commands = []

for name, move in moves.items():
    try:
        io.recvuntil('Enter choice: ')
        # print('Performing', name)
        for step in move:
            commands.append(step)
            io.sendline(step.encode())
        print('Performed', name)
    except: 
        break

with open('commands.txt', 'w') as f:
    f.write('\n'.join(commands))

io.interactive()
