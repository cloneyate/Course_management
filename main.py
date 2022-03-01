import tkinter as tk
import tkinter.messagebox
import api
from tkinter import ttk
from score import turn_to_score
import sys



def main_window(user):
    user=api.login(user[0],user[1])
    if type(user)!=tuple:
        print("密码错误")
        return 0
    user=list(user)
    def refresh_frame(frame):
        for child in list(frame.children.values()):
            child.destroy()

    def change_profile():
        refresh_frame(frame2)
        temp_frame=tk.Frame(frame2)
        temp_frame.pack()
        frame_list=[tk.Frame(temp_frame) for i in range(6)]
        for i,f in enumerate(frame_list):
            f.grid(row=i,sticky="w",pady=2)
        userID_label=tk.Label(frame_list[0],text="账号").grid(row=0,column=0)
        userID_label2=tk.Label(frame_list[0],text=user[0]).grid(row=0,column=1,columnspan=2,sticky=tk.W)

        name_label=tk.Label(frame_list[2],text="姓名").grid(row=2,column=0)
        name_entry=tk.Entry(frame_list[2])
        name_entry.insert(0,user[2])
        name_entry.grid(row=2,column=1,columnspan=2)

        age_label=tk.Label(frame_list[3],text="年龄").grid(row=3,column=0)
        age_entry=tk.Entry(frame_list[3])
        age_entry.insert(0,user[3])
        age_entry.grid(row=3,column=1,columnspan=2)

        dep_label=tk.Label(frame_list[4],text="学院").grid(row=4,column=0)
        dep_entry=tk.Entry(frame_list[4])
        dep_entry.insert(0,user[5])
        dep_entry.grid(row=4,column=1,columnspan=2)

        sexVar=tk.StringVar()
        sexVar.set("男")
        sex_label=tk.Label(frame_list[5],text="性别").grid(row=5,column=0)
        tk.Radiobutton(frame_list[5],variable=sexVar,text="男",value="男").grid(row=5,column=1)
        tk.Radiobutton(frame_list[5],variable=sexVar,text="女",value="女").grid(row=5,column=2)

        def update():
            name=name_entry.get()
            age=age_entry.get()
            sex=sexVar.get()
            dep=dep_entry.get()
            user[2:6]=[name,age,sex,dep]
            result=api.update_user(user[0],name,age,sex,dep)
            tkinter.messagebox.showinfo(message=result)

        def turn_to_change_password():
            cp_window=tk.Toplevel()
            cp_window.title("更改密码")
            old_password_label=tk.Label(cp_window,text="旧密码").grid(row=0,column=0)
            old_password_entry=tk.Entry(cp_window,show="*")
            old_password_entry.grid(row=0,column=1)

            new_password_label=tk.Label(cp_window,text="新密码").grid(row=1,column=0)
            new_password_entry=tk.Entry(cp_window,show="*")
            new_password_entry.grid(row=1,column=1)

            def change_password():
                old_password=old_password_entry.get()
                new_password=new_password_entry.get()
                result=api.change_password(user[0],old_password,new_password)
                tkinter.messagebox.showinfo(message=result)

            cp_button=tk.Button(cp_window,text="确认",command=change_password).grid(row=2,column=1,stick=tk.E)




        button=tk.Button(temp_frame,text="保存",command=update).grid(row=6,columnspan=3,stick=tk.W)
        password_label=tk.Label(frame_list[1],text="密码").grid(row=1,column=0)
        password_button=tk.Button(frame_list[1],text="更改",command=turn_to_change_password).grid(row=1,column=1,columnspan=2,stick=tk.W)



    def choose_course():
        refresh_frame(frame2)
        courses=api.get_courses()
        courses=[course for course in courses if api.course_is_chose(course[0],user[0])==False]

        for i in range(len(courses)):
            courses[i]=list(courses[i])
        columns=["课程ID","课程名","简介","课程开始日期","课程结束日期","授课教师"]
        courses_table=ttk.Treeview(frame2,show="headings", columns=columns)
        for col in columns:
            courses_table.column(col,width=800//len(columns))
            courses_table.heading(col,text=col)

        for i,course in enumerate(courses):
            teachers=api.get_teacher(course[0])
            course.append(",".join([i[1] for i in teachers]))
            courses_table.insert("",i,values=course)
        courses_table.pack(side="left",fill="both")

        courseID_chose=-1
        itemID_selected=""

        def run():
            result=api.choose_course(courseID_chose,user[0])
            courses_table.delete(itemID_selected)
            choose_course_button.place_forget()
            tkinter.messagebox.showinfo(message="选课成功") if result else tkinter.messagebox.showinfo(message="选课失败")

        choose_course_button=tkinter.Button(frame2,text="选课",command=run)

        def treeviewClick(event):
            for item in courses_table.selection():
                nonlocal itemID_selected
                itemID_selected=item
                X,Y,width,height=courses_table.bbox(item)
                choose_course_button.place(x=750,y=Y+height//2,anchor="center")
                nonlocal courseID_chose
                courseID_chose=courses_table.item(item,"values")[0]

        courses_table.bind('<ButtonRelease-1>', treeviewClick)

    def create_course():
        refresh_frame(frame2)
        temp_frame=tk.Frame(frame2)
        temp_frame.pack()
        frame_list=[tk.Frame(temp_frame) for i in range(5)]
        label_texts=["课程序号","课程名称","课程简介","开始时间","结束时间"]
        label_list=[tk.Label(parent,text=text).pack(side="left",anchor="n") for text,parent in zip(label_texts,frame_list)]
        entry_list=[tk.Entry(parent) if frame_list.index(parent)!=2 else tk.Text(parent) for parent in frame_list ]
        [entry.pack(side="right",anchor="n")for entry in entry_list]
        #entry_list=[tk.Entry(frame3),tk.Entry(frame3),tk.Text(frame3),tk.Entry(frame3),tk.Entry(frame3)]
        for i,f in enumerate(frame_list):
            f.grid(row=i,sticky="w",pady=2)

        def create():
            courseID,courseName,description,startDate,endDate=[entry.get()  if type(entry)!=tk.Text else entry.get('1.0',tk.END)for entry in entry_list]
            result=api.create_course(courseID,courseName,description,startDate,endDate,user[0])
            tkinter.messagebox.showinfo(message="创建成功") if result==True else tkinter.messagebox.showinfo(message="创建失败"+str(result))

        tk.Button(temp_frame,text="创建",command=create).grid(row=len(frame_list),pady=2,sticky="w")


    def view_courses():
        refresh_frame(frame2)
        courses=api.get_grades(user[0])
        for i in range(len(courses)):
            courses[i]=list(courses[i])
        if userType==1:
            columns=["课程ID","课程名","课程开始日期","课程结束日期","授课教师"]
            for i in range(len(courses)):
                courses[i].pop(4)
        elif userType==2:
            columns=["课程ID","课程名","课程开始日期","课程结束日期","成绩","授课教师"]
            for i in range(len(courses)):
                courses[i][4]="未评分" if courses[i][4]==-1 else courses[i][4]
        courses_table=ttk.Treeview(frame2,show="headings", columns=columns)
        for col in columns:
            courses_table.column(col,width=800//len(columns))
            courses_table.heading(col,text=col)
        courses_table.pack(side="left",fill="both")
        for i,course in enumerate(courses):
            teachers=api.get_teacher(course[0])
            course.append(",".join([i[1] for i in teachers]))
            item=courses_table.insert("",i,values=course,open=True)


        courseID_selected=-1
        itemID_selected=""
        def drop_course():
            result=api.drop_course(courseID_selected,user[0])
            courses_table.delete(itemID_selected)
            button.place_forget()
            tkinter.messagebox.showinfo(message="退课成功") if result else tkinter.messagebox.showinfo(message="退课失败")



        if userType==1:
            button=tkinter.Button(frame2,text="评分",command=lambda :turn_to_score(courseID_selected))
        elif userType==2:
            button=tkinter.Button(frame2,text="退课",command=drop_course)


        def treeviewClick(event):
            for item in courses_table.selection():
                nonlocal itemID_selected
                itemID_selected=item

                X,Y,width,height=courses_table.bbox(item)
                button.place(x=750,y=Y+height//2,anchor="center")
                nonlocal courseID_selected
                courseID_selected=courses_table.item(item,"values")[0]

        courses_table.bind('<ButtonRelease-1>', treeviewClick)



    permissionDic={
               1:[["编辑个人资料",change_profile],
               ["创建课程",create_course],
               ["查看任课课程",view_courses]],
               2:[["编辑个人资料",change_profile],
                  ["选课",choose_course],
                   ["查看我的课程",view_courses]]}

    userType=user[-1]
    #print(user)
    main=tk.Tk()
    main.title("教学管理系统")
    main.geometry("800x600")
    frame1=tk.LabelFrame(main,width=800,height=100,borderwidth=3,bg="white")
    frame1.pack_propagate(0)
    frame1.pack(side="top",fill="both")
    frame2=tk.LabelFrame(main,width=800,height=500,borderwidth=3)
    frame2.pack_propagate(0)
    frame2.pack(side="left",fill="both")
    frame2.grid_propagate(False)

    if userType==1:
        welcome_text=F"欢迎您,{user[2]}老师"
    else:
        welcome_text=F"欢迎您,{user[2]}同学"
    welcome_label=tk.Label(frame1,text=welcome_text,font=20,bg="white")
    welcome_label.pack(side="top")
    #conn=init_or_connect_DB()
    frame4=tk.Frame(frame1,bg="white")
    frame4.pack(side="bottom",pady=12)
    for ac in permissionDic[userType]:
        tk.Button(frame4,text=ac[0],command=ac[1]).pack(padx=3,pady=3,side="left",fill="x")

    main.mainloop()



if __name__=="__main__":
    main_window([sys.argv[1],sys.argv[2]])
