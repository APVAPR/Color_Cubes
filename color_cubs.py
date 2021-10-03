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
    colors = ['red', 'blue', 'green', 'pink', 'yellow', 'grey']
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
        print(f'Start list {temp_lst}')
        count = 0
        if not (x, y) in temp_lst:
            temp_lst.append((x, y))
            count += 1

        if mwb[x][y]['bg'] == mwb[x][y - 1]['bg'] and (x, y - 1) not in temp_lst:
            temp_lst.append((x, y - 1))
            count += 1
            print('Добавил левую')
        if mwb[x][y]['bg'] == mwb[x][y + 1]['bg'] and (x, y + 1) not in temp_lst:
            temp_lst.append((x, y + 1))
            count += 1
            print('Добавил правую')
        if mwb[x][y]['bg'] == mwb[x - 1][y]['bg'] and (x - 1, y) not in temp_lst:
            temp_lst.append((x - 1, y))
            count += 1
            print('Добавил верхнюю')
        if mwb[x][y]['bg'] == mwb[x + 1][y]['bg'] and (x + 1, y) not in temp_lst:
            temp_lst.append((x + 1, y))
            count += 1
            print('Добавил нижнюю')
        if count == 0:
            print('Остался один экземпляр')
            return temp_lst

        for row, col in temp_lst:
            print(f'row = {row}, x = {x}')
            print(f'col = {col}, y = {y}')
            if mwb[row][col]['bg'] == mwb[x][y]['bg']:
                if not (row == x and col == y):
                    print('Для всех кроме центральной применяю рекрсивную функцию ')
                    self.check_around(row, col, temp_lst)

                    print('Рекурсивная функция отработрала')
        print(f'Возвращаю список {temp_lst}')
        return temp_lst

    def change_color(self, same_color_list):
        for r, c in same_color_list:
            Main_window.buttons[r][c].config(bg='black', state='disabled')

    def button_push(self):
        same_color_btn = self.check_around(self.x, self.y, [])
        self.change_color(same_color_btn)


class Main_window:
    ROW = 20
    COLUMN = 10
    buttons = []

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

    def check_color(self):
        pass

    def start_new_round(self):
        self.win.mainloop()


a = Main_window()

a.start_new_round()
