import eval
import matplotlib
matplotlib.use('Qt4Agg',warn=False, force=True)
import matplotlib.pyplot as plt
import random
import sys
nsp = eval.NumericStringParser()
from PyQt4 import QtCore, QtGui, uic
Ui_MainWindow, QtBaseClass = uic.loadUiType("GA.ui")

class ga(): #Genetic Algorithm
    
    x=[]    #Variables
    xd=[]   #Binary of the variables
    c=[]    #Cost
    d=[]    #Highest cost in each generation for graph
    v=2     #Variable count
    cf="0"  #Cost function       
    ind=[]  #Index for graph
    vf=[]   #Variable symbols used
    size=10 #Size of Binary Variable
    le=15   #Population size
    l=0     #Lower limit of variables
    h=4     #Higher limit of variables
    gen=20  #Number of generations
    mi=True #Minima or Maxima
    rl=True #True for Real, False for Binary
        
    def vcc(self):  #variable counter
        if(self.cf.count('x')>0):
            cnt=1
            if(self.cf.count("'")>0):
                for i in range(len(self.cf)):
                    if(self.cf[i]=='x'):
                        cnta=1
                        while(self.cf[i+1]=="'"):
                            cnta+=1
                            if(i<len(self.cf)-2):
                                i+=1
                            else: break
                        if(cnta>cnt):cnt=cnta
        else:
            cnt=0
        return cnt
    
    def init(self):   #Value Init
        self.cf=self.cf.replace("z","x''").replace("y","x'").replace(" ","")
        self.cf=self.cf.replace("cos(","cos((pi/180)*").replace("sin","sin((pi/180)*").replace("tan","tan((pi/180)*")
        self.v=self.vcc(self)
        for j in range(self.v):
            appr="x"
            for i in range(j):
                appr=appr+"'"
            self.vf.append(appr)
        for i in range(self.v):
            temx=[]
            temxd=[]
            for j in range(self.le):
                temx.append(random.uniform(self.l,self.h))
                temxd.append(0)
            self.x.append(temx)
            self.xd.append(temxd)
        for i in range(self.le):
            self.c.append(0.0)
        for i in range(self.gen+1):
            self.ind.append(i)
            
    def rcost(self): #Real Parametric Fitness Function
        for i in range(self.le):
            self.c[i]=self.cf
            for j in range(self.v-1,-1,-1):
                self.c[i]=self.c[i].replace(self.vf[j],"("+str(self.x[j][i])+")")
            self.c[i]=float(nsp.eval(self.c[i]))
        if(mi==True):
            x=sorted(zip(self.c,*self.x))
        else:
            x=sorted(zip(self.c,*self.x),reverse=True)
        cs,*xs=zip(*x)
        for i in range(self.le):
            self.c[i]=float(cs[i])
            for j in range(self.v):
                self.x[j][i]=xs[j][i]
                
    def rcrossover(self): #Real Parametric Crossover Function
        for i in range(self.v):
            for j in range(int(self.le/2)):
                self.x[i][self.le-j-1]=random.uniform(self.x[i][j],self.x[i][j+1])
        self.rcost(self)

    def rmutate(self):  #Real Parametric Mutation Function
        for i in range(self.v):
            j=random.randint(int(self.le/2),self.le-1)
            self.x[i][j]=random.uniform(self.l,self.h)
        self.rcost(self)
    
    def polt(self):  #Graph Plotter
        plt.plot(self.ind,self.d)
        plt.ylabel('Cost')
        plt.xlabel('Generation')
        plt.title('Cost/Generation')
    
    def final(self,z): #Generation Value Printer
        print ('Generation '+str(z)+"/"+str(self.gen))
        for i in range (self.le):
            print("cost =","%8f"%round(self.c[i],5),end=" ")
            for j in range(self.v):
                print(self.vf[j],"%8f"%round(self.x[j][i],5),end=" ")
            print(" ")

    def pres(self):  #Precision Calculator
        b=format(0,'0>'+str(self.size))
        a=format(1,'0>'+str(self.size))
        a=float(int(str(a),2))
        a=a/(2**self.size-1)
        a=(a*(self.h-self.l))+self.l
        b=float(int(str(b),2))
        b=(b*(self.h-self.l))+self.l
        c=a-b
        return c

    def quant(self):  #Binary Converter
        a=self.h-self.l
        if(a==0):a=1
        for j in range(self.v):
            bx=[]
            for i in range(self.le):
                bx.append(((2**self.size)-1)*((self.x[j][i]-self.l)/a))
                self.xd[j][i]=int(format(int(bx[i]),'b'))
                
    def bcost(self):    #Binary Fitness Function
        for i in range(self.le):
            self.c[i]=self.cf
            for j in range(self.v-1,-1,-1):
                self.c[i]=self.c[i].replace(self.vf[j],"("+str(self.x[j][i])+")")
            self.c[i]=float(nsp.eval(self.c[i]))
        if(mi==True):
            z=sorted(zip(self.c,*self.xd))
            x=sorted(zip(self.c,*self.x))
        else:
            z=sorted(zip(self.c,*self.xd),reverse=True)
            x=sorted(zip(self.c,*self.x),reverse=True)
        cs,*xds=zip(*z)
        cy,*xs=zip(*x)
        for i in range(self.le):
            self.c[i]=float(cs[i])
            for j in range(self.v):
                self.x[j][i]=xs[j][i]
                self.xd[j][i]=xds[j][i]
                
    def bcrossover(self): #Binary Crossover Function
        xd=[]
        for j in range(self.v):
            xd1=[]
            for i in range(self.le):
                xd1.append(format(self.xd[j][i],'0>'+str(self.size)))
            xd.append(xd1)
            a=xd[0][0]
        for k in range(self.v):
            for i in range(int(self.le/2)):
                for j in range(self.size):
                    r1=random.randint(0,1)
                    if(r1):a=a[:j]+xd[k][i][j]+a[j+1:]
                    else:a=a[:j]+xd[k][i+1][j]+a[j+1:]
                self.xd[k][self.le-i-1]=int(a)
                
    def bmutate(self):  #Binary Mutation Function
        for j in range(self.v):
            i =random.randint(int(self.le-(self.le/2)+1)-1,self.le-1)
            self.xd[j][i]=format(self.xd[j][i],'0>'+str(self.size))
            rx=random.randint(0,self.size-1)
            if(int(self.xd[j][i][rx])):
                self.xd[j][i]=int(self.xd[j][i][:rx]+'0'+self.xd[j][i][rx+1:])
            else:
                self.xd[j][i]=int(self.xd[j][i][:rx]+'1'+self.xd[j][i][rx+1:])
            self.xd[j][i]=int(self.xd[j][i])
            
    def dequant(self): #Decimal Converter
        for j in range(self.v):
            bx=[]
            for i in range (self.le):
                bx.append(float(int(str(self.xd[j][i]),2)))
                bx[i]=bx[i]/(2**self.size-1)
                self.x[j][i]=(bx[i]*(self.h-self.l))+self.l
 
    def __new__(self,re,cf,l,h,gen,le,mi,size): #Initialize GA
        self.cf=cf
        self.l=l
        self.h=h
        self.h=h
        self.gen=gen
        self.le=le
        self.mi=mi
        self.size=size
        self.rl=re
        self.init(self)
        
        if(re==True):
            print("Real Parametric Genetic Algorithm")
            self.size=10
            self.rcost(self)
            self.d.append(self.c[0])
            self.final(self,0)
            for i in range(self.gen):
                self.rcrossover(self)
                for j in range(50):
                    self.rmutate(self)
                self.d.append(self.c[0])
                self.final(self,i+1)
        
        else:
            print("Binary Genetic Algorithm")
            self.quant(self)
            self.dequant(self)
            self.bcost(self)
            self.d.append(self.c[0])
            self.final(self,0)
            for i in range(self.gen):
                self.quant(self)
                self.bcrossover(self)
                self.dequant(self)
                self.bcost(self)
                self.quant(self)
                for j in range(50):
                    self.bmutate(self)
                self.dequant(self)
                self.bcost(self)
                self.d.append(self.c[0])
                self.final(self,i+1)
        
        self.polt(self)
        self.fin=[]
        
        for j in range(self.v):
            self.fin.append(self.x[j][0])
            
        return (self.c[0],self.fin,self.pres(self))

class gui(QtGui.QMainWindow, Ui_MainWindow): #GUI
    def final(self,cost,values,mi,size,pres):
        self.vf=[]
        ms=QtGui.QMessageBox()
        for j in range(len(values)):
            appr="x"
            for i in range(j):
                appr=appr+"'"
            self.vf.append(appr)
            
        x="Cost = "+str("%8f"%round(cost,5))
        if(size>-1):
            x=x+" Precision = "+str("%8f"%round(pres,5))
        y=""
        for j in range(len(values)):
            if(len(values)<4):
                y=y+" "+self.vf[j].replace("x''","z").replace("x'","y")+" = "+"%8f"%round(values[j],5)
            else:
                y=y+" "+self.vf[j]+" = "+"%8f"%round(values[j],5)
        if(mi==True):
            abc="Minima"
        else:
            abc="Maxima"
        ms.setText("Function : "+self.cf.upper()+"("+abc+")"+"\n"+x+"\n"+y)
        ms.exec_()
        
    def default(self,cf,le,l,h,gen,size):  #default value initializer
        self.ef.setText(cf)
        self.pop.setText(str(le))
        self.ll.setText(str(l))
        self.hl.setText(str(h))
        self.ge.setText(str(gen))
        self.sz.setText(str(size))
        self.b1.setChecked(True)
        self.r1.setChecked(True)
    
    def ret(self):
        return(self.r1.isChecked(),self.cf,self.le,self.gen,self.l,self.h,self.b1.isChecked(),self.size)
    
    def disp(self):  #Value Loader
        self.cf=str(self.ef.text())
        self.le=int(self.pop.toPlainText())
        self.l=float(self.ll.toPlainText())
        self.h=float(self.hl.toPlainText())
        self.gen=int(self.ge.toPlainText())
        self.size=int(self.sz.toPlainText())
        if(self.cf!=""):
            self.close()
            
    def clk(self):  #Button Toggle
        if(self.r1.isChecked()):
            self.sz.setDisabled(True)
        else:
            self.sz.setDisabled(False)
            
    def __init__(self, parent=None): #Initialize GUI
        super(gui, self).__init__(parent)
        self.setupUi(self)
        self.r1.toggled.connect(self.clk)
        self.r2.toggled.connect(self.clk)
        self.default("((1.5-x+(x*y))^2)+((2.25-x+x*(y^2))^2)+((2.625-x+x*(y^3))^2)",15,0,4,20,10)
        self.ok.clicked.connect(self.disp)
        
app = QtGui.QApplication(sys.argv)
ui=gui()
ui.show()
app.exec_()

re,cf,le,gen,l,h,mi,sz=ui.ret()
cost,values,pres=ga(re,cf,l,h,gen,le,mi,sz)
if(re==True):
    ui.final(cost,values,mi,-1,pres)
else:
    ui.final(cost,values,mi,sz,pres)    
plt.show()
