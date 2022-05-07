import tkinter as tk
import random
from texttable import Texttable

count = 0
colors_name = {'#eb3734': 'red', '#3499eb': 'blue', '#4fbd70': 'green', '#bd79ad': 'pink', '#d9d780': 'yellow',
               '#36856e': 'darkgreen', }


def color_rand():
    colors = ['#eb3734', '#3499eb', '#4fbd70', '#bd79ad', '#d9d780', '#36856e']
    return random.choice(colors)


class My_Button(tk.Button):
    def __init__(self, master, x, y, *args, **kwargs):
        super().__init__(master, width=3, bg=f'{color_rand()}', command=self.button_push)
        self.master = master
        self.x = x
        self.y = y
        self.status = self['bg']
        self.list_btn_for_change = []

    def __str__(self):
        if self["bg"] == 'black':
            return f'{self["bg"]}[{self.x}] [{self.y}]'
        return f'{colors_name[self.status]}[{self.x}] [{self.y}]'

    def __repr__(self):
        if self["bg"] == 'black':
            return f'{self["bg"]}[{self.x}] [{self.y}]'
        return f'{colors_name[self.status]}[{self.x}] [{self.y}]'

    def button_push(self):
        same_color_btn = self.check_around(self.x, self.y, [])
        if len(same_color_btn) > 1:
            Main_window.counter_scores(same_color_btn)
            self.itarate_same_btn_lst(same_color_btn, self.change_clr_to_up_btn)
            black_column = Main_window.check_low_row()
            if black_column:
                Main_window.shift_column(black_column)

    def check_around(self, x, y, some_btn_lst=None):
        """
        Определяет такой ли цвет у соседних кнопок, как у нажатой кнопки.
        Добавляет кортеж с координатами таких кнопок в список.
        Рекурсивно проверяет у рядом стоящих одноцветных кнопок цвет соседних
        Возвращает список с координатами одноцветных с нажатой кнопок

        """
        if some_btn_lst is None:
            some_btn_lst = []
        mwb = Main_window.buttons
        count = 0
        if not (x, y) in some_btn_lst:
            some_btn_lst.append((x, y))
            count += 1
        center_btn = mwb[x][y]['bg']
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                btn = mwb[x + i][y + j]['bg']
                if btn == center_btn and (x + i, y + j) not in some_btn_lst:
                    some_btn_lst.append((x + i, y + j))
                    count += 1
        if count == 0:
            return some_btn_lst

        for row, col in some_btn_lst:
            if mwb[row][col]['bg'] == mwb[x][y]['bg']:
                if not (row == x and col == y):
                    self.check_around(row, col, some_btn_lst)
        return some_btn_lst

    @staticmethod
    def itarate_same_btn_lst(same_color_list, func):
        same_color_list = sorted(same_color_list, key=lambda x: (x[0], x[1]))
        for r, c in same_color_list:
            func(r, c)

    @staticmethod
    def colorate_btn(row, col, color='black'):
        if row and col:
            Main_window.buttons[row][col].config(bg=color, state='disabled')

    @staticmethod
    def change_clr_to_up_btn(row, col):
        """
        функция изменяет цвет по всей колонке.

        """
        mwb = Main_window.buttons

        for i in range(row, -1, -1):
            btn = mwb[i][col]
            btn2 = mwb[i - 1][col]
            if btn2['bg'] == 'black':
                btn['bg'] = 'black'
            else:
                btn2['bg'], btn['bg'] = btn['bg'], btn2['bg']




class Main_window:
    win = tk.Tk()
    win.title('Color Cubs')
    win.config(bg='#8eb6ce')

    ROW = 10
    COLUMN = 5
    buttons = []
    scores = 0

    def __init__(self):

        for row in range(Main_window.ROW + 2):
            temp = []
            for col in range(Main_window.COLUMN + 2):
                btn = My_Button(self.win, x=row, y=col)
                temp.append(btn)
                btn.grid(row=row, column=col)
                if col == 0 or col == Main_window.COLUMN + 1 or row == 0 or row == Main_window.ROW + 1:
                    btn.config(bg='black', state='disabled')
            Main_window.buttons.append(temp)

    def creat_menu(self):
        menubar = tk.Menu(self.win)
        self.win.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Game', command=self.reload_game)
        file_menu.add_command(label='Settings')
        file_menu.add_command(label='Quit', command=self.win.destroy)
        menubar.add_cascade(label='File', menu=file_menu)

    @staticmethod
    def check_low_row():
        empty_column_list = []
        for col in range(1, Main_window.COLUMN):
            btn = Main_window.buttons[Main_window.ROW][col]
            if btn['bg'] == 'black':
                empty_column_list.append(col)
        return empty_column_list

    @staticmethod
    def shift_column(black_col_list):
        for black_column in black_col_list:
            for row in range(Main_window.ROW, -1, -1):
                for col in range(black_column, 0, -1):
                    btn1 = Main_window.buttons[row][col]
                    btn2 = Main_window.buttons[row][col - 1]
                    if btn2['bg'] == btn1['bg'] == 'black':
                        continue
                    else:
                        btn1['bg'], btn2['bg'] = btn2['bg'], btn1['bg']

    @staticmethod
    def counter_scores(same_btns):
        Main_window.scores += len(same_btns) ** 2

    @staticmethod
    def show_in_console():
        table = Texttable()
        for i in Main_window.buttons:
            table.add_row(i)

        score_row = ['' for j in range(len(i))]
        score_row[-1] = Main_window.scores
        score_row[-2] = 'Score is:'
        table.add_row(score_row)
        print(table.draw())

    def reload_game(self):
        print(self.win.winfo_children())
        [child.destroy() for child in self.win.winfo_children()]
        Main_window.scores = 0
        self.__init__()
        # self.start_new_round()

    def finish_game(self):
        pass

    def start_new_round(self):
        self.creat_menu()
        self.win.mainloop()


if __name__ == '__main__':
    a = Main_window()
    a.start_new_round()
