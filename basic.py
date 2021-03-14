from sys import *
token =[]
num_stack=[]
symbols={}
def open_file(filename):


    data =open(filename,"r").read()
    data+= "<EOF>"
    return data
    

def lex(filecontent):
    tok=""
    state = 0
    string=""
    expr = ""
    n= ""
    varStarted=0
    var=""
    isexpr = 0
    filecontent=list(filecontent)
    for char in filecontent:
        tok += char
        if tok ==" ":
            if state== 0:
                tok =""
            else:
                tok = " "
        elif tok == "\n" or tok=="<EOF>":
            
            if expr != "" and isexpr==1:
                token.append("EXPR:" + expr)
                expr=""
            elif expr != "" and isexpr ==0:
                token.append("NUM:" + expr)
                expr=""
            elif var !="":
                token.append("VAR:"+ var)
                var= ""
                varStarted=0
                
            tok= ""
        elif tok=="=" and state==0:
            if expr != "" and isexpr ==0:
                token.append("NUM:" + expr)
                expr=""
            if var !="":
                token.append("VAR:"+ var)
                var= ""
                varStarted=0
            if token[-1] == "EQUALS":
                token[-1] = "EQEQ"
            else:
            
                token.append("EQUALS")
            tok=""
           
        elif tok== "$" and state ==0:
            varStarted=1
            var +=tok
            tok=""
        elif varStarted==1:
            if tok==">" or tok=="<":
                if var !="":
                
                    token.append("VAR:"+ var)
                    var= ""
                    varStarted=0
                
            var+=tok
            tok=""
        elif tok=="out" or tok=="OUT":
            token.append("OUT")
            tok=""
        elif tok=="if" or tok=="IF":
            token.append("IF")
            tok=""
        elif tok=="else" or tok=="ELSE":
            token.append("ELSE")
            tok=""
        elif tok=="then" or tok=="THEN":
            if expr != "" and isexpr ==0:
                token.append("NUM:" + expr)
                expr=""
            token.append("THEN")
            tok=""
        elif tok=="input" or tok=="INTPUT":
            token.append("INPUT")
            tok=""
        elif tok=="0" or tok=="1" or tok=="2" or tok=="3":
           
            expr += tok
            tok=""
        elif tok =="+" or tok=="-" or tok=="/" or tok=="*" or tok=="(" or tok==")":
            isexpr=1
            expr += tok
            tok=""
        elif tok== "\t":
            tok=""
        elif tok =="\"" or tok==" \"":
            if state ==0:
                
                state =1
            elif state ==1:
                token.append("STRING:"+ string + " \"")
                string=""
                state =0
                tok =""
        elif state ==1:
            string += tok
            tok=""
    
    #print(token)
    return token
    
    #return ''


def evalExpr(expr):
    
    return eval(expr)
    
        

def doPrint(toPrint):
    if (toPrint[0:6]=="STRING"):
        toPrint= toPrint[8:]
        toPrint= toPrint[:-1]
    elif (toPrint[0:3]=="NUM"):
        toPrint= toPrint[4:]
    elif (toPrint[0:4]=="EXPR"):
        toPrint=evalExpr(toPrint[5:])
        
        
    print(toPrint)


def doAssign(varname, varvalue):
    symbols[varname[4:]] = varvalue
        
def getVar(varname):
    varname =varname[4:]
    if varname in symbols:
        
        return symbols[varname]
    else:
        return "Var Error: undefined VAR"
        exit()
        
def getInt(string,varname):
    i=input(string[1:-1]+ " ")
    symbols[varname] = "STRING:\"" +i +"\""


    
def pars(toks):
    i= 0
    while(i<len(toks)):
        
        if toks[i] + " " + toks[i+1][0:6] == "OUT STRING" or toks[i] + " " + toks[i+1][0:3] == "OUT NUM" or toks[i] + " " + toks[i+1][0:4] == "OUT EXPR"or toks[i] + " " + toks[i+1][0:3] == "OUT VAR":
            if toks[i+1][0:6] == "STRING":
                doPrint(toks[i+1])
            elif toks[i+1][0:3] == "NUM":
                doPrint(toks[i+1])
            elif toks[i+1][0:4] == "EXPR":
                doPrint(toks[i+1])
            elif toks[i+1][0:3] == "VAR":
                doPrint(getVar(toks[i+1]))

            i+=2
            
        elif toks[i]+" "+toks[i+1] =="ELSE THEN":
            if toks[i] == "ELSE":
            
                pass
            i+=2
            
        elif toks[i][0:3] + " " + toks[i+1]+" "+ toks[i+2][0:6] =="VAR EQUALS STRING" or toks[i][0:3] + " " + toks[i+1]+" "+ toks[i+2][0:3] =="VAR EQUALS NUM" or toks[i][0:3] + " " + toks[i+1]+" "+ toks[i+2][0:4] =="VAR EQUALS EXPR" or toks[i][0:3] + " " + toks[i+1]+" "+ toks[i+2][0:3] =="VAR EQUALS VAR":
            
            if toks[i+2][0:6] == "STRING":
                doAssign(toks[i],toks[i+2])
            elif toks[i+2][0:3] == "NUM":
                doAssign(toks[i],toks[i+2])
            elif toks[i+2][0:4] == "EXPR":
                doAssign(toks[i],"NUM:" + str(evalExpr(toks[i+2][XX:])))
            elif toks[i+2][0:3] == "VAR":
                doAssign(toks[i],getVar(toks[i+2]))
            i+=3
            
        elif toks[i]+" "+toks[i+1][0:6]+ " "+toks[i+2][0:3] =="INPUT STRING VAR":
            getInt(toks[i+1][7:],toks[i+2][4:])
            i+=3
        elif toks[i]+" "+toks[i+1][0:3]+ " "+toks[i+2]+ " "+toks[i+3][0:3]+ " "+toks[i+4] =="IF NUM EQEQ NUM THEN" or toks[i]+" "+toks[i+1][0:3]+ " "+toks[i+2]+ " "+toks[i+3][0:3]+ " "+toks[i+4] =="IF VAR EQEQ VAR THEN":
            if toks[i+1][4:] ==toks[i+3][4:]:
                
                
                pass
                
                
            else:
                
                
                
                print("false")
                exit()
                
            i+=5
            
        
    #print(symbols)        
def run():
    
    
    data= open_file(argv[1])  
    toks=lex(data)
    pars(toks)


run()