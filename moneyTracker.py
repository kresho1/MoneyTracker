import tkinter as tk
from tkinter import *
from tkinter import ttk
from decimal import *
import matplotlib.pyplot as plt
import matplotlib
import datetime
from tkinter import messagebox
import pymysql
import matplotlib.animation as animation
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import sys
import time
import psutil
import os

        
        
ENTRY_FONT = ("Consolas", 8, 'bold')
NAS_FONT = ("Consolas", 15)
LARGE_FONT = ("Consolas", 13)
CLOCK_FONT = ("Consolas", 10)


matplotlib.rcParams['text.color'] = '#FA8E4B'
matplotlib.rcParams['font.family'] = 'Consolas'
matplotlib.rcParams['lines.linewidth'] = 2
font1 = {'fontname':'Consolas'}
stanje_menija = 'normal'

raspon = 'month'
#chart rashoda
fig1, ax1 = plt.subplots()
fig1.set_facecolor('#424D59')
fig1.set_size_inches(3.7, 3.7)

def animateR(interval):
    global raspon
    if raspon == 'day':
        labels = PieChart('rashodi').raspon(raspon, 'kat')
        sizes = PieChart('rashodi').raspon(raspon, 'iznos')
    elif raspon == 'week':
        labels = PieChart('rashodi').raspon(raspon, 'kat')
        sizes = PieChart('rashodi').raspon(raspon, 'iznos')
    elif raspon == 'month':
        labels = PieChart('rashodi').raspon(raspon, 'kat')
        sizes = PieChart('rashodi').raspon(raspon, 'iznos')
    else:
        labels = PieChart('rashodi').kategorija()
        sizes = PieChart('rashodi').iznosi()
    def explodde(lista):
        
        explode = []
        for i in range(len(lista)):
            explode.append(0)
        explode[lista.index(max(lista))] = 0.1
        return tuple(explode)
    try:
        explode = explodde(sizes)
    except ValueError:
        explode = (0, 0)
        labels = ["Empty", "Empty"]
        sizes = [10, 10]
    ax1.clear()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.set_title('Statistika troskova', color="#FA8E4B", **font1)

#chart prihoda
fig2, ax2 = plt.subplots()
fig2.set_facecolor('#424D59')
fig2.set_size_inches(3.7, 3.7)
def animateP(interval):
    global raspon
    if raspon == 'day':
        labels = PieChart('prihodi').raspon(raspon, 'kat')
        sizes = PieChart('prihodi').raspon(raspon, 'iznos')
    elif raspon == 'week':
        labels = PieChart('prihodi').raspon(raspon, 'kat')
        sizes = PieChart('prihodi').raspon(raspon, 'iznos')
    elif raspon == 'month':
        labels = PieChart('prihodi').raspon(raspon, 'kat')
        sizes = PieChart('prihodi').raspon(raspon, 'iznos')
    else:
        labels = PieChart('prihodi').kategorija()
        sizes = PieChart('prihodi').iznosi()
        
    def explodde(lista):
        
        explode = []
        for i in range(len(lista)):
            explode.append(0)
        explode[lista.index(max(lista))] = 0.1
        return tuple(explode)
    
    try:
        explode = explodde(sizes)
    except ValueError:
        explode = (0, 0)
        labels = ["Empty", "Empty"]
        sizes = [10, 10]
    ax2.clear()
    ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax2.set_title('Statistika prihoda', color="#FA8E4B", **font1)


class MainWindow(Toplevel):
    def __init__(self, *args, **kwargs):  # metod koji kreira glavni prozor i smijesta frejm u njega
        Toplevel.__init__(self, *args, **kwargs)
        Toplevel.iconbitmap(self, default='money.ico')
        Toplevel.wm_title(self, 'Money Tracker')
        container = tk.Frame(self)  # kreiranje frejma
        container.grid(column=0, row=0, sticky='nsew')
        
        self.configure(background='#424D59')
        self.resizable(False, False)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container, background='#424D59', foreground="#FA8E4B") #glavna linija
        
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command = lambda: messagebox.showinfo("Obavjestenje", "Opcija u izdrad!!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.configure(foreground="#FA8E4B", background='#424D59')
        menubar.entryconfig("File", state=stanje_menija)
        
        
        valutaMenu = tk.Menu(menubar, tearoff=0)
        valutaMenu.add_command(label="Dinar (RSD)", command=valutaRSD)
        valutaMenu.add_command(label="Evro (EUR)", command=valutaEUR)
        valutaMenu.add_command(label="Dolar (USD)", command=valutaUSD)
        valutaMenu.add_command(label="Konvertibilna marka (BAM)", command=valutaBAM)
        menubar.add_cascade(label='Valuta', menu=valutaMenu)
        valutaMenu.configure(foreground="#FA8E4B", background='#424D59')
        menubar.entryconfig("Valuta", state=stanje_menija)
        vrijemeMenu = tk.Menu(menubar, tearoff=0)
        vrijemeMenu.add_command(label="Danas", command = setRasponDay)
        vrijemeMenu.add_command(label="Zadnjih 7 dana", command = setRasponWeek)
        vrijemeMenu.add_command(label="Zadnji mjesec", command = setRasponMonth)
        vrijemeMenu.add_command(label="Sve", command = setRasponAll)
        menubar.add_cascade(label='Vremenski raspon', menu=vrijemeMenu)
        vrijemeMenu.configure(foreground="#FA8E4B", background='#424D59')
        menubar.entryconfig("Vremenski raspon", state=stanje_menija)
        Toplevel.config(self, menu=menubar)

        self.frames = {}  # kreiranje dictionary-a, u koji se smjestaju stranice

        for F in (
                PageOne, PageTwo,
                PageThree):  # glavni dio... ovdje se ubacuju stranice... samo dodas naziv klase u kojoj si..
            # ..kreirao glavni prozor
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageOne)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        if cont == PageOne:
            self.geometry("373x630+600+100")
        elif cont == PageTwo:
            self.geometry("358x200+600+250")
        elif cont == PageThree:
            self.geometry("358x200+600+250")
  

def setRasponDay():
    global raspon
    raspon = 'day'

def setRasponMonth():
    global raspon
    raspon = 'month'

def setRasponWeek():
    global raspon
    raspon = 'week'

def setRasponAll():
    global raspon
    raspon = 'all'
  
def converter(iz, u, iznos):
            
    #din
    if iz == 'RSD' and u == 'RSD':
            conv = float(iznos)
            print('iz din u din')
    elif iz == 'RSD' and u == 'EUR':
            conv = float(iznos) / 123.6
            print(conv)
            print('iz din u Eur')
    elif iz == 'RSD' and u == 'USD':
            conv = float(iznos) / 113.9
            print(conv)
            print('iz din u dol')
    elif iz == 'RSD' and u == 'BAM':
            conv = float(iznos) / 63.3
            print(conv)
            print('iz din u bam')
    #BAM       
    if iz == 'BAM' and u == 'RSD':
            conv = float(iznos) * 63.3
            print(conv)
            print('iz bam u din')
    elif iz == 'BAM' and u == 'EUR':
            conv = float(iznos) * 0.51
            print(conv)
            print('iz bam u Eur')
    elif iz == 'BAM' and u == 'USD':
            conv = float(iznos) * 0.55
            print(conv)
            print('iz bam u dol')
    elif iz == 'BAM' and u == 'BAM':
            conv = float(iznos)
            print(conv)
            print('iz bam u bam')
                  

    #USD
    if iz == 'USD' and u == 'RSD':
            conv = float(iznos) * 113.9
            print(conv)
            print('iz dol u din')
    elif iz == 'USD' and u == 'EUR':
            conv = float(iznos) / 0.92
            print(conv)
            print('iz dol u eur')
    elif iz == 'USD' and u == 'USD':
            conv = float(iznos)
            print(conv)
            print('iz dol u dol')
    elif iz == 'USD' and u == 'BAM':
            conv = float(iznos) * 1.8
            print(conv)
            print('iz dol u bam')

    #EUR
    if iz == 'EUR' and u == 'RSD':
            conv = float(iznos) * 123.6
            print(conv)
            print('iz eur u din')
    elif iz == 'EUR' and u == 'EUR':
            conv = float(iznos)
            print(conv)
            print('iz eur u eur')
    elif iz == 'EUR' and u == 'USD':
            conv = float(iznos) * 1.08
            print(conv)
            print('iz eur u dol')
    elif iz == 'EUR' and u == 'BAM':
            conv = float(iznos) * 1.95
            print(conv)
            print('iz eur u bam')
    return '{0:.2f}'.format(conv)
def upload():
            bal = Novac()
            global trenVal
            global balans
            a = bal.balans()
            balans.set(str(a))

def upl():
            bal = Novac()
            global trenVal
            global balans
            a = bal.balans()
def valutaEUR():
            global trenVal
            global trenVal2
            global balans
            c = balans.get()
            balans.set(converter(trenVal2.get(), 'EUR', float(c) ))
            trenVal.set('**BALANS**\n   EUR')
            trenVal2.set('EUR')
            upl()
def valutaRSD():
            global trenVal
            global trenVal2
            global balans
            c = balans.get()
            balans.set(converter(trenVal2.get(), 'RSD', float(c)))
            trenVal.set('**BALANS**\n   RSD')
            trenVal2.set('RSD')
            upl()
def valutaUSD():
            global trenVal
            global trenVal2
            global balans
            c = balans.get()
            balans.set(converter(trenVal2.get(), 'USD', float(c)))
            trenVal.set('**BALANS**\n   USD')
            trenVal2.set('USD')
            upl()
def valutaBAM():
            global trenVal
            global trenVal2
            global balans
            c = balans.get()
            balans.set(converter(trenVal2.get(), 'BAM', float(c)))
            trenVal.set('**BALANS**\n   BAM')
            trenVal2.set('BAM')
            upl()

class PageOne(tk.Frame):
    
    
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)        
        global trenVal
        global trenVal2
        global balans
        balans = StringVar()
        trenVal = StringVar()
        trenVal2 = StringVar()
        trenVal2.set('RSD')
        trenVal.set('**BALANS**\n   RSD')
        bal = Novac()
        a = bal.balans()
        balans.set(str('{0:.2f}'.format(a)))
        #r= PieChart('prihodi').raspon('month', 'kat')
        
        
        if len(str(a)) <= 5:
            razmak = 150
        elif len(str(a)) <=8:
            razmak = 140
        else:
            razmak =90
        ttk.Style().configure("TNotebook", background='#424D59')
        ttk.Style().configure("TNotebook", lightcolor="#00BDD9")
        ttk.Style().configure("TNotebook.Tab", foreground="#424D59", background="#424D59")
        ttk.Style().configure("bluegray.TFrame", background="#00BDD9")
        ttk.Style().configure("sivi.TButton", background="#424D59", foreground="#424D59")
        ttk.Style().configure("nar.TLabel",  background="#FA8E4B")
        
        lFrame = ttk.Frame(self, style="bluegray.TFrame")
        lFrame.grid(column=0, row=3, sticky='nsew')
        balanceFrame = tk.Frame(self, background='#424D59')
        balanceFrame.grid(column=0, row=1, sticky='nsew')
        balanceLabel1 = ttk.Label(balanceFrame, textvariable=trenVal, font=LARGE_FONT, anchor=CENTER,
                                 background='#424D59', foreground="#FA8E4B")
        balanceLabel1.grid(column=1, row=0, sticky='w')
        balanceLabel2 = ttk.Label(balanceFrame, textvariable=balans, font=LARGE_FONT,
                                 background='#424D59', foreground="#FA8E4B")
        balanceLabel2.grid(column=1, row=1, columnspan=2, sticky='ew')
        balanceLabel1.place(x=140, y=1)
        balanceLabel2.place(x=razmak, y=45)
        tab = ttk.Notebook(self)
        pieFrameT = ttk.Frame(tab)
        pieFrameP = ttk.Frame(tab)
        tab.add(pieFrameT, text='Troskovi')
        tab.add(pieFrameP, text='Prihodi')
        tab.grid(column=0, row=0)

        self.slikaM = tk.PhotoImage(file='minus.png')
        self.slikaM = self.slikaM.subsample(2)
        self.slikaP = tk.PhotoImage(file='plus.png')
        self.slikaP = self.slikaP.subsample(2)
        self.lines = tk.PhotoImage(file='lines.png')
        self.lines = self.lines.subsample(4)

        lLabel1 = ttk.Label(balanceFrame, image=self.lines, style ="nar.TLabel")
        lLabel2 = ttk.Label(balanceFrame, image=self.lines, style ="nar.TLabel")
        lLabel1.grid(column=0, row=0, columnspan=1, sticky='nsew')
        lLabel2.grid(column=2, row=0, columnspan=1, sticky='e')
        lLabel2.place(x=310)

        button1 = tk.Button(lFrame, background='#424D59',
                            command=lambda: controller.show_frame(PageThree))
        button1.config(image=self.slikaM, compound=CENTER)
        button1.grid(column=0, row=0, sticky='w')
        button2 = tk.Button(lFrame, image=self.slikaP, background='#424D59',
                            command=lambda: controller.show_frame(PageTwo))
        button2.grid(column=1, row=0, sticky='e')

            
        #chart1
        
        ax1.axis('equal')
        canvas = FigureCanvasTkAgg(fig1, pieFrameT)
        canvas.show()
        canvas.get_tk_widget().pack()
        
##        toolbar = NavigationToolbar2TkAgg(canvas, pieFrameT)    #ostavio sam mogucnost da  ukljucim nav bar
##        toolbar.update()
##        canvas._tkcanvas.pack()

        #chart2
        
        ax2.axis('equal')
        canvas = FigureCanvasTkAgg(fig2, pieFrameP)
        canvas.show()
        canvas.get_tk_widget().pack()
        
        # toolbar = NavigationToolbar2TkAgg(canvas, pieFrameP)
        # toolbar.update()
        # canvas._tkcanvas.pack()
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='#424D59')
        ttk.Style().configure("tirkiz.TFrame", background="#424D59", foreground="#FA8E4B")
        ttk.Style().configure("my.TLabel", background="#424D59", foreground="#FA8E4B")
        ttk.Style().configure("moj.TCombobox", background="#FA8E4B", foreground="#424D59")
        ttk.Style().configure("moj.TButton", background="#FA8E4B", foreground="#424D59")
        def tick():
            time1 = ''
            time2 = time.strftime('%H:%M:%S')
            if time2 != time1:
                time1 = time2
                a= datetime.date.today()
                clock.config(text="Datum: {}\t\tVrijeme:  {}".format(a,time2),
                             background="#424D59", foreground="#FA8E4B", relief=SUNKEN)
            clock.after(200, tick)

        def unosUBazu():

            if katVar.get()=="" or opisKat.get()=="" or sumaNovca.get()=="":
                messagebox.showinfo("Greska", "Morate popuniti sva polja!")
                return
            else:
                try:
                    
                    ac= float(sumaNovca.get())
                    db = pymysql.connect("localhost", "root", "", "MoneyTracker")
                    cursor = db.cursor()
                    command = "INSERT INTO prihodi(kategorije, opis, iznos) VALUES('{}','{}','{}')".format(katVar.get(), opisKat.get(), sumaNovca.get())
                    try:
                        cursor.execute(command)
                        db.commit()
                        
                    except:

                        db.rollback()
                    db.close()
                    opisKat.set('')
                    sumaNovca.set('')
                    katVar.set('')
                    iznosEntry.focus_set()
                    upload()
                except ValueError:
                    messagebox.showinfo("Greska", "Iznos mora biti broj!")
                    sumaNovca.set('')


            
        sumaNovca = StringVar()
        katVar = StringVar()
        opisKat = StringVar()
        valVar = StringVar()
        
        clockFrame= ttk.Frame(self, style="tirkiz.TFrame")
        clockFrame.grid(column=0, row=0, sticky="ew")
        frame2 = ttk.Frame(self, style="tirkiz.TFrame")
        frame2.grid(column=0, row=1)




        clock = tk.Label(clockFrame, font=CLOCK_FONT)
        clock.grid(column=0, row=0)

        

        
        
        naslovP = ttk.Label(frame2, text='\t**Unos prihoda**\n', font=NAS_FONT, style="my.TLabel")
        naslovP.grid(column=0, row=0, columnspan=2, sticky='nsew')
        iznosLabel = ttk.Label(frame2, text='Iznos', font=LARGE_FONT, style="my.TLabel")
        iznosLabel.grid(column=0, row=1, sticky='e')
        opisLabel = ttk.Label(frame2, text='Opis', font=LARGE_FONT, style="my.TLabel")
        opisLabel.grid(column=0, row=3, sticky='e')
        kat = ttk.Label(frame2, text="Kategorija", font=LARGE_FONT, style="my.TLabel")
        kat.grid(row=2, column=0, sticky='e')
        
##        valutaLabel = ttk.Label(frame2, text='Valuta', font=LARGE_FONT, style="my.TLabel")
##        valutaLabel.grid(column=0, row=4, sticky='e')
##        valuta = ttk.Combobox(frame2, textvariable=valVar, width=40, style="moj.TCombobox")
##        valuta.grid(column=1, row=4)
##        valuta['values'] = ("Dinar(RSD)", "Euro(€)", "Konvertibilna marka(KM)", "Dolar($)")
##        valuta['state'] = 'readonly'
##        valuta.bind("<<ComboboxSelected>>", setVal)
        
        kategorija = ttk.Combobox(frame2, textvariable=katVar, width=40, style="moj.TCombobox")
        kategorija.grid(column=1, row=2)
        global katPrihod
        katPrihod = ["Plata", "Ustedjevina", "Bonusi", "Stipendija"]
        kategorija['values'] = (katPrihod)
        kategorija['state'] = 'readonly'
        iznosEntry = tk.Entry(frame2, textvariable=sumaNovca, width=40, font=ENTRY_FONT, foreground="#424D59", background="#FA8E4B")
        iznosEntry.grid(column=1, row=1, sticky='nsew')
        opis = tk.Entry(frame2, textvariable=opisKat, font=ENTRY_FONT, foreground="#424D59", background="#FA8E4B")
        opis.grid(column=1, row=3, sticky='nsew')
        unosBut = ttk.Button(self, text='Unesi', style='moj.TButton', command=unosUBazu)
        unosBut.grid(column=0, row=2)
        unosBut.place(x=280, y=175)
        nazadBut = ttk.Button(self, text='<<<', style='moj.TButton',
                              command=lambda: controller.show_frame(PageOne))
        nazadBut.grid(column=0, row=2)
        nazadBut.place(x=3, y=175)
        tick()


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='#424D59')
        ttk.Style().configure("tirkiz.TFrame", background="#424D59", foreground="#FA8E4B")
        ttk.Style().configure("my.TLabel", background="#424D59", foreground="#FA8E4B")
        ttk.Style().configure("moj.TCombobox", background="#FA8E4B", foreground="#424D59")
        ttk.Style().configure("moj.TButton", background="#FA8E4B", foreground="#424D59")
        def tick():
            time1 = ''
            time2 = time.strftime('%H:%M:%S')
            if time2 != time1:
                time1 = time2
                a= datetime.date.today()
                clock.config(text="Datum: {}\t\tVrijeme:  {}".format(a,time2),
                             background="#424D59", foreground="#FA8E4B", relief=SUNKEN)
            clock.after(200, tick)

        def unosUBazu():

            if katVar.get()=="" or opisKat.get()=="" or sumaNovca.get()=="":
                messagebox.showinfo("Greska", "Morate popuniti sva polja!")
                return
            else:
                try:
                    
                    a= float(sumaNovca.get())
                    db = pymysql.connect("localhost", "root", "", "MoneyTracker")
                    cursor = db.cursor()
                    command = "INSERT INTO rashodi(kategorije, opis, iznos) VALUES('{}','{}','{}')".format(katVar.get(), opisKat.get(), sumaNovca.get())
                    try:
                        cursor.execute(command)
                        db.commit()
                    except:

                        db.rollback()
                    db.close()
                    opisKat.set('')
                    sumaNovca.set('')
                    katVar.set('')
                    iznosEntry.focus_set()
                    upload()
                except ValueError:
                    messagebox.showinfo("Greska", "Iznos mora biti broj!")
                    sumaNovca.set('')
                    iznosEntry.focus_set()
            


        sumaNovca = StringVar()
        katVar = StringVar()
        opisKat = StringVar()
        valVar = StringVar()
        
        clockFrame= ttk.Frame(self, style="tirkiz.TFrame")
        clockFrame.grid(column=0, row=0, sticky="ew")
        frame2 = ttk.Frame(self, style="tirkiz.TFrame")
        frame2.grid(column=0, row=1)




        clock = tk.Label(clockFrame, font=CLOCK_FONT)
        clock.grid(column=0, row=0)

        

        
        
        naslovP = ttk.Label(frame2, text='\t**Unos rashoda**\n', font=NAS_FONT, style="my.TLabel")
        naslovP.grid(column=0, row=0, columnspan=2, sticky='nsew')
        iznosLabel = ttk.Label(frame2, text='Iznos', font=LARGE_FONT, style="my.TLabel")
        iznosLabel.grid(column=0, row=1, sticky='e')
        opisLabel = ttk.Label(frame2, text='Opis', font=LARGE_FONT, style="my.TLabel")
        opisLabel.grid(column=0, row=3, sticky='e')
        kat = ttk.Label(frame2, text="Kategorija", font=LARGE_FONT, style="my.TLabel")
        kat.grid(row=2, column=0, sticky='e')
        
##        valutaLabel = ttk.Label(frame2, text='Valuta', font=LARGE_FONT, style="my.TLabel")
##        valutaLabel.grid(column=0, row=4, sticky='e')
##        valuta = ttk.Combobox(frame2, textvariable=valVar, width=40, style="moj.TCombobox")
##        valuta.grid(column=1, row=4)
##        valuta['values'] = ("Dinar(RSD)", "Euro(€)", "Konvertibilna marka(KM)", "Dolar($)")
##        valuta['state'] = 'readonly'
##        valuta.bind("<<ComboboxSelected>>", setVal)
        
        kategorija = ttk.Combobox(frame2, textvariable=katVar, width=40, style="moj.TCombobox")
        kategorija.grid(column=1, row=2)
        katRashod = ["Racuni", "Odjeca", "Auto", "Hrana", "Zdravlje", "Kozmetika", "Prevoz", "Pokloni", "Kuca"]
        kategorija['values'] = (katRashod)
        kategorija['state'] = 'readonly'
        iznosEntry = tk.Entry(frame2, textvariable=sumaNovca, width=40, font=ENTRY_FONT, foreground="#424D59", background="#FA8E4B")
        iznosEntry.grid(column=1, row=1, sticky='nsew')
        opis = tk.Entry(frame2, textvariable=opisKat, font=ENTRY_FONT, foreground="#424D59", background="#FA8E4B")
        opis.grid(column=1, row=3, sticky='nsew')
        unosBut = ttk.Button(self, text='Unesi', style='moj.TButton', command=unosUBazu)
        unosBut.grid(column=0, row=2)
        unosBut.place(x=280, y=175)
        nazadBut = ttk.Button(self, text='<<<', style='moj.TButton',
                              command=lambda: controller.show_frame(PageOne))
        nazadBut.grid(column=0, row=2)
        nazadBut.place(x=3, y=175)
        tick()        
            
        
                


        
class Novac:


    def balans(self):
        db = pymysql.connect("localhost", "root", "", "MoneyTracker")
        cursor1 = db.cursor()
        cursor2 = db.cursor()
        command1 = 'SELECT SUM(iznos) FROM prihodi;'
        command2 = 'SELECT SUM(iznos) FROM rashodi;'

        cursor1.execute(command1)
        prihod = cursor1.fetchone()[0]
        cursor2.execute(command2)
        rashod = cursor2.fetchone()[0]
        if prihod == None or rashod == None:
            if prihod == None and rashod != None:
                prihod = '0'
            elif prihod != None and rashod == None:
                rashod = '0'
            elif prihod == None and rashod == None:
                prihod = '0'
                rashod = '0'
            
        
        bal = float(prihod) - float(rashod)
        
        return bal
        

    def iznos(self):
        db = pymysql.connect("localhost", "root", "", "MoneyTracker")
        cursor1 = db.cursor()
        cursor2 = db.cursor()
        command1 = 'SELECT SUM(iznos) FROM prihodi;'
        command2 = 'SELECT SUM(iznos) FROM rashodi;'

        cursor1.execute(command1)
        prihod = cursor1.fetchone()[0]
        cursor2.execute(command2)
        rashod = cursor2.fetchone()[0]
        if prihod == None or rashod == None:
            if prihod == None and rashod != None:
                prihod = '0'
            elif prihod != None and rashod == None:
                rashod = '0'
            elif prihod == None and rashod == None:
                prihod = '0'
                rashod = '0'
            
        print(prihod)
        print(rashod)
        bal = float(prihod) - float(rashod)
        return bal


class PieChart:

    def __init__(self, cat):
        self.cat = cat

    def kategorija(self):
        db = pymysql.connect("localhost", "root", "", "MoneyTracker")
        cursor = db.cursor()
        command = 'SELECT kategorije FROM {};'.format(self.cat)
        cursor.execute(command)
        kat = cursor.fetchall()
        lista = [x for y in kat for x in y]
        def funkcija(kat):
            seen = set()
            seen_add = seen.add
            return [x for x in kat if not (x in seen or seen_add(x))]
        newLista = funkcija(lista)
        
        return newLista

    def iznosi(self):
        db = pymysql.connect("localhost", "root", "", "MoneyTracker")
        cursor = db.cursor()
        cursor1 = db.cursor()
        command = 'SELECT iznos FROM {};'.format(self.cat)
        command1 = 'SELECT kategorije FROM {};'.format(self.cat)
        cursor1.execute(command1)
        cursor.execute(command)
        kat = cursor1.fetchall()
        iznos = cursor.fetchall()
        listaIznos = [x for y in iznos for x in y]
        listaKat = [x for y in kat for x in y]
        def funkcija(kat):
            seen = set()
            seen_add = seen.add
            return [x for x in kat if not (x in seen or seen_add(x))]
        newKat = funkcija(listaKat)
        zbir = 0
        index = 0
        newIznos = []
        for item in newKat:
            for ittem in listaKat:
                if item == ittem:
                    zbir += int(listaIznos[index])
                index += 1
            newIznos.append(zbir)
            zbir = 0
            index = 0
        
        return newIznos
    
    def raspon(self, raspon, tabela):
        
        try:
            db = pymysql.connect("localhost", "root", "", "MoneyTracker")
            cursor = db.cursor()
            cursor1 = db.cursor()
            if raspon == 'day':
                command = 'SELECT iznos FROM {} WHERE date(datumVrijeme) = CURDATE();'.format(self.cat)
                command1 = 'SELECT kategorije FROM {} WHERE date(datumVrijeme) = CURDATE();'.format(self.cat)
            elif raspon == 'week':
                command = 'SELECT iznos FROM {} WHERE date(datumVrijeme) BETWEEN date_sub(now(), INTERVAL 1 WEEK) and now();'.format(self.cat)
                command1 = 'SELECT kategorije FROM {} WHERE date(datumVrijeme) BETWEEN date_sub(now(), INTERVAL 1 WEEK) and now();'.format(self.cat)
            elif raspon == 'month':
                command = 'SELECT iznos FROM {} WHERE date(datumVrijeme) BETWEEN date_sub(now(), INTERVAL 1 MONTH) and now();'.format(self.cat)
                command1 = 'SELECT kategorije FROM {} WHERE date(datumVrijeme) BETWEEN date_sub(now(), INTERVAL 1 MONTH) and now();'.format(self.cat)
            elif raspon == 'all':
                command = 'SELECT iznos FROM {}'.format(self.cat)
                command1 = 'SELECT kategorije FROM {}'.format(self.cat)
            cursor1.execute(command1)
            cursor.execute(command)
            kat = cursor1.fetchall()
            iznos = cursor.fetchall()
            listaIznos = [x for y in iznos for x in y]
            listaKat = [x for y in kat for x in y]
            def funkcija(kat):
                seen = set()
                seen_add = seen.add
                return [x for x in kat if not (x in seen or seen_add(x))]
            newKat = funkcija(listaKat)
            zbir = 0
            index = 0
            newIznos = []
            for item in newKat:
                for ittem in listaKat:
                    if item == ittem:
                        zbir += int(listaIznos[index])
                    index += 1
                newIznos.append(zbir)
                zbir = 0
                index = 0
            if tabela == 'iznos':
                return newIznos
            elif tabela == 'kat':
                return newKat
        except IndexError:
            if tabela == 'iznos':
                return [1]
            if tabela == 'kat':
                return ['BazaPrazna']








    

app = MainWindow()
ani = animation.FuncAnimation(fig1, animateR, interval=1000)
ani1 = animation.FuncAnimation(fig2, animateP, interval=1000)
app.mainloop()


