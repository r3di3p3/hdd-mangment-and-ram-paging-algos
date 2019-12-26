'''
Created on 25 déc. 2019

@author: redZA
'''
from tkinter import *
from tkinter import IntVar,messagebox
from _overlapped import NULL
from random import randint
from time import sleep
import threading

#variables
window = Tk()
direction_list = [ ("left" , -1) ,("Right", 1)]
direction = IntVar(window, -1, "direction")
rb = NULL
length_ref_chain = 10
ref_chain = NULL
ref_index = 0
current_position = IntVar(window, 1, "current_position")
counter = IntVar(window, 0,"Counter") 

def inti_chain_ref():
    global length_ref_chain,ref_chain,ref_index
    i = 0 
    ref_index = 0
    counter.set(0)
    ref_chain = list()
    while(i < length_ref_chain):
        i =i +1
        ref_chain.append(randint(1,100))
                                         
def move_fifo_algo():
    global ref_chain,ref_index,current_position,direction,counter,listbox_ref
    val = ref_chain[ref_index]
    if(val > int(current_position.get())):
        #put direction
        direction.set(1)
        #update conter 
        counter.set(int(counter.get()) + (val - int(current_position.get())))
        #put head in the right position
        current_position.set(val)
        
    elif(val < int(current_position.get())):
        direction.set(-1)
        counter.set(int(counter.get()) +  (int(current_position.get() - val)))
        current_position.set(val)

        
    listbox_ref.itemconfig(ref_index, bg="green")
    
    entry_current_position.config(state="normal")
    entry_current_position.delete(0, END)
    entry_current_position.insert(0, str(current_position.get()))
    entry_current_position.config(state="disabled")
    ref_index = ref_index + 1  

def move_scan_algo_command():
    global current_position,length_ref_chain,ref_chain,listbox_ref,direction,ref_index
    i = ref_index
    #while(obj_found != length_ref_chain):
    while(i < length_ref_chain):
        if(int(current_position.get()) == int(ref_chain[i])):
            #obj_found = obj_found + 1
            listbox_ref.itemconfig(i, bg="red")               
        i = i + 1
    current_position.set(int(current_position.get()) + int(direction.get()))
    counter.set(int(counter.get()) + 1)
    if(int(current_position.get()) == 1):
        direction.set(1)
    elif(int(current_position.get()) == 100):
        direction.set(-1)
    
    entry_current_position.config(state="normal")
    entry_current_position.delete(0, END)
    entry_current_position.insert(0, str(current_position.get()))
    entry_current_position.config(state="disabled")

def init_reset_command():
    global length_ref_chain,entry_length_ref
    try:
        length_ref_chain = int(entry_length_ref.get())
    except Exception:
        messagebox.showerror("Error", "Lenght is not a integer")
        entry_length_ref.delete(0, END)
        entry_length_ref.insert(0, str(10))
        length_ref_chain = 10
        
    inti_chain_ref()
    update_listbox_ref()
def compare_all_command():
    global button_fifo,button_scan,button_rest_init,button_compare_all
    t = threading.Thread(target=compare_all_command_thread)
    t.start()
    button_fifo.config(state=DISABLED)
    button_scan.config(state=DISABLED)
    button_rest_init.config(state=DISABLED)
    button_compare_all.config(state=DISABLED)
def compare_all_command_thread():
    global current_position,length_ref_chain,ref_chain,direction,counter,label_info_scan,label_info_fifo,ref_index,button_fifo,button_scan,button_rest_init,button_compare_all
    try:
        e = int(current_position.get())
        t = int(counter.get())
        d = direction.get()
        #using SCAN
        obj_found = 0
        while(obj_found != length_ref_chain):
            i =0 
            while(i < length_ref_chain):
                if(int(current_position.get()) == int(ref_chain[i])):
                    obj_found = obj_found + 1
                    listbox_ref.itemconfig(i, bg="red")               
                i = i + 1
            current_position.set(int(current_position.get()) + int(direction.get()))
            counter.set(int(counter.get()) + 1)
            if(int(current_position.get()) == 1):
                direction.set(1)
            elif(int(current_position.get()) == 100):
                direction.set(-1)
            label_info_scan.config(text=str(counter.get()))
            label_info_scan.update_idletasks()
        current_position.set(e)
        counter.set(t)
        direction.set(d)
        
        for i in ref_chain:
            move_fifo_algo()
        label_info_fifo.config(text=str(counter.get()))
        label_info_fifo.update_idletasks()
        
        current_position.set(e)
        counter.set(t)
        direction.set(d)
        entry_current_position.config(state="normal")
        entry_current_position.delete(0, END)
        entry_current_position.insert(0, str(current_position.get()))
        entry_current_position.config(state="disabled")  
        ref_index = 0  
        update_listbox_ref()
    except Exception as r:
        print(r)
    button_fifo.config(state=NORMAL)
    button_scan.config(state=NORMAL)
    button_rest_init.config(state=NORMAL)
    button_compare_all.config(state=NORMAL)
def update_listbox_ref():
    global listbox_ref,ref_chain
    p=0
    listbox_ref.delete(0, END)
    for i in ref_chain:
        listbox_ref.insert(p, i)
        p = p+1

def update_current_position(value):
    global entry_current_position,current_position,direction,rb
    
    entry_current_position.config(state="normal")
    entry_current_position.delete(0, END)
    entry_current_position.insert(0, str(value))
    entry_current_position.config(state="disabled")
    if(int(value) == 100):
        #rb.select()
        direction.set(-1)
    elif(int(value) ==1):
        #rb.deselect()
        direction.set(1)  
             
#create graphicalinterfacae
window.config(width=640,height=480)
window.title("Device Mangement HDD")

#create all buttons
button_exit = Button(window,text="EXIT",command=exit)
button_exit.grid(row=0,column=5,padx=2,pady=2 ,sticky=N+E+W+S)
button_rest_init = Button(window,text="Init/ResetAll",command=init_reset_command)
button_rest_init.grid(row=1,column=5, padx=2,pady=2, sticky=N+S+E+W)

button_fifo = Button(window,text="Use FIFO",command=move_fifo_algo)
button_fifo.grid(row = 2,column=5,padx=2,pady=2,sticky=N+S+E+W)
button_scan = Button(window,text="Use SCAN",command=move_scan_algo_command)
button_scan.grid(row = 3,column=5,padx=2,pady=2,sticky=N+S+E+W)


button_compare_all = Button(window,text="CompareAll",command=compare_all_command)
button_compare_all.grid(row=9,column=5, padx=2,pady=2, sticky=N+S+E+W)

#Listbox 
listbox_ref = Listbox(window,height=20)
scrollbar = Scrollbar(window, orient="vertical",width=20)
scrollbar.config(command=listbox_ref.yview)

listbox_ref.grid(row = 1,column=0,padx=1,pady=17,rowspan=10,columnspan=2,sticky=N+S+E+W)
scrollbar.grid(row = 1,column=2,padx=2,pady=2,rowspan=10,sticky=N+S+E)

#labels
label6 = Label(window,text= "Reference chain")  .grid(row = 0, column = 0,columnspan=2,pady=10,sticky=N+S+E+W)
label0 = Label(window,text="Lenght of ref :")   .grid(row = 0, column = 3,sticky=N+S+E+W)
label1 = Label(window,text="Using Fifo :")      .grid(row = 2, column = 3,sticky=N+S+E+W)
label_info_fifo = Label(window,text="No information")      
label_info_fifo.grid(row = 2, column = 4,sticky=N+S+E+W)
label2 = Label(window,text="Using SCAN :")      .grid(row = 3, column = 3,sticky=N+S+E+W)
label_info_scan = Label(window,text="No information")      
label_info_scan.grid(row =3, column = 4,sticky=N+S+E+W)
label4 = Label(window,text="Current Position :").grid(row = 5, column = 3,sticky=N+S+E+W)
label5 = Label(window,text="Direction")              .grid(row = 6, column = 3,sticky=N+S+E+W)
counter_label = Label(window,textvariable=counter)  .grid(row = 6, column = 4,sticky=N+S+E+W)
#radio Button
for text, val in direction_list:
    rb = Radiobutton(window, text=text, variable= direction, value= val)
    if(val == 1):
        rb.grid(row = 7, column = 3,columnspan=1,sticky=N+S+W)
    else:
        rb.grid(row = 7, column = 3,columnspan=1,sticky=N+S+E)
    
    
#entrys
entry_length_ref  = Entry(window)
entry_length_ref.insert(0, str(10))
entry_length_ref.grid(row = 0, column = 4,padx=10,sticky=E+W)
entry_current_position = Entry(window)
entry_current_position.insert(0, str(current_position.get()))
entry_current_position.config(state="disabled")
entry_current_position.grid(row = 5, column = 4,padx=10,sticky=E+W)

#scale
scale = Scale(window,from_=1,to=100,resolution=1,orient=HORIZONTAL,
              label="Head Position",tickinterval=100,
              variable=current_position,command=update_current_position)
scale.grid(row = 12, column = 0,padx=10,pady=10,rowspan=3,columnspan=6,sticky=E+W)
window.mainloop()