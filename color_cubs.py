import tkinter as tk
import random
from texttable import Texttable
import tkinter.font as font
from tkinter.messagebox import showinfo

count = 0
colors_name = {'#000000':'black', '#eb3734': 'red', '#3499eb': 'blue', '#4fbd70': 'green', '#bd79ad': 'pink', '#d9d780': 'yellow',
               '#36856e': 'darkgreen'}
colors_name_reverse = {v: k for k, v in colors_name.items()}


class My_Button(tk.Button):

    def __init__(self, master, x, y, *args, **kwargs):
        random_color = My_Button.color_rand()
        super().__init__(master, width=1, bg=f'{random_color}')
        self.master = master
        self.x = x
        self.y = y
        self._color = colors_name[random_color]

    def __str__(self):
        return colors_name[self['bg']]

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, col):
        if col[0] == '#':
            self['bg'] = col
            self._color = colors_name[self['bg']]
        else:
            self['bg'] = colors_name_reverse[col]
            self._color = col

    @staticmethod
    def color_rand():
        colors = ['#eb3734', '#3499eb', '#4fbd70', '#bd79ad', '#d9d780', '#36856e']
        return random.choice(colors)


class Main_window:
    win = tk.Tk()
    win.title('Color Cubs')
    win.config(bg='black')

    ROW = 5
    COLUMN = 5
    buttons = []
    scores = 0
    moves = 0

    def __init__(self):

        self.scores_label = None
        self.make_game_buttons_list()
        self.show_scores_label()
        self.start_new_round()

    def make_game_buttons_list(self):
        for row in range(self.ROW + 2):
            temp = []
            for col in range(self.COLUMN + 2):
                btn = My_Button(self.win, x=row, y=col)
                btn.config(command=lambda button=btn: self.button_push(button))
                temp.append(btn)
                btn.grid(row=row, column=col)
                if col == 0 or col == self.COLUMN + 1 or row == 0 or row == self.ROW + 1:
                    btn.color = '#000000'
                    btn.config(state=tk.DISABLED)
            self.buttons.append(temp)
        self.check_lonely_button()

    def show_scores_label(self):
        self.scores_label = tk.Label(self.win, text=f'Scores: {self.scores}', font='Arial')
        self.scores_label.grid(row=self.ROW + 3, column=self.COLUMN // 2, columnspan=500)

    def button_push(self, clicked_button: My_Button):
        same_color_btn = self.check_around(clicked_button.x, clicked_button.y, [])
        if len(same_color_btn) > 1:
            self.iterate_same_btn_lst(same_color_btn, self.change_color_column)
            black_column = self.check_low_row()
            if black_column:
                self.shift_column(black_column)
            self.change_button_state()
            self.counter_scores(same_color_btn)
            self.moves += 1
        self.show_in_console()
        self.scores_label.config(text=f'Moves: {self.moves} Scores: {self.scores}')
        self.is_finish_game()

    def check_around(self, x, y, some_btn_lst=None):
        """
        Определяет такой ли цвет у соседних кнопок, как у кнопки[x][y].
        Добавляет кортеж с координатами таких кнопок в список.
        Рекурсивно проверяет у рядом стоящих одноцветных кнопок цвет соседних
        Возвращает список с координатами одноцветных с нажатой кнопок

        """
        if some_btn_lst is None:
            some_btn_lst = []
        count = 0
        if not (x, y) in some_btn_lst:
            some_btn_lst.append((x, y))
            count += 1
        center_btn = self.buttons[x][y]
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                btn = self.buttons[x + i][y + j]
                if btn.color == center_btn.color and (x + i, y + j) not in some_btn_lst:
                    some_btn_lst.append((x + i, y + j))
                    count += 1
        if count == 0:
            return some_btn_lst

        for row, col in some_btn_lst:
            if self.buttons[row][col].color == self.buttons[x][y].color:
                if not (row == x and col == y):
                    self.check_around(row, col, some_btn_lst)
        return some_btn_lst

    def check_lonely_button(self):
        change_color = self.buttons[-2][1].color
        btns = []
        for row in self.buttons:
            for button in row:
                btns.append(button)
        btns = sorted(btns, key=lambda x: x.color)
        # for i in sorted(self.buttons, key=lambda color: color['bg']):
        #     if

        [print(i.color, i['bg']) for i in btns]
        print(len(btns))

    def change_button_state(self):
        for row in self.buttons:
            for button in row:
                if button.color == 'black' and button['state'] != 'disabled':
                    button['state'] = tk.DISABLED
                elif button.color != 'black' and button['state'] == 'disabled':
                    button['state'] = tk.NORMAL

    def change_color_column(self, row, col):
        """
        функция изменяет цвет по всей колонке.

        """
        for i in range(row, -1, -1):
            btn = self.buttons[i][col]
            btn2 = self.buttons[i - 1][col]
            if btn2.color == 'black':
                btn.color = 'black'
            else:
                btn2.color, btn.color = btn.color, btn2.color

    @staticmethod
    def iterate_same_btn_lst(same_color_list, func):
        same_color_list = sorted(same_color_list, key=lambda x: (x[0], x[1]))
        for r, c in same_color_list:
            func(r, c)

    def check_low_row(self):
        empty_column_list = []
        for col in range(1, self.COLUMN):
            btn = self.buttons[self.ROW][col]
            if btn.color == 'black':
                empty_column_list.append(col)
        return empty_column_list

    def shift_column(self, black_col_list):
        for black_column in black_col_list:
            for row in range(self.ROW, -1, -1):
                for col in range(black_column, 0, -1):
                    btn1 = self.buttons[row][col]
                    btn2 = self.buttons[row][col - 1]
                    btn1.color, btn2.color = btn2.color, btn1.color

    def counter_scores(self, same_btns):
        self.scores += len(same_btns) ** 2

    def create_menu(self):
        menubar = tk.Menu(self.win)
        self.win.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Game', command=self.reload_game)
        file_menu.add_command(label='Settings', command=self.create_settings_menu)
        file_menu.add_command(label='Quit', command=self.win.destroy)
        menubar.add_cascade(label='File', menu=file_menu)

    def create_settings_menu(self):
        setting_menu = tk.Toplevel(self.win)
        setting_menu.wm_title('Settings')
        tk.Label(setting_menu, text='Rows count:').grid(row=0, column=0)
        tk.Label(setting_menu, text='Column count:').grid(row=1, column=0)
        row_entry = tk.Entry(setting_menu)
        row_entry.insert(0, self.ROW)
        row_entry.grid(row=0, column=1)
        column_entry = tk.Entry(setting_menu)
        column_entry.insert(0, self.COLUMN)
        column_entry.grid(row=1, column=1)
        btn = tk.Button(setting_menu, text='Confirm', command=lambda: self.change_settings(row_entry, column_entry))
        btn.grid(row=2, column=0, columnspan=2)

    def change_settings(self, row: tk.Entry, column: tk.Entry):
        self.ROW = int(row.get())
        self.COLUMN = int(column.get())
        self.reload_game()

    def show_in_console(self):
        table = Texttable()
        for i in self.buttons:
            table.add_row(i)

        score_row = ['' for _ in range(len(i))]
        score_row[-1] = self.scores
        score_row[-2] = 'Score is:'
        table.add_row(score_row)
        print(table.draw())

    def reload_game(self):
        self.show_in_console()
        self.buttons.clear()
        [child.destroy() for child in self.win.winfo_children()]
        self.scores = self.moves = 0
        self.__init__()

    def is_all_buttons_black(self):
        for row in self.buttons:
            for button in row:
                if button.color != 'black':
                    return False
        return True

    def is_same_button_around(self, row, col):
        center_btn = self.buttons[row][col]
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                btn = self.buttons[row + i][col + j]
                if btn.color == center_btn.color and (btn is not center_btn):
                    return True
        return False

    def is_has_moves(self):
        for row in self.buttons[1: self.ROW + 1]:
            for button in row[1: self.COLUMN + 1]:
                if button['state'] != 'disabled':
                    if self.is_same_button_around(button.x, button.y):
                        return True
        return False

    @staticmethod
    def win_window(text, win_lose):
        win = tk.Toplevel()
        win.title('You win!' if win_lose else 'Game over!')
        # win.eval('tk::PlaceWindow %s center' % win.winfo_pathname(win.winfo_id()))
        label = tk.Label(win, text=text)
        label['font'] = font.Font(size=20)
        label.pack()

    def is_finish_game(self):
        is_finish = is_win = False

        if self.is_all_buttons_black():
            self.scores *= 2
            print("You win!!!")
            text = f'You win!!! Your score is: {self.scores}'
            is_finish = is_win = True

        elif not self.is_has_moves():
            print(f'Game over. Your score is : {self.scores}')
            text = f'Game over. Your score is: {self.scores}'
            is_finish = True
            is_win = False

        if is_finish:
            self.win_window(text, is_win)
            # showinfo('You win!' if is_win else 'Game over!', 'Game over')
            for row in self.buttons:
                for button in row:
                    if button['state'] == tk.NORMAL or button['state'] == tk.ACTIVE:
                        button['state'] = tk.DISABLED

    def start_new_round(self):
        self.create_menu()
        self.win.mainloop()


if __name__ == '__main__':
    a = Main_window()
