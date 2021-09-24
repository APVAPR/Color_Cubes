import tkinter as tk
import random


def print_hello():
    return 'hello'


count = 0


def sklonenie():
    global count
    for i in range(2, 5):
        if count % 10 == i:
            return 'раза'
    return 'раз'


def counter():
    global count
    count += 1
    button1['text'] = f'Нажали {count} {sklonenie()}'


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
        super(My_Button, self).__init__(master, width=3, bg=f'{color_rand()}', command=self.check_status)
        self.master = master
        self.x = x
        self.y = y
        self.status = self['bg']


    def __str__(self):
        return f'{self.status}, {self.x}, {self.y}'


    def check_around(self, lst=[]):
        """
        Check color around self button

        """
        same_color_btn_tmp = lst

        if len(same_color_btn_tmp) == 1:
            return same_color_btn_tmp

        for i in range(-1, 2):
            btn_around = Main_window.buttons[self.x][self.y + i]
            if btn_around['bg'] == self['bg']:
                same_color_btn_tmp.append(btn_around)
                self.check_around(btn_around)
        btn_around = Main_window.buttons[self.x - 1][self.y]
        if btn_around['bg'] == self['bg']:
            same_color_btn_tmp.append(btn_around)
            self.check_around(btn_around)
        btn_around = Main_window.buttons[self.x + 1][self.y]
        if btn_around['bg'] == self['bg']:
            same_color_btn_tmp.append(btn_around)
            self.check_around(btn_around)
        return same_color_btn_tmp


        # same_color_btn_tmp = []
        # count = 0
        # for i in range(-1, 2):
        #     btn_around = Main_window.buttons[self.x][self.y + i]
        #     if btn_around['bg'] == self['bg']:
        #         same_color_btn_tmp.append(btn_around)
        #         count += 1
        # btn_around = Main_window.buttons[self.x - 1][self.y]
        # if btn_around['bg'] == self['bg']:
        #     same_color_btn_tmp.append(btn_around)
        #     count += 1
        # btn_around = Main_window.buttons[self.x + 1][self.y]
        # if btn_around['bg'] == self['bg']:
        #     same_color_btn_tmp.append(btn_around)
        #     count += 1
        # print(count, same_color_btn_tmp)


    def check_status(self):
        print(self.check_around())


class Main_window:
    ROW = 20
    COLUMN = 10
    buttons = []

    def __init__(self):
        self.win = tk.Tk()
        self.win.title('Color Cubs')
        photo = tk.PhotoImage(file='Logo.png')
        self.win.iconphoto(False, photo)
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
