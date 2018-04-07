# coding:utf-8

import Tkinter as tk
from ScrolledText import ScrolledText
import threading
import hashlib
from random import randint

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def __del__(self):
        pass

    def createWidgets(self):
        self.contentDest = tk.StringVar()
        self.contentDest.set(u'随意写个用户名')
        self.entryDest = tk.Entry(self, width=60)
        self.entryDest["textvariable"] = self.contentDest
        self.entryDest.grid(row=0)
        self.entryDest.focus()
        self.entryDest.bind('<Return>', lambda event: self.start())

        self.buttonStart = tk.Button(self, text='生成序列号', width=25)
        self.buttonStart['command'] = self.start
        self.buttonStart['fg'] = 'black'
        self.buttonStart.grid(row=1)

        self.text = ScrolledText(self, font=('Courier New', 13), fg='green', bg='black', width=50)
        self.text.grid(row=2, columnspan=1)

    def start(self):
        self.running = True
        self.td = threading.Thread(target=self.gen_key)
        self.td.setDaemon(True)
        self.td.start()

    def get_md5(self, src_txt):
        m = hashlib.md5()
        try:
            src_txt = src_txt.encode("utf-8")
        except:
            pass
        m.update(src_txt)   
        return m.hexdigest()

    def gen_key(self):
        try:
            self.text.delete(0.0, "end")
            name = self.contentDest.get()

            self.text.insert("end", u"注册名:【%s】\n" % name)
            salt = str(randint(10000,30000))
            self.text.insert("end", u"盐 值:【%s】\n" % salt)
            salted_text = u"ax5{}b52w{}vb3".format(name,salt)
            self.text.insert("end", u"盐混淆:【%s】\n" % salted_text)
            hashed_text = self.get_md5(salted_text)
            self.text.insert("end", u"哈希值:【%s】\n" % hashed_text)
            result_key = u"{}{}{}".format(hashed_text[:4],salt,hashed_text[4:])
            self.text.insert("end", u"序列号:【%s】\n" % result_key)
            self.text.insert("end", (u"^-^成功生成^-^\n"
                                    u"请复制注册名和序列号进行软件激活:"
                                    u"菜单栏->HELP->Register->输入激活"))
        except Exception as e:
            self.text.insert("end", u'生成失败，请填写英文名重新生成')
            

root = tk.Tk()
root.withdraw()
app = Application(master=root)
root.title("DbSchema序列号生成器")
try:
    root.iconbitmap("logo.ico")
except:
    pass
screen_width = root.winfo_screenwidth()
root.resizable(False, False)
root.update_idletasks()
root.deiconify()
screen_height = root.winfo_screenheight() - 100
root.geometry('%sx%s+%s+%s' % (
    root.winfo_width() + 10, root.winfo_height() + 10, (screen_width - root.winfo_width()) / 2,
    (screen_height - root.winfo_height()) / 2))
root.deiconify()
app.mainloop()