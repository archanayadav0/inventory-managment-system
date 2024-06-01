from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Mangement System | Developed By Archana")
        self.root.config(bg="white")
        self.root.focus_force()
        #=========================
        # All Variables======
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()             
        self.var_sup_invoice=StringVar()        
        self.var_name=StringVar()
        self.var_contact=StringVar()
        self.var_desc=StringVar()
        #===title=======
        title=Label(self.root,text="Supplier Details",font=("bold",15),bg="#0f4d7d",fg="white").place(x=40,y=10,width=1200,height=40)

        #======searchFrame======
        
        
        #=====options====
        lbl_search=Label(self.root,text="Search By Invoice No.",bg="white",font=("goudly old style",13))
        lbl_search.place(x=730,y=150)
        txt_search=Entry(self.root,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=900,y=150)
        btn_search=Button(self.root,text="search",command=self.search,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=1110,y=150,width=150,height=28)

        
        
       #=====content============
       #=====row1=======
        lbl_supplier_invoice=Label(self.root,text="Invoice No.",font=("goudy old style",15),bg="white").place(x=50,y=80)  

        txt_supplier_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=("goudy old style",15),bg="lightyellow").place(x=150,y=80,width=180)
       
        #======row2=======
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15),bg="white").place(x=50,y=120)
        
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=150,y=120,width=180)
       
        #========row3========
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=50,y=160)
       
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow").place(x=150,y=160,width=180)
       
        #=======row4=======
        lbl_desc=Label(self.root,text="Description",font=("goudy old style",15),bg="white").place(x=50,y=200)
        
        self.txt_desc=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_desc.place(x=150,y=200,width=500,height=250)
        
        #=======button=======
        btn_add=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=150,y=480,width=110,height=28)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=275,y=480,width=110,height=28)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=400,y=480,width=110,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=525,y=480,width=110,height=28)


        #=====Supplier Details=====
        sup_frame=Frame(self.root,bd=3,relief=RIDGE)
        sup_frame.place(x=730,y=200,width=530,height=400)

        scrolly=Scrollbar(sup_frame,orient=VERTICAL)
        scrollx=Scrollbar(sup_frame,orient=HORIZONTAL)

        self.SupplierTable=ttk.Treeview(sup_frame,columns=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)    

        self.SupplierTable.heading("invoice",text="Invoice No.")
        self.SupplierTable.heading("name",text="Name")
        self.SupplierTable.heading("contact",text="Contact")
        self.SupplierTable.heading("desc",text="Desc")       
        self.SupplierTable["show"]="headings"

        self.SupplierTable.column("invoice",width=90)
        self.SupplierTable.column("name",width=100)
        self.SupplierTable.column("contact",width=100)
        self.SupplierTable.column("desc",width=100)
        self.SupplierTable.pack(fill=BOTH,expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>",self.get_data)


        self.show()
#===================for add======================================================================
    def add(self):
       con=sqlite3.connect(database=r'ims.db')
       cur=con.cursor()
       try:
          if self.var_sup_invoice.get()=="":
             messagebox.showerror("Error","Invoice must be required",parent=self.root)
          else:
             cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
             row=cur.fetchone()
             if row!=None:
                messagebox.showerror("Error","This Invoice no. already assigned, try different",parent=self.root)
             else:
                cur.execute("Insert into supplier(invoice,name,contact,desc) values(?,?,?,?)",(
                   self.var_sup_invoice.get(),
                   self.var_name.get(),                 
                   self.var_contact.get(),                                     
                   self.txt_desc.get('1.0',END)

                ))
                con.commit()
                messagebox.showinfo("success","Supplier Added Successfully",parent=self.root )
                self.show()          
       except Exception as ex:
          messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)
#====showing data of employee table in box which is present below =========
    def show(self):
       con=sqlite3.connect(database=r'ims.db')
       cur=con.cursor()
       try: 
          cur.execute("select * from supplier")
          rows=cur.fetchall()
          self.SupplierTable.delete(*self.SupplierTable.get_children())
          for row in rows:
             self.SupplierTable.insert('',END,values=row) 
       except Exception as ex:
          messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)
#=======select all data from table and showing in self boxes=======
    def get_data(self,ev):
       f=self.SupplierTable.focus()
       content=(self.SupplierTable.item(f))
       row=content['values']
       print(row)
       self.var_sup_invoice.set(row[0]),
       self.var_name.set(row[1]),      
       self.var_contact.set(row[2]),                         
       self.txt_desc.delete('1.0',END),
       self.txt_desc.insert(END,row[3]),
#=========for update============================================================     
    def update(self):
       con=sqlite3.connect(database=r'ims.db')
       cur=con.cursor()
       try:
          if self.var_sup_invoice.get()=="":
             messagebox.showerror("Error","Invoice no. Must be required",parent=self.root)
          else:
             cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
             row=cur.fetchone()
             if row==None:
                messagebox.showerror("Error","Invalid Invoice no.",parent=self.root)
             else:
                cur.execute("Update supplier set name=?,contact=?,desc=? where invoice=?",(                
                   self.var_name.get(),                   
                   self.var_contact.get(),                                     
                   self.txt_desc.get('1.0',END),                 
                   self.var_sup_invoice.get(),
))
                con.commit()
                messagebox.showinfo("success","Supplier Updated Successfully",parent=self.root )
                self.show()          
       except Exception as ex:
          messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)          
#================delete========================================================================
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
             messagebox.showerror("Error","Invoice no. Must be required",parent=self.root)
            else:
             cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
             row=cur.fetchone()
             if row==None:
                messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
             else:
                op=messagebox.askyesno("confirm","Do you really want to delete?",parent=self.root)
                if op==True:
                 cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                 con.commit()
                 messagebox.showinfo("Delete","Supplier Deleted Successfully",parent=self.root)
                 
                 self.clear()
        except Exception as ex:
          messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root) 
#===============clear=============================================================================
    def clear(self):
       self.var_sup_invoice.set(""),
       self.var_name.set(""),      
       self.var_contact.set(""),                       
       self.txt_desc.delete('1.0',END),  
       self.var_searchtxt.set("")
       self.show()
#========search==================================================================================  
    def search(self):
         con=sqlite3.connect(database=r'ims.db')
         cur=con.cursor()
         try:
          if self.var_searchtxt.get()=="":
             messagebox.showerror("Error","Invoice No. should be required",parent=self.root)              
          else:           
             cur.execute(f"select * from supplier where invoice=?",(self.var_searchtxt.get(),))           
             row=cur.fetchone()
             self.SupplierTable.delete(*self.SupplierTable.get_children())
             if row!=NONE:
                self.SupplierTable.insert('',END, values=row)
             else:                
                 messagebox.showerror("Error","No record found!!!",parent=self.root)        
         except Exception as ex:
          messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)
           
      

if __name__=="__main__":
 root=Tk()
 obj=supplierClass(root)
 root.mainloop()




         