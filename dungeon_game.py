import random

CELLS = [
    (0,0),(1,0),(2,0),(3,0),(4,0),
    (0,1),(1,1),(2,1),(3,1),(4,1),
    (0,2),(1,2),(2,2),(3,2),(4,2),
    (0,3),(1,3),(2,3),(3,3),(4,3),
    (0,4),(1,4),(2,4),(3,4),(4,4),
  ]

starting_cells = CELLS.copy()

class Game:
    def __init__(self, cells):
        self.CELLS = cells
        self.monster = Monster()
        self.player = Player()
        self.monster.check_if_too_close(self.player)
        self.egg_1 = Egg()
        self.egg_2 = Egg()
        self.egg_3 = Egg()
        self.basket = Basket()
        self.door = Door()

    def determine_monster_action(self):
        self.monster.chase_or_block()
        if self.monster.chase == 1:
            self.monster.move(self.player)
        else:
            if not self.player.has_basket:
                self.monster.move(self.basket)
            elif not self.player.has_eggs:
                self.monster.move(random.choice(Egg._eggs))
            else:
                self.monster.move(self.door)
        
    def drawMap(self):
        print('-'*21)
        for cell in self.CELLS:
            cell_empty = True
            for token in Token._all:
                if token.current_cell == cell:
                    print('|'+str(token), end = '')
                    cell_empty = False
                    break
            if cell_empty:
                print('|   ', end='')
            if cell[0] == 4:
                print('|\n'+'-'*21)

    def play(self):
        print("""
Welcome to the dungeon, oh adventurer! Your mission is to steal all three of the monster's eggs. To collect the 
eggs, you will need a basket to hold them in. Once you have all the eggs you can leave the dungeon through the 
door. But be careful! The monster is very protective of its eggs, and he can move diagonally, while you can only 
move up or down! And he may decide to chase after you or to protect the item you are seeking!If the monster 
catches you, it won't be pretty!""")
        while True:
            self.drawMap()
            self.determine_monster_action()
            self.player.move()
            # self.monster.check_cell()
            # if self.player.dead:
            #     break
            if self.player.wrong_move:
                self.player.wrong_move = False
                self.monster.undo_move()
                continue
            self.player.check_cell()
            if self.player.dead or self.player.escaped:
                break
            self.player.swapped(self.monster)
            if self.player.dead or self.player.escaped:
                break

        self.drawMap()
            
        
        print("Thanks for playing!")


    
    
class Token:
    _all = []
    
    def __init__(self):
        self.current_cell = starting_cells.pop(random.randint(0,len(starting_cells)-1))
        self._all.append(self)
        self.previous_cell = self.current_cell

    def move_up(self):
        self.previous_cell = self.current_cell
        self.current_cell = (self.current_cell[0], self.current_cell[1]-1)
    
    def move_down(self):
        self.previous_cell = self.current_cell
        self.current_cell = (self.current_cell[0], self.current_cell[1]+1)
    
    def move_left(self):
        self.previous_cell = self.current_cell
        self.current_cell = (self.current_cell[0]-1, self.current_cell[1])
    
    def move_right(self):
        self.previous_cell = self.current_cell
        self.current_cell = (self.current_cell[0]+1, self.current_cell[1])

    def check_cell(self):
        for token in self._all:
            if token != self:
                if token.current_cell == self.current_cell:
                    token.found(self)
        

    
class Player(Token):
    def __init__(self):
        super().__init__()
        self.has_basket = False
        self.has_eggs = False
        self.dead = False
        self.escaped = False
        self.eggs = 0
        self.player = True
        self.wrong_move = False
        

    def __str__(self):
        return ' P '
        
    
    def move(self):
        print(f'Current cell: {self.current_cell}\nWhere would you like to move?')
        direction = input("Enter 'u' for up, 'd' for down, 'l' for left, or 'r' for right: \n") 
        if direction == 'u':
            if self.current_cell[1] == 0:
                print("You can't move that direction. Try again")
                self.wrong_move = True
            else: 
                self.move_up()
        elif direction == 'd':
            if self.current_cell[1] == 4:
                print("You can't move that direction. Try again")
                self.wrong_move = True
            else:
                self.move_down()
        elif direction == 'l':
            if self.current_cell[0] == 0:
                print("You can't move that direction. Try again")
                self.wrong_move = True
            else:
                self.move_left()
        elif direction == 'r':
            if self.current_cell[0] == 4:
                print("You can't move that direction. Try again")
                self.wrong_move = True
            else:
                self.move_right()
        else:
            print('invalid prompt. Try again')
            self.wrong_move = True

    def found(self, finder):
        print("Uh oh, looks like the monster got you! You are now dead.")
        self.dead = True

    def swapped(self, enemy):

        if self.current_cell[:] == enemy.previous_cell[:] and self.previous_cell[:] == enemy.current_cell[:]:
        
            print("Uh oh, looks like the monster got you! You can't move through the monster! You are now dead.")
            self.dead = True
    


