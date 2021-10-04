import tkinter as tk
import random

count = 0


def bg_color_change():
    global win
    s = [i for i in str(random.randint(100000, 1000000))]
    w = ['a', 'b', 'c', 'd', 'f']
    for i in range(1, 6, 2):
        s[i] = random.choice(w)
    bgcolor = '#' + ''.join(s)
    win.config(bg=bgcolor)


def rgb_color_rand():
    s = [i for i in str(random.randint(100000, 1000000))]
    w = ['a', 'b', 'c', 'd', 'f']
    for i in range(1, 6, 2):
        s[i] = random.choice(w)
    bgcolor = '#' + ''.join(s)
    return bgcolor


def color_rand():
    colors = ['#eb3734', '#3499eb', '#4fbd70', '#bd79ad', '#d9d780', '#36856e']
    return random.choice(colors)


class My_Button(tk.Button):
    def __init__(self, master, x, y, *args, **kwargs):
        super(My_Button, self).__init__(master, width=3, bg=f'{color_rand()}', command=self.button_push)
        self.master = master
        self.x = x
        self.y = y
        self.status = self['bg']
        self.list_btn_for_change = []

    def __str__(self):
        return f'{self.status}[{self.x}] [{self.y}]'

    def __repr__(self):
        return f'{self.status}[{self.x}] [{self.y}]'

    def check_around(self, x, y, lst=[]):
        """
        Определяет такой ли цвет у кнопок по сторонам, как у нажатой кнопки.
        Добавляет кортеж с координатами таких кнопок в список.
        Рекурсивно проверяет у рядом стоящих одноцветных кнопок цвет соседних
        Возвращает список с координатами одноцветных с нажатой кнопок

        """

        temp_lst = lst
        mwb = Main_window.buttons
        # print(f'Start list {temp_lst}')
        count = 0
        if not (x, y) in temp_lst:
            temp_lst.append((x, y))
            count += 1
        center_btn = mwb[x][y]['bg']
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                btn = mwb[x + i][y + j]['bg']
                if btn == center_btn and (x + i, y + j) not in temp_lst:
                    temp_lst.append((x + i, y + j))
                    count += 1

        if count == 0:
            return temp_lst

        for row, col in temp_lst:
            if mwb[row][col]['bg'] == mwb[x][y]['bg']:
                if not (row == x and col == y):
                    self.check_around(row, col, temp_lst)

        return temp_lst

    def itarate_same_btn_lst(self, same_color_list, func):
        same_color_list = sorted(same_color_list, key=lambda x: (x[0], x[1]))
        for r, c in same_color_list:
            func(r, c)

    def colorate_btn(self, row, col, color='black'):
        if row and col:
            Main_window.buttons[row][col].config(bg=color, state='disabled')

    def change_clr_to_up_btn(self, row, col):
        """
        функция изменяет цвет по всей колонке.
        :param row:
        :param col:
        :return:
        """
        mwb = Main_window.buttons

        for i in range(row, -1, -1):
            btn = mwb[i][col]
            btn2 = mwb[i - 1][col]
            if btn2['bg'] == 'black':
                btn['bg'] = 'black'
            else:
                btn2['bg'], btn['bg'] = btn['bg'], btn2['bg']

    def counter_scores(self, same_btns):
        Main_window.scores += len(same_btns) ** 2

    def button_push(self):
        same_color_btn = self.check_around(self.x, self.y, [])
        if len(same_color_btn) > 1:
            self.counter_scores(same_color_btn)
            print(Main_window.scores)
            self.itarate_same_btn_lst(same_color_btn, self.change_clr_to_up_btn)
            black_column = []
            black_column = Main_window.check_low_row()
            if black_column:
                Main_window.shift_column(black_column)
                black_column = []



class Main_window:
    ROW = 20
    COLUMN = 10
    buttons = []
    scores = 0

    def __init__(self):
        self.win = tk.Tk()
        self.win.title('Color Cubs')
        # photo = tk.PhotoImage(file='Logo.png')
        # self.win.iconphoto(False, photo)
        # self.win.geometry('800x600+500+200')
        self.win.config(bg='#8eb6ce')

        for row in range(Main_window.ROW + 2):
            temp = []
            for col in range(Main_window.COLUMN + 2):
                btn = My_Button(self.win, x=row, y=col)
                temp.append(btn)
                btn.grid(row=row, column=col)
                if col == 0 or col == Main_window.COLUMN + 1 or row == 0 or row == Main_window.ROW + 1:
                    btn.config(bg='black', state='disabled')
            Main_window.buttons.append(temp)

    def finish_game(self):
        pass

    def creat_menu(self):
        menubar = tk.Menu(self.win)
        self.win.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Game', command=self.start_new_round)
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
        print(empty_column_list)
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


    def start_new_round(self):
        self.creat_menu()
        self.win.mainloop()


a = Main_window()

a.start_new_round()
