import os
from tokenizer import*

written_lines = []

#OS_functions = ['Math','Output','Keyboard','Sys','Array','String','Screen','Memory']
return_datatype = []#in the first pass, every time the code goes through a function declaration, it can store the function name and the return datatype
file_reader = open('/home/admin/Documents/VS_Code_related/py_files/Main.jack','r')
lines = file_reader.readlines()#will parse the lines from Main.jack in Square
var_names = []
method_names = []
function_names = []
constructor_names = []
line_count = 0
program_brackets = 0

programStructures_declaration_keywords = ['function','constructor','method']
var_declaration_keywords = ['var','field','static']
other_statement_keywords = ['return','let','do']
loop_statement_keywords = ['while','if','else']

def is_char(word):
    if("'" in word):
        return True
    else:
        return False

def is_stringConstant(word):
    if('"' in word):
        return True
    else:
        return False

datatype = ['int','String','char','boolean','Array','void']
'''
should have the names of the `methods`, `functions`, `variables`, and the `class_name` ready

The parser can go through 2 passes:

1st pass) takes the method, functions, varaible names  ( _`class name is stored anyways`_ )

2nd pass) while evaluating the code, check if the methods, functions, or variables are called and used properly
'''

for line in lines:#removing comments before the 1st pass
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
'''
this is the first pass
'''
for line in lines: 
    try:
        words = splitting_everything(line)
        if('{' in words):
            program_brackets+=1
        if('}' in words):
            program_brackets-=1
        if(words[0] in var_declaration_keywords):
            #print("it is a variable declaration")            
            if(len(words) == 4):
                #print("only 1 variable is declared")
                if(words[2].isidentifier()):
                    var_names.append(words[2])
                    #print(words[2]+"--its length is "+len(words[2]))
            else:
                for j in range(2,len(words)-1,2):
                    var_names.append(words[j])
        elif(words[0]=='method'):
            if(words[1] not in datatype):
                print("line number "+line_count+": "+words[1]+" is not a valid datatype -->"+line)
            else:
                return_datatype.append(words[1])
                method_names.append(words[2])#stores the method name
            #return_datatype.append(words[1])
        elif(words[0]=='function'):
            if(words[1] not in datatype):#checks is the return type given is valid or not
                print(words[1]+" is not a valid datatype-->"+ line)
            else:
                return_datatype.append(words[1])
                #it stores the function name
                function_names.append(words[2])
        elif(words[0] == 'constructor'):
            constructor_names.append(words[2])
    except:
        pass
    line_count+=1
if(program_brackets!=0):
    print("the number of { and } didn't match.")
if('new' not in constructor_names and len(constructor_names)!=0):
    print("it is mandatory to call at least one of the constructors as _new_ ")

#print(var_names)
'''
the first pass has been completed. Its the for loop 
'''

#checks do syntax
def check_do_syntax(line):
    words = splitting_everything(line)
    while(words[0] == 'do'):
        if (words[len(words)-1] !=';'):
            print("do Statements should end with a semi-colon --> "+line)
            break
        if('.' not in line) and (words[1] not in method_names):
            print("only method names can be mentioned without calling their class names.-->"+line)
            break
        if(line.index(')')-line.index('(')!=1): #its not like (); ; its more like (x);
            for i in range(words.index('(')+1,words.index(')'),2):#checking if the parameters are identifier or integer
                if (words[i] not in var_names) or (words[i].isdigit()) or ('"' in words[i]):
                    print(" you should give appropriate arguments-->"+line)
                    break
    if('.' in line and words[1]+'.jack' in os.listdir(os.getcwd())):#if this is statisfied then it means that the class called is in the same folder as the current running one
        pass
    else:
        print("the class called is not in the same folder as the currently evaluated file-->"+line)
    return

def check_class(line):
    global class_name
    words = splitting_everything(line)
    for i in words:
        if i == 'class':
            if words[words.index(i)+2] != '{':
                print("there should be a { -->"+line)
                break
            elif(words[words.index(i)+1]+'.jack' not in os.listdir(os.getcwd)):
                print("Are the name of the file and this class name the same?")
        else:
            class_name = words[1]
    return

def constructor_eval(line):
    words = splitting_everything(line)
    for i in words:
        if(i == class_name and words.index(i)!=1):
            print("constructor should have the same name as the class -->"+line)
            break
    return

def if_syntax_evaluate(line):
    words = splitting_everything(line)
    
    while(words[0]=='if'):
        if(words[1]=='('):
            if (words[len(words)-2] !=')' and words[len(words)-1] == '{'):
                    print("The opening bracket --(-- for the overall expression does not have a closing bracket -->"+line)
                    break
            else:
                if (words[len(words)-1] !="{"):
                    print("there has to be an opening braces --{-- for the if condition -->"+line)
                    break
        else:
            print("After _if_ keyword, there has to be an opening bracket-->"+line)
            break
    return

def checking_while_syntax(line):
    words = splitting_everything(line)
    while(words[0]=='while'):
        if(words[1]=='('):
            if (words[len(words)-2] !=')' and words[len(words)-1] == '{'):
                    print("The opening bracket --(-- for the overall expression does not have a closing bracket-->"+line)
                    break
            else:
                if (words[len(words)-1] !="{"):
                    print("there has to be an opening braces --{-- for the while condition-->"+line)
                    break
        else:
            print("After _while_ keyword, there has to be an opening bracket-->"+line)
            break
    return

def evaluting_else_syntax(line):
    words = splitting_everything(line)
    while(words[0]=='else'):
        if(len(words)==2):
            if(words[1] != '{'):
                print("there should be a opening curly braces after keyword <else> -->"+line)
                break
        else:
            print("Else statements always go like this -- else {-->"+line)
            break
    return

def check_return_syntax(line):
    words = splitting_everything(line)
    while(words[0]=='return'):
        if(words[len(words)-1]!=';'):
            print("the return statement should end with a semi-colon -->"+line)
            break
        elif(return_datatype[len(return_datatype)-1] == 'int'):
            if ~(words[1].isdigit()):
                print("the data that is being returned must be of integer datatype-->"+line)
                break
        if(return_datatype[len(return_datatype)-1] == 'String'):
            if ~(is_stringConstant(words[1])):
                print("the data that is being returned must of string datatype-->"+line)
                break
        if(return_datatype[len(return_datatype)-1] == 'char'):
            if ~(is_char(words[1])):
                print("the datatype to be returned is char-->"+line)
                break
            
        if(return_datatype[len(return_datatype)-1] == 'boolean'):
            if(words[1] != 'true' or words[1] != 'false'):
                print("datatype to be returned is bool-->"+line)
                break

        if(return_datatype[len(return_datatype)-1] == 'void'):
            if (len(words)!=2 and words != ['return',';']):
                print("you dont have to return antything since the datatype to be returned is void-->"+line)
                break
    return

def let_syntax_checking(line):
    words = splitting_everything(line)
    while(words[0] == 'let'):
            if(words[len(words)-1]!=';'):#checking for the semi-colon at the end of the line
                print("let statements should end with semicolon -->"+line)
                break
            else:
                if words[1] not in var_names:
                    print("after <let> keyword, there should be an identifier. This variable "+words[1]+" is not declared-->"+line)
                    break
                if(words[2] == '='):#if it is somethigng like --let x = x + 1;--this if condition checks for the '=' 
                    for i in range(3,len(words)-1,2):#this checks at the alternate places, starting from x
                        if (words[1].isidentifier() or (words[i].isidentifier() or words[i].isalpha() or is_stringConstant(words[i]) or is_char(words[i]) or words[i].isdigit())):
                            pass
                        else:
                            print("the right identifier or the right values aren't being given-->>"+words[i]+" in line-->"+line)
                            break
    return

def var_check(line):#should check the lines with variable declarations
    words = splitting_everything(line)
    for token in words:
        if (token in var_declaration_keywords and words.index(token) != 0):
            print("first word should be _var_-->"+line)
            break
        if (token == ';' and words.index(token) != len(words)-1):
            print("the variable declaration should end with a semicolon-->"+line)
            break
        if(token in datatype and words.index(token)!=1):
            #print("give a valid datatype here -> "+line)
            print("type the datatype after the <var> keyword -->"+line)
            break
        if(len(words) == 4):#only 1 variable is declared in this case
            if (words[2].isidentifier()):
                pass
            else:
                print(words[2]+" is not a valid variable name-->"+line)
                break
        else:
            if(len(words) > 4): #means there are multiple variables
                for j in range(2,len(words)-1,2):#checks every alternate position between the datatype and the semi-colon
                    if (words[j].isidentifier()):#checks if the variables given have valid names or not
                        pass
                    else:
                        print(words[j]+" is not a valid variable name-->"+line)     
                        break   
        pass
    return

'''
now the code will be passed again. and it will be evaluated more
'''
for statement in lines:
    split_line = splitting_everything(statement)
    print(split_line)
    
    try:
        match split_line[0]:
            case 'do':
                written_lines.extend(doStatement_eval(statement))
                check_do_syntax(statement)
            case 'let':
                written_lines.extend(letStatement_eval(statement))
                let_syntax_checking(statement)
            case 'while':
                checking_while_syntax(statement)
                written_lines.extend(evaluate_while_statement(statement))
            case 'if':
                written_lines.extend(eval_if_statement(statement))
                if_syntax_evaluate(statement)
            case 'else':
                written_lines.extend(else_statement(statement))
                evaluting_else_syntax(statement)
            case 'class':
                written_lines.extend(eval_class_dec(statement))
                check_class(statement)
            case 'return':
                written_lines.extend(returnStatement_eval(statement))
                check_return_syntax(statement)
            case'constructor':
                written_lines.extend(subroutine_dec(statement))
                constructor_eval(statement)
            case 'var':
                written_lines.extend(eval_a_var_statement(statement))
                var_check(statement)
            case 'field':
                written_lines.extend(class_var_dec(statement))
                var_check(statement)
            case 'static':
                written_lines.extend(class_var_dec(statement))
                var_check(statement)
            case '}':
                written_lines.append(output_line_str('symbol','}')+'\n')
                written_lines.append(program_structure_declared_until_now.pop())
                pass
                #written_lines.append(program_structure_declared_until_now.pop())
                pass
            case 'method':
                written_lines.extend(subroutine_dec(statement))
            case 'function':
                written_lines.extend(subroutine_dec(statement))
                pass
    except:
        pass
print("Parsing completed")
print(written_lines)
#print(doStatement_eval("do reduce();"))
with open('/home/admin/Documents/VS_Code_related/py_files/output.xml','w') as file_writer:
    file_writer.writelines(written_lines)
    file_writer.close()
file_reader.close()
