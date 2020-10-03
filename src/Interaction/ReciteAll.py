# coding=utf-8

from src.Interaction.ReciteBase import *


class RA(RB):
    """ReciteAll"""

    # TODO 全默模块
    def __init__(self, poemMessage: list):
        super().__init__(poemMessage)

    def startDictation(self):
        self.initFrame()
        self.initWidgets()

    def initWidgets(self):
        super(RA, self).initWidgets()
        for i in range(50):
            e = tk.Entry(self.moveFrame)
            e.insert(0, str(i))
            e.pack(expand=True, fill=tk.X)
