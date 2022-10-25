from pkg_resources import to_filename
file_read = open('/home/sameer/Documents/nand2tetris/nand2tetris/projects/10/Square/Main.jack','r')
lines = file_read.readlines()
writing = []
keywords = ['class','constructor','function','method','field','static','var','int','char','boolean','void','true','false','null','this','let','do','if','else','while','return']
symbols = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']
program_structure_declared_until_now = []
line_no = 1
for line in lines:
    try:
        if "//" in line:#deals with end of line comments
            to_be_replaced = line[0:line.index("//")]
            req_index = lines.index(line)
            lines = lines[:req_index]+[to_be_replaced]+lines[req_index+1:]
        elif "/**" in line:#help deal with API comments
            lines.remove(line)
        elif(len(line)==0):
            lines.remove(line)
        else:
            line = line+'\n'
    except:
        lines.remove(line)
#for x in lines:
#    print(x) #this works good

#now wcomments have been removed
def splitting_everything(line):
    if(line!=''):
        for digit in line:
            if(digit in symbols):
                line = line.replace(digit,"\n"+digit+"\n")
    else:
        pass
    return line.split()
    
def output_line_str(program_struct,obj):
  return "<"+program_struct+">"+obj+"</"+program_struct+">"

def letStatement_eval(line):
    new_list = ['<letStatement>\n']
    potential_tokens = splitting_everything(line)
    term_var = False
    program_structure_declared_until_now.append('</letStatement>\n')
    bracket = line.count('(')#number of brackets
    for tokens in potential_tokens:
        if(tokens in keywords):
            #print('<keyword>')
            new_list.append(output_line_str('keyword',tokens)+'\n')
        elif(tokens == '}'):
            new_list.append(program_structure_declared_until_now.pop())
            new_list.append(output_line_str('symbol','}')+'\n')
        elif(tokens == '('):
            new_list.append(output_line_str('symbol','(')+'\n')
            #new_list.append('<expressionList>')
            term_var = True

            #the arguments are essentially expression; so after op brackt, before close bracket, before after every comma
            if(line.index(')')-line.index('(')==1):
                new_list.append('<expressionList> </expressionList>\n')
            else:
                new_list.append('<expressionList>\n')
                new_list.append('<expression>\n')
        elif(tokens == ')'):
            if(line.index(')')-line.index('(')==1):
                pass#there is no expression if its an empty expressionList
            else:
                new_list.append('</expression>\n')
                new_list.append('</expressionList>\n')
            new_list.append(output_line_str('symbol',')')+'\n')
            
            if(bracket==1):
                term_var = False
        elif(tokens.isdigit()):
            #will be a term if inside an expression
            if(term_var and bracket>0):
                new_list.append('<term>\n')
                new_list.append(output_line_str('integerConstant',tokens)+'\n')
                new_list.append('</term>\n')
            else:
                new_list.append(output_line_str('integerConstant',tokens)+'\n')
        elif(tokens in symbols and (tokens != ',' and tokens != '}')):
            new_list.append(output_line_str('symbol',tokens)+'\n')#can never be a term also
        elif(tokens == ','):
            new_list.append('</expression>\n')#before comma there was an expression
            new_list.append(output_line_str('symbol',tokens)+'\n')
            new_list.append('<expression>\n')#after comma there's another expression

        else:#this part is for identifier, but identifier can also be inside an expression
            if(term_var and bracket>0):
                new_list.append('<term>\n')
                new_list.append(output_line_str('identifer',tokens)+'\n')
                new_list.append('</term>\n')
            else:
                new_list.append(output_line_str('identifier',tokens)+'\n')
    new_list.append(program_structure_declared_until_now.pop())
    return new_list


def returnStatement_eval(line):
    new_list = ['<returnStatement>\n']
    potential_tokens = splitting_everything(line)
    term_var = False
    program_structure_declared_until_now.append('</returnStatement>\n')
    bracket = line.count('(')#number of brackets
    for tokens in potential_tokens:
        if(tokens in keywords):
            #print('<keyword>')
            new_list.append(output_line_str('keyword',tokens)+'\n')
        elif(tokens == '('):
            new_list.append(output_line_str('symbol','(')+'\n')
            #new_list.append('<expressionList>')
            term_var = True

            #the arguments are essentially expression; so after op brackt, before close bracket, before after every comma
            if(line.index(')')-line.index('(')==1):
                new_list.append('<expressionList> </expressionList>\n')
            else:
                new_list.append('<expression>\n')
        elif(tokens == ')'):
            if(line.index(')')-line.index('(')==1):
                pass#there is no expression if its an empty expressionList
            else:
                new_list.append('</expression>\n')
                new_list.append('</expressionList>\n')
            new_list.append(output_line_str('symbol',')')+'\n')
            
            if(bracket==1):
                term_var = False
        elif(tokens.isdigit()):
            #will be a term if inside an expression
            if(term_var and bracket>0):
                new_list.append('<term>\n')
                new_list.append(output_line_str('integerConstant',tokens)+'\n')
                new_list.append('</term>\n')
            else:
                new_list.append(output_line_str('integerConstant',tokens)+'\n')
        elif(tokens in symbols and tokens != ','):
            new_list.append(output_line_str('symbol',tokens)+'\n')#can never be a term also
        elif(tokens == ','):
            new_list.append('</expression>\n')#before comma there was an expression
            new_list.append(output_line_str('symbol',tokens)+'\n')
            new_list.append('<expression>\n')#after comma there's another expression

        else:#this part is for identifier, but identifier can also be inside an expression
            if(term_var and bracket>0):
                new_list.append('<term>\n')
                new_list.append(output_line_str('identifer',tokens)+'\n')
                new_list.append('</term>\n')
            else:
                new_list.append(output_line_str('identifier',tokens)+'\n')
    new_list.append(program_structure_declared_until_now.pop())
    return new_list

def doStatement_eval(line):
    new_list = ['<doStatement>\n']
    potential_tokens = splitting_everything(line)
    term_var = False
    program_structure_declared_until_now.append('</doStatement>\n')
    bracket = line.count('(')#number of brackets
    for tokens in potential_tokens:
        if(tokens in keywords):
            #print('<keyword>')
            #new_list.append(output_line_str('keyword',tokens))
            if(term_var):
                new_list.append('<term>\n')
                new_list.append(output_line_str('keyword',tokens)+'\n')
                new_list.append('</term>\n')
            else:
                new_list.append(output_line_str('keyword',tokens)+'\n')
        elif(tokens == '}'):
            new_list.append(program_structure_declared_until_now.pop())
            new_list.append(output_line_str('symbol','}')+'\n')

        elif(tokens == '('):
            new_list.append(output_line_str('symbol','(')+'\n')
            new_list.append('<expressionList>\n')
            term_var = True

            #the arguments are essentially expression; so after op brackt, before close bracket, before after every comma
            if(line.index(')')-line.index('(')==1):
                pass#there is no expression if its an empty expressionList
            else:
                new_list.append('<expression>\n')
        elif(tokens == ')'):
            if(line.index(')')-line.index('(')==1):
                pass#there is no expression if its an empty expressionList
            else:
                new_list.append('</expression>\n')
            new_list.append('</expressionList>\n')
            new_list.append(output_line_str('symbol',')')+'\n')
            
            if(bracket==1):
                term_var = False
        elif(tokens.isdigit()):
            #will be a term if inside an expression
            if(term_var and bracket>0):
                new_list.append('<term>\n')
                new_list.append(output_line_str('integerConstant',tokens)+'\n')
                new_list.append('</term>\n')
            else:
                new_list.append(output_line_str('integerConstant',tokens)+'\n')
        elif(tokens in symbols and tokens != ',' and tokens != '}'):
            new_list.append(output_line_str('symbol',tokens)+'\n')#can never be a term also
        elif(tokens == ','):
            new_list.append('</expression>\n')#before comma there was an expression
            new_list.append(output_line_str('symbol',tokens)+'\n')
            new_list.append('<expression>\n')#after comma there's another expression

        else:#this part is for identifier, but identifier can also be inside an expression
            if(term_var and bracket>0):
                new_list.append('<term>\n')
                new_list.append(output_line_str('identifer',tokens)+'\n')
                new_list.append('</term>\n')
            else:
                new_list.append(output_line_str('identifier',tokens)+'\n')
    new_list.append(program_structure_declared_until_now.pop())
    return new_list


#for evaluating while statements
def evaluate_while_statement(line):
    list = []
    ls = splitting_everything(line)
    list.append('<whileStatement>\n')
    program_structure_declared_until_now.append('</whileStatement>\n')
    bracket_condition = False #for now it is so because no bracket has been opened
    count_bracket = 0#keeps count of number of brackets opened
    for l in ls:
        if(l in keywords):
            if(bracket_condition):
                list.append('<term>\n')
                list.append(output_line_str('keyword',l)+'\n')
                list.append('</term>\n')
            else:
                list.append(output_line_str('keyword',l)+'\n')
        elif(l in symbols):
            if(l == '('):
                #print("opening backet")
                count_bracket += 1
                bracket_condition = True
                if(count_bracket>1):
                    list.append('<term>\n')
                list.append(output_line_str('symbol','(')+'\n')
                list.append('<expression>\n')

            elif(l == ')'):
                #print("cliosing bracket")
                count_bracket-=1#no of brackets to be closed decreases
                if(count_bracket == 0):
                    #print("now all brackets are closed. so bracket_condition is False")
                    bracket_condition = False
                list.append('</expression>\n')
                list.append(output_line_str('symbol',')')+'\n')
                if(count_bracket>=1):
                    list.append('</term>\n')
            elif(l == '{'): #means this is where the line either ends or its like { do reduce(); }
                program_structure_declared_until_now.append('</statements>\n')
                list.append(output_line_str('symbol','{')+'\n')
                list.append('<statements>\n')
                if(ls.index(l) != len(ls)-1): #means line does not end with {
                    list.extend(doStatement_eval(line[line.index('{')+1:len(line)]))#evaluate the remaining statement in doStatement_eval() method
                    list.append(program_structure_declared_until_now.pop())
                    return list
            else:
                #print("other symbol")
                list.append(output_line_str('symbol',l)+'\n')#these are symbols like + - / * and so on

        elif(l.isdigit()):
            if(bracket_condition):
                list.append('<term>\n')
                list.append(output_line_str('integerConstant',l)+'\n')
                list.append('</term>\n')
            else:
                list.append(output_line_str('integerConstant',l)+'\n')
        elif(l.isidentifier()):
            if(bracket_condition):
                list.append('<term>\n')
                list.append(output_line_str('identifier',l)+'\n')
                list.append('</term>\n')
            else:
                list.append(output_line_str('identifer',l)+'\n')
    return list

def else_statement(line):
    ls = []
    words = line.split()
    for word in words:
        if(word in keywords):
            ls.append(output_line_str('keyword',word)+'\n')
        elif(word in symbols):
            ls.append(output_line_str('symbol',word)+'\n')
    return ls

def eval_if_statement(line):
    list = []
    ls = splitting_everything(line)
    list.append('<ifStatement>\n')
    program_structure_declared_until_now.append('</ifStatement>\n')
    bracket_condition = False #for now it is so because no bracket has been opened
    count_bracket = 0#keeps count of number of brackets opened
    for l in ls:
        if(l in keywords):
            if(bracket_condition):
                list.append('<term>\n')
                list.append(output_line_str('keyword',l)+'\n')
                list.append('</term>\n')
            else:
                list.append(output_line_str('keyword',l)+'\n')
        elif(l in symbols):
            if(l == '('):
                #print("opening backet")
                count_bracket += 1
                bracket_condition = True
                if(count_bracket>1):
                    list.append('<term>\n')
                list.append(output_line_str('symbol','(')+'\n')
                list.append('<expression>\n')

            elif(l == ')'):
                #print("cliosing bracket")
                count_bracket-=1#no of brackets to be closed decreases
                if(count_bracket == 0):
                    #print("now all brackets are closed. so bracket_condition is False")
                    bracket_condition = False
                list.append('</expression>\n')
                list.append(output_line_str('symbol',')')+'\n')
                if(count_bracket>=1):
                    list.append('</term>\n')
            elif(l == '{'): #means this is where the line either ends or its like { do reduce(); }
                program_structure_declared_until_now.append('</statements>\n')
                list.append(output_line_str('symbol','{')+'\n')
                list.append('<statements>\n')
                if(ls.index(l) != len(ls)-1): #means line does not end with {
                    list.extend(doStatement_eval(line[line.index('{')+1:len(line)]))#evaluate the remaining statement in doStatement_eval() method
                    list.append(program_structure_declared_until_now.pop())
                    return list
            else:
                #print("other symbol")
                list.append(output_line_str('symbol',l)+'\n')#these are symbols like + - / * and so on

        elif(l.isdigit()):
            if(bracket_condition):
                list.append('<term>\n')
                list.append(output_line_str('integerConstant',l)+'\n')
                list.append('</term>\n')
            else:
                list.append(output_line_str('integerConstant',l)+'\n')
        elif(l.isidentifier()):
            if(bracket_condition):
                list.append('<term>\n')
                list.append(output_line_str('identifier',l)+'\n')
                list.append('</term>\n')
            else:
                list.append(output_line_str('identifer',l)+'\n')
        #where should I add the condition that checks if l=='{' is the ls[len(ls)-1],i.e, the last element of the list that has everything seperated
    return list

def eval_class_dec(line):
    #words = line.split()
    words = splitting_everything(line)
    to_be_returned_to_writing = []
    program_structure_declared_until_now.append('</class>\n')
    to_be_returned_to_writing.append('<class>\n')
    for word in words:
        if word in keywords:
            to_be_returned_to_writing.append(output_line_str('keyword','class')+'\n')
        elif word in symbols:
            to_be_returned_to_writing.append(output_line_str('symbol',word)+'\n')
        else:
            to_be_returned_to_writing.append(output_line_str('identifier',word)+'\n')
    
    return to_be_returned_to_writing
    #done with defining a method for 'class' lines I guess
    
def class_var_dec(line): #something like field Square square; || field int direction;
    words = line.split() #also handles field int x, y;
    output_lines = []
    program_structure_declared_until_now.append('</classVarDec>\n')
    output_lines.append('<classVarDec>\n')
    for word in words:
        if word in keywords:
            output_lines.append(output_line_str('keyword',word)+'\n') #should take care of the field or static keyword in the beginning of the sentence
        elif ';' in word:
            output_lines.append(output_line_str('identifier',word[0:len(word)-1])+'\n') #takes care of the _square_ in --field Square square;--
            output_lines.append(output_line_str('symbol',word[len(word)-1:len(word)])+'\n') #takes care of _;_ in --field Square square;--
        
        elif ',' in word:
            output_lines.append(output_line_str('identifier',word[0:len(word)-1])+'\n')#helps in handling if there are multiple variables... handles 'x'
            output_lines.append(output_line_str('symbol',word[len(word)-1:len(word)])+'\n')#handles ','
        
        else:
            output_lines.append(output_line_str('identifier',word)+'\n') #takes care of _Square_ in --field Square square;--
    output_lines.append(program_structure_declared_until_now.pop())#end of class variable declaration

    return output_lines #returning these lines

def eval_a_var_statement(string):
    lists = []

    words = string.split() #word should be like ['var','int','a,','b;']
    #var <datatype> <var_name>;
    #it can also be -- var <datatype> <var1>, <var2>, var3>;
    program_structure_declared_until_now.append('</VarDec>\n')
    lists.append('<VarDec>\n')
    for parts in words:#parts are var int a; b;
        if(parts in keywords):
            lists.append('<keyword>'+parts+'</keyword>\n')
        if(',' in parts):#should take care of a in a,
            lists.append('<identifier>'+parts[0:len(parts)-1]+'</identifier>\n')
        if(';' in parts):#should take care of a in a;
            lists.append(output_line_str('symbol',parts[0:len(parts)-1])+'\n')
        for alphabets in parts:#alphabets are a ; || v a r || i n t || a ,
            if(alphabets in symbols):
                lists.append(output_line_str('symbol',alphabets)+'\n')
    lists.append(program_structure_declared_until_now.pop())
    return lists

def subroutine_dec(line):#this can be method int getNumerator() { return numerator; } || function int gcd(int a, int b, int c) { ||
    #method Fraction plus(Fraction other) { || constructor Fraction new(int x, int y) {
    output_lines = []
    parameterList = []
    words = line.split()

    if line.index(')') - line.index('(') == 1:#empty parameterLiist, so ignore
        pass
    else:
        parameterList = line[line.index('(')+1:line.index(')')].split(',')#else save the elements in the parameterList in a seperate list
    for i in range(1,len(parameterList),2):
        parameterList.insert(i,',')#inserting the commas between each element
    if (len(parameterList)==1 or 2):
        pass
    else:
        parameterList.insert(len(parameterList)-1,',')

    for word in words:
        if(word in keywords) and words.index(word)==0:
            output_lines.append(output_line_str('keyword',word)+'\n') #this should be 'method'||'function'||'constructor'
        elif word in symbols:
            if(word == '{'):  #this was originally meant for {
                program_structure_declared_until_now.append('</subroutineBody>\n') #subroutineBody is declared before tokenizing the symbol
                output_lines.append('<subroutineBody>\n')#including <subroutineBody>
            output_lines.append(output_line_str('symbol',word)+'\n')#now we tokenize the symbol
        elif '(' in word and ')' in word: #this means the element is something like main() or display(2)
            method_name = word[0:word.index('(')]
            output_lines.append(output_line_str('identifier',method_name)+'\n') #tokenizes the method name --main||draw
            output_lines.append(output_line_str('symbol','(')+'\n')#the opening bracket in a method, constructor, or function declaration
            if(word.index(')')-word.index('(')==1):#if the word was main()
                output_lines.append(output_line_str('parameterList',' ')+'\n') #then we can show that the parameterList is empty
                output_lines.append(output_line_str('symbol',')')+'\n')#and we can tokenise the closing bracket as well
        elif '(' in word:
            #this elif condition has to deal with plus(Fraction
            subroutine_name = word[0:word.index('(')] #this is -- plus||new||gcd
            output_lines.append(output_line_str('identifier',subroutine_name)+'\n')# plus||new||gcd
            output_lines.append(output_line_str('symbol','(')+'\n')#the opening bracket in a method, constructor, or function declaration
            #why not deal with the parameterList in this elif condition itself?
            program_structure_declared_until_now.append('</parameterList>\n')
            output_lines.append('<parameterList>\n')
            for parameter in parameterList:
                if(parameter==','):
                    output_lines.append(output_line_str('symbol',',')+'\n')
                else:
                    two_parts = parameter.split()
                    for part in two_parts:
                        if(part in keywords):
                            output_lines.append(output_line_str('keyword',part)+'\n') #deals with the int part in the parameterList
                        else:
                            output_lines.append(output_line_str('identifier',part)+'\n')#because in subroutine declarations, we don't give integer or string parameters
            output_lines.append(program_structure_declared_until_now.pop())
            
        elif ')' in word:
            #has to deal with other)
            #now that all the parameters have been dealt with, we can just tokenize the closing bracket )
            output_lines.append(output_line_str('symbol',')')+'\n')
    output_lines.insert(1,output_line_str('identifier',words[1]))#this tokenizes 'Fraction'||'int' --the 2nd word in the line
    return output_lines

#tokenizing them
for line in lines:
    words = line.split()
    try:
        if(words[0]=='var'):
            #print(str(line_no)+" --> "+ words[0])
            writing.extend(eval_a_var_statement(line))
        elif((words[0]=='field') or (words[0] == 'static')):
            #print(str(line_no)+" --> "+ words[0])
            writing.extend(class_var_dec(line))       
        elif(words[0]=='let'):
            writing.extend(letStatement_eval(line))
        elif(words[0]=='do'):
            writing.extend(doStatement_eval(line))
        elif(words[0]=='method') or (words[0]=='function') or (words[0]=='constructor'):
            writing.extend(subroutine_dec(line))
        elif(words[0]=='class'):
            #print("found a class declaration") --its not coming here
            writing.extend(eval_class_dec(line))
        elif(words[0]=='while'):
            writing.extend(evaluate_while_statement(line))
        elif(words[0]=='if'):
            writing.extend(eval_if_statement(line))
        elif(words[0] == '}'):
            writing.append(output_line_str('symbol','}')+'\n')
            writing.append(program_structure_declared_until_now.pop())
        elif(words[0]=='else'):
            writing.extend(else_statement(line))
        elif(words[0] == 'return') or (words[0] == 'return;'):
            writing.extend(returnStatement_eval(line))
    except:
        #print("empty line")
        pass
    line_no+=1
    #print(words)

with open('/home/sameer/Documents/VS_Code_related/py_files/new.xml','w') as file_writer:
    file_writer.writelines(writing)
    file_writer.close()
