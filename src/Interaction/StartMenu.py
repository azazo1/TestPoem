# coding=utf-8
import tkinter as tk
import tkinter.messagebox as tkmsg
import src
from src.NetGetPoem.GetPoem import getPoemMessageByName, getPoemMessageByUrl
from src.Interaction.ReciteAll import RA
from src.Interaction.RecitePart import RP
from src.Interaction.ReciteBase import RB


def changeParser():
    src.IF_BS4_PARSER[0] = not src.IF_BS4_PARSER[0]
    tkmsg.showinfo('更改', 'HTML解析器状态:' + ('开启' if src.IF_BS4_PARSER[0] else '关闭'))


class StartMenu:
    button_size = (8, 2)
    window_size = (400, 230)

    def __init__(self, put=''):
        """
        :param put: 提前放置在entry的字符
        """
        self.window = tk.Tk()
        self.frame_poemName = tk.Frame(self.window)
        self.frame_buttons = tk.Frame(self.window)
        self.entry = tk.Entry()  # 临时控件
        self.corrector = Corrector(self, None, self.frame_poemName)
        self.initWindow()
        self.initFrames()
        self.window.update()
        self.initWidgets(put)

    def recite(self, isReciteAll: bool):
        isRight, poemM = self.corrector.checkPoem()
        R = RA if isReciteAll else RP
        if isRight:  # 启动背诵
            r = R(poemM)
            self.close()
            r.mainloop()
            self.__init__()  # 重新启动StartMenu
            self.mainloop()

    def initFrames(self):
        self.frame_poemName.pack(expand=True, fill=tk.BOTH)
        self.frame_buttons.pack(expand=True, fill=tk.BOTH)

    def initWidgets(self, put=''):
        # 安放输入框与提示
        fpoem = tk.Frame(self.frame_poemName)
        fentry = tk.Frame(fpoem)
        tk.Label(fpoem, text='输入诗名:').pack(side=tk.LEFT)
        self.entry = tk.Entry(fentry, width=20)
        self.entry.insert(0, put)
        self.corrector.entry = self.entry
        self.corrector.frame = fentry
        self.entry.pack(fill=tk.X, expand=True)
        fentry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        fpoem.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=int(self.window.winfo_width() / 10))
        # 安放按钮
        tk.Button(fpoem, text='退出', command=self.close).pack(side=tk.LEFT)
        fb1 = tk.Frame(self.frame_buttons)  # 按钮容器1
        fb2 = tk.Frame(self.frame_buttons)  # 按钮容器2
        tk.Button(fb1, height=self.button_size[1], width=self.button_size[0], text='全背',
                  command=lambda: self.recite(True)).pack(expand=True)
        tk.Button(fb2, height=self.button_size[1], width=self.button_size[0], text='抽查',
                  command=lambda: self.recite(False)).pack(expand=True)
        fb1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        fb2.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # 安放设置菜单
        # HTML解析器开关
        parserMenu = tk.Menu(self.window)
        parserMenu.add_command(label='HTML解析器开关', command=changeParser)
        self.window.configure(menu=parserMenu)

    def initWindow(self):
        self.window.geometry('x'.join([str(i) for i in self.window_size]))
        self.window.title(src.Application_name + '--' + src.Author)

    def mainloop(self):
        self.window.mainloop()

    def close(self):
        self.window.destroy()


class Corrector:
    def __init__(self, father: StartMenu, entry: tk.Entry, frame: tk.Frame):
        self.entry = entry
        self.frame = frame
        self.out = print
        self.tempFrames = []
        self.chosen = tk.StringVar()
        self.poemUrls = {}  # 提供对应诗歌的url
        self.parent = father

    def correctEntry(self, poemName: str):
        """修改Entry内容"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, poemName)

    def forgetCorrector(self):
        """关闭上一个建议栏"""
        for frame in self.tempFrames:
            frame: tk.Frame
            frame.pack_forget()
            self.tempFrames.remove(frame)

    def showCorrector(self, poemNamesUrls: list):
        """提供一个修正诗名的建议栏"""

        def move(position):
            moveFrame.place_configure(
                y=-int(position) / 100 * (moveFrame.winfo_height() - moveFrame.master.winfo_height()),
                x=0
            )

        self.chosen.set('|||')
        packFrame = tk.LabelFrame(self.frame, text='选择一个正确的诗名', height=self.parent.window.winfo_height() // 3)
        chooseFrame = tk.Frame(packFrame, bd=5, relief=tk.SUNKEN)
        padFrame = tk.Frame(chooseFrame)
        moveFrame = tk.Frame(padFrame)
        self.tempFrames.append(packFrame)
        for name, url in poemNamesUrls:
            rb = tk.Radiobutton(moveFrame, text=name, variable=self.chosen, value=f'{name}|||{url}',
                                command=self.choose)
            rb.pack()
        scale = tk.Scale(packFrame, from_=0, to=100, showvalue=False, command=move)
        moveFrame.place(x=0, y=0)
        padFrame.pack(expand=True, fill=tk.BOTH)
        chooseFrame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, ipadx=chooseFrame['bd'], ipady=chooseFrame['bd'])
        scale.pack(fill=tk.Y, side=tk.LEFT)
        packFrame.pack(expand=True, fill=tk.X)

    def choose(self):
        name, url = self.chosen.get().split('|||')
        self.poemUrls.setdefault(name, url)
        self.correctEntry(name)
        self.forgetCorrector()

    def checkPoem(self) -> [bool, list]:
        """
        检查诗歌名称是否正确，并提出建议;
        :return 诗歌信息
        """
        url = self.poemUrls.setdefault(self.entry.get(), '')  # 自动提取url
        self.chosen.set('')  # 清除原来的选项
        if not self.entry.get():
            return False, None  # 不能为空

        respon = getPoemMessageByName(self.entry.get()) if 'http' not in url else getPoemMessageByUrl(url)
        if respon[0] == 1:
            return True, respon[1]
        elif respon[0] == 2:
            self.showCorrector(respon[1])
        elif respon[0] == 3:
            tkmsg.showerror('名称错误', '没有诗的名称叫"' + self.entry.get() + '"' +
                            '\n详细异常：\n' + respon[1])
        return False, None


if __name__ == '__main__':
    a = StartMenu('行路难其一')
    a.mainloop()
