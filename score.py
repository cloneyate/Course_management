import tkinter as tk
from tkinter import ttk
import api


def turn_to_score(courseID):
    courseID_selected=-1
    itemID_selected=""
    score_window=tk.Toplevel()
    grades=api.get_students_grades(courseID=courseID)
    columns=["学生ID","姓名","成绩"]
    table=ttk.Treeview(score_window,show="headings", columns=columns)
    for col in columns:
        table.column(col,width=150)
        table.heading(col,text=col)
    table.pack(side="left",fill="both")
    for i,grade in enumerate(grades):
        item=table.insert("",i,values=grade[2:],open=True)

    frame=tk.Frame(score_window,width=150)
    Vars=[tk.IntVar(),tk.StringVar(),tk.IntVar()]
    tk.Label(frame,text=F"当前课程:{grades[0][1]}").grid(row=0,columnspan=2)
    tk.Label(frame,text="请选择学生").grid(row=1,columnspan=2)
    for i,var in enumerate(Vars):
        if i<2:
            tk.Label(frame,text=columns[i]).grid(row=i+2,column=0)
            tk.Label(frame,textvariable=var).grid(row=i+2,column=1)
        else:
            tk.Label(frame,text=columns[i]).grid(row=i+2,column=0)
            grade_entry=tk.Entry(frame,textvariable=var)
            grade_entry.grid(row=i+2,column=1)
    def update():
        api.update_score(Vars[0].get(),courseID,grade_entry.get())
        table.set(itemID_selected,column="成绩",value=grade_entry.get())

    tk.Button(frame,text="评分",command=update).grid(row=len(Vars)+2,column=1)

    def treeviewClick(event):
        for item in table.selection():
            nonlocal itemID_selected
            itemID_selected=item
            values_selected=table.item(itemID_selected,"values")
            for i,var in enumerate(Vars):
                var.set(values_selected[i])
            nonlocal courseID_selected
            courseID_selected=table.item(item,"values")[0]
            print(courseID_selected)
    table.bind('<ButtonRelease-1>', treeviewClick)



    frame.pack(side="right",fill="both")
