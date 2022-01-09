import copy
from optparse import OptionParser
import itertools
from colorama import Fore
W=[]
target = []
sozluk=open("turkce_kelime_listesi.txt", 'r')
sozluk=sozluk.readlines()
for i in range(len(sozluk)):
    sozluk[i]=sozluk[i][:-1]
sozluk=set(sozluk)
mylist=[]

def IsTurkish(L, allowPrint=False):
    numberofspaces=L.count(' ')
    A=makelist(L,allowPrint)
    global B
    A=sum(A,[])
    for i in range(len(A)):
        A[i]=A[i].lower()
        A[i]=A[i].replace('λ',' ')
        for l in range(numberofspaces):
            try:
                if A[i][-1]==' ':
                    A[i]=A[i][:-1]
                elif A[i][0]==' ':
                    A[i]=A[i][1:]
            except:
                pass
    B=[]
    A=set(A)

    for word in A:
        if word in sozluk and len(word)>1:
            W.append(word)
            B.append(Fore.GREEN + str(word) + Fore.RESET)
        else:
            B.append(Fore.RED + str(word) + Fore.RESET)
    B.sort()
    B=list(sorted(B,key=len))
    if allowPrint:
        print(', '.join(str(item) for item in B))
    global mylist
    mylist=[]
    A=list(A)
    return A,W,3

def makelist(L,allowPrint):
    global mylist
    letters=letterslist(L,allowPrint)
    combinations(target,letters)
    mylist=permutate(mylist)
    return mylist

def letterslist(L,allowPrint):
    letters=[]
    for letter in L:
        letter=letter.replace(' ', 'λ')
        if not letter.isalpha() and letter != 'λ':
            try:
                for i in range(int(letter[1:])):
                    letters.append(letter[:1])
            except:
                if allowPrint:
                    print('Hocam biraz da insaf lütfen!')
                else:
                    pass
        else:
            letters.append(letter)
    return letters

def combinations(target,data):
    for i in range(len(data)):
        new_target = copy.copy(target)
        new_data = copy.copy(data)
        new_target.append(data[i])
        new_data = data[i+1:]
        global mylist
        mylist.append(str(new_target))
        combinations(new_target,new_data)
    for i in range(len(mylist)):
        mylist[i]=mylist[i].replace('[','')
        mylist[i]=mylist[i].replace(']','')
        mylist[i]=mylist[i].replace('\'','')
        mylist[i]=mylist[i].replace(',','')
        mylist[i]=mylist[i].replace(' ','')


def permutate(L):
    empty=[]
    for word in L:
        string_permutations = itertools.permutations(word)
        string_permutations = list(string_permutations)
        string_permutations = [''.join(permutation) for permutation in string_permutations]
        empty.append(string_permutations)
    return empty


if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    W,A,x=IsTurkish(args,allowPrint=True)
