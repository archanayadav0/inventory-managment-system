import sqlite3
import time
from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import os
import tempfile
class BillClass:
 def __init__(self,root):
      self.root=root
      self.root.geometry("1350x700+0+0")
      self.root.title("Billing | Inventory Mangement System | Developed By Archana")
      self.root.config(bg="white")
      self.cart_list=[]
      self.chk_print=0
        #===title=====
      self.icon_title=PhotoImage(file="images/logo1.png")
      title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new romen",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)
        #===btn_logout===
      btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=100)
        #===clock=====
      self.lbl_clock=Label(self.root,text="Welcome toInventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS" ,font=("times new roman",15),bg="#4d636d",fg="white")
      self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
      #====Product Frame=============
      self.var_search=StringVar()
      ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
      ProductFrame1.place(x=6,y=110,width=410,height=520)

      pTitle=Label(ProductFrame1,text="All Products",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)
           
      ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
      ProductFrame2.place(x=4,y=42,width=395,height=90)

      lbl_search=Label(ProductFrame2,text="Search Product | By Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)

      lbl_search=Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=2,y=45)

      txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=128,y=47,width=150,height=22)
      btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=284,y=45,width=100,height=24)

      btn_show_all=Button(ProductFrame2,text="Show All",command=self.show,font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=284,y=10,width=100,height=24)

#==========product details============================================
      ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
      ProductFrame3.place(x=4,y=137,width=395,height=350)

      scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
      scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)

      self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
      scrollx.pack(side=BOTTOM,fill=X)
      scrolly.pack(side=RIGHT,fill=Y)
      scrollx.config(command=self.product_Table.xview)
      scrolly.config(command=self.product_Table.yview)    

      self.product_Table.heading("pid",text="pid")
      self.product_Table.heading("name",text="Name")
      self.product_Table.heading("price",text="price")
      self.product_Table.heading("qty",text="QTY")
      self.product_Table.heading("status",text="Status")       
      self.product_Table["show"]="headings"

      self.product_Table.column("pid",width=50)
      self.product_Table.column("name",width=100)
      self.product_Table.column("price",width=100)
      self.product_Table.column("qty",width=40)
      self.product_Table.column("status",width=90)
      self.product_Table.pack(fill=BOTH,expand=1)
      self.product_Table.bind("<ButtonRelease-1>",self.get_data)
      lbl_note=Label(ProductFrame1,text="Note:'Enter 0 Quantity to remove product from the Cart'",font=("goudy old style",10),anchor='w',bg="white",fg="red").pack(side=BOTTOM,fill=X)
      #=====================customer frame==========
      self.var_cname=StringVar()
      self.var_contact=StringVar()
      CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
      CustomerFrame.place(x=420,y=110,width=530,height=70)
      cTitle=Label(CustomerFrame,text="Customer Details",font=("goudy old style",15),bg="lightgray").pack(side=TOP,fill=X)

      lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",15),bg="white").place(x=5,y=35)
      txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13),bg="lightyellow").place(x=80,y=35,width=180)

      lbl_contact=Label(CustomerFrame,text="Contact No.",font=("times new roman",15),bg="white").place(x=270,y=35)
      txt_name=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg="lightyellow").place(x=380,y=35,width=140)
 #=========calculator or cart frame===============================================
      Cal_cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
      Cal_cart_Frame.place(x=420,y=190,width=530,height=360)
#=========calculator frame===============================================
      self.var_cal_input=StringVar()
      Cal_Frame=Frame(Cal_cart_Frame,bd=9,relief=RIDGE,bg="white")
      Cal_Frame.place(x=5,y=10,width=268,height=340)

      txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=('arial',15,'bold'),width=21,bd=10,relief=GROOVE,state='readonly',justify=RIGHT)
      txt_cal_input.grid(row=0,columnspan=4)

      btn_7=Button(Cal_Frame,text='7',font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=0)

      btn_8=Button(Cal_Frame,text='8',font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=1)

      btn_9=Button(Cal_Frame,text='9',font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=2)

      btn_sum=Button(Cal_Frame,text='+',font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=3)
      
      btn_4=Button(Cal_Frame,text='4',font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=0)

      btn_5=Button(Cal_Frame,text='5',font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=1)

      btn_6=Button(Cal_Frame,text='6',font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=2)

      btn_subtract=Button(Cal_Frame,text='-',font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=3)

      btn_1=Button(Cal_Frame,text='1',font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=0)

      btn_2=Button(Cal_Frame,text='2',font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=1)

      btn_3=Button(Cal_Frame,text='3',font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=2)

      btn_multiply=Button(Cal_Frame,text='*',font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=3)

      btn_0=Button(Cal_Frame,text='0',font=('arial',15,'bold'),command=lambda:self.get_input(0),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=0)

      btn_C=Button(Cal_Frame,text='C',font=('arial',15,'bold'),command=self.clear_cal,bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=1)

      btn_divide=Button(Cal_Frame,text='/',font=('arial',15,'bold'),command=lambda:self.get_input('/'),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=2)

      btn_equal=Button(Cal_Frame,text='=',font=('arial',15,'bold'),command=self.perform_cal,bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=3)

#=============Cart Details=============================================================
      cart_Frame=Frame(Cal_cart_Frame,bd=3,relief=RIDGE)
      cart_Frame.place(x=280,y=8,width=245,height=342)
      self.cartTitle=Label(cart_Frame,text="Cart \t Total Product: [0]",font=("goudy old style",15),bg="lightgray")
      self.cartTitle.pack(side=TOP,fill=X)

      scrolly=Scrollbar(cart_Frame,orient=VERTICAL)
      scrollx=Scrollbar(cart_Frame,orient=HORIZONTAL)

      self.Cart_Table=ttk.Treeview(cart_Frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
      scrollx.pack(side=BOTTOM,fill=X)
      scrolly.pack(side=RIGHT,fill=Y)
      scrollx.config(command=self.Cart_Table.xview)
      scrolly.config(command=self.Cart_Table.yview)    

      self.Cart_Table.heading("pid",text="pid")
      self.Cart_Table.heading("name",text="Name")
      self.Cart_Table.heading("price",text="price")
      self.Cart_Table.heading("qty",text="QTY")         
      self.Cart_Table["show"]="headings"
      self.Cart_Table.column("pid",width=40)
      self.Cart_Table.column("name",width=90)
      self.Cart_Table.column("price",width=90)
      self.Cart_Table.column("qty",width=50)   
      self.Cart_Table.pack(fill=BOTH,expand=1)
      self.Cart_Table.bind("<ButtonRelease-1>",self.get_data_cart)
#======Menu Frame==============================================
      self.var_pid=StringVar()
      self.var_pname=StringVar()
      self.var_qty=StringVar()
      self.var_price=StringVar()
      self.var_stock=StringVar()
      
      MenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
      MenuFrame.place(x=420,y=550,width=530,height=80)

      lbl_p_name=Label(MenuFrame,text="Product Name",font=("times new roman",12),bg="white").place(x=5,y=3)
      txt_p_name=Entry(MenuFrame,textvariable=self.var_pname,font=("times new roman",12),bg="lightyellow",state='readonly').place(x=5,y=30,width=190,height=18)
       
      lbl_p_price=Label(MenuFrame,text="Price Per Qty",font=("times new roman",12),bg="white").place(x=210,y=3)
      txt_p_price=Entry(MenuFrame,textvariable=self.var_price,font=("times new roman",12),bg="lightyellow",state='readonly').place(x=210,y=30,width=180,height=18)

      lbl_p_qty=Label(MenuFrame,text="Quantity",font=("times new roman",12),bg="white").place(x=400,y=3)
      txt_p_qty=Entry(MenuFrame,textvariable=self.var_qty,font=("times new roman",12),bg="lightyellow").place(x=400,y=30,width=120,height=18)

      self.lbl_inStock=Label(MenuFrame,text="In Stock",font=("times new roman",12),bg="white")
      self.lbl_inStock.place(x=5,y=50)
      
      btn_clear_cart=Button(MenuFrame,text="clear",command=self.clear_cart,font=("times new romen",12,"bold"),bg="lightgray",cursor="hand2").place(x=160,y=50,width=130,height=23)
      btn_add_cart=Button(MenuFrame,text="Add | Update cart",command=self.add_update_cart,font=("times new romen",12,"bold"),bg="orange",cursor="hand2").place(x=320,y=50,width=170,height=23)

#=============billing Area================
      billFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
      billFrame.place(x=953,y=110,width=315,height=410)

      bTitle=Label(billFrame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)
      scrolly=Scrollbar(billFrame,orient=VERTICAL)
      scrolly.pack(side=RIGHT,fil=Y)
      self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
      self.txt_bill_area.pack(fill=BOTH,expand=1)
      scrolly.config(command=self.txt_bill_area.yview)

#===========billing buttons====================
      billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
      billMenuFrame.place(x=953,y=520,width=315,height=111)

      self.lbl_amount=Label(billMenuFrame,text='Bill Amount\n[0]',font=("goudy old style",13,"bold"),bg="#3f51b5",fg="white")
      self.lbl_amount.place(x=2,y=3,width=103,height=65)

      self.lbl_discount=Label(billMenuFrame,text='Discount\n[5%]',font=("goudy old style",13,"bold"),bg="#8bc34a",fg="white")
      self.lbl_discount.place(x=110,y=3,width=100,height=65) 

      self.lbl_net_pay=Label(billMenuFrame,text='Net Pay\n[0]',font=("goudy old style",13,"bold"),bg="#607d8b",fg="white")
      self.lbl_net_pay.place(x=215,y=3,width=100,height=65) 

      btn_print=Button(billMenuFrame,text='Print',command=self.print_bill,cursor='hand2',font=("goudy old style",12,"bold"),bg="lightgreen",fg="white")
      btn_print.place(x=2,y=70,width=90,height=35)

      btn_clear_all=Button(billMenuFrame,text='Clear All',command=self.clear_all,cursor='hand2',font=("goudy old style",12,"bold"),bg="gray",fg="white")
      btn_clear_all.place(x=94,y=70,width=90,height=35) 

      btn_generate=Button(billMenuFrame,text='Generate Bill/Save Bill',command=self.generate_bill,cursor='hand2',font=("goudy old style",12,"bold"),bg="#009688",fg="white")
      btn_generate.place(x=187,y=70,width=125,height=35)       
      
#=====footer============================ error not showing
      footer=Label(self.root,text="IMS-Inventory Management System | Developed By Archana\nFor any Technical Issue contact: 6378xxxx05",font=("times new roman",11),bg="#4d636d",fg="white",).pack(side=BOTTOM,fill=X)
                 
      self.show()
      self.update_date_time()
      
#===========All Functions of calculator====================================
 def get_input(self,num):
   xnum=self.var_cal_input.get()+str(num)
   self.var_cal_input.set(xnum)

 def clear_cal(self):
   self.var_cal_input.set('')  

 def perform_cal(self):
   result=self.var_cal_input.get()
   self.var_cal_input.set(eval(result))
#=============function for billing area======================================
 def show(self):
       con=sqlite3.connect(database=r'ims.db')
       cur=con.cursor()#"pid","name","price","qty","status"
       try: 
          cur.execute("select pid,pname,price,qty,status from product where status='Active'")
          rows=cur.fetchall()
          self.product_Table.delete(*self.product_Table.get_children())
          for row in rows:
             self.product_Table.insert('',END,values=row) 
       except Exception as ex:
          messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)  

 def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:       
          if self.var_search.get()=="":
             messagebox.showerror("Error","Search input should be required",parent=self.root)      
          else:  
             cur.execute(f"select pid,pname,price,qty,status from product where pname LIKE'%"+self.var_search.get()+ "%'")
             rows=cur.fetchall()
             if len(rows)!=0:
                self.product_Table.delete(*self.product_Table.get_children())
                for row in rows:
                    self.product_Table.insert('',END,values=row)
             else:
                 messagebox.showerror("Error","No record found!!!",parent=self.root)        

        except Exception as ex:
          messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)

 def get_data(self, ev):
    f = self.product_Table.focus()
    content = self.product_Table.item(f)
    row = content['values']

    # Check if row has at least 4 elements before accessing them
    if len(row) >= 4:
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')
    else:
        # Handle the case where row doesn't have enough elements
        # You can print an error message or take appropriate action here
        print("Row does not have enough elements")


#========calculator ke side vale frame se vapes data fetch krne ke liye function=====
 def get_data_cart(self,ev):
       f=self.Cart_Table.focus()
       content=(self.Cart_Table.item(f))
       row=content['values']
       self.var_pid.set(row[0])
       self.var_pname.set(row[1])
       self.var_price.set(row[2])
       self.var_qty.set(row[3])
       self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
       self.var_stock.set(row[4])
                

 def add_update_cart(self):
        if self.var_pid.get()=='':
           messagebox.showerror('Error',"Please select product from the list",parent=self.root)        
        elif self.var_qty.get()=='':
           messagebox.showerror('Error',"Quantity is Required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
           messagebox.showerror('Error',"Invalid Quantity",parent=self.root)  
        else:    
           #price_cal=float(int(self.var_qty.get())*float(self.var_price.get()))
           #price_cal=float(price_cal)
           price_cal=self.var_price.get()
           cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
        
#==========update_cart====================
        present='no'        
        index_=0
        for row in self.cart_list:
           if self.var_pid.get()==row[0]:
              present='yes'
              break
           index_+=1
        if present=='yes':
            op=messagebox.askyesno('confirm',"Product already present\nDo you want to Update| Remove from the Cart List",parent=self.root)
            if op==True:
               if self.var_qty.get()=="0":
                  self.cart_list.pop(index_)
               else:
                  #price_cal = float(int(self.var_qty.get()) * float(self.var_price.get()))
                  #self.cart_list[index_][2]=price_cal
                  self.cart_list[index_][3]=self.var_qty.get()   
        else:
           self.cart_list.append(cart_data)

        self.show_cart()
        self.bill_updates()

 def bill_updates(self):
    self.bill_amount=0
    self.net_pay=0
    self.discount=0
    for row in self.cart_list:
       self.bill_amount=self.bill_amount+(float(row[2])*int(row[3]))
    self.discount=(self.bill_amount*5)/100   
    self.net_pay=self.bill_amount-self.discount
    self.lbl_amount.config(text=f'Bill Amount\n{str(self.bill_amount)}')
    self.lbl_net_pay.config(text=f'Net Pay\n{str(self.net_pay)}')
    self.cartTitle.config(text=f"Cart \t Total Product:[{str(len(self.cart_list))}]")           
           

 def show_cart(self):
    try:
       self.Cart_Table.delete(*self.Cart_Table.get_children()) 
       for row in self.cart_list:
          self.Cart_Table.insert('',END,values=row)
    except Exception as ex:
       messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)             




 def generate_bill(self):
   if self.var_cname.get()==''or self.var_contact.get()=='':
      messagebox.showerror("Error",f"Customer Details are required",parent=self.root)
   elif len(self.cart_list)==0:
       messagebox.showerror("Error",f"Please Add Product To The Cart",parent=self.root)

   else:
      #======Bill Top===================
      self.bill_top()
      #=====Bill Middle=============
      self.bill_middle()
      #====Bill Bottom============
      self.bill_bottom()

      fp=open(f'bill/{str(self.invoice)}.txt','w')
      fp.write(self.txt_bill_area.get('1.0',END))
      fp.close()
      messagebox.showinfo('Saved',"Bill has been generated/Save in Backend",parent=self.root)
      self.chk_print=1
       
 def bill_top(self):
    self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
    bill_top_temp=f'''
\t\tXYZ-Inventory
\tPhone No. 98725*****, Delhi-125001
{str("="*36)}
Customer Name: {self.var_cname.get()}
ph no.:{self.var_contact.get()}
Bill No.{str(self.invoice)}\t\tDate: {str(time.strftime("%d/%m/%Y"))} 
{str("="*36)}
Product Name\t\tQTY\tPrice
{str("="*36)}
     '''  
    self.txt_bill_area.delete('1.0',END)
    self.txt_bill_area.insert('1.0',bill_top_temp)

 def bill_bottom(self):
    bill_bottom_temp=f'''
{str("="*36)}
Bill Amount\t\t\tRs.{self.bill_amount}
Discount\t\t\tRs.{self.discount}
Net Pay\t\t\tRs.{self.net_pay}
{str("="*36)}\n 
    '''
    self.txt_bill_area.insert(END,bill_bottom_temp)

 def bill_middle(self):
   con=sqlite3.connect(database=r'ims.db')
   cur=con.cursor()
   try:  
      for row in self.cart_list:
         
          pid=row[0]
          name=row[1]
          qty=int(row[4])-int(row[3])
          if int(row[3])==int(row[4]):
             status='Inactive'
          if int(row[3])!=int(row[4]):
             status='Active'
          price=float(row[2])*int(row[3])
          price=str(price)
          self.txt_bill_area.insert(END,"\n"+name+"\t\t\t"+row[3]+"\tRs."+price)
#=========update qty in product table after generating the bill==========
          cur.execute('Update product set qty=?,status=? where pid=?',(
             qty,
             status,
             pid
          )) 
          con.commit()
      con.close()
      self.show()       
   except Exception as ex:
       messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)   

 def clear_cart(self):
     self.var_pid.set('')           
     self.var_pname.set('')
     self.var_price.set('')
     self.var_qty.set('')
     self.lbl_inStock.config(text=f"In Stock")
     self.var_stock.set('')

 def clear_all(self):
    del self.cart_list[:]
    self.var_cname.set('')
    self.var_contact.set('')
    self.txt_bill_area.delete('1.0',END)
    self.cartTitle.config(text=f"Cart \t Total Product:[0]")
    self.var_search.set('')
    self.clear_cart()
    self.show()
    self.show_cart()

 def update_date_time(self):
    time_=time.strftime("%I:%M:%S")
    date_=time.strftime("%d-%m-%Y")
    self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time:{str(time_)}")
    self.lbl_clock.after(200,self.update_date_time)

 def print_bill(self):
    if self.chk_print==1:
       messagebox.showinfo('Print',"Please wait while printing",parent=self.root)
       new_file=tempfile.mktemp('.txt')
       open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
       os.startfile(new_file,'print')  
    else:
       messagebox.showerror('Print',"Please generate bill, to print the receipt",parent=self.root)
        
 def logout(self):
    self.root.destroy()
    os.system("python login.py")           


    
if __name__=="__main__":
 root=Tk()
 obj=BillClass(root)
 root.mainloop()
