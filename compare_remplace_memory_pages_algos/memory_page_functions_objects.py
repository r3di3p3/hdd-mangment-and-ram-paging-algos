'''
Created on 18 déc. 2019

@author: redZA
'''
from random import randint
from _overlapped import NULL

#variables
ram_table = NULL
ram_LRU = list() #[LRU]
ram_size = 8  # the number of pages in RAM
ref = list()
ref_lim = 10 # the size of referce list
max_pages_number = 16

current_page = -1 # the last case memory (page) load it [FIFO]
'''
HELP
RAM 
[-1,-1,-1,-1,...] the value incase is for the page
RAM_LRU
[0,0,....] value of used least recently used
'''

'''
    Function to create table for RAM_TABLEand RAM_LRU 
    LRU : Last recent used 
    in : int size_ram, ram_table table type int, ram_lru type bool
    out :   ram_table
            ram_LRU
'''
def create_ram_table(size,ram_table,ram_LRU,view = NULL):
    i=0
    ram_table = list()
    while(i< size):
        ram_table.insert(i, -1)
        ram_LRU.insert(i,0)
        if(view != NULL):
            view.insert(i,"%s : Empty :\t\t%s"%(str(i),str(bin(0))))
        i = i +1
    return ram_table,ram_LRU

'''
    Create random calls for the page 
    in : ram_size
    out : ref_table (table)
'''
def create_ref_chain(ram_size,ref_lim,max_pages_number,view = NULL):
    i = 0
    ref = list()
    while(i < ref_lim):
        ref.append(randint(0,max_pages_number))
        if(view != NULL):
            view.insert(i,str(ref[i]))
        i = i + 1 
    return ref

'''
    This function will search in ram_table for "page_call"
    if it's found return True
    if not return False
    IN :    ram_table (memory)
            ram_LRU : lRUvalue for each memory page
            ram_size : memmory size
            page_call : the id of the page called
    OUT : bool isCharged
'''
def call_page(ram_table,ram_LRU,ram_size,page_call):    
    i =0
    isFound = False
    while(i < ram_size):
        if(ram_table[i] == page_call):
            #update the LRU value
            isFound = True
            ram_LRU[i] = ram_LRU[i] >> 1
            ram_LRU[i] =ram_LRU[i] | 0x100000000000000000000000
        else:
            #update the LRU value
            ram_LRU[i] = ram_LRU[i] >> 1
        i = i +1
    return isFound
'''
    Function to load page_call to the memory, using Fifo to load the page
    IN :    ram_table (memory)
        ram_LRU : lRUvalue for each memory page
        ram_size : memmory size
        page_call : the id of the page called
    OUT : ram_table
            ram_LRU
            current_page : the index of the memory
'''
def def_page_fifo(ram_table,ram_LRU,ram_size,page_call):
    global current_page
    current_page = (current_page+1) % ram_size
    ram_table[current_page] = page_call
    return ram_table,ram_LRU,current_page

'''
    Function to load page_call to the memory, it's use Least Recent used algo to load the page
    IN :    ram_table table represents all areas of pages in memory
            ram_LRU : array represents the history byte values of each memory page
            ram_size : the number of page in memory 
            page_call : number of page to load
    OUT :   ram_table all case of RAM | 
            ram_LRU : byte for evrey page storie | 
            toDelete :The @ of the case RAM 
'''
def def_page_LRU(ram_table,ram_LRU,ram_size,page_call):
    i = 0
    toDelete = 0 
    #search for the LRU page
    while(i < ram_size):
        ram_LRU[i] = ram_LRU[i] >> 1
        if(i == 0 & toDelete == 0):
            if((ram_LRU[toDelete] << 1) > ram_LRU[i]):
                toDelete = i
        else:
            if((ram_LRU[toDelete] << 1) > ram_LRU[i]):
                toDelete = i
        #shift for the LRU value for the case
        ram_LRU[i] = ram_LRU[i] >> 1 
        i = i + 1
    #load the page 
    ram_table[toDelete] = page_call
    #restart LRU value of this case 
    ram_LRU[toDelete]  = ram_LRU[toDelete] | 0x100000000000000000000000         
    return ram_table,ram_LRU,toDelete

'''
    Function to load page_call to the memory, it's use Opitmal to load the page
    IN :    ram_table table represents all areas of pages in memory
            ram_LRU : array represents the history byte values of each memory page
            ram_size : the number of page in memory 
            page_call : number of page to load
    OUT :   ram_table all case of RAM | 
            ram_LRU : byte for evrey page storie | 
            toDelete :The @ of the case RAM 
'''
def def_page_optimal(ram_table,ram_LRU,ram_size,page_call,ref_id,ref,ref_lim):
    i = 0 
    #search for empty cas in memory
    while(i< ram_size):
        if(ram_table[i] == -1):
            ram_table[i] = page_call
            return ram_table,ram_LRU,i
        i = i+1
    i = 0 
    #anlyse all refrence table
    index_page_toDelete = 0 
    nbr_call_max = 0
    while(i< ram_size):
        tmp_nbr_call = 0
        p = ref_id
        while(p < ref_lim):
            tmp_nbr_call = tmp_nbr_call + 1 
            if(ref[p] == ram_table[i]):
                break
            p = p + 1   
        if(tmp_nbr_call > nbr_call_max):
            nbr_call_max = tmp_nbr_call
            index_page_toDelete = i 
        i = i + 1
    ram_table[index_page_toDelete] = page_call
    #print("calls : ",nbr_call_max)
    return ram_table,ram_LRU,index_page_toDelete
     
def main_fifo():
    global ref_lim,ram_table,page_actuel,ram_LRU
    print("[+] Creation de table ram ")
    [ram_table,ram_LRU] = create_ram_table(ram_size, ram_table,ram_LRU)
    print(ram_table)
    print("[+] creation de la chaine de ref")
    ref = create_ref_chain(ram_size ,ref_lim)
    print(ref)
    print("[+] Fifo")
    for i in ref:
        print("\n")
        if(call_page(ram_table, ram_LRU, ram_size, i) != True):
            print("[-] Page not found in RAM, load it now ...")
            [ram_table,ram_LRU,case] = def_page_fifo(ram_table,ram_LRU,ram_size,i)
            print("Page %s charged in case %s"%(i,case))
        else:
            print("[+] Page found in RAM")   
        print("[+] RAM memory")
        print(ram_table)
        
def main_lru():
    global ref_lim,ram_table,page_actuel,ram_LRU,ref
    case = 0
    print("[+] Creation de table ram ")
    [ram_table,ram_LRU] = create_ram_table(ram_size, ram_table,ram_LRU)
    print(ram_table)
    print("[+] creation de la chaine de ref")
    ref = create_ref_chain(ram_size ,ref_lim)
    print(ref)
    print("[+] start CAll ref")
    for i in ref:
        print("\n\n")
        if(call_page(ram_table, ram_LRU, ram_size, i) != True):
            print("[-] Page not found in RAM, load it now ...")
            [ram_table,ram_LRU,case] = def_page_LRU(ram_table,ram_LRU,ram_size,i)
            print("Page %s charged in case %s"%(i,case))
        else:
            print("[+] Page found in RAM")   
        print("[+] RAM memory")
        print(ram_table)
        
def main_optimal():
    global ref_lim,ram_table,page_actuel,ram_LRU,ref,max_pages_number
    case = 0
    o = 0
    print("[+] Creation de table ram ")
    [ram_table,ram_LRU] = create_ram_table(ram_size, ram_table,ram_LRU)
    print(ram_table)
    print("[+] creation de la chaine de ref")
    ref = create_ref_chain(ram_size ,ref_lim,max_pages_number)
    print(ref)
    print("[+] start CAll ref")
    i = 0
    while(i < ref_lim):
        print("\nCall page %s"%(i))
        if(call_page(ram_table, ram_LRU, ram_size, ref[i]) != True):
            print("[-] Page not found in RAM, load it now ...")
            [ram_table,ram_LRU,case] = def_page_optimal(ram_table, ram_LRU, ram_size, ref[i], i)
            print("Page %s charged in case %s"%(ref[i],case))
            o = o+1
        else:
            print("[+] Page found in RAM")  
        
        print("[+] RAM memory")
        print(ram_table)
        i = i + 1 

'''
nbr_of_dp = 0

print("[+] creation de la chaine de ref")
ref = create_ref_chain(ram_size ,ref_lim,max_pages_number)
print(ref)
print("[+] Creation de table ram ")
[ram_table,ram_LRU] = create_ram_table(ram_size, ram_table,ram_LRU)
print(ram_table)
print("[+] START simulation using FIFO")
print("[+] Fifo")
for i in ref:
    #print("")
    if(call_page(ram_table, ram_LRU, ram_size, i) != True):
        #print("[-] Page not found in RAM, load it now ...")
        [ram_table,ram_LRU,case] = def_page_fifo(ram_table,ram_LRU,ram_size,i)
        #print("Page %s charged in case %s"%(i,case))
        nbr_of_dp = nbr_of_dp + 1 
    #else:
        #print("[+] Page found in RAM")
print("[+] *************************************************** FIFO %s"%(nbr_of_dp))
print("[+] Creation de table ram ")
[ram_table,ram_LRU] = create_ram_table(ram_size, ram_table,ram_LRU)
print(ram_table)
print("[+] START simulation using LRU")
print("[+] LRU")
nbr_of_dp = 0 
for i in ref:
    #print("")
    if(call_page(ram_table, ram_LRU, ram_size, i) != True):
        #print("[-] Page not found in RAM, load it now ...")
        [ram_table,ram_LRU,case] = def_page_LRU(ram_table,ram_LRU,ram_size,i)
        #print("Page %s charged in case %s"%(i,case))
        nbr_of_dp = nbr_of_dp + 1
    #else:
        #print("[+] Page found in RAM") 
print("[+] *************************************************** LRU %s"%(nbr_of_dp))
print("[+] Creation de table ram ")
[ram_table,ram_LRU] = create_ram_table(ram_size, ram_table,ram_LRU)
print(ram_table)
nbr_of_dp = 0 
print("[+] START simulation using Optimal")
print("[+] optimal")
i = 0
while(i < ref_lim):
    #print("")
    if(call_page(ram_table, ram_LRU, ram_size, ref[i]) != True):
        #print("[-] Page not found in RAM, load it now ...")
        [ram_table,ram_LRU,case] = def_page_optimal(ram_table, ram_LRU, ram_size, ref[i], i)
        #print("Page %s charged in case %s"%(ref[i],case))
        nbr_of_dp = nbr_of_dp + 1
    #else:
        #print("[+] Page found in RAM")   
    i = i + 1
print("[+] *************************************************** optimal %s"%(nbr_of_dp))  
'''  