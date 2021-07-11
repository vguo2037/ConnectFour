import numpy as np

# variable number of rows & columns, ascii optimisations

MIN_NROW_NCOL = 4

MAX_NCOL = 26
COL_SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def get_nRow_nCol():
    num_row, num_col = None, None
    while True:
        try:
            num_row, num_col = input("").split("x", 2)
        except ValueError:
            print("Please use the format HEIGHT x WIDTH.")
            continue
        except EOFError:
            print("Keyboard interrupt")
            exit()

        try:
            num_row, num_col = int(num_row), int(num_col)
        except ValueError:
            print("Both height and width must be integer values.")
            num_row, num_col = None, None
            continue
        except TypeError:
            print("Please use the format HEIGHT x WIDTH.")
            num_row, num_col = None, None
            continue

        if num_row<MIN_NROW_NCOL or num_col<MIN_NROW_NCOL:
            print("Both height and width must be at least 4.")
            num_row, num_col = None, None
            continue
        elif num_col>MAX_NCOL:
            print(f"Width must be no more than {MAX_NCOL}.")
            num_row, num_col = None, None
            continue
        else:
            break
    return num_row, num_col

print("Please enter the number of rows and columns of board in the format HEIGHT x WIDTH.")
num_row, num_col = get_nRow_nCol()

class ConnectFour:
    CHOICES = set(range(num_col))

    def __init__(self):
        self.matrix = np.zeros((num_row, num_col), np.int8)

    def start(self):
        cur_player = 1
        end = False
        number_of_moves = 0
        total_moves = num_row * num_col

        while not end:
            valid = False
            
            print(f"  {COL_SYMBOLS[0]}", end="")
            for i in range(1, num_col):
                print(f"   {COL_SYMBOLS[i]}", end="")
            print()
            for i in range(num_row):
                for j in range(num_col):
                    print(f"│ {self.matrix[i][j]} ", end="")
                print("│")
            print("⎺"*(num_col*4+1))

            print(f'Player {cur_player} move. Choose a column by typing its letter:')
            while not valid:
                try:
                    choice_sym = input()
                    if not choice_sym:
                        continue
                    choice = int(COL_SYMBOLS.index(choice_sym))
                except ValueError:
                    print(f'Invalid column. Choose columns from A to {COL_SYMBOLS[num_col-1]}')
                    continue
                except EOFError:
                    print("Keyboard interrupt")
                    exit()
                valid = self.check_choice(choice)
            row = self.drop(cur_player, choice)
            number_of_moves += 1
            if self.check_win(cur_player, choice, row):
                print(f'Player {cur_player} has won!')

                print(f"  {COL_SYMBOLS[0]}", end="")
                for i in range(1, num_col):
                    print(f"   {COL_SYMBOLS[i]}", end="")
                print()
                for i in range(num_row):
                    for j in range(num_col):
                        print(f"│ {self.matrix[i][j]} ", end="")
                    print("│")
                print("⎺"*(num_col*4+1))

                end = True
            if number_of_moves == total_moves:
                print('Game is over!')
                end = True
            # Switch players
            if cur_player == 1:
                cur_player = 2
            else:
                cur_player = 1

    def column_is_full(self, column):
        for i in range(num_row):
            if self.matrix[i][column] == 0:
                return False
        return True

    def check_choice(self, choice):
        if choice not in self.CHOICES:
            print(f'Invalid column. Choose columns from A to {COL_SYMBOLS[choice]}')
            return False
        if self.column_is_full(choice):
            print('The column is full. Choose another one')
            return False
        return True

    def drop(self, cur_player, column):
        for i in reversed(range(num_row)):
            if self.matrix[i][column] == 0:
                self.matrix[i][column] = cur_player
                break
        return i

    def check_win(self, cur_player, column, row):
        # horizontal
        count = 0
        for i in range(num_col):
            if self.matrix[row][i] == cur_player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

        # vertical
        count = 0
        for i in range(num_row):
            if self.matrix[i][column] == cur_player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

        # left diagonal
        count = 0
        diag = np.diag(self.matrix, column - row)
        for i in diag:
            if i == cur_player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

        # right diagonal
        count = 0
        diag = np.diag(np.fliplr(self.matrix), (num_col - 1- column)-row)
        for i in diag:
            if i == cur_player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0


if __name__ == '__main__':
    connectFour = ConnectFour()
    connectFour.start()
