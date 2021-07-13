class ConnectFour:
    import numpy as np
    import time
    from blessed import Terminal

    term = Terminal()
    style_default = term.white_on_blue
    style_p1 = term.yellow_on_blue
    style_p2 = term.red_on_blue

    min_nRow_nCol = 4
    max_nCol = 26
    COL_SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    TITLE = "Connect Four"

    TITLE = ["  _____                       __    ____             \n",
             " / ___/__  ___  ___  ___ ____/ /_  / __/__  __ ______\n",
             "/ /__/ _ \\/ _ \\/ _ \\/ -_) __/ __/ / _// _ \\/ // / __/\n",
             "\\___/\\___/_//_/_//_/\\__/\\__/\\__/ /_/  \\___/\\_,_/_/   \n"]

    ################################################################
    with term.cbreak(), term.hidden_cursor():
        # clear the screen
        print(term.home + term.white_on_blue + term.clear)

        for i in range(len(TITLE)):
            title_part = term.move_xy(term.width//2-len(TITLE[0])//2,
                                      term.height//2-len(TITLE)//2+i) + \
                         TITLE[i]
            print(title_part, end="", flush=True)

        start_txt = False
        start = term.move_xy(term.width//2-8, term.height*3//4) + \
            "Press S to start"
        start_erase = term.move_xy(term.width//2-8, term.height*3//4) + \
            "                "
        while term.inkey(timeout=0.75) != "s":
            if not start_txt:
                print(start, end="", flush=True)
                start_txt = True
            else:
                print(start_erase, end="", flush=True)
                start_txt = False

    print(term.home + term.clear)

    ################################################################
    def __init__(self):
        """__init__"""
        print(self.term.home + self.term.clear)
        self.num_row, self.num_col = self.get_nrow_ncol()
        self.avail_choices = set(range(self.num_col))
        self.matrix = self.np.zeros((self.num_row, self.num_col), self.np.int8)

    def get_nrow_ncol(self):
        """set custom board size"""
        num_row, num_col = None, None
        size = self.term.move_xy(self.term.width//2-32,
                                 self.term.height//3) + \
            "Please enter the size of the board " + \
            "in the format HEIGHT x WIDTH.\n"
        print(size, end="", flush=True)
        size_buffer = self.term.move_y(self.term.height//2) + \
            f"\n{' '*(self.term.width//2-2)}"

        while True:
            try:
                print(size_buffer, end="", flush=True)
                num_row, num_col = input("").split("x", 2)
            except ValueError:
                error = self.term.move_xy(self.term.width//2-18,
                                          self.term.height//3) + \
                        "Please use the format HEIGHT x WIDTH."
                print(self.term.home + self.term.clear)
                print(error, end="", flush=True)
                continue
            try:
                num_row, num_col = int(num_row), int(num_col)
            except ValueError:
                error = self.term.move_xy(self.term.width//2-22,
                                          self.term.height//3) + \
                        "Both height and width must be integer values."
                num_row, num_col = None, None
                print(self.term.home + self.term.clear)
                print(error, end="", flush=True)
                continue
            except TypeError:
                error = self.term.move_xy(self.term.width//2-18,
                                          self.term.height//3) + \
                        "Please use the format HEIGHT x WIDTH."
                num_row, num_col = None, None
                print(self.term.home + self.term.clear)
                print(error, end="", flush=True)
                continue
            if num_row < self.min_nRow_nCol or num_col < self.min_nRow_nCol:
                error = self.term.move_xy(self.term.width//2-20,
                                          self.term.height//3) + \
                    "Both height and width " + \
                    f"must be at least {self.min_nRow_nCol}."
                num_row, num_col = None, None
                print(self.term.home + self.term.clear)
                print(error, end="", flush=True)
                continue
            elif num_col > self.max_nCol:
                error = self.term.move_xy(self.term.width//2-15,
                                          self.term.height//3) + \
                        f"Width must be no more than {self.max_nCol}."
                num_row, num_col = None, None
                print(self.term.home + self.term.clear)
                print(error, end="", flush=True)
                continue
            else:
                break
        return num_row, num_col

    def start(self):
        """plays game of set size"""
        print(self.term.home + self.term.clear)
        cur_player = 1
        end = False
        number_of_moves = 0
        total_moves = self.num_row * self.num_col

        col_head_txt = f"  {self.COL_SYMBOLS[0]}"
        for i in range(1, self.num_col):
            col_head_txt += f"   {self.COL_SYMBOLS[i]}"
        col_head = self.term.move_xy(self.term.width//2-(self.num_col*4+1)//2,
                                     self.term.height//4) + col_head_txt
        print(col_head, end="\n", flush=True)

        for i in range(self.num_row):
            print(" " * (self.term.width//2-(self.num_col*4+1)//2), end="")
            for j in range(self.num_col):
                print(f"│ {self.matrix[i][j]} ", end="")
            print("│")
        print(" " * (self.term.width//2-(self.num_col*4+1)//2), end="")
        print("⎺"*(self.num_col*4+1))

        prompt1_p1 = self.term.move_xy(
                         self.term.width//2-8,
                         self.term.height//4+self.num_row+5) + \
            f"Player {self.style_p1('1')+self.style_default}'s turn."
        prompt1_p2 = self.term.move_xy(
                         self.term.width//2-8,
                         self.term.height//4+self.num_row+5) + \
            f"Player {self.style_p2('2')+self.style_default}'s turn."
        prompt1_win1 = self.term.move_xy(
                           self.term.width//2-8,
                           self.term.height//4+self.num_row+5) + \
            f"Player {self.style_p1('1') + self.style_default} has won!"
        prompt1_win2 = self.term.move_xy(
                           self.term.width//2-8,
                           self.term.height//4+self.num_row+5) + \
            f"Player {self.style_p2('2') + self.style_default} has won!"
        prompt1_draw = self.term.move_xy(
                           self.term.width//2-6,
                           self.term.height//4+self.num_row+5) + \
            "Game is over!"
        prompt1_erase = self.term.move_xy(
                            self.term.width//2-8,
                            self.term.height//4+self.num_row+5) + \
            "                  "

        last_col = self.COL_SYMBOLS[self.num_col-1]
        prompt2 = self.term.move_xy(self.term.width//2-18,
                                    self.term.height//4+self.num_row+7) + \
            "Choose a column by typing its letter."
        prompt2_error = self.term.move_xy(
                            self.term.width//2-21,
                            self.term.height//4+self.num_row+7) + \
            f"Invalid column. Choose a column from A to {last_col}"
        prompt2_full = self.term.move_xy(
                           self.term.width//2-23,
                           self.term.height//4+self.num_row+7) + \
            f"Column is full. Choose a column from A to {last_col}"
        prompt2_erase = self.term.move_xy(
                            self.term.width//2-23,
                            self.term.height//4+self.num_row+7) + \
            "                                               "
        prompt2_end = self.term.move_xy(self.term.width//2-18,
                                        self.term.height//4+self.num_row+7) + \
            "Press R to restart, press Q to quit."

        with self.term.cbreak(), self.term.hidden_cursor():
            print()
            print()
            if cur_player == 1:
                print(prompt1_erase+prompt1_p1, end="", flush=True)
            else:
                print(prompt1_erase+prompt1_p2, end="", flush=True)
            print(prompt2_erase+prompt2, end="", flush=True)
            while not end:
                valid = False

                while not valid:
                    try:
                        choice_sym = self.term.inkey(timeout=0.5)
                        if not choice_sym:
                            continue
                        choice = int(self.COL_SYMBOLS.index(
                                         choice_sym.upper()))
                    except ValueError:
                        print(prompt2_error, end="", flush=True)
                        continue
                    valid = self.check_choice(choice,
                                              prompt2_error, prompt2_full)

                if cur_player == 1:
                    print(prompt1_erase+prompt1_p2, end="", flush=True)
                else:
                    print(prompt1_erase+prompt1_p1, end="", flush=True)
                print(prompt2_erase+prompt2, end="", flush=True)
                row = self.drop(cur_player, choice)

                number_of_moves += 1
                if self.check_win(cur_player, choice, row):
                    if cur_player == 1:
                        print(prompt1_win1, end="", flush=True)
                    else:
                        print(prompt1_win2, end="", flush=True)
                    end = True
                if number_of_moves == total_moves:
                    print(prompt1_erase+prompt1_draw, end="", flush=True)
                    end = True
                # Switch players
                if cur_player == 1:
                    cur_player = 2
                else:
                    cur_player = 1

            print(prompt2_erase+prompt2_end, end="", flush=True)
            while True:
                choice_sym = self.term.inkey(timeout=0.5)
                if choice_sym == "r":
                    return True
                if choice_sym == "q":
                    print(f"\n\n\n\n{' '*(self.term.width//2-16)}" + \
                          "GAME ENDED. RETURN TO MAIN MENU.\n\n\n")
                    return False

    def column_is_full(self, column):
        """check if a chosen column is full"""
        for i in range(self.num_row):
            if self.matrix[i][column] == 0:
                return False
        return True

    def check_choice(self, choice, prompt2_error, prompt2_full):
        """check if a chosen column is within the board"""
        if choice not in self.avail_choices:
            print(prompt2_error, end="", flush=True)
            return False
        if self.column_is_full(choice):
            print(prompt2_full, end="", flush=True)
            return False
        return True

    def drop(self, cur_player, column):
        """drops a disc in a column"""
        for i in range(self.num_row):
            self.time.sleep(0.15)
            if cur_player == 1:
                disc_text = self.style_p1("1")
            else:
                disc_text = self.style_p2("2")
            disc = self.term.move_xy(
                     self.term.width//2-(self.num_col*4+1)//2+2+4*column,
                     self.term.height//4+1+i) + disc_text
            disc_erase = self.term.move_xy(
                           self.term.width//2-(self.num_col*4+1)//2+2+4*column,
                           self.term.height//4+i) + self.style_default("0")
            if self.matrix[i][column] == 0:
                print(disc)
                if i > 0:
                    print(disc_erase)
            else:
                break
        for i in reversed(range(self.num_row)):
            if self.matrix[i][column] == 0:
                self.matrix[i][column] = cur_player
                break
        print(self.style_default)
        return i

    def check_win(self, cur_player, column, row):
        """check if a player has won"""
        count = 0
        for i in range(self.num_col):
            if self.matrix[row][i] == cur_player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

        # vertical
        count = 0
        for i in range(self.num_row):
            if self.matrix[i][column] == cur_player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

        # left diagonal
        count = 0
        diag = self.np.diag(self.matrix, column - row)
        for i in diag:
            if i == cur_player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

        # right diagonal
        count = 0
        diag = self.np.diag(self.np.fliplr(self.matrix),
                            (self.num_col - 1 - column) - row)
        for i in diag:
            if i == cur_player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0


if __name__ == '__main__':
    play = True
    while play:
        connectFour = ConnectFour()
        play = connectFour.start()