class Monster(Token):
    def __init__(self):
        super().__init__()
        self.player = False
        self.chase = 0

    def check_if_too_close(self, prey):
        while abs(self.current_cell[0]-prey.current_cell[0]) < 2 and abs(self.current_cell[1]-prey.current_cell[1]) < 2:
            new_cell = starting_cells.pop(random.randint(0,len(starting_cells)-1))
            starting_cells.append(self.current_cell)
            self.current_cell = new_cell
        
    def move_up_left(self):
        self.previous_cell = self.current_cell  
        self.current_cell = (self.current_cell[0]-1, self.current_cell[1]-1)

    def move_up_right(self):
        self.previous_cell = self.current_cell    
        self.current_cell = (self.current_cell[0]+1, self.current_cell[1]-1)
    
    def move_down_left(self):
        self.previous_cell = self.current_cell  
        self.current_cell = (self.current_cell[0]-1, self.current_cell[1]+1)

    def move_down_right(self):
        self.previous_cell = self.current_cell    
        self.current_cell = (self.current_cell[0]+1, self.current_cell[1]+1)

      



    def move(self, prey):
        if self.current_cell[0] < prey.current_cell[0] and self.current_cell[1] < prey.current_cell[1]:
            self.move_down_right()
        elif self.current_cell[0] < prey.current_cell[0] and self.current_cell[1] > prey.current_cell[1]:
            self.move_up_right()
        elif self.current_cell[0] > prey.current_cell[0] and self.current_cell[1] < prey.current_cell[1]:
            self.move_down_left()
        elif self.current_cell[0] > prey.current_cell[0] and self.current_cell[1] > prey.current_cell[1]:
            self.move_up_left()
        elif self.current_cell[0] > prey.current_cell[0]:
            self.move_left()
        elif self.current_cell[0] < prey.current_cell[0]:
            self.move_right()
        elif self.current_cell[1] > prey.current_cell[1]:
            self.move_up()
        elif self.current_cell[1] < prey.current_cell[1]:
            self.move_down()

    def chase_or_block(self):
        self.chase = random.randint(0,1)
        

    def undo_move(self):
        self.current_cell = self.previous_cell

    def __str__(self):
        return ' M '

    def found(self, finder):
        print("Uh oh, looks like the monster got you! You are now dead.")
        finder.dead = True
        

class Egg(Token):
    _eggs = []
    
    def __init__(self):
        super().__init__()
        self._all.append(self)
        self._eggs.append(self)
    
    def found(self, finder):
        if finder.player:
            if finder.dead:
                return
            if finder.has_basket:
                finder.eggs += 1
                self._eggs.remove(self)
                self.current_cell = None
                if finder.eggs < 3:
                    print(f"Congradulations, you've found an egg! Only {3-finder.eggs} to go.")
                elif finder.eggs == 3:
                    finder.has_eggs = True
                    print("Congradulations, you found all the eggs! Now try to find the door... before the monster gets you!")
            else:
                print("Sorry, you need a basket to collect this egg.")
        

    def __str__(self):
        return ' E '

class Basket(Token):
    def found(self,finder):
        if finder.player:
            if finder.dead:
                return
            print("Congradulations, You've found the basket! Now collect the three eggs.")
            finder.has_basket = True
            self.current_cell = None

    def __str__(self):
        return ' B '

class Door(Token):
    def found(self, finder):
            if finder.player:
                if finder.dead:
                    return
                if finder.has_eggs:
                    print("Congradulations, you have escaped the dungeon with all the eggs!!")
                    finder.escaped = True
                else:
                    print("Sorry, you need all three eggs to exit the dungeon.")

    def __str__(self):
        return ' D '


my_game = Game(CELLS)
my_game.play()