import time
import re

vmfile=''
isArithmetic=0
isPushPop=0
isLabel=0
isGoto=0
isIfgoto=0
isInit=0
isCall=0
isReturn=0
isFunctionDeclaration=0
LABEL_COUNT=-1
REL_JUMP_FLAG=-1
asmfile=''

def openFile():
    global vmfile
    vmfile=input('enter vm file name')
    vmf=open(vmfile)
    global asmfile
    asmfile=input('enter asm file name')
    createFile()
    vmflines=vmf.readlines()
    for x in vmflines:
        x=x[0:len(x)-1]
        Arithmetic(x)
        global isArithmetic
        if isArithmetic == 1:
            isArithmetic=0
            continue
        PushPop(x)
        global isPushPop
        if isPushPop==1:
            isPushPop=0
            continue
        Label(x)
        global isLabel
        if isLabel==1:
            isLabel=0
            continue
        Goto(x)
        global isGoto
        if isGoto==1:
            isGoto=0
            continue
        Ifgoto(x)
        global isIfgoto
        if isIfgoto==1:
            isIfgoto=0
            continue
        Init(x)
        global isInit
        if isInit==1:
            isInit=0
            continue
        Call(x)
        global isCall
        if isCall==1:
            isCall=0
            continue
        Return(x)
        global isReturn
        if isReturn==1:
            isReturn=0
            continue
        FunctionDeclaration(x)
        global isFunctionDeclaration
        if isFunctionDeclaration==1:
            isFunctionDeclaration=0
            continue
        

                 
# Function to create file with name specified
def createFile():
    asm=open(asmfile,'w+')

# Function to convert all arithmetic VM code to Assembly code
def Arithmetic(x):
    f=open(asmfile,'a')
    # Flag to check if the arithmetic function has been used
    global isArithmetic
    if 'add'==x:
        common_addsuborand()
        f.write('M=M+D\n@SP\nM=M+1\n')
        isArithmetic=1
    elif 'sub'==x:
        common_addsuborand()
        f.write('M=M-D\n@SP\nM=M+1\n')
        isArithmetic=1
    elif 'and'==x:
        common_addsuborand()
        f.write('M=M&D\nM=M+1\n')
        isArithmetic=1
    elif 'or'== x:
        common_addsuborand()
        f.write('M=M|D\nM=M+1\n')
        isArithmetic=1
    elif 'gt'==x:
        common_relational('JLE')
        isArithmetic=1
    elif 'lt'==x:
        common_relational('JGE')
        isArithmetic=1
    elif 'eq'==x:
        common_relational('JNE')
        isArithmetic=1
    elif 'not'==x:
        f.write('@SP\nA=M-1\nM=!M\n')
        isArithmetic=1
    elif 'neg'==x:
        f.write('D=0\n@SP\nA=M-1\nM=D-M\n')
        isArithmetic=1

# Since add, sub, or & and operations have some common lines of code, a common function can be used for them
def common_addsuborand():
    f=open(asmfile,'a')
    f.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\n')

# Since gt, lt, eq , or operations have common lines of code, a common function can be used for them
def common_relational(j_stat):
    f=open(asmfile,'a')
    global REL_JUMP_FLAG
    REL_JUMP_FLAG=REL_JUMP_FLAG+1
    f.write("@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@FALSE{}\nD;{}\n@SP\nA=M\nM=-1\n@CONTINUE{}\n0;JMP\n(FALSE{})\n@SP\nA=M\nM=0\n(CONTINUE{})\n".format(str(REL_JUMP_FLAG),j_stat,str(REL_JUMP_FLAG),str(REL_JUMP_FLAG),str(REL_JUMP_FLAG)))

def PushPop(x):
    f=open(asmfile,'a')
    global isPushPop
    x=x.split(' ')
    if x[0]=='push':
        if x[1]=='constant':
            f.write("@{}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(x[2]))
            isPushPop=1
        elif x[1]=='local':
            common_push('LCL',x[2],False)
            isPushPop=1
        elif x[1]=='argument':
            common_push('ARG',x[2],False)
            isPushPop=1
        elif x[1]=='this':
            common_push('THIS',x[2],False)
            isPushPop=1
        elif x[1]=='that':
            common_push('THAt',x[2],False)
            isPushPop=1
        elif x[1]=='temp':
            common_push('R5',str(int(x[2])+5),False)
            isPushPop=1
        elif (x[1]=='pointer' and x[2]=='0'):
            common_push('THIS',x[2],True)
            isPushPop=1
        elif (x[1]=='pointer' and x[2]=='1'):
            common_push('THAT',x[2],True)
            isPushPop=1
        elif (x[1]=='static'):
            # every file has its static space
            f.write('@{}{}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'.format(asmfile,x[2]))
            isPushPop=1
    elif x[0]=='pop':
        if x[1]=='local':
            common_pop('LCL',x[2],False)
            isPushPop=1
        elif x[1]=='argument':
            common_pop('ARG',x[2],False)
            isPushPop=1
        elif x[1]=='this':
            common_pop('THIS',x[2],False)
            isPushPop=1
        elif x[1]=='that':
            common_pop('THAT',x[2],False)
            isPushPop=1
        elif x[1]=='temp':
            common_pop('R5',str(int(x[2])+5),False)
            isPushPop=1
        elif (x[1]=='pointer' and x[2]=='0'):
            common_pop('THIS',x[2],True)
            isPushPop=1
        elif (x[1]=='pointer' and x[2]=='1'):
            common_pop('THAT',x[2],True)
            isPushPop=1
        elif x[1]=='static':
            # every file has a static space
            f.write("@{}{}\nD=A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n".format(asmfile,x[2]))
            isPushPop=1

# template for push local, this, that, argument, temp, pointer, static            
def common_push(term,index,ispointer):
    f=open(asmfile,'a')
    # when it's a pointer, just read the data stored in THIS or THAT
    if (ispointer):
        noPointerCode= ""
    else:
        noPointerCode="@"+index+"\nA=D+A\nD=M\n"
    f.write("@{}\nD=M\n{}@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(str(term),noPointerCode))

# template for pop local, this, that, argument, temp, pointer, static
def common_pop(term,index,ispointer):
    f=open(asmfile,'a')
    # whe it's a pointer R13 will store address of THIS or THAT
    if ispointer:
        noPointerCode='D=A\n'
    else:
        noPointerCode='D=M\n@'+str(index)+'\nD=D+A\n'
    f.write('@{}\n{}@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n'.format(term,noPointerCode))

def Label(x):
    f=open(asmfile,'a')
    x=x.split(' ')
    if x[0]=='label':
        x=x[1]
        if validlabel(x):
            f.write("({})\n".format(x))
            global isLabel
            isLabel=1
        else:
            print("Label format might be wrong")

def Goto(x):
    f=open(asmfile,'a')
    x=x.split(' ')
    if(x[0]=='goto'):
        x=x[1]
        if validlabel(x):
            f.write("@{}\n0;JMP\n".format(x))
            global isGoto
            isGoto=1
        else:
            print("Label format might be wrong")

def Ifgoto(x):
    f=open(asmfile,'a')
    x=x.split(' ')
    if(x[0]=='if-goto'):
        x=x[1]
        if validlabel(x):
            f.write("@SP\nAM=M-1\nD=M\nA=A-1\n@{}\nD;JNE\n".format(x))
            global isIfgoto
            isIfgoto=1
        else:
            print('Label format might be wrong')

def validlabel(l):
    f=open(asmfile,'a')
    if(re.findall("[a-zA-Z1-9$_]",l)):
        if(re.findall("\A[a-zA-Z]",l)):
            return True
        else:
            return False

def Init(x):
    f=open(asmfile,'a')
    if 'init' in x:
        f.write("@256\nD=A\n@SP\nM=D\n")
        Call("Sys.init",0)
        global isInit
        isInit=1

def Call(x):
    f=open(asmfile,'a')
    x=x.split(' ')
    x=x[0]
    if x[0]=='call':
        fnName=x[1]
        argnum=x[2]
        global LABEL_COUNT
        LABEL_COUNT=LABEL_COUNT+1
        newlabel="RETURN_LABEL"+str(LABEL_COUNT)
        # to push return address
        f.write("@{}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(newlabel))
        # to push LCL
        common_push("LCL",0,True)
        # to push ARG
        common_push('ARG',0,True)
        # to push THIS
        common_push('THIS',0,True)
        # to push THAT
        common_push('THAT',0,True)
        f.write('@SP\nD=M\n@5\nD=D-A\n@{}\nD=D-A\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n@{}\n0;JMP\n({})\n'.format(argnum,fnName,newlabel))
        global isCall
        isCall=1

def Return(x):
    f=open(asmfile,'a')
    if 'return' in x:
        f.write('@LCL\nD=M\n@R11\nM=D\n@5\nA=D-A\nD=M\n@R12\nM=D\n')
        common_pop('ARG',0,False)
        f.write('@ARG\nD=M\n@SP\nM=D+1\n')
        PrevFrameSaver('THAT')
        PrevFrameSaver('THIS')
        PrevFameSaver('ARG')
        PrevFrameSaver('LCL')
        f.write('@R12\nA=M\n0;JMP\n')
        global isReturn
        isReturn=1

def PrevFrameSaver(pos):
    f=open(asmfile,'a')
    f.write('@R11\nD=M-1\nAM=D\nD=M\n@{}\nM=D'.format(pos))

def FunctionDeclaration(x):
    f=open(asmfile,'a')
    x=x.split(' ')
    if x[0]=='function':
        fnName=x[1]
        num_of_local_vars=int(x[2])
        f.write('({})\n'.format(fnName))
        for i in range(num_of_local_vars):
            PushPop('push constant 0')

openFile()
