import sys
import tkinter as tk
from tkinter import *
import datetime
from tkcalendar import Calendar, DateEntry
from tkinter.messagebox import showerror, showinfo
from tkinter import messagebox as mb
import sqlite3 as sql
import re
import os
from PIL import ImageTk, Image
from functools import partial

def admin(frame):     #admin frame----------asiggns trips to driver and confirms for customer
    frame.master.destroy()
    def get_customer_list():
        conn = sql.connect("database/booking/booking.db")
        query = conn.execute("SELECT id,email,pickaddress,picktime,dropaddress,name,phone,active,driver FROM RESERVED")
        temp = []
        for row in query:
            if row[7] == 0:
                temp.append(row)
        conn.close()
        return temp

    def get_available_driver():
        conn = sql.connect("database/rides/rides.db")
        temp = []
        query = conn.execute("SELECT email,name,active FROM ACTIVE")
        for row in query:
            if row[2] == 0:
                temp.append(row[0])
        conn.close()
        return temp

    def refresh(frame):
        frame.destroy()
        frame = Frame(window, background="white")
        frame.pack(fill=BOTH, expand=YES)
        print(frame)
        body(frame)

    def register_driver(email, id, root):
        print(email.get(), id)
        verify = mb.askokcancel("Verify", "{} will be selected driver for this customer.".format(email.get()))
        if verify:
            conn = sql.connect("database/booking/booking.db")
            conn.execute("UPDATE RESERVED set active=1,driver='{}' where id='{}'".format(email.get(), id))
            conn.commit()
            conn.close()
            conn = sql.connect("database/rides/rides.db")
            conn.execute("UPDATE ACTIVE set active=1 where email='{}'".format(email.get()))
            conn.commit()
            conn.close()
            refresh(root)

    def card(canvas, datas, x, y, driver_var, root):   #designs full info of booking made by customer
        driver_var.trace('w', lambda name, index, mode, email=driver_var: register_driver(email, datas[0], root))
        canvas.create_rectangle(40 + x, 50 + y, 290 + x, 200 + y, fill="gainsboro", outline="gainsboro")

        email = Label(root, text="Email : " + datas[1], bg="gainsboro")
        canvas.create_window(80 + x, 60 + y, window=email, anchor=NW)
        pcka_lbl = Label(root, text="From : " + datas[2], bg="gainsboro")
        canvas.create_window(80 + x, 80 + y, window=pcka_lbl, anchor=NW)
        drpa_lbl = Label(root, text="To : " + datas[4], bg="gainsboro")
        canvas.create_window(80 + x, 100 + y, window=drpa_lbl, anchor=NW)
        time_lbl = Label(root, text="Date : " + datas[3], bg="gainsboro")
        canvas.create_window(150 + x, 100 + y, window=time_lbl, anchor=NW)
        phn_lbl = Label(root, text="Phone : " + datas[6], bg="gainsboro")
        canvas.create_window(80 + x, 120 + y, window=phn_lbl, anchor=NW)
        name_lbl = Label(root, text="Name : " + datas[5], bg="gainsboro")
        canvas.create_window(80 + x, 140 + y, window=name_lbl, anchor=NW)
        drivers = get_available_driver()
        option_lbl = OptionMenu(root, driver_var, *drivers)
        option_lbl.configure(width=20, border=0)
        canvas.create_window(80 + x, 165 + y, window=option_lbl, anchor=NW)
        return email

    def body(root):
        Label(root, text="ADMIN HOME", font=("Futura", 22, "bold"), fg="darkolivegreen").pack(ipady=(10))
        hscroll = Scrollbar(root, orient=VERTICAL)

        hscroll.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(root, bd=0, highlightthickness=0, yscrollcommand=hscroll.set, bg="white",
                        scrollregion=(0, 0, 500, 500))
        canvas.pack(fill=BOTH, expand=YES)

        customers = get_customer_list()
        x, y, count = 0, 0, 1

        for datas in customers:

            card(canvas, datas, x, y, StringVar(), root)
            x += 260
            if count % 2 == 0:
                x = 0
                y += 160

            count += 1

    window = tk.Tk()
    w = 600
    h = 600

    window.geometry(str(w) + 'x' + str(h))
    window.wm_resizable(False, False)
    frame = Frame(window)
    frame.pack(fill=BOTH, expand=YES)

    body(frame)

    window.mainloop()


###########################################################################


def show_frame(frame):

    if  (str(frame) == '.!frame8' ):
        frame.destroy()
        frame = Frame(root, background="white")
        frame.grid(row=0, column=0, sticky="nsew")
        print(frame)
        cust_home(frame)
    if (str(frame) == '.!frame9'):
        frame.destroy()
        frame = Frame(root, background="white")
        frame.grid(row=0, column=0, sticky="nsew")
        print(frame)
        dr_home(frame)

    if str(frame) == '.!frame' or str(frame) == '.!frame2' or str(frame) == '.!frame3' or str(
            frame) == '.!frame4' or str(frame) == '.!frame6':
        w = 600
        h = 440
    else:
        w = 600
        h = 600
    root.geometry("{}x{}".format(w, h))
    print(frame)

    frame.tkraise()



    pass


def create_rectangle(canvas,x1, y1, x2, y2, **kwargs):

    if 'alpha' in kwargs:
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = root.winfo_rgb(fill) + (alpha,)

    canvas.create_rectangle(x1, y1, x2, y2, **kwargs)


def img_src(param, param1):
    pass


def wel_dashboard(frame):   # Frame 1 opening page of the system

    canvas = Canvas(frame,width= 600, height= 600)
    canvas.pack()

    # Load an image in the script
    img = ImageTk.PhotoImage(Image.open("bgs.jpg"))

    # Add image to the Canvas Items
    canvas.create_image(10, 10, anchor=NW, image=img)

    riderbtn = tk.Button(frame, text="Driver", fg="deepskyblue2", background="lightpink1", border=0,
                          command=lambda: show_frame(dr_dash))
    riderbtn.configure(width=35, height=4)
    userbtn = tk.Button(frame, text="Customer", fg="darkslateblue", background="forestgreen", border=0,
                            command=lambda: show_frame(cust_dash))
    userbtn.configure(width=35, height=4)
    administratorbtn = tk.Button(frame, text="Admin", fg="darkorchid", background="chocolate2", border=0,
                            command=lambda: admin(frame))
    administratorbtn.configure(width=35, height=4)

    create_rectangle(canvas,150,110,450,360,fill="lightgoldenrod2",width=0,stipple="gray50")
    canvas.create_window(300, 175, window=riderbtn)
    canvas.create_window(300, 240, window=userbtn)
    canvas.create_window(300, 305, window=administratorbtn)



def title_img(frame):
    tsrc = img_src("images/title.png", (350, 37))
    title = tk.Label(frame, image=tsrc)
    title.image = tsrc
    title.pack()


def id_validation(email):  #----------Email validation-----------------
    regex = '^[A-Za-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if (re.search(regex, email)):
        return True
    else:
        return False


def pw_check(pw):           #---------------password validation----------------
    if len(pw) > 5:
        return True
    else:
        return False


def check_empty(data):
    print(data)
    for d in data:
        if len(d) <= 0:
            return False

    return True

def add_id_to_temp(id):
    file = open('temp/temp.txt','w')
    file.write(id)
    file.close()
def get_id_from_temp():
    file = open('temp/temp.txt','r')
    id=file.readline()
    file.close()
    return id

def login(page):  #--------------------Login for customer and driver-----------------------
    global temp_login
    raw_email = email_var.get()
    raw_pw = pw_var.get()
    e_chck = id_validation(raw_email)
    p_chck = pw_check(raw_pw)
    if not p_chck:
        showerror("Invalid", "Password length must be greater than 8.")
        return None
    if not e_chck:
        showerror("Invalid", "Email not valid!")
        return None
    if page == 1:
        print("customer")
        conn = sql.connect("database/cust/cust_lg.db")
    elif page == 2:
        print("driver")
        conn = sql.connect("database/dr/dr_lg.db")
    tbl_exist = table_check(conn, "LOGIN")

    if tbl_exist:
        cursor = conn.execute("SELECT email,password FROM LOGIN")
        for row in cursor:

            if raw_email == row[0] and raw_pw == row[1]:
                conn.close()
                print("Login successful")
                temp_login = raw_email
                add_id_to_temp(raw_email)
                if page==1:

                    show_frame(cust_desk_frame)
                elif page==2:
                    show_frame(dr_desk)

                return True

        conn.close()
        print("Error credentials")
        return False
    else:
        conn.close()
        showerror("Empty", "Empty database!!")


def filter_signup(email, data):
    conn = sql.connect("database/{}/{}".format(data, data + '_lg.db'))
    chck = table_check(conn, "LOGIN")
    cursor = conn.execute("SELECT email,password FROM LOGIN")
    for row in cursor:
        print(row[0])
        if row[0] == email:
            conn.close()
            return True
    conn.close()
    return False

def check_dublicate(email,table,data):
    conn = sql.connect("database/{}/{}".format(data, data+'.db' ))
    chck = table_check(conn, "{}".format(table))
    print(chck)
    if chck:
        cursor = conn.execute("SELECT email FROM {}".format(table))
        for row in cursor:
            print(row[0])
            if row[0] == email:
                conn.close()
                return True
        conn.close()
        return False
    else:
        return None


def table_check(conn, tablename):
    chck = conn.execute(
        "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{name}'".format(name=tablename))
    if chck.fetchone()[0] == 1:
        return True
    else:
        return False


def signup(page):           #-----------------signup for customer and driver------------
    raw_email = email_var.get()
    raw_pw = pw_var.get()
    raw_address = address_var.get()
    raw_phone = phone_var.get()
    raw_acn = acn_var.get()
    raw_cvv = cvv_var.get()
    e_chck = id_validation(raw_email)
    p_chck = pw_check(raw_pw)
    empty_chck = check_empty([raw_address, raw_phone, raw_acn, raw_cvv])
    print(empty_chck)
    if not empty_chck:
        showerror("Empty", "Incomplete form!")
        return None
    if page == 1:
        data = "cust"
    elif page == 2:
        data = "dr"
    if not p_chck:
        showerror("Invalid", "Password length must be greater than 8.")
        return None
    if not e_chck:
        showerror("Invalid", "Email not valid!")
        return None
    conn = sql.connect("database/{}/{}".format(data, data + "_lg.db"))
    newconn = sql.connect("database/rides/rides.db")


    if page == 2:
        chck_tbl = table_check(newconn, "ACTIVE")
        print(chck_tbl, "olo")
        if not chck_tbl:
            print("hello")
            newconn.execute("CREATE TABLE ACTIVE (email TEXT NOT NULL,name TEXT NOT NULL, active int NOT NULL )")

    tbl_exist = table_check(conn, "LOGIN")
    if not tbl_exist:
        if page == 1:
            conn.execute(
                "CREATE TABLE LOGIN (email TEXT NOT NULL, password TEXT NOT NULL,address TEXT NOT NULL,phone TEXT NOT NULL,acn TEXT NOT NULL,cvv TEXT NOT NULL)")
        elif page == 2:

            conn.execute(
                "CREATE TABLE LOGIN (email TEXT NOT NULL, password TEXT NOT NULL,address TEXT NOT NULL,phone TEXT NOT NULL,name TEXT NOT NULL,license TEXT NOT NULL)")
    if filter_signup(raw_email, data):
        print("found")
        showerror("Invalid", "Email already used!")
        return None
    if page == 1:
        rslt = conn.execute(
            "INSERT INTO LOGIN(email,password,address,phone,acn,cvv) VALUES ('{}','{}','{}','{}','{}','{}')".format(
                raw_email, raw_pw, raw_address, raw_phone, raw_acn, raw_cvv))
    elif page == 2:
        newconn.execute("INSERT INTO ACTIVE(email,name,active) VALUES ('{}','{}','{}')".format(raw_email, raw_acn, 0))
        rslt = conn.execute(
            "INSERT INTO LOGIN(email,password,address,phone,name,license) VALUES ('{}','{}','{}','{}','{}','{}')".format(
                raw_email, raw_pw, raw_address, raw_phone, raw_acn, raw_cvv))

    print(rslt)
    newconn.commit()
    newconn.close()
    conn.commit()
    conn.close()
    if page==1:

        show_frame(cust_dash)
    else:
        show_frame(dr_dash)


def cust_lg(frame):          #---------customer Login page-------------
    frame = Frame(frame, background="khaki4")
    frame.grid(row=10, column=0, sticky="nsew", padx=175, ipady=(20), pady=(40, 0))
    log_title = Label(frame, text="Welcome User", fg="#4D4D76", bg="khaki4", font=("Ubuntu", 15, "bold"))
    log_title.configure(width=21)
    log_title.pack(pady=(50, 0))
    email_label = Label(frame, text="Email Id:", bg="khaki4")
    email_label.pack(padx=(0, 190), pady=(20, 0))
    email = Entry(frame, font=("Futura", 14), textvariable=email_var)
    email.pack(ipady=(4))
    pw_label = Label(frame, text="Password:", bg="khaki4")
    pw_label.pack(padx=(0, 170), pady=(5, 0))
    pw = Entry(frame, font=("Futura", 14, "normal"), show="*", textvariable=pw_var)
    pw.pack(ipady=(4))
    submit = Button(frame, text="Login", bg="wheat2", border="0", command=lambda: login(1))
    submit.configure(width=31)
    submit.pack(pady=(20, 0), ipady=(10))
    home = Button(frame, text="Home", bg="maroon1", fg="black", border="0", command=lambda: show_frame(opening_frame))
    home.configure(width=31)
    home.pack(pady=(5, 0), ipady=(10))

def cust_regii(frame):          #--------customer signup page----------------
    frame = Frame(frame, background="rosybrown2")
    frame.grid(row=10, column=0, sticky="nsew", padx=130, ipady=(20), pady=(40, 0))
    log_title = Label(frame, text="Customer Registration", fg="#4D4D76", bg="rosybrown2", font=("Ubuntu", 15, "bold"))
    log_title.configure(width=21)
    log_title.pack(pady=(50, 0))
    email_label = Label(frame, text="Email Id:", bg="rosybrown2")
    email_label.pack(padx=(0, 190), pady=(20, 0))
    email = Entry(frame, font=("Futura", 14), textvariable=email_var)
    email.pack(ipady=(4))
    pw_label = Label(frame, text="Password:", bg="rosybrown2")
    pw_label.pack(padx=(0, 170), pady=(5, 0))
    pw = Entry(frame, font=("Futura", 14, "normal"), show="*", textvariable=pw_var)
    pw.pack(ipady=(4))

    address_label = Label(frame, text="Address:", bg="rosybrown2")
    address_label.pack(padx=(0, 175), pady=(5, 0))
    address = Entry(frame, font=("Futura", 14, "normal"), textvariable=address_var)
    address.pack(ipady=(4))
    phone_label = Label(frame, text="Phone No.:", bg="rosybrown2")
    phone_label.pack(padx=(0, 185), pady=(5, 0))
    phone = Entry(frame, font=("Futura", 14, "normal"), textvariable=phone_var)
    phone.pack(ipady=(4))

    credit_label_frame = tk.Frame(frame, background="rosybrown2")
    credit_label_frame.pack()
    credit_frame = tk.Frame(frame, background="rosybrown2")
    credit_frame.pack()

    credit_label = Label(credit_label_frame, text="Account No.:", bg="rosybrown2")
    credit_label.pack(padx=(0, 65), side=LEFT)
    credit_label = Entry(credit_frame, font=("Futura", 7, "normal"), textvariable=acn_var)
    credit_label.pack(ipady=(4), padx=(62, 0), side=LEFT)
    cvv_label = Label(credit_label_frame, text="CVV No.:", bg="rosybrown2")
    cvv_label.pack(padx=(10, 65), pady=(0, 0), side=LEFT)
    cvv_label = Entry(credit_frame, font=("Futura", 7, "normal"), textvariable=cvv_var)
    cvv_label.pack(ipady=(4), padx=(10, 62), side=LEFT)

    submit = Button(frame, text="Register", bg="seagreen2", border="0", command=lambda: signup(1))
    submit.configure(width=31)
    submit.pack(pady=(20, 0), ipady=(10))
    home = Button(frame, text="Home", bg="brown4", fg="white", border="0", command=lambda: show_frame(opening_frame))
    home.configure(width=31)
    home.pack(pady=(5, 0), ipady=(10))


def dr_lg(frame):      #-------------------Driver login page-----------------------
    frame = Frame(frame, background="cornsilk2")
    frame.grid(row=10, column=0, sticky="nsew", padx=175, ipady=(20), pady=(40, 0))
    log_title = Label(frame, text="Welcome Driver", fg="seagreen3", bg="cornsilk2", font=("Ubuntu", 15, "bold"))
    log_title.configure(width=21)
    log_title.pack(pady=(50, 0))
    email_label = Label(frame, text="Email Id:", bg="cornsilk2")
    email_label.pack(padx=(0, 190), pady=(20, 0))
    email = Entry(frame, font=("Futura", 14), textvariable=email_var)
    email.pack(ipady=(4))
    pw_label = Label(frame, text="Password:", bg="cornsilk2")
    pw_label.pack(padx=(0, 170), pady=(5, 0))
    pw = Entry(frame, font=("Futura", 14, "normal"), show="*", textvariable=pw_var)
    pw.pack(ipady=(4))
    submit = Button(frame, text="Login", bg="darkslategrey", border="0", command=lambda: login(2))
    submit.configure(width=31)
    submit.pack(pady=(20, 0), ipady=(10))
    home = Button(frame, text="Home", bg="dodgerblue", fg="white", border="0", command=lambda: show_frame(opening_frame))
    home.configure(width=31)
    home.pack(pady=(5, 0), ipady=(10))


def dr_regii(frame):                        #------------------driver signup page--------------------
    frame = Frame(frame, background="mistyrose")
    frame.grid(row=10, column=0, sticky="nsew", padx=130, ipady=(20), pady=(40, 0))
    log_title = Label(frame, text="New Driver Registration", fg="firebrick3", bg="mistyrose", font=("Ubuntu", 15, "bold"))
    log_title.configure(width=21)
    log_title.pack(pady=(50, 0))
    email_label = Label(frame, text="Email Id:", bg="mistyrose")
    email_label.pack(padx=(0, 180), pady=(20, 0))
    email = Entry(frame, font=("Futura", 10), textvariable=email_var)
    email.pack(ipady=(4))
    pw_label = Label(frame, text="Password:", bg="mistyrose")
    pw_label.pack(padx=(0, 170), pady=(5, 0))
    pw = Entry(frame, font=("Futura", 10, "normal"), show="*", textvariable=pw_var)
    pw.pack(ipady=(4))

    address_label = Label(frame, text="Address:", bg="mistyrose")
    address_label.pack(padx=(0, 175), pady=(5, 0))
    address = Entry(frame, font=("Futura", 10, "normal"), textvariable=address_var)
    address.pack(ipady=(4))
    phone_label = Label(frame, text="Phone No.:", bg="mistyrose")
    phone_label.pack(padx=(0, 165), pady=(5, 0))
    phone = Entry(frame, font=("Futura", 10, "normal"), textvariable=phone_var)
    phone.pack(ipady=(4))
    credit_label_frame = tk.Frame(frame, background="mistyrose")
    credit_label_frame.pack()
    credit_frame = tk.Frame(frame, background="mistyrose")
    credit_frame.pack()

    name_label = Label(credit_label_frame, text="Full Name:", bg="mistyrose")
    name_label.pack(padx=(45, 55), side=LEFT)
    name = Entry(credit_frame, font=("Futura", 10, "normal"), textvariable=acn_var)
    name.pack(ipady=(4), padx=(62, 0), side=LEFT)
    cvv_label = Label(credit_label_frame, text="License No.:", bg="mistyrose")
    cvv_label.pack(padx=(0, 80), pady=(0, 0), side=LEFT)
    lic = Entry(credit_frame, font=("Futura", 10, "normal"), textvariable=cvv_var)
    lic.pack(ipady=(4), padx=(10, 62), side=LEFT)

    submit = Button(frame, text="Register", bg="cadetblue", border="0", command=lambda: signup(2))
    submit.configure(width=31)
    submit.pack(pady=(20, 0), ipady=(10))
    home = Button(frame, text="Home", bg="sienna2", fg="deepskyblue2", border="0", command=lambda: show_frame(opening_frame))
    home.configure(width=31)
    home.pack(pady=(5, 0), ipady=(10))


def customer_dashboard(frame):              #-----------------customer dashboard----------------------
    canvas = Canvas(frame)
    canvas.pack(fill=BOTH, expand=YES)
    cvimg = img_src("images/bg/bg2.jpg", (600, 600))
    canvas.image = cvimg
    im = canvas.create_image(0, 0, image=cvimg, anchor=NW)
    custlgbtn = tk.Button(frame, text="Customer Login", fg="black", background="orchid2", border=0,
                          command=lambda: show_frame(cust_lg_frame))
    custlgbtn.configure(width=30, height=3)
    custlgbtn.pack(pady=(150, 10))
    custregiibtn = tk.Button(frame, text="New Customer Registration", fg="black", background="cyan2", border=0,
                            command=lambda: show_frame(cust_regii_frame))
    custregiibtn.configure(width=30, height=3)
    create_rectangle(canvas, 150, 110, 450, 300, fill="white",alpha=0.3, width=0)
    canvas.create_window(300, 175, window=custlgbtn)
    canvas.create_window(300, 240, window=custregiibtn)




def driver_dashboard(frame):                 #-----------------------driver dashboard-----------------------
    canvas = Canvas(frame)
    canvas.pack(fill=BOTH, expand=YES)
    cvimg = img_src("images/bg/bg4.jpg", (600, 600))
    canvas.image = cvimg
    canvas.create_image(0, 0, image=cvimg, anchor=NW)
    driverlgbtn = tk.Button(frame, text="Driver Login", fg="coral", background="darkturquoise", border=0,
                          command=lambda: show_frame(dr_lg_frame))
    driverlgbtn.configure(width=35, height=3)
    driversignupbtn = tk.Button(frame, text="New Driver Registration", fg="limegreen", background="tomato3", border=0,
                            command=lambda: show_frame(dr_regii_frame))
    driversignupbtn.configure(width=35, height=3)
    create_rectangle(canvas, 150, 110, 450, 300, fill="white", alpha=0.4, width=0)
    canvas.create_window(300, 175, window=driverlgbtn)
    canvas.create_window(300, 240, window=driversignupbtn)


def book_ride():
    temp_login = get_id_from_temp()
    print(temp_login)
    chck = check_empty([pck_adrs.get(), pck_time.get(), drp_adrs.get(), name_var.get(), phone_var.get()])
    if not chck:
        showerror("Empty", "Empty Field!!")
        return None
    else:
        conn = sql.connect("database/booking/booking.db")
        chck_table = table_check(conn, "RESERVED")
        if not chck_table:
            query = conn.execute(
                "CREATE TABLE RESERVED (id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT NOT NULL, pickaddress TEXT NOT NULL,picktime TEXT NOT NULL,dropaddress TEXT NOT NULL,name TEXT NOT NULL,phone TEXT NOT NULL,active int NOT NULL,driver TEXT NOT NULL)")

        query = conn.execute(
            "INSERT INTO RESERVED(email,pickaddress,picktime,dropaddress,name,phone,active,driver) VALUES('{}','{}','{}','{}','{}','{}','{}','{}')".format(
               temp_login , pck_adrs.get(), pck_time.get(), drp_adrs.get(), name_var.get(),
                phone_var.get(),0,"Pending"))
        conn.commit()
        conn.close()
        showinfo("Successful", "Taxi reservation successfull!!")
        show_frame(cust_desk_frame)

def logout():
    add_id_to_temp("")
    show_frame(opening_frame)

def cust_home(frame):                              #------------customer home----------------------
    top_frame = Frame(frame, bg="navajowhite")
    top_frame.pack()

    body_frame = Frame(frame, bg="lightsteelblue1")
    body_frame.pack(fill=BOTH, expand=YES, pady=(30, 10))

    bottom_frame = Frame(frame, bg="lavender")
    bottom_frame.pack(side=BOTTOM, fill=BOTH, ipady=(20))

    home_title = Label(top_frame, text="Book Taxi Here", bg="navajowhite", fg="plum4", font=("Futura", 15, "bold"))
    home_title.configure(height=3)
    home_title.pack(padx=(222, 0), side=LEFT)

    already_booked = check_dublicate(get_id_from_temp(),"RESERVED","booking")
    print("chck",already_booked)
    if  not already_booked:
        p_a_label = Label(body_frame, text="Pick-up Address:", bg="lightsteelblue1")
        p_a_label.pack(padx=(0, 173))
        pick_address = Entry(body_frame, textvariable=pck_adrs)
        pick_address.pack(ipady=(6), ipadx=(70))

        p_t_label = Label(body_frame, text="Pick-up Date:", bg="lightsteelblue1")
        p_t_label.pack(padx=(0, 190), pady=(2, 0))
        pick_time = DateEntry(body_frame, textvariable=pck_time)
        pick_time.pack(ipady=(6), ipadx=(50))

        d_a_label = Label(body_frame, text="Drop Address:", bg="lightsteelblue1")
        d_a_label.pack(padx=(0, 166), pady=(2, 0))
        drop_address = Entry(body_frame, textvariable=drp_adrs)
        drop_address.pack(ipady=(6), ipadx=(70))

        name_label = Label(body_frame, text="Full Name:", bg="lightsteelblue1")
        name_label.pack(padx=(0, 206), pady=(2, 0))
        name_ = Entry(body_frame, textvariable=name_var)
        name_.pack(ipady=(6), ipadx=(70))

        phone_label = Label(body_frame, text="Mobile No.:", bg="lightsteelblue1")
        phone_label.pack(padx=(0, 217), pady=(2, 0))
        phone = Entry(body_frame, textvariable=phone_var)
        phone.pack(ipady=(6), ipadx=(70))

        find_taxi_btn = tk.Button(body_frame, text="Book Ride", bg="tan4", fg="white", border=0,
                                  command=book_ride)
        find_taxi_btn.configure(height=2, width=38)
        find_taxi_btn.pack(pady=(50, 0))



    else:
        customer_recent_page(body_frame)
    copyright = Label(bottom_frame, bg="lavender", fg="silver",
                      text="Copyright @ {}".format(datetime.date.today().year))
    copyright.pack(side=LEFT, padx=(255, 0))


def get_your_trip(conn, userid):
    query = conn.execute("SELECT rowid,email,pickaddress,picktime,dropaddress,name,phone,active,driver FROM RESERVED")
    temp=[]
    for row in query:
        print(row)
        if row[1] == userid:
            temp.append(row)
    return temp


def list_to_str(data):
    temp=""
    for i in range(1,len(data)):
        temp+=data[i]
        temp+="               "
    return temp.rstrip()

def delete_customer_reservation(id,conn,frame,taxi_list):
    print(taxi_list,"chck list")
    row_id= taxi_list[id][0]
    if taxi_list[id][7]==1:
        newconn = sql.connect("database/rides/rides.db")
        newconn.execute("UPDATE ACTIVE set active=0 WHERE email='{}'".format(taxi_list[8]))
        newconn.commit()
        newconn.close()
    conn.execute("DELETE FROM RESERVED WHERE id={}".format(row_id))
    conn.commit()
    conn.close()
    show_frame(cust_desk_frame)



def trip_finish(data):
    conn = sql.connect("database/booking/booking.db")
    row_id = data[0]
    if data[7] == 1:
        newconn = sql.connect("database/rides/rides.db")
        newconn.execute("UPDATE ACTIVE set active=0 WHERE email='{}'".format(data[8]))
        newconn.commit()
        newconn.close()
    conn.execute("DELETE FROM RESERVED WHERE id={}".format(row_id))
    conn.commit()
    conn.close()
    show_frame(dr_desk)

def customer_recent_page(frame):
    title_frame = Frame(frame,bg="white")
    title_frame.pack(pady=(150,0))

    body = tk.Frame(frame, bg="white")
    body.pack()

    conn = sql.connect("database/booking/booking.db")
    chck_table = table_check(conn,"RESERVED")
    if chck_table:
        taxi_list = get_your_trip(conn, get_id_from_temp())
        print("tc",taxi_list)
        if len(taxi_list) ==0:
            txt= "No Reservation!"
            error = Label(body, text=txt, fg="dimgray", background="whitesmoke", font=("Futura", 22, "bold"))
            error.configure(height=3, width=20)
            error.pack(pady=(200, 0))
        else:
            id_label = Label(title_frame, text="Id", font=("Futura", 10, "bold"), fg="dimgray", bg="gainsboro")
            id_label.configure(width=7, height=2)
            id_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
            pckadrs_label = Label(title_frame, text="Pick-Address", font=("Futura", 10, "bold"), fg="dimgray",
                                  bg="gainsboro")
            pckadrs_label.configure(width=12, height=2)
            pckadrs_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
            pcktme_label = Label(title_frame, text="Pick-Date", font=("Futura", 10, "bold"), fg="dimgray", bg="gainsboro")
            pcktme_label.configure(width=10, height=2)
            pcktme_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
            drpadrs_label = Label(title_frame, text="Drop-Address", font=("Futura", 10, "bold"), fg="dimgray",
                                  bg="gainsboro")
            drpadrs_label.configure(width=12, height=2)
            drpadrs_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
            name_label = Label(title_frame, text="Name", font=("Futura", 10, "bold"), fg="dimgray", bg="gainsboro")
            name_label.configure(width=12, height=2)
            name_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
            phone_label = Label(title_frame, text="Phone", font=("Futura", 10, "bold"), fg="dimgray", bg="gainsboro")
            phone_label.configure(width=12, height=2)
            phone_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))

            count = 1
            del_btn_list=[]
            for data in taxi_list:
                id=IntVar()
                id.set(data[0])
                body = tk.Frame(frame, bg="white")
                body.pack()
                id_label = Label(body, text=str(count))
                id_label.configure(width=7, height=2)
                id_label.pack(side=LEFT, padx=(20, 1), pady=(0, 3))
                pckadrs_label = Label(body, text=data[2])
                pckadrs_label.configure(width=12, height=2)
                pckadrs_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))
                pcktme_label = Label(body, text=data[3])
                pcktme_label.configure(width=10, height=2)
                pcktme_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))
                drpadrs_label = Label(body, text=data[4])
                drpadrs_label.configure(width=12, height=2)
                drpadrs_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))
                name_label = Label(body, text=data[5])
                name_label.configure(width=12, height=2)
                name_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))
                phone_label = Label(body, text=data[6])
                phone_label.configure(width=12, height=2)
                phone_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))

                delimg = img_src("images/delete.png",(20,20))
                delete = Button(body,image=delimg,border=0,bg="white",textvariable =id ,command=partial(delete_customer_reservation,taxi_list.index(data),conn,frame,taxi_list))
                delete.image=delimg
                delete.pack(side=LEFT)
                del_btn_list.append(delete)
                count += 1
    else:
        conn.close()
    status_frame=Frame(frame,bg="white")
    status_frame.pack(fill=BOTH)
    dr_label=Label(status_frame,text="Driver email: ",font=("Futura",12,"bold"),bg="white")
    dr_label.pack(side=LEFT,pady=(10,0),padx=(50,0))
    driver=Label(status_frame,text=data[8])
    driver.pack(side=LEFT,pady=(10,0))



def get_driver_trip():
    conn = sql.connect("database/booking/booking.db")
    chck_tbl = table_check(conn,"RESERVED")
    temp = []
    if chck_tbl:
        query = conn.execute(
            "SELECT rowid,email,pickaddress,picktime,dropaddress,name,phone,active,driver FROM RESERVED")

        for row in query:
            print(row[1])
            if row[8] == get_id_from_temp():
                temp.append(row)

    return temp


def dr_home(frame):                 #-------------------driver home-----------------
    top_frame = Frame(frame, bg="slategray")
    top_frame.pack()

    body_frame = Frame(frame, bg="oldlace")
    body_frame.pack(pady=(10, 10))

    title_frame = Frame(frame, bg="oldlace")
    title_frame.pack(pady=(10, 0))

    body = tk.Frame(frame, bg="oldlace")
    body.pack()

    bottom_frame = Frame(frame, bg="floralwhite")
    bottom_frame.pack(side=BOTTOM, fill=BOTH, ipady=(20))



    home_title = Label(top_frame, text="Welcome Driver", bg="slategray", fg="salmon1", font=("Futura", 15, "bold"))
    home_title.configure(height=3,width=13)
    home_title.pack(padx=(222, 0), side=LEFT)
   # logoutimg = img_src("images/logout.png", (40, 40))
    logout_ = Button(top_frame, text="logout", bg="violetred1", border=0, command=logout)
#    logout_.image = logoutimg
    logout_.pack(padx=(178, 0), side=RIGHT)


    title=Label(body_frame,text="My Trips",bg="oldlace", font=("Futura", 12, "bold"))
    title.pack()


    id_label = Label(title_frame, text="Id", font=("Futura", 10, "bold"), fg="thistle4", bg="snow3")
    id_label.configure(width=7, height=2)
    id_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
    pckadrs_label = Label(title_frame, text="Pick-Address", font=("Futura", 10, "bold"), fg="thistle4",
                          bg="snow3")
    pckadrs_label.configure(width=12, height=2)
    pckadrs_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
    pcktme_label = Label(title_frame, text="Pick-Date", font=("Futura", 10, "bold"), fg="thistle4", bg="snow3")
    pcktme_label.configure(width=10, height=2)
    pcktme_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
    drpadrs_label = Label(title_frame, text="Drop-Address", font=("Futura", 10, "bold"), fg="thistle4",
                          bg="snow3")
    drpadrs_label.configure(width=12, height=2)
    drpadrs_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
    name_label = Label(title_frame, text="Name", font=("Futura", 10, "bold"), fg="thistle4", bg="snow3")
    name_label.configure(width=12, height=2)
    name_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))
    phone_label = Label(title_frame, text="Phone", font=("Futura", 10, "bold"), fg="thistle4", bg="snow3")
    phone_label.configure(width=12, height=2)
    phone_label.pack(side=LEFT, padx=(0, 1), pady=(0, 5))



    if len(get_driver_trip())>0:
        data = get_driver_trip()[0]

        id = IntVar()
        id.set(data[0])
        body = tk.Frame(frame, bg="antiquewhite")
        body.pack()
        id_label = Label(body, text=str(1))
        id_label.configure(width=7, height=2)
        id_label.pack(side=LEFT, padx=(20, 1), pady=(0, 3))
        pckadrs_label = Label(body, text=data[2])
        pckadrs_label.configure(width=12, height=2)
        pckadrs_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))
        pcktme_label = Label(body, text=data[3])
        pcktme_label.configure(width=10, height=2)
        pcktme_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))
        drpadrs_label = Label(body, text=data[4])
        drpadrs_label.configure(width=12, height=2)
        drpadrs_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))
        name_label = Label(body, text=data[5])
        name_label.configure(width=12, height=2)
        name_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))
        phone_label = Label(body, text=data[6])
        phone_label.configure(width=12, height=2)
        phone_label.pack(side=LEFT, padx=(0, 1), pady=(0, 3))
        conn=sql.connect("database/rides/rides.db")
       # complete_img = img_src("images/check.png", (20, 20))
        complete_lbl = Button(body, text="complete ride", border=0, bg="antiquewhite",command = lambda : trip_finish(data))
      #  complete_lbl.image = complete_img
        complete_lbl.pack(side=LEFT)
    else:
        Label(body,text="No Trips Currently!!",font=("Futura",16)).pack(pady=(100,0),ipadx=(50),ipady=(10))


    copyright = Label(bottom_frame, bg="floralwhite", fg="silver",
                      text="Copyright @ {}".format(datetime.date.today().year))
    copyright.pack(side=LEFT, padx=(250, 0))

root = tk.Tk()
root.wm_title("Taxi Ride")
w = 600
h = 440
images = []
temp_login = "mayank@gmail.com"
email_var = StringVar()
pw_var = StringVar()
address_var = StringVar()
phone_var = StringVar()
acn_var = StringVar()
cvv_var = StringVar()
am_pm = StringVar()
am_pm.set("AM")
pck_adrs = StringVar()
pck_time = StringVar()
drp_adrs = StringVar()
name_var = StringVar()

root.geometry(str(w) + 'x' + str(h))
root.wm_resizable(False, False)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

opening_frame = tk.Frame(root,background="white")
cust_dash = tk.Frame(root, background="white")
dr_dash = tk.Frame(root, background="white")
cust_lg_frame = tk.Frame(root)
cust_regii_frame = tk.Frame(root)
dr_lg_frame = tk.Frame(root)
dr_regii_frame = tk.Frame(root)
cust_desk_frame = tk.Frame(root, background="white")
dr_desk = tk.Frame(root, background="white")
print(dr_desk)
for frame in (opening_frame, cust_dash, dr_dash, cust_lg_frame, cust_regii_frame,
              dr_lg_frame, dr_regii_frame, cust_desk_frame,dr_desk):
    frame.grid(row=0, column=0, sticky="nsew")
wel_dashboard(opening_frame)
customer_dashboard(cust_dash)
driver_dashboard(dr_dash)
cust_lg(cust_lg_frame)
cust_regii(cust_regii_frame)
dr_lg(dr_lg_frame)
dr_regii(dr_regii_frame)
cust_home(cust_desk_frame)

dr_home(dr_desk)


show_frame(opening_frame)

root.mainloop()
