from turtle import *
from math import *
from time import *

from tkinter import *



class Func:
    def per(n):
        z = n
        steps = 0
        results = []
        while 1:
            digits = []
            if n < 10:
                results.append(0)
                break
            else:
                for c in range(len(str(n))):
                    digits.append(int(str(n)[c:c + 1]))
                p = 1
                for j in digits:
                    p *= j
                results.append(p)
                steps += 1
                n = p
        results.remove(0)
        print(z, '->', steps, results)

    class Fibonacci:
        def __init__(self, length):
            self.t = Turtle()
            self.t.up()
            self.t.left(180)
            self.t.forward(length)
            self.t.left(90)
            self.t.forward(length / 2)
            self.t.left(90)
            self.t.down()
            global phi
            phi = float((1 + sqrt(5)) / 2)

        def draw_square(self, size, speed, n):
            self.t.speed(speed)
            for i in range(n):
                self.t.forward(size)
                self.t.left(90)

        def g_rect(self, size, stop=30):
            self.draw_square(size, 100, 4)
            self.t.forward(size)
            size /= phi
            for i in range(stop):
                self.draw_square(size, 100, 4)
                self.t.forward(size)
                self.t.left(90)
                self.t.forward(size)
                size /= phi

    def BsCv(b, n):
        print()
        z = n
        string = []
        stri = []
        exp = []
        if n == 0:
            string.append(0)
        a = 1 / int(b)
        while int(a) < int(n):
            a *= int(b)
            if a > n:
                a /= int(b)
                break
            exp.append(a)
        for i in exp:
            string.append(int(n % int(b)))
            n -= (n % int(b))
            n /= int(b)
        string.reverse()
        out = ""
        for i in string:
            out = out + str(i)
        return (z, "into Base", b, "->", out)

    def SquarePat(a2, b2, c2, d2):
        t = 0
        print(a2, b2, c2, d2)
        sleep(1)
        a1 = 0
        b1 = 0
        c1 = 0
        d1 = 0
        while not (int(a1) == int(b1) and int(b1) == int(c1) and int(c1) == int(d1) and int(d1) == int(a1)) or not (
                int(a2) == int(b2) and int(b2) == int(c2) and int(c2) == int(d2) and int(d2) == int(a2)):
            if not (int(a1) == int(b1) and int(b1) == int(c1) and int(c1) == int(d1) and int(d1) == int(a1)) or not (
                    int(a2) == int(b2) and int(b2) == int(c2) and int(c2) == int(d2) and int(d2) == int(a2)):
                a1 = abs(int(a2) - int(b2))
                b1 = abs(int(b2) - int(c2))
                c1 = abs(int(c2) - int(d2))
                d1 = abs(int(d2) - int(a2))
                if not (int(a1 + b1 + c1 + d1) == 0):
                    print(a1, b1, c1, d1)
                sleep(1)
                t += 1
            if not (int(a1) == int(b1) and int(b1) == int(c1) and int(c1) == int(d1) and int(d1) == int(a1)) or not (
                    int(a2) == int(b2) and int(b2) == int(c2) and int(c2) == int(d2) and int(d2) == int(a2)):
                a2 = abs(int(a1) - int(b1))
                b2 = abs(int(b1) - int(c1))
                c2 = abs(int(c1) - int(d1))
                d2 = abs(int(d1) - int(a1))
                if not (int(a2 + b2 + c2 + d2) == 0):
                    print(a2, b2, c2, d2)
                sleep(1)
                t += 1
        print("Steps: " + str(t))

    class DtctBool:
        def isodd(n):
            if n % 2:
                return (True)
            elif not (n % 2):
                return (False)

        def iseven(n):
            if n % 2:
                return (False)
            elif not (n % 2):
                return (True)

        def isprime(n):
            pass

        def is_fib(n):
            a = [0, 1]
            while a[-1] < n:
                a.append(int(a[-2] + a[-1]))

            if a[-1] == n:
                return (True)
            else:
                return (False)
    class TimeEvent:
        def __init__(self, title, time_1, description, func=None):
            self.start_time = time_1
            self.title = title
            self.event_description = description
            self.func = func

        def detect_event(self):

            while not (self.start_time <= time.time()):
                time.sleep(1)

            print("\n")
            print("At", time.time(), self.title, "was executed.")
            exec(self.func)

        def get_attr(self):
            return [self.title, self.event_description, self.start_time]


    class Calendar:
        def __init__(self, Name):
            self.Name = Name
            self.events = []

        def create_event(self, title, time_1, description, func):
            self.created_evt = TimeEvent(title, time_1, description, func)
            self.events.append(self.created_evt)

        def run_events(self):
            for i in self.events:
                i.detect_event()
                print(self.Name, "->", i.title)

    class Clock:
          def __init__(self,name):
            self.name=name
            self.tk=Tk()
            self.tk.title(str(self.name))
            self.tk.resizable(0, 0)
            self.tk.wm_attributes("-topmost", 1)
            self.canvas = Canvas(self.tk, width=250, height=250, highlightthickness=0)
            self.canvas.pack()
            self.tk.update()
            self.timetext = self.canvas.create_text(100,100, text="",state='normal')
          def kill(self):
              self.destroy()
          def run_time(self):
            while 1:
              a=list(localtime())
              c="/"
              c1=":"
              f=int(a[3])
              if f>12:
                  f-=12
              if f<12:   
                  f=str(f)
                  g=int(a[5])
                  g=str(g)
                  day=int(a[2])
                  b=str(a[1])+c+str(day)+c+str(a[0])
                  d=f+c1+str(a[4])+c1+g
                  sleep(1)
                  self.tk.update()
                  self.canvas.itemconfig(self.timetext,text=str(self.name+"\n"+b+"\n"+d))

    class MakeTrans:
      def __init__(self,precode,postcode):
        self.first=precode
        self.two=postcode
        self.a=[]
        self.b=[]
        self.first=self.first.lower()
        self.two=self.two.lower()
        if len(precode)==len(postcode):
          for i in range(len(self.first)):
            self.a.append(self.first[i:i+1])
            self.b.append(self.two[i:i+1])
        else:
          ValueError("MakeTrans Args must have the length.")

      def change(self,string):
            string=string.lower()
            out=[]
            for i in range(len(string)):
              out.append(string[i:i+1])
            out2=[]
            for i in range(len(out)):
              for r in range(len(self.a)):
                  if out[i]==self.a[r]:
                      out2.append(self.b[r])
              if out[i]==" ":
                      out2.append(" ")    
            out1=""
            for i in out2:
                out1=out1+str(i)
            print(out1)





