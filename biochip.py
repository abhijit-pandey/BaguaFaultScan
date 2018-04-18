
# coding: utf-8

# In[123]:

import math


# In[124]:

class dmfb:
    def __init__(self,ctrl):
        self.control = ctrl
        self.defect  = False
        self.drop    = False


# In[137]:

#Initializing The Digital Microfluidic Bio-Chip
print('Enter the Number of Rows: ')
row = int(input())
print('Enter the Number of Columns: ')
col = int(input())
chip = []
ver = 0
activate_log = []
occur_ver = {'1' : 1, '3' : 2, '5' : 3, '2' : 4, '4' : 5}
occur_hor = {'1' : 1, '2' : 2, '3' : 3, '4' : 4, '5' : 5}
for i in range(row):
    hor = ver
    new = []
    for j in range(col):
        new.append(dmfb((hor%5)+1))
        hor += 1
    ver = (ver + 2)%5
    chip.append(new)
for i in range(row):
    for j in range(col):
        print(chip[i][j].control, end=" ")
    print()


# In[126]:

def make_defect(x, y):
    global chip
    chip[x-1][y-1].defect = True


# In[127]:

def clear_log():
    global activate_log
    activate_log = []


# In[128]:

def washout():
    global chip,row,col
    for i in range(row):
        for j in range(col):
            chip[i][j].drop = False


# In[129]:

def activate(pin):
    global chip,row,col,activate_log
    for i in range(row):
        for j in range(col):
            if(chip[i][j].control == pin):
                if(i!=0 and chip[i-1][j].drop):
                    chip[i-1][j].drop = False
                    if(not chip[i][j].defect):
                        chip[i][j].drop = True

                if(j!=0 and chip[i][j-1].drop):
                    chip[i][j-1].drop = False
                    if(not chip[i][j].defect):
                        chip[i][j].drop = True

                if(i!=row-1 and chip[i+1][j].drop):
                    chip[i+1][j].drop = False
                    if(not chip[i][j].defect):
                        chip[i][j].drop = True

                if(j!=col-1 and chip[i][j+1].drop):
                    chip[i][j+1].drop = False
                    if(not chip[i][j].defect):
                        chip[i][j].drop = True
    activate_log.append(pin)


# In[130]:

def releaseDrop():
    global chip
    chip[0][0].drop = True
    activate(1)


# In[131]:

def show():
    for i in range(row):
        for j in range(col):
            if(chip[i][j].drop):
                print(1, end=" ")
            else:
                print(0, end=" ")
        print()
def show_defect():
    for i in range(row):
        for j in range(col):
            if(chip[i][j].defect):
                print('X', end=" ")
            else:
                print(0, end=" ")
        print()


# In[132]:

def place_in_col(pin):
    global row,col,chip
    s = 1
    p = occur_ver[str(pin)]    
    n = math.floor(row/5)
    if((row%5)+1 > p):
        n +=1
    for _ in range(n-1):
        releaseDrop()
        for i in range(1,5):
            activate((s + 2*i - 1)%5 + 1)
    releaseDrop()
    for i in range(1,p):
        activate((s + 2*i - 1)%5 + 1)


# In[133]:

def place_in_row(pin):
    global row,col,chip
    s = 1
    p = occur_hor[str(pin)]    
    n = math.floor(col/5)
    if((col%5)+1 > p):
        n +=1
    for _ in range(n-1):
        releaseDrop()
        for i in range(1,5):
            activate((s + i - 1)%5 + 1)
    releaseDrop()
    for i in range(1,p):
        activate((s + i - 1)%5 + 1)


# In[134]:

def check_col(pin):
    global row, col, chip
    p = (pin +col-2)%5 + 1
    fault = []
    for i in range(row):
        if(chip[i][col-1].control == p):
            if(chip[i][col-1].drop == False):
                fault.append(i+1)
    return fault
def check_row(pin):
    global row, col, chip
    fault = []
    p = (pin + (row-1)*2 -1)%5 + 1
    for i in range(col):
        if(chip[row-1][i].control == p):
            if(chip[row-1][i].drop == False):
                fault.append(i+1)
    return fault


# In[138]:

print('Enter the Number of Defects: ')
k = int(input())
for _ in range(k):
    print('Enter row number for Defect: ')
    x = int(input())
    print('Enter column number for Defect: ')
    y = int(input())
    make_defect(x,y)
fr = []
fc = []
for pin in range(1,6):
    washout()
    place_in_col(pin)
    for i in range(1,col):
        activate((pin + i -1)%5 + 1)
    k = check_col(pin)
    for i in k:
        fr.append(i)
for pin in range(1,6):
    washout()
    place_in_row(pin)
    for i in range(1,row):
        activate((pin + 2*i -1)%5 + 1)
    k = check_row(pin)
    for i in k:
        fc.append(i)
print('Faulty Rows: '+str(fr))
print('Faulty Columns: '+str(fc))
print('Press Enter to Terminate ...')
input()


# In[136]:

len(activate_log)


# In[ ]:



