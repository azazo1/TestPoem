# coding=utf-8
import tkinter as tk
import tkinter.messagebox as tkmsg


class RB:
    """ReciteBase"""

    def __init__(self, poemMessage: list):
        self.window = tk.Tk()
        self.titleFrame = tk.Frame(self.window)
        self.widgetsFrame = tk.Frame(self.window)
        self.contentFrame = tk.Frame(self.widgetsFrame, bd=5, relief=tk.SUNKEN)
        self.padFrame = tk.Frame(self.contentFrame)
        self.controlFrame = tk.Frame(self.widgetsFrame)
        self.moveFrame = tk.Frame(self.padFrame)
        self.scale = tk.Scale(self.controlFrame)
        self.checkButton = tk.Scale(self.controlFrame)
        self.quitButton = tk.Scale(self.controlFrame)
        self.symbol = '，', '。', '？', '！', '……', '；'
        self.poemName = poemMessage[0]
        self.poemAuthor = poemMessage[1]
        self.poemDynasty = poemMessage[2]
        self.poemContent = poemMessage[3]
        self.temp = {}
        self.initWindow()
        self.showPoem()

    def initWidgets(self):
        tk.Label(self.titleFrame, text=f'《{self.poemName}》').pack()
        tk.Label(self.titleFrame, text=f'[作者] {self.poemAuthor}').pack()
        tk.Label(self.titleFrame, text=f'[朝代] {self.poemDynasty}').pack()
        tk.Scale(self.controlFrame, from_=0, to=100, showvalue=False, command=self.move).pack(expand=True, fill=tk.Y)

    def initFrame(self):
        self.titleFrame.pack(fill=tk.X)
        self.widgetsFrame.pack(expand=True, fill=tk.BOTH)
        self.contentFrame.pack(expand=True, fill=tk.BOTH, ipadx=self.contentFrame['bd'], ipady=self.contentFrame['bd'],
                               side=tk.LEFT)
        self.padFrame.pack(expand=True, fill=tk.BOTH)
        self.controlFrame.pack(expand=True, fill=tk.Y)
        self.moveFrame.place(x=0, y=0, relwidth=1.0)

    def initWindow(self):
        self.window.title('默写：' + self.poemName)  # 继承时记得改名字
        self.window.attributes('-fullscreen', True)
        # self.window.attributes('-topmost', True)
        self.window.geometry(f'{self.window.winfo_screenwidth()}x{self.window.winfo_screenheight()}')

    def move(self, num):
        """移动moveFrame"""
        self.moveFrame.place_configure(x=0, y=-int(num) / 100 * (
                self.moveFrame.winfo_height() - self.moveFrame.master.winfo_height()))

    def startDictation(self):
        self.initFrame()
        self.initWidgets()

    def showPoem(self, *args):
        showframe = self.temp['showframe'] = tk.Frame(self.window)
        showframe.pack()
        tk.Label(showframe, text='诗歌查看：' + self.poemName).pack()
        tk.Label(showframe, text='【作者】' + self.poemAuthor).pack()
        tk.Label(showframe, text='【朝代】' + self.poemDynasty).pack()
        t = tk.Text(showframe)
        t.insert(1.0, self.poemContent)
        t.pack(expand=True, fill=tk.BOTH)
        bframe = tk.Button(showframe, bd=0)
        tk.Button(bframe, text='开始默写',
                  command=lambda: [i.destroy() for i in self.temp.values()].append(  # append处只是用来执行多个语句
                      self.startDictation())) \
            .pack(side=tk.LEFT)

        tk.Button(bframe, text='取消默写', command=self.close).pack(side=tk.LEFT)
        bframe.pack()

    def mainloop(self):
        self.window.mainloop()

    def close(self):
        self.window.destroy()
if __name__ == '__main__':
    RB(['','','','']).mainloop()
