'''
Created on 18 déc. 2019

@author: redZA
'''
#import 
from tkinter import Tk,messagebox,Label,Button,Listbox,W,E,N,S,Entry,END,Scrollbar
from memory_page_functions_objects import *
import memory_page_functions_objects
#variables 
reference_chain_last_used_id = 0
def about_command():
    messagebox.showinfo("About", "Create by redza\napplication to simulate the algorithm for replacing pages in memory.")
    
def inti_reste_all_command(noUpdateRef = False):
    global label_FIFO_calls,label_LRU_calls,label_OPTIMAL_calls,ref,ram_size,ref_lim,max_pages_number,ram_table,ram_LRU,listbox_ram,listbox_ref,label_lref_call,reference_chain_last_used_id
    reference_chain_last_used_id = 0 
    memory_page_functions_objects.current_page = -1  #reset value for FIFO Algo
    #empty list box
    listbox_ram.delete(0, END)
    if(noUpdateRef == False):
        listbox_ref.delete(0, END)
    #label
    label_lref_call.config(text="None")
    label_lref_call.update_idletasks()
    #check and update walue from entry
    if(update_Values_From_Entry() == False):
        return 
    #init_ram and LRU
    if(noUpdateRef == False) :
        ref = create_ref_chain(ram_size ,ref_lim,max_pages_number,view=listbox_ref) 
        label_FIFO_calls.config(text="FIFO\nNo information")
        label_LRU_calls.config(text="LRU\nNo information")
        label_OPTIMAL_calls.config(text="OPTIMAL\nNo information")
        label_FIFO_calls.update_idletasks()
        label_LRU_calls.update_idletasks()
        label_OPTIMAL_calls.update_idletasks()
    [ram_table,ram_LRU] = create_ram_table(ram_size, ram_table,ram_LRU,view=listbox_ram)
    
    
def use_fifo_command():
    global reference_chain_last_used_id,ram_table,ram_LRU
    case = 0
    try:
        #use value in variable and list
        if(call_page(ram_table, ram_LRU, ram_size, ref[reference_chain_last_used_id]) != True):
            [ram_table,ram_LRU,case] = def_page_fifo(ram_table,ram_LRU,ram_size,ref[reference_chain_last_used_id])
            messagebox.showinfo("Page infromation - FIFO ALGO", "Page %s is not in memory\nPage %s load in case %s"%
                                (ref[reference_chain_last_used_id],ref[reference_chain_last_used_id],case))
        else:
            messagebox.showinfo("Page infromation", "Page %s is in memory, no need to load"%(ref[reference_chain_last_used_id]))        
        #update the interface
        update_last_ref_selected(reference_chain_last_used_id)
        update_memory_listbox(case)
        reference_chain_last_used_id = reference_chain_last_used_id + 1 
    except Exception as e :
        messagebox.showerror("Error", "Empty, you need to inti the memory and reference chain\nPress \"Init/Reset All\" %s"%(e))

def use_lru_command():
    global reference_chain_last_used_id,ram_table,ram_LRU
    case = 0
    try:
        #use value in variable and list
        if(call_page(ram_table, ram_LRU, ram_size, ref[reference_chain_last_used_id]) != True):
            [ram_table,ram_LRU,case] = def_page_LRU(ram_table,ram_LRU,ram_size,ref[reference_chain_last_used_id])
            messagebox.showinfo("Page infromation - LRU ALGO", "Page %s is not in memory\nPage %s load in case %s"%
                                (ref[reference_chain_last_used_id],ref[reference_chain_last_used_id],case))
        else:
            messagebox.showinfo("Page infromation", "Page %s is in memory, no need to load"%(ref[reference_chain_last_used_id]))        
        #update the interface
        update_last_ref_selected(reference_chain_last_used_id)
        update_memory_listbox(case)
        reference_chain_last_used_id = reference_chain_last_used_id + 1 
    except Exception as e :
        messagebox.showerror("Error", "Empty, you need to inti the memory and reference chain\nPress \"Init/Reset All\" %s"%(e))
          
def use_optimal_command():
    global reference_chain_last_used_id,ram_table,ram_LRU
    case = 0
    try:
        #use value in variable and list
        if(call_page(ram_table, ram_LRU, ram_size, ref[reference_chain_last_used_id]) != True):
            [ram_table,ram_LRU,case] = def_page_optimal(ram_table, ram_LRU, ram_size, ref[reference_chain_last_used_id], reference_chain_last_used_id,ref,ref_lim)
            messagebox.showinfo("Page infromation - OPTIMAL ALGO", "Page %s is not in memory\nPage %s load in case %s"%
                                (ref[reference_chain_last_used_id],ref[reference_chain_last_used_id],case))
        else:
            messagebox.showinfo("Page infromation", "Page %s is in memory, no need to load"%(ref[reference_chain_last_used_id]))        
        #update the interface
        update_last_ref_selected(reference_chain_last_used_id)
        update_memory_listbox(case)
        reference_chain_last_used_id = reference_chain_last_used_id + 1 
    except Exception as e :
        messagebox.showerror("Error", "Empty, you need to inti the memory and reference chain\nPress \"Init/Reset All\" %s"%(e))

def compare_all_command():
    global ram_table,   ram_LRU,   ref,  ram_size
    label_FIFO_calls.config(text="FIFO\n waiting ...etc")
    label_LRU_calls.config(text="LRU\n waiting ...etc")
    label_OPTIMAL_calls.config(text="OPTIMAL\n waiting ...etc")
    label_FIFO_calls.update_idletasks()
    label_LRU_calls.update_idletasks()
    label_OPTIMAL_calls.update_idletasks()
    try:
        #FIFO
        nbr_of_dp = 0
        for i in ref:
            if(call_page(ram_table, ram_LRU, ram_size, i) != True):
                [ram_table,ram_LRU,case] = def_page_fifo(ram_table,ram_LRU,ram_size,i)
                nbr_of_dp = nbr_of_dp + 1 
        label_FIFO_calls.config(text="FIFO\nDF : %s"%(str(nbr_of_dp)))
        label_FIFO_calls.update_idletasks()
        
        [ram_table,ram_LRU] = create_ram_table(ram_size, ram_table,ram_LRU)
        nbr_of_dp = 0 
        for i in ref:
            if(call_page(ram_table, ram_LRU, ram_size, i) != True):
                [ram_table,ram_LRU,case] = def_page_LRU(ram_table,ram_LRU,ram_size,i)
                nbr_of_dp = nbr_of_dp + 1
        label_LRU_calls.config(text="LRU\nDF : %s"%(str(nbr_of_dp)))
        label_LRU_calls.update_idletasks()
        
        [ram_table,ram_LRU] = create_ram_table(ram_size, ram_table,ram_LRU)
        nbr_of_dp = 0 
        i = 0
        while(i < ref_lim):
            if(call_page(ram_table, ram_LRU, ram_size, ref[i]) != True):
                [ram_table,ram_LRU,case] = def_page_optimal(ram_table, ram_LRU, ram_size, ref[i], i,ref,ref_lim)
                nbr_of_dp = nbr_of_dp + 1
            i = i + 1     
        label_OPTIMAL_calls.config(text="OPTIMAL\nDF : %s"%(str(nbr_of_dp)))
        label_OPTIMAL_calls.update_idletasks()
        
        inti_reste_all_command(noUpdateRef=True)
        [ram_table,ram_LRU] = create_ram_table(ram_size, ram_table,ram_LRU)
        update_memory_listbox()
    except Exception as a:
        messagebox.showerror("Error", "Use Init/Reset All\nError: %s"%(a))
        label_FIFO_calls.config(text="FIFO\nERROR")
        label_LRU_calls.config(text="LRU\nERROR")
        label_OPTIMAL_calls.config(text="OPTIMAL\n ERROR")
        label_FIFO_calls.update_idletasks()
        label_LRU_calls.update_idletasks()
        label_OPTIMAL_calls.update_idletasks()
        
          
def update_last_ref_selected(i):
    global label_lref_call,ref,listbox_ref
    label_lref_call.config(text=str(ref[i]))
    label_lref_call.update_idletasks()
    listbox_ref.itemconfig(i, bg="green")
    
def update_memory_listbox(case = -1):
    global listbox_ram,ram_size,ram_table,ref,reference_chain_last_used_id
    i = 0
    listbox_ram.delete(0, END)
    while(i< ram_size):
        if(ram_table[i] == -1):
            listbox_ram.insert(i,"%s : Empty:\t\t%s"%(str(i),str(bin(ram_LRU[i]))))
        else:
            listbox_ram.insert(i,"%s : %s:\t\t%s"%(str(i),str(ram_table[i]),str(bin(ram_LRU[i]))))
        i = i + 1
    if(case != -1):
        listbox_ram.itemconfig(case, bg="red")
def intit_values_entry():
    global entry_nbr_pages,entry_ref_size,entry_memory_size,ram_size,ref_lim,max_pages_number
    entry_memory_size.insert(0,str(ram_size))
    entry_nbr_pages.insert(0,str(max_pages_number))
    entry_ref_size.insert(0,str(ref_lim))
    
def update_Values_From_Entry():
    global entry_nbr_pages,entry_ref_size,entry_memory_size,ram_size,ref_lim,max_pages_number
    try:
        ram_size = int(entry_memory_size.get())
        ref_lim = int(entry_ref_size.get())
        max_pages_number = int(entry_nbr_pages.get())
    except ValueError:
        messagebox.showerror("Error", "Value entry is not a entier")
        return False
    except Exception as e:
        messagebox.showerror("Error","Error : %s"%(e))
        return False
    return True
#creating window
window = Tk()
window.config(width=480,height=800)
window.title("Change Page in memory")
#create all object 
button_fifo = Button(window,text="Use FIFO Algo",command=use_fifo_command)
button_fifo.grid(column = 2,row = 1,padx=1,pady=2,sticky=W+E+N+S)
button_lru = Button(window,text="Use LRU Algo",command=use_lru_command)
button_lru.grid(column = 2,row = 2,padx=1,pady=2,sticky=W+E+N+S)
button_optimal = Button(window,text="Use Optimal Algo",command=use_optimal_command)
button_optimal.grid(column = 2,row = 3,padx=1,pady=2,sticky=W+E+N+S)
button_reset = Button(window,text="Init/Reset All",command=inti_reste_all_command)
button_reset.grid(column = 2,row = 4,padx=1,pady=2,sticky=W+E+N+S)
button_compare = Button(window,text="Compare All",command=compare_all_command)
button_compare.grid(column = 2,row = 5,padx=1,pady=2,sticky=W+E+N+S)
button_ok = Button(window,text="About",command=about_command)
button_ok.grid(column=1,row=15,padx=2,pady=2,sticky=W+E+N+S)
button_exit = Button(window,text="EXIT",command=exit)
button_exit.grid(column=2,row=15,padx=2,pady=2,sticky=W+E+N+S)

listbox_ram = Listbox(window,height=20)
listbox_ram.grid(column = 0,row = 1,padx=17,pady=17,rowspan=7,sticky=N)
listbox_ref = Listbox(window,height=20)
listbox_ref.grid(column = 1,row = 1,padx=17,pady=0,rowspan=7)

scrollbar = Scrollbar(window, orient="vertical")
scrollbar.config(command=listbox_ram.yview)
scrollbar.grid(column = 0,row = 1,padx=0,pady=5,rowspan=7,sticky=N+S+E)
listbox_ram.config(yscrollcommand=scrollbar.set)

scrollbar0 = Scrollbar(window, orient="horizontal")
scrollbar0.config(command=listbox_ram.xview)
scrollbar0.grid(column = 0,row = 1,padx=17,pady=0,rowspan=7,sticky=W+S+E)
listbox_ram.config(xscrollcommand=scrollbar0.set)

scrollbar1 = Scrollbar(window, orient="vertical")
scrollbar1.config(command=listbox_ref.yview)
scrollbar1.grid(column = 1,row = 1,padx=0,pady=0,rowspan=7,sticky=N+S+E)
listbox_ref.config(yscrollcommand=scrollbar1.set)

lab1 = Label(window,text="Memory").grid(column = 0,row = 0,padx=10,pady=10)
lab2 = Label(window,text="Reference chain").grid(column = 1,row = 0,padx=10,pady=10)
lab3 = Label(window,text="Last Ref Called").grid(column = 0,row = 8,padx=10,pady=10,sticky = W+E+N+S)
lab4 = Label(window,text="Nombre of pages").grid(column = 0,row = 9,padx=10,pady=10,sticky=W+E+N+S)
lab5 = Label(window,text="Reference chain Size").grid(column = 0,row = 10,padx=10,pady=10,sticky=W+E+N+S)
lab6 = Label(window,text="Memory size (page)").grid(column=0,row =11 ,padx=10,pady=10,sticky=W+E+N+S)
label_lref_call = Label(window,text="None")
label_lref_call.grid(column = 1,row = 8,padx = 2,pady=2,sticky = W+E+N+S)
label_FIFO_calls = Label(window,text="FIFO\nno informations")
label_FIFO_calls.grid(column = 2,row = 6,padx = 2,pady=2,sticky = W+E+N+S)
label_LRU_calls = Label(window,text="LRU\nno informations")
label_LRU_calls.grid(column = 2,row = 7,padx = 2,pady=2,sticky = W+E+N+S)
label_OPTIMAL_calls = Label(window,text="OPTIMAL\nno informations")
label_OPTIMAL_calls.grid(column = 2,row = 8,padx = 2,pady=2,sticky = W+E+N+S)

entry_nbr_pages = Entry(window)
entry_nbr_pages.grid(column=1,row=9,padx=2,pady=2,sticky= W+E)
entry_ref_size = Entry(window)
entry_ref_size.grid(column=1,row=10,padx=2,pady=2,sticky= W+E)
entry_memory_size = Entry(window)
entry_memory_size.grid(column=1,row=11,padx=2,pady=2,sticky= W+E)

#inti_value 
intit_values_entry()
window.mainloop()
