import os
import smtplib
import time
from tkinter import*
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import email_pass
class Login_System:
 def __init__(self,root):
  self.root=root
  self.root.title("Login System | Developed By Archana | webcode")
  self.root.geometry("1350x700+0+0")
  self.root.config(bg="#fafafa")
  self.otp=''
  #=======Image======================
  self.phone_image=ImageTk.PhotoImage(file="images/phone.png")
  self.lbl_phone_image=Label(self.root,image=self.phone_image,bd=0).place(x=200,y=30)
  #======Login Frame==================
  self.employee_id=StringVar()
  self.password=StringVar()
  login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
  login_frame.place(x=650,y=60,width=350,height=460)

  title=Label(login_frame,text="Login System",font=("Elephant",30,"bold"),bg="white").place(x=25,y=20)

  lbl_employee_id=Label(login_frame,text="Employee ID",font=("Andalus",15),bg="white",fg="#767171").place(x=35,y=90)
  
  txt_employee_id=Entry(login_frame,textvariable=self.employee_id,font=("times new roman",13),bg="lightgrey",fg="black").place(x=35,y=125,width=280,height=30) 


  lbl_pass=Label(login_frame,text="Password",font=("Andalus",15),bg="white",fg="#767171").place(x=35,y=180)
  
  txt_pass=Entry(login_frame,textvariable=self.password,show="*",font=("times new roman",13),bg="lightgrey",fg="black").place(x=35,y=215,width=280,height=30) 

  btn_login=Button(login_frame,command=self.login,text="Log In",font=("Arial Rounded MT Bold",18),bg="blue",fg="white").place(x=35,y=270,width=280,height=35)

  hr=Label(login_frame,bg="lightblue").place(x=35,y=340,width=280,height=2)
  or_=Label(login_frame,text="OR",bg="white",fg="lightblue",font=("times new roman",15,"bold")).place(x=145,y=328)

  btn_forget=Button(login_frame,text="Forget Password?",command=self.forget_window,font=("times new roman",18),bg="white",fg="blue").place(x=35,y=380,width=280,height=35)

#=========Frame 2============================================
  register_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
  register_frame.place(x=650,y=530,width=350,height=60)

  lbl_reg=Label(register_frame,text="SUBCRIBE | LIKE | SHARE",font=("times new roman",15),bg="white",fg="black").place(x=45,y=17)



#=========Animation Image======================================
  self.im1=ImageTk.PhotoImage(file="images/im1.png")
  self.im2=ImageTk.PhotoImage(file="images/im2.png")
  self.im3=ImageTk.PhotoImage(file="images/im3.png")

  self.lbl_change_image=Label(self.root,bg="white")
  self.lbl_change_image.place(x=367,y=153,width=240,height=415)

  self.animate()
 
#==========All Functions========================================
 def animate(self):
    self.im=self.im1
    self.im1=self.im2
    self.im2=self.im3
    self.im3=self.im
    self.lbl_change_image.config(image=self.im)
    self.lbl_change_image.after(2000,self.animate)  

 def login(self):
   con=sqlite3.connect(database=r'ims.db')
   cur=con.cursor()
   try:
        if self.employee_id.get()=="" or self.password.get()=="":
           messagebox.showerror('Error',"All fields are required",parent=self.root)
        else:   
           cur.execute("select utype from employee where eid=? AND pass=?",(self.employee_id.get(),self.password.get()))
           user=cur.fetchone()
           if user==None:
              messagebox.showerror('Error',"Invalid USERNAME/PASSWORD",parent=self.root)
           else:
              if user[0]=="Admin":
                self.root.destroy()
                os.system("python dashboard.py")
              else:
                 self.root.destroy()
                 os.system("python billing.py")           
   except Exception as ex:
          messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

 def forget_window(self):
   con=sqlite3.connect(database=r'ims.db')
   cur=con.cursor()
   try:
         if self.employee_id.get()=="":
            messagebox.showerror('Error',"Employee ID must be required",parent=self.root)
         else:
          cur.execute("select email from employee where eid=?",(self.employee_id.get(),))
          email=cur.fetchone()
          if email==None:
              messagebox.showerror('Error',"Invalid Employee ID,try again",parent=self.root)
          else:
             #=====forget window=========================
             self.var_otp=StringVar()
             self.var_new_pass=StringVar()
             self.var_conf_pass=StringVar()
             #call send_email_function()
             chk=self.send_email('archanayadav28022019@gmail.com')
             if chk!='s':
                messagebox.showerror("Error","Connection Error, try again",parent=self.root)
             else:
              self.forget_win=Toplevel(self.root)
              self.forget_win.title('RESET PASSWORD')
              self.forget_win.geometry('400x350+500+100')
              self.forget_win.focus_force()

              title=Label(self.forget_win,text='Reset Password',font=('goudy old style',15,'bold'),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)

              lbl_reset=Label(self.forget_win,text="Enter OTP sent on Registered Email",font=("times new roman",15)).place(x=20,y=60)
              txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("times new roman",15),bg="lightyellow").place(x=20,y=100,width=250,height=30)

              self.btn_reset=Button(self.forget_win,text="SUBMIT",command=self.validate_otp,font=("times new roman",15),bg="lightblue")
              self.btn_reset.place(x=280,y=100,width=100,height=30)

              lbl_new_pass=Label(self.forget_win,text="New Password",font=("times new roman",15)).place(x=20,y=160)
              txt_new_pass=Entry(self.forget_win,textvariable=self.var_new_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=190,width=250,height=30)

              lbl_conf_pass=Label(self.forget_win,text="Confirm Password",font=("times new roman",15)).place(x=20,y=225)
              txt_conf_pass=Entry(self.forget_win,textvariable=self.var_conf_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=255,width=250,height=30)

              self.btn_update=Button(self.forget_win,text="Update",command=self.update_password,state=DISABLED,font=("times new roman",15),bg="lightblue")
              self.btn_update.place(x=150,y=300,width=100,height=30)
                                     
   except Exception as ex:
      messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)


 def update_password(self):
    if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
       messagebox.showerror("Error","Password is required",parent=self.forget_win)
    elif self.var_new_pass.get()!= self.var_conf_pass.get():
       messagebox.showerror("Error","New Password & confirm password should be same",parent=self.forget_win)
    else:
       con=sqlite3.connect(database=r'ims.db')
       cur=con.cursor()
       try: 
          cur.execute("Update employee SET pass=? where eid=?",(self.var_new_pass.get(),self.employee_id.get()))
          con.commit()
          messagebox.showinfo("Success","Password updated sucessfully",parent=self.forget_win)
          self.forget_win.destroy()
       except Exception as ex:
         messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

         
        



 def validate_otp(self):
    if int(self.otp)==int(self.var_otp.get()):
       self.btn_update.config(state=NORMAL)
       self.btn_reset.config(state=DISABLED)
    else:
       messagebox.showerror("Error","Invalid OTP, Try again",parent=self.forget_win)  

 def send_email(self,to_):         #port number
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    email_=email_pass.email_
    pass_=email_pass.pass_  

    s.login(email_,pass_)

    self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))
    subj='IMS-Reset Password OTP'
    msg=f'Dear Sir/Madam,\n\nYour Reset OTP is {str(self.otp)}.\n\nWith Regards,\nIMS Team'
    msg="Subject:{}\n\n{}".format(subj,msg)
    s.sendmail(email_,to_,msg)  
    chk=s.ehlo()
    if chk[0]==250:
       return 's'
    else:
      return 'f'                


root=Tk()
obj=Login_System(root)
root.mainloop()   
            