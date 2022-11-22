"""

@author: Manas Patil
Description: This is pass1 intermediate code generator developed for mnemonics listed in mnemonics dictionary below.

"""

mnemonic=[['STOP','ADD','SUB','MULT','MOVER','MOVEM','COMP','BC','DIV','READ','PRINT','START','END','ORIGIN','EQU','LTORG','DS','DC','AREG','BREG','CREG','EQ','LT','GT','NE','LE','GT','ANY'],['IS','IS','IS','IS','IS','IS','IS','IS','IS','IS','IS','AD','AD','AD','AD','AD','DL','DL','RG','RG','RG','CC','CC','CC','CC','CC','CC','CC'],['00','01','02','03','04','05','06','07','08','09','10','01','02','03','04','05','01','02','01','02','03','01','02','03','04','05','06','07']]

#opening input file for program
file=open('input.txt','r')
lines=file.readlines()


symTable=[]
sym_lc=[]
symbls=[]
sym_size=[]
lit_table=[]
lit_add=[]
pool_table=[]
literal_list=[]
littabline=0
symtabline=0
pt=0
pool_table.append(0)

#file to store intermediate code
ifp=open("intermediate.txt","a")
ifp.truncate(0)            


for line in lines:
    line=line.replace(',',' ')
    line=line.replace('\t',' ')
    line=line.strip()
    substrings=line.split(' ')
    
    #ASSEMBLER DIRECTIVES
    if(substrings[0]=='START'):                 #intializing lc                   
        lc=int(substrings[1])
        ifp.write("\t(AD,01)\t(C,"+substrings[1]+')\n')
        continue
        
    elif(substrings[0]=='END'):          #no increment of lc for assembler directives 
        ifp.write("\t(AD,02)\n")
        if(littabline !=pool_table[pt]):   #handling literals without LTORG
            LTindex=pool_table[pt]
            for i in range(pool_table[pt],littabline):
                lit_add.append(lc)
                ifp.write("\t(DL,02)\t(C,"+str(lit_table[i])+")\n")
                lc=lc+1        
        continue
        
    elif(substrings[0]=='ORIGIN'):
        new_lc=substrings[1].split('+')       #substrings[1]=NEXT+3
        temp_index=symbls.index(new_lc[0])    #new_lc[0]==L1 && new_lc[1]==3
        lc=sym_lc[temp_index]+int(new_lc[1])
        ifp.write("\t(AD,03)\t(C,"+str(lc)+")\n")
        continue
    
    elif 'LTORG' in line:
        LTindex=pool_table[pt]              
        for i in range(LTindex,littabline):
            lit_add.append(lc)
            ifp.write("\t(DL,02)\t(C,"+str(lit_table[i])+")\n")
            lc=lc+1
        pt=pt+1
        pool_table.append(littabline)
        continue
    
    elif 'EQU' in line:
        idx=symbls.index(substrings[2])
        if substrings[0] in symbls:
            s_idx=symbls.index(substrings[0])
            sym_lc[s_idx]=sym_lc[idx]
        else:
            sym_lc.append(sym_lc[idx])
            symbls.append(substrings[0])
            sym_size.append(1)
        ifp.write("\t(AD,04)\t(S,"+str(idx)+")\n")
        continue
    
    
    
    for i in range(len(substrings)):
#=======for imperative and conditional codes statement
        if substrings[i] in mnemonic[0]:                 
            mot_index=mnemonic[0].index(substrings[i])
            ifp.write("\t("+mnemonic[1][mot_index]+","+str(mnemonic[2][mot_index])+")")
            if substrings[i]=='DC' or substrings[i]=='DS':
                ifp.write("(C,"+substrings[i+1]+")")
                lc=lc+int(substrings[i+1])-1
                i=len(substrings)
                continue
        
#=======for literals
        elif '=' in substrings[i]:                       
            literal=line.split('=')
            lit_table.append(int(literal[1][1:-1]))    #negative slicing for string to int i.e '50'
            ifp.write("\t(L,"+str(littabline)+")")
            littabline=littabline+1
            
#=======for symbols
        elif substrings[i] not in mnemonic[0] and i==0:
            if substrings[i] in symbls:
                index_sym=symbls.index(substrings[i])
                sym_lc[index_sym]=lc
            else:
                sym_lc.append(lc)
                symbls.append(substrings[i])
                sym_size.append(1)
#             symtabline=symtabline+1
        
#=======for symbols without lc initialization
        else:
            if substrings[i] not in symbls:
                symbls.append(substrings[i])
                sym_lc.append("**")
                sym_size.append(1)
#                 symtabline=symtabline+1
            ifp.write("\t(S,"+str(symbls.index(substrings[i]))+")")
        
    ifp.write("\n")
    lc=lc+1
            
symTable.append(symbls)
symTable.append(sym_lc)
symTable.append(sym_size)

print("---------------------------------------")
print("Symbols\t\tAddress\t\tSize\n")
for i in range(0,len(symTable)+1):
    print(symTable[0][i],"\t\t",symTable[1][i],"\t\t",symTable[2][i])
print("---------------------------------------")

print("Literals\tAddress\n")
for i in range(0,len(lit_table)):
#     lit_add.append(lc+i)
    print(lit_table[i],"\t\t",lit_add[i])
print("---------------------------------------");

print("---------------------------------------")
print("Pools")
for i in range(0,len(pool_table)):
    print(pool_table[i])
print("---------------------------------------")
            



ifp.close()     
            
            
            
            
        
        