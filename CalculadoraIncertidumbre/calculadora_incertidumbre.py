"""
@author: Tony Santiago Montes Buitrago
@doc:
    Este programa permite con facilidad calcular incertidumbres de cantidades
    y sus valores.

"""
from time import localtime
historialPath = './historial.txt'

def saveHistorial(vs:dict, psb):
	with open(historialPath,'a') as file:
		message = "\nENTRY %s/%s/%s - %s:%s:%s\n"%tuple([i for i in localtime()[:6]])
		message += f"\tVars:\n"
		for k,v in vs.items():
			message += f"\t\t'{k}':{v}\n"
		message += f"\tExpression:\n\t\t'{operation.get()}'\n"
		if isinstance(psb, Exception): 
			message += f"\t{psb.__class__} raised:\n"
			message += f"\t\t{psb}"
		else:
			message += f"\tResult:\n"
			message += f"\t\t{psb}\n"
		file.write(message)

def advise(*msgs, **printopts):
    print("WARN:", *msgs, **printopts)

class UnitError(Exception):
    pass

def sqrt(x):
    return x**(1/2)

def evalUnit(unit, torepr=False):
    return unit

def unite(tp,u1,u2):
    if tp in ("ADDITION", "SUBSTRACTION"):
        if u1 == u2:
            un = u1
        else:
            raise UnitError("For the operation + and - the units of operands"+
                            f" must be equal. ({u1} ≠ {u2})")
    elif tp == ("DIVISION"):
        if u1 == u2:
            un = ""
        elif u1 == "":
            un = f"({u2})^(-1)"
        elif u2 == "":
            un = u1
        else:
            un = f"({u1})/({u2})"
            un = evalUnit(un)
    elif tp == ("PRODUCT"):
        if u1 == u2 and u1 == "":
            un = ""
        elif u1 == "":
            un = u2
        elif u2 == "":
            un = u1
        elif u1 == u2:
            un = f"({u1})^2"
        else:
            un = f"({u1})*({u2})"
            un = evalUnit(un)
    elif tp == ("POW"):
        if u1:
            if u2 == 0:
                un = ""
            elif u2 == 1:
                un = u1
            else:
                un = f"({u1})^{u2}"
        else:
            un = ""
    return un

def incert(tp,x,y,ox,oy):    
    if tp in ("ADDITION", "SUBSTRACTION"):
        calc = sqrt((ox)**2 + (oy)**2)
    
    elif tp == ("DIVISION"):
        try:
            calc = (x/y)*(sqrt((ox/x)**2 + (oy/y)**2))
        except ZeroDivisionError:
            calc = 0
    elif tp == ("PRODUCT"):
        try:
            calc = (x*y)*(sqrt((ox/x)**2 + (oy/y)**2))
        except:
            calc = 0
    elif tp == ("POW"):
        try:
            calc = (abs(y)*(x**(y-1))*ox)
        except:
            calc = 0
    return calc

"""Number with uncertainty and units"""

class N():
    __doc__ = """Class N defines a number with its uncertainty and unit.
The operators +, -, *, /, ** are defined between elements N, int and float.
"""
    
    def __init__(self, value, uncert=0, unit=""):
        if type(value) in (int, float):
            self.n = value
        else:
            raise TypeError("Value type must be a real number.")
        
        if type(uncert) in (int,float):
            self.i = uncert
        else:
            raise TypeError("Uncertainty type must be a real number.")
        
        if type(unit) is str:
            self.unit = evalUnit(unit)
        else:
            raise TypeError("Unit must be a str.")
    
    def __add__(self, sValue):
        tp = "ADDITION"
        
        x = self.n
        ox = self.i
        u1 = self.unit
        
        if type(sValue) is N:    
            y = sValue.n
            oy = sValue.i    
            u2 = sValue.unit
        elif type(sValue) in (int,float):
            y = sValue
            oy = 0
            u2 = ""
        else:
            raise TypeError("Not stated operation + for types: "+
                            f"(N) and ({sValue.__class__.__name__})")
        
        return N(x+y, incert(tp,x,y,ox,oy), unite(tp,u1,u2))
    
    def __sub__(self, sValue):
        tp = "SUBSTRACTION"
        
        x = self.n
        ox = self.i
        u1 = self.unit
        
        if type(sValue) is N:    
            y = sValue.n
            oy = sValue.i    
            u2 = sValue.unit
        elif type(sValue) in (int,float):
            y = sValue
            oy = 0
            u2 = ""
        else:
            raise TypeError("Not stated operation - for types: "+
                            f"(N) and ({sValue.__class__.__name__})")
        
        return N(x-y, incert(tp,x,y,ox,oy), unite(tp,u1,u2))
    
    def __truediv__(self, sValue):
        tp = "DIVISION"
        
        x = self.n
        ox = self.i
        u1 = self.unit
        
        if type(sValue) is N:    
            y = sValue.n
            oy = sValue.i    
            u2 = sValue.unit
        elif type(sValue) in (int,float):
            y = sValue
            oy = 0
            u2 = ""
        else:
            raise TypeError("Not stated operation / for types: "+
                            f"(N) and ({sValue.__class__.__name__})")
                
        return N(x/y, incert(tp,x,y,ox,oy), unite(tp,u1,u2))
    
    def __mul__(self, sValue):
        tp = "PRODUCT"
        
        x = self.n
        ox = self.i
        u1 = self.unit
        
        if type(sValue) is N:    
            y = sValue.n
            oy = sValue.i   
            u2 = sValue.unit
        elif type(sValue) in (int,float):
            y = sValue
            oy = 0
            u2 = ""
        else:
            raise TypeError("Not stated operation * for types: "+
                            f"(N) and ({sValue.__class__.__name__})")
        
        return N(x*y, incert(tp,x,y,ox,oy), unite(tp,u1,u2))
    
    def __pow__(self, n):
        
        tp = "POW"
        
        x = self.n
        ox = self.i
        u1 = self.unit
        
        if type(n) is N:    
            y = n.n
            oy = 0   
        elif type(n) in (int,float):
            y = n
            oy = 0
        else:
            raise TypeError("Not stated operation ** for types: "+
                            f"(N) and ({n.__class__.__name__})")
        
        u2 = y if (n*10)%10 else int(y)
        
        return N(x**y, incert(tp,x,y,ox,oy), unite(tp,u1,u2))
    
    def __repr__(self, rounder=0):
	    if rounder:    
	        if self.unit:
	            return "(%s ± %s)[%s]"%(round(self.n,rounder),round(self.i,rounder),
	                              evalUnit(self.unit, True))
	        else:
	            return "(%s ± %s)"%(round(self.n,rounder),round(self.i,rounder))
	    else:
	        if self.unit:
	            return "(%s ± %s)[%s]"%(self.n,self.i,
	                              evalUnit(self.unit, True))
	        else:
	            return "(%s ± %s)"%(self.n,self.i)


"""Graphic Interface"""

import tkinter as tk
from functools import partial

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', **kwentryargs):
        super().__init__(master, **kwentryargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        
        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self.bind("<Key>", self.foc_in)
        
        self.isput = False
        
    def put_placeholder(self, *args):
        self.delete('0', 'end')
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color
        self.isput = True

    def quit_placeholder(self, *args):
        self.delete('0', 'end')
        self['fg'] = self.default_fg_color
        self.isput = False
    
    def foc_in(self, *args):
        if self.isput:
            self.quit_placeholder()

    def foc_out(self, *args):
        if not self.isput:
            if not self.get():
                self.put_placeholder()
                
    def grid(self, **kwargs):
        self.put_placeholder()
        super().grid(**kwargs)

def quitNum(idx):
    global nums
    
    for row in range(len(nums)):
        if nums[row][0] == idx:
            for j in nums[row][1]:
                j.destroy()
            del nums[row]
            break

def addNum(vals=('','','','')):
    global nums
    global idcount
    
    thing = [
        tk.Entry(mainFrame, font=('Bookman Old Style',10), justify='center', fg='red'),     # Var Name
        tk.Entry(mainFrame, font=('Bookman Old Style',10), justify='center'),               # Number
        tk.Entry(mainFrame, font=('Bookman Old Style',10), justify='center'),               # Uncertainty
        tk.Entry(mainFrame, font=('Bookman Old Style',10), justify='center', text=vals[3]), # Unit
        tk.Button(mainFrame, text='-', command=partial(quitNum, idcount)),                  # QuitButton
        tk.Label(mainFrame, font=('Bookman Old Style',10), text='', fg='red')               # LabelAlert
        ]
    
    for j in range(len(vals)):
        thing[j].insert(0,vals[j])
    
    for j in range(len(thing)):
        thing[j].grid(row=idcount+1, column=j)
    
    nums.append((idcount, thing))
    idcount += 1
    
def verifyNumber(num) -> bool:
    """
    True: Valid number
    False: Not a number
    """
    try:
        vl = eval(num)
    except:
        return False
    
    if type(vl) in (int, float):
        return True
    else:
        return False

def verifyName(name) -> bool:
    """
    True: Valid name
    False: Not a valid identifier
    """
    if name[0].isdigit():
        return False
    
    for i in name:
        if 48 > ord(i) > 57:
            if 65 > ord(i) > 90:
                if 97 > ord(i) > 122:
                    return False
    return True
    
def operateCMD():
    global nums
    vrLT = {}
    Ndoable = False
    for i in range(len(nums)):
        actualErr = ''
        
        name = nums[i][1][0].get()
        num = nums[i][1][1].get()
        unc = nums[i][1][2].get()
        unt = nums[i][1][3].get()
        if not(name or num or unc or unt):
            nums[i][1][len(nums[i][1])-1].config(text='')
            continue # ignore
        
        if name:
            if not verifyName(name):
                actualErr = (f"Invalid name '{name}'")
        else:
            actualErr = ("Name cannot be empty")
        
        if num:
            if not verifyNumber(num):
                actualErr = ("Number is not a number")
            else:
                num = float(num)
        else:
            actualErr = ("Number cannot be empty")
        
        if unc:
            if not verifyNumber(unc):
                actualErr = ("Uncertainty is not a number")
            else:
                unc = float(unc)
        else:
            unc = 0.0
        
        if actualErr:
            Ndoable = True
            nums[i][1][len(nums[i][1])-1].config(fg='red', text=actualErr)
        else:
            inN = N(num, unc, unt)
            vrLT[name] = inN
            nums[i][1][len(nums[i][1])-1].config(fg='black', text=f"{name} = {inN}")
        
    if Ndoable:
    	return

    try:
        rs = eval(operation.get().replace('^', '**'), vrLT.copy())
        result.config(fg='black', text=rs)
        try:
        	saveHistorial(vrLT, rs)
        except:
        	pass
    except Exception as e:
        result.config(fg='red', text=e.args[0])
        result.grid(row=2, column=1, columnspan=3)
        try:
        	saveHistorial(vrLT, e)
        except:
        	pass
        return 
    operation.placeholder = ''
    result.grid(row=2, column=1, columnspan=3)
    addResult.grid(row=1, column=4, rowspan=2)
    addResult.config(command=partial(buttonAddResult,rs))

def clearCMD():
    global operation, result, nums
    operation.delete('0','end')
    operation.placeholder = ''
    result.config(fg='black', text='')
    addResult.grid_forget()
    for i in nums:
        for j in i[1][:-2]:
            j.delete('0','end')
        i[1][-1].config(fg='black', text='')

def buttonAddResult(resultVar):
    newr = tk.Tk()
    newr.title("Add Var")

    tk.Label(newr, font=('Bookman Old Style',10), text="Add result as var", justify='center').grid(row=0)
    tk.Label(newr, font=('Bookman Old Style',10), text=str(resultVar), justify='center', bg='orange').grid(row=1)
    tk.Label(newr, font=('Bookman Old Style',10), text="Digit the name", justify='center').grid(row=2)
    entName = tk.Entry(newr, font=('Bookman Old Style',10), justify='center')
    entName.grid(row=3)
    alLab = tk.Label(newr, font=('Bookman Old Style',10), justify='center', text='', fg='red')
    alLab.grid(row=5)
    tk.Button(newr, font=('Bookman Old Style',10), text="Add", command=partial(
    	addResultAsVar, entName, alLab, resultVar)).grid(row=4)


def addResultAsVar(entry, alert, nVar):
    if entry.get():
        if verifyName(entry.get()):
            if type(nVar) is N:
            	addNum((entry.get(), nVar.n, nVar.i, nVar.unit))
            else:
                addNum((entry.get(), nVar, '0', ''))
            result.grid_forget()
            addResult.grid_forget()
            alert.master.destroy()
        else:
            alert.config(text=f"'{entry.get()}' is not a valid name")
    else:
        alert.config(text="Enter name to continue")

root = tk.Tk()
root.title("Uncertainty Calculator")
mainFrame = tk.Frame(root)
downFrame = tk.Frame(root)

mainFrame.pack()
downFrame.pack()

tk.Label(mainFrame, text="Var Name").grid(row=0, column=0)
tk.Label(mainFrame, text="Number").grid(row=0, column=1)
tk.Label(mainFrame, text="Uncertainty").grid(row=0, column=2)
tk.Label(mainFrame, text="Unit").grid(row=0, column=3)

idcount = 0
nums = []

tk.Button(downFrame, text="Operate", font=('',10,'bold'), fg='blue',
                    command=operateCMD).grid(row=0, column=4, padx=30)
tk.Button(downFrame, text="Clear", font=('',10,'bold'), fg='orange',
                    command=clearCMD).grid(row=0, column=0, padx=30)
tk.Button(downFrame, text='+', command=addNum).grid(row=0, column=5)

operation = EntryWithPlaceholder(downFrame, "a*(t^2)", bd=2, 
                font=('Bookman Old Style',10), justify='center', width=50)
operation.grid(row=0, column=1, columnspan=3)

tk.Label(downFrame, text="Result", font=('Bookman Old Style',10)).grid(
    row=1,column=1, columnspan=3)
result = tk.Label(downFrame, fg='red', font=('Bookman Old Style',10), 
                  justify='center')
addResult = tk.Button(downFrame, text="Add Result as Var", font=('',10,'bold'))

def mainINTERFACE():
    addNum(("a", "CLICK TO EDIT", "0.21", "m/(s^2)"))
    addNum()
    
    root.mainloop()

mainINTERFACE()

"""Usage example
A = N(1, 0, 'atm')
B = N(2, 0.1, 'atm')

print(f"A = {A}")
print(f"B = {B}")
print(f"A+B = {A+B}")
print(f"A-B = {A-B}")
print(f"A*B = {A*B}")
print(f"A/B = {A/B}")
print(f"B/A = {B/A}")
print(f"A**3 = {A**3}")
print(f"B**3 = {B**3}")
"""


