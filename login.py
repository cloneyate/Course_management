import tkinter as tk
import tkinter.messagebox
import api
from main import main_window


def turn_to_register():
    register_window=tk.Toplevel()
    register_window.title("注册")

    userID_label=tk.Label(register_window,text="账号").grid(row=0,column=0)
    userID_entry=tk.Entry(register_window)
    userID_entry.grid(row=0,column=1)

    password_label=tk.Label(register_window,text="密码").grid(row=1,column=0)
    password_entry=tk.Entry(register_window,show="*")
    password_entry.grid(row=1,column=1)

    name_label=tk.Label(register_window,text="姓名").grid(row=2,column=0)
    name_entry=tk.Entry(register_window)
    name_entry.grid(row=2,column=1)

    age_label=tk.Label(register_window,text="年龄").grid(row=3,column=0)
    age_entry=tk.Entry(register_window)
    age_entry.grid(row=3,column=1)


    dep_label=tk.Label(register_window,text="学院").grid(row=4,column=0)
    dep_entry=tk.Entry(register_window)
    dep_entry.grid(row=4,column=1)

    sexVar=tk.StringVar()
    sexVar.set("男")

    sex_label=tk.Label(register_window,text="性别").grid(row=5,column=0)
    tk.Radiobutton(register_window,variable=sexVar,text="男",value="男").grid(row=5,column=1,sticky=tk.W)
    tk.Radiobutton(register_window,variable=sexVar,text="女",value="女").grid(row=5,column=1,sticky=tk.E)

    typeVar=tk.IntVar()
    typeVar.set(2)
    type_label=tk.Label(register_window,text="身份").grid(row=6,column=0)
    tk.Radiobutton(register_window,variable=typeVar,text="学生",value=2).grid(row=6,column=1,sticky=tk.W)
    tk.Radiobutton(register_window,variable=typeVar,text="教师",value=1).grid(row=6,column=1,sticky=tk.E)

    def register():
        userID=userID_entry.get()
        password=password_entry.get()
        name=name_entry.get()
        age=age_entry.get()
        sex=sexVar.get()
        dep=dep_entry.get()
        userType=typeVar.get()
        result=api.register(userID,password,name,age,sex,dep,userType)
        tkinter.messagebox.showinfo(message=result)
        register_window.destroy()

    register_button=tk.Button(register_window,text="注册",command=register).grid(row=7,columnspan=2)
    register_window.mainloop()






def login():
    ID=ID_entry.get()
    password=password_entry.get()
    if ID and password:
        result=api.login(ID,password)
        if type(result)==tuple:
            window.destroy()
            main_window([ID,password])
        else:
            tkinter.messagebox.showinfo(message=result)
    else:
        tkinter.messagebox.showinfo(message="请完全填写")

window=tk.Tk()
window.title("课程管理系统登录")
#window.geometry("800x600")
logo=tk.PhotoImage(file="logo.png")
window.iconphoto(True,logo)
ID_label=tk.Label(window,text="账号")
password_label=tk.Label(window,text="密码")
ID_entry=tk.Entry(window)
password_entry=tk.Entry(window,show="*")
register_button=tk.Button(window,text="注册",command=turn_to_register)
login_button=tk.Button(window,text="登入",command=login)

ID_label.grid(row=0,column=1)
password_label.grid(row=1,column=1)
ID_entry.grid(row=0,column=2)
password_entry.grid(row=1,column=2)
register_button.grid(row=0,column=3,padx=8)
login_button.grid(row=1,column=3,padx=8)

logo_label=tk.Label(window, image=logo)
logo_label.grid(row=0,column=0,rowspan=2)
window.mainloop()
