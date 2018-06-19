#program reads arguments from cmd-line and returns data based on input-
#see line 99 for usages

#import moduals
import sys
import tokenize
import token
import difflib

#Returns tokens/attribues list of tuples
#Carl's Code
#http://pages.cpsc.ucalgary.ca/~aycock/231/as3/tokentest.py
def file2tokens(filename):
	try:
		f = open(filename, 'rb')
		tokens = []
		for t in tokenize.tokenize(f.readline):
			tokens.append( (token.tok_name[t.type], t.string) )
		f.close()
	except IOError:
		return None
	return tokens

#Returns float ratio 0.6+ are similar
#Carl's Code
#http://pages.cpsc.ucalgary.ca/~aycock/231/as3/difftest.py
def similarity(L1, L2):
	matcher = difflib.SequenceMatcher(None, L1, L2)
	return matcher.ratio()

#Methods

#dangerMethod
def danger(L):
    i,e,v,o,t=0,0,0,0,0
    for x in range (len(L)):
        if L[x][1]=='import':    
            i=i+1
        elif L[x][1]=='exec':
            e=e+1
        elif L[x][1]=='eval':
            v=v+1
        elif L[x][1]=='open':
            o=o+1
        elif L[x][1][0:2] and L[x][1][-2:]=='__':
            t=t+1
            m=L[x][1]
    if i>0:
        print('import *',i)
    if e>0:
        print('exec *',e)
    if v>0:
        print('eval *',v)
    if o>0:
        print('open *',o)
    if t>0:
        print(m,'*',t)
    if i<1 and e<1 and v<1 and o<1 and t<1:
        print('NO possibly malicous code found')

#for printing str only once see slide 8 https://docs.google.com/presentation/d/1-svRtTGa1ihQI6WZbhp8InqHZiKVDvV6MnTnn2TVxYo/edit#slide=id.i0
#imports Method
def imports(L):
    _modual={}
    for x in range (len(L)):
        if L[x][1]=='import' and L[x-2][1] !='from':
            modual=L[x+1][1]
            _modual[modual]=1
        elif L[x][1]=='from':
            modual=L[x+1][1]
            _modual[modual]=1
    for modual in _modual:
        print(modual)
    if (len(_modual))<1:
        print('NO imports')

#tdiff Method
def tdiff(L):
    L1=[]
    for x in range (len(L)):
        if L[x][0]== 'COMMENT' or L[x][0]== 'NL' or L[x][0]== 'NEWLINE':
            continue
        elif L[x][0]!='COMMENT' or L[x][0]!= 'NL' or L[x][0]!= 'NEWLINE':
            L1.append(L[x][0])
    return L1

#adiff Method
def adiff(L):
    L1=[]
    for x in range (len(L)):
        if '#' in L[x][1] or L[x][1]== '\n':
            continue
        elif ('#' not in L[x][1] or L[x][1]!= '\n'):
            L1.append(L[x][1])
    return L1

#error checking and calling method functions
#XXX changing order changes priority of error msg printed.i.e: number of files-
#message priority over token failed message

#usage error message
methods=['danger','tdiff','imports','adiff']
error='Wrong number of files'
if len(sys.argv) == 1 or (sys.argv[1]) not in methods :
    print('Usage:\t',
          'python3 as3.py danger file.py\n\t',
          'python3 as3.py tdiff file1.py file2.py\n\t',
          'python3 as3.py imports file.py\n\t',
          'python3 as3.py adiff file1.py file2.py')
    sys.exit()
#if wrong # of files print error message
if (sys.argv[1]) == 'danger' and len(sys.argv) != 3:
    print(error)
    sys.exit()
elif (sys.argv[1]) == 'tdiff' and len(sys.argv) != 4:
    print(error)
    sys.exit()
elif (sys.argv[1]) == 'imports' and len(sys.argv) != 3:
    print(error)
    sys.exit()
elif (sys.argv[1]) == 'adiff' and len(sys.argv) != 4:
    print(error)
    sys.exit()
#tokenization fails for input file
if len(sys.argv)==3 and file2tokens(sys.argv[2]) == None:
    print('Error: Tokenization Failed / file does not exist')
    sys.exit()
elif len(sys.argv)==4 and file2tokens(sys.argv[2]) == None or len(sys.argv)==4 and file2tokens(sys.argv[3]) ==None:
    print('Error: Tokenizaton Failed / file does not exist')
    sys.exit()

#imports call and file2tokens call
if sys.argv[1] =='imports':
    E=file2tokens(sys.argv[2])
    imports(E)

#danger call and file2tokens call
elif sys.argv[1] == 'danger':
    P=file2tokens(sys.argv[2])
    danger(P)

#tdiff call and all relevant functions
elif sys.argv[1] == 'tdiff':
    A=file2tokens(sys.argv[2])
    L1=tdiff(A)
    B=file2tokens(sys.argv[3])
    L2=tdiff(B)
    S=(similarity(L1,L2))
    if S>=0.6:
        print('files are similar','=>',S)
    elif S<0.6:
        print('files are not similar','=>',S)

#adiff call and all relevant functions
elif sys.argv[1] == 'adiff':
    A=file2tokens(sys.argv[2])
    L1=adiff(A)
    B=file2tokens(sys.argv[3])
    L2=adiff(B)
    S=(similarity(L1,L2))
    if S>=0.6:
        print('files are similar','=>',S)
    elif S<0.6:
        print('files are not similar','=>',S)
#XXX Print() on adiff and tdiff not part of function because of return statement-
#and ease(Mabey try to move??? into function).
#End of program


    
