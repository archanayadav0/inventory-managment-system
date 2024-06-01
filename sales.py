from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import os
class salesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Mangement System | Developed By Archana")
        self.root.config(bg="white")
        self.root.focus_force()

        #===title=======
        title=Label(self.root,text="Customer Bill Reports",font=("bold",18),bg="#0f4d7d",fg="white",bd=3,relief=RIDGE).place(x=20,y=9,width=1200,height=30)
       #======variable=======================
        self.bill_list=[]
        self.var_invoice=StringVar()
#========================================================================
        lbl_invoice_no=Label(self.root,text="Invoice No.",font=("goudy old style",15),bg="white").place(x=50,y=70)
        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=("goudy old style",15),bg="lightyellow").place(x=160,y=70)
        btn_search=Button(self.root,text="Search",command=self.search,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=370,y=70,width=150,height=27)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=530,y=70,width=150,height=27)
#==========Bill List=======================
        sales_Frame=Frame(self.root,bd=3,relief=RIDGE)
        sales_Frame.place(x=50,y=120,width=200,height=330)

        scrolly=Scrollbar(sales_Frame,orient=VERTICAL)
        self.Sales_List=Listbox(sales_Frame,font=("goudy old style",15),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH,expand=1)
       # self.Sales_List.bind("<ButtonRelease-1>,self.get_data")
        self.Sales_List.bind("<<ListboxSelect>>", self.get_data)

#==========Bill Area=========================
        bill_Frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_Frame.place(x=280,y=120,width=410,height=330)

        title2=Label(bill_Frame,text="Customer Bill Area",font=("bold",18),bg="orange")
        title2.pack(side=TOP,fill=X)
        scrolly2=Scrollbar(bill_Frame, orient=VERTICAL)
        self.bill_area=Text(bill_Frame,bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)

#=============Image========================
        self.bill_photo=Image.open("images/cat2.jpg")
        # Resize the image with LANCZOS
        self.bill_photo = self.bill_photo.resize((500, 350), Image.LANCZOS)
        self.bill_photo=ImageTk.PhotoImage(self.bill_photo) 


        lbl_image=Label(self.root,image=self.bill_photo,bd=0)
        lbl_image.place(x=700,y=110)

        self.show()
 #============================================================================
    def show(self):
       del self.bill_list[:]
       self.Sales_List.delete(0,END)
       for i in os.listdir('bill'):
          if i.split('.')[-1]=='txt':
              self.Sales_List.insert(END,i)
              self.bill_list.append(i.split('.')[0])     
               
    
    def get_data(self, ev):
      index_= self.Sales_List.curselection()
      file_name=self.Sales_List.get(index_)
      print(file_name)
      self.bill_area.delete('1.0',END)
      fp=open(f'bill/{file_name}','r')
      for i in fp:
         self.bill_area.insert(END,i)
      fp.close()
    
    def search(self):
       if self.var_invoice.get()=="":
          messagebox.showerror("Error","Invoice no. should be required",parent=self.root)
       else:
          if self.var_invoice.get() in self.bill_list:
             fp=open(f'bill/{self.var_invoice.get()}.txt','r')
             self.bill_area.delete('1.0',END)
             for i in fp:
                self.bill_area.insert(END,i)
             fp.close()
          else: 
             messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)   
            
    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)   








if __name__=="__main__":
 root=Tk()
 obj=salesClass(root)
 root.mainloop()        