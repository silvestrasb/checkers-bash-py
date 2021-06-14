#!/usr/bin/python3
import curses
import time

menu = ['Checkers', 'Exit']

class Zirgas:

    def __init__(self, stdscr, current_x, current_y):
        self.current_x = current_x
        self.current_y = current_y
        self.stdscr = stdscr
        self.board = Zirgas.board()
        self.temp_board = Zirgas.board()

    def board():
        board = []

        for a in range(8):
            board.append("|" + " |" * 8 + str(8 - a))

        board.append(" 8 7 6 5 4 3 2 1")

        return board

    def point(self, x, y, sign="X", temp=True):
        kelintas_y = 8 - y

        if temp:
            board = self.temp_board
        else:
            board = self.board

        eilute = board[kelintas_y][1:]

        self.current_x = x
        self.current_y = y
        kelintas_y = 8 - y
        pakeista_eilute = '|'
        kelintas_x = 2 * (8 - x)
        changed_item = ''

        for a in range(len(eilute)):
            if a == kelintas_x:
                changed_item = eilute[a]
                pakeista_eilute += sign
                continue
            pakeista_eilute += eilute[a]

        if temp:
            self.board = board[:]
            self.board[kelintas_y] = pakeista_eilute
        else:
            self.board[kelintas_y] = pakeista_eilute
            self.temp_board[kelintas_y] = pakeista_eilute

        return changed_item

    def chekers_board(self):
        self.point(8, 1, "O", False)
        self.point(8, 3, "O", False)
        self.point(7, 2, "O", False)
        self.point(6, 1, "O", False)
        self.point(6, 3, "O", False)
        self.point(5, 2, "O", False)
        self.point(4, 1, "O", False)
        self.point(4, 3, "O", False)
        self.point(3, 2, "O", False)
        self.point(2, 1, "O", False)
        self.point(2, 3, "O", False)
        self.point(1, 2, "O", False)

        self.point(8, 7, "@", False)
        self.point(7, 8, "@", False)
        self.point(7, 6, "@", False)
        self.point(6, 7, "@", False)
        self.point(5, 8, "@", False)
        self.point(5, 6, "@", False)
        self.point(4, 7, "@", False)
        self.point(3, 8, "@", False)
        self.point(3, 6, "@", False)
        self.point(2, 7, "@", False)
        self.point(1, 8, "@", False)
        self.point(1, 6, "@", False)

    def print(self, announcement_text):
        self.point(self.current_x, self.current_y)
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        for row in range(len(self.board)):
            for square_idx, square in enumerate(self.board[row]):

                x = w // 2 - (len(self.board[1]) // 2 - square_idx)
                y = h // 2 - (len(self.board) // 2 - row)

                self.stdscr.addstr(y, x, square)

        h, w = self.stdscr.getmaxyx()
        x = w // 2 - len(announcement_text) // 2
        y = h // 2 - (len(self.board) // 2 - len(self.board) - 3)

        self.stdscr.addstr(y, x, announcement_text)
        self.stdscr.refresh()

    def forward(self):
        x = self.current_x
        y = self.current_y + 1
        return self.point(x, y)

    def backward(self):
        x = self.current_x
        y = self.current_y - 1
        return self.point(x, y)

    def left(self):
        x = self.current_x + 1
        y = self.current_y
        return self.point(x, y)

    def current_point(self):
        return point(self.current_x, self.current_y)

    def right(self):
        x = self.current_x - 1
        y = self.current_y
        return self.point(x, y)

    def path(self, current_x, current_y, move_x, move_y):
        change = abs(current_x - move_x)
        if abs(current_x - move_x)  == abs(current_y - move_y):
            if current_x + change == move_x and current_y + change == move_y:
                for a in range(change):
                    self.point(current_x, current_y, " ", False)
                    current_x += 1
                    current_y += 1
            elif current_x + change == move_x and current_y - change == move_y:
                for a in range(change):
                    self.point(current_x, current_y, " ", False)
                    current_x += 1
                    current_y -= 1
            elif current_x - change == move_x and current_y + change == move_y:
                for a in range(change):
                    self.point(current_x, current_y, " ", False)
                    current_x -= 1
                    current_y += 1
            elif current_x - change == move_x and current_y - change == move_y:
                for a in range(change):
                    self.point(current_x, current_y, " ", False)
                    current_x -= 1
                    current_y -= 1


def play_rectangle(stdscr):
    zirgas = Zirgas(stdscr, 0, 0)
    zirgas.chekers_board()
    zirgas.current_y = 4
    zirgas.current_x = 4
    zirgas.print("press f2 to rewind your moves")

    player_wants_to_move = False
    changed_item = str()
    memory = dict()
    turn = 0
    memory[turn] = zirgas.temp_board[:]
    while 1:

        x = zirgas.current_x
        y = zirgas.current_y

        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and y < 8:
            changed_item = zirgas.forward()

        elif key == curses.KEY_DOWN and y > 1:
            changed_item = zirgas.backward()

        elif key == curses.KEY_LEFT and x < 8:
            changed_item = zirgas.left()

        elif key == curses.KEY_RIGHT and x > 1:
            changed_item = zirgas.right()
        elif key == curses.KEY_F1:
            return 1
            break

        elif (key == curses.KEY_ENTER or key == 10 or key == 13) and player_wants_to_move:

            player_wants_to_move = False
            zirgas.path(start_x, start_y, x, y)

            if sign == "@" and y == 1:
                sign = "B"
            elif sign == "O" and y == 8:
                sign = "W"

            zirgas.point(x, y, sign, False)
            turn += 1
            memory[turn] = zirgas.temp_board[:]



        elif (key == curses.KEY_ENTER or key == 10 or key == 13) and not player_wants_to_move:

                start_x = x
                start_y = y
                sign = changed_item
                zirgas.point(x, y, " ", False)

                player_wants_to_move = True


        elif key == curses.KEY_F2 and not player_wants_to_move:
            if turn > 0:
                turn -= 1
                zirgas.temp_board = memory[turn]
                memory[turn] = zirgas.temp_board[:]


        announcement_text = ''

        zirgas.print(announcement_text)
        stdscr.refresh()


def print_board(stdscr, current_row_idx, current_line_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for a in range(3):
        for b in range(3):
            x = w // 2 - (b - 1)
            y = h // 2 - (a - 1)

            if a == current_row_idx and b == current_line_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, "X")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, "X")


def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row_idx = 0

    print_menu(stdscr, current_row_idx)

    while 1:
        key = stdscr.getch()

        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < (len(menu) - 1):
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if menu[current_row_idx] == "Exit":
                break
            elif menu[current_row_idx] == "Checkers":
                if play_rectangle(stdscr):
                    break
            stdscr.refresh()
            stdscr.getch()
        elif key == curses.KEY_F1:
            break

        print_menu(stdscr, current_row_idx)

        stdscr.refresh()


curses.wrapper(main)
