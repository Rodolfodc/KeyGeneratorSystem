
import random
from math import sqrt


# http://inventwithpython.com/hacking/chapter23.html
# http://inventwithpython.com/hacking/

def rabinMiller(num):

     #divisao por tentativas para "melhorar" a busca por um primo

     lowPrimes =  [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79,83, 89, 97, 101, 103, 107,
                  109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173,179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
                  233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293,307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
                  367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433,439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
                  499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,587, 593, 599, 601, 607, 613, 617, 619, 631, 641,
                  643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719,727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
                  797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863,877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
                  947, 953, 967, 971, 977, 983, 991, 997]
     
     
     for x in lowPrimes:
         if num/2 > x:
             if num % x == 0 :
                 return False
     
     
     r = num - 1
     t = 0
     while r % 2 == 0:
         r = r // 2
         t += 1

     for trials in range(50): 
         a = random.randrange(2, num - 2)
         v = pow(a, r, num)
         if v != 1: 
             i = 0
             while v != (num - 1):
                 if i == t - 1:
                     return False
                 else:
                     i = i + 1
                 v = (v ** 2) % num
     return True
    

def randPrime(keySize):
     ''' gera um primo com metade do tamanho do parametro passado '''
     # x = 1
     r = False
     
     while(r == False):
         #x = random.randrange(2**(keySize-1),2**keySize)
         x = random.getrandbits(keySize)
         if x%2 == 0 :
             x += 1
         r = rabinMiller(x)
         
     return x

def extendedEuclid(a,b):
    if b == 0:
        c = a
        x = 1
        y = 0
        ret = [c,x,y]
        return ret
    else:
        x2 = 1
        x1 = 0
        y2 = 0
        y1 = 1
        while(b > 0):
            q = a//b
            r = a%b
            x = x2 - q*x1
            y = y2 - q*y1
            a = b
            b = r
            x2 = x1
            x1 = x
            y2 = y1
            y1 = y
        c = a
        x = x2
        y = y2
        ret = [c,x,y]
        return ret

            
            
def euclid(a,b):
    while(b != 0):
        r = a%b
        a = b
        b = r
    return a
    

def giveCoPrime(x):
    a = random.randrange(1, x, 2)
    euclid(x,a)
    while(euclid(x,a) != 1):
        a = random.randrange(1, x, 2)
    return a

def generateD(phi,e):
    x = extendedEuclid(phi,e)
    return x[2]

def generateElement (keySize):
    ''' gera o elemento e devolve uma lista com [p,q,e,k]


     p-primo, q - primo, e - coprimo de phi((p-1)*(q-1)),k = p*q
     phi(k) = funcao totiente ou funcao de euler'''
    p = randPrime(keySize//2)
    q = randPrime(keySize//2)
    while(p == q):
        q = randPrime(keySize//2)
    phi = (p-1)*(q-1)
    n = p*q
    e = giveCoPrime(phi)
    element = [p,q,e,n]
    return element

def generateDFromElement(element):
    phi = (element[0]-1)*(element[1]-1)
    d = generateD(phi,element[2])
    element.append(d)
    return element

def isEqualToSomeElementFromSpace(space, element):
    if space :
        for aux in space:
            if element[3] == aux[3]:
                return True
        return False
    else:
        return False

def generateSpace(numOfElements,keySize):
    ''' Gera uma lista de elementos ou seja varios [p,q,e,k]


         exp: espaco de tamanho 3 => [[p,q,e,k],[p1,q1,e1,k1],[p2,q2,e2,k2]]'''
    space = []
    for aux in range(numOfElements):
        element = generateElement(keySize)
        while(isEqualToSomeElementFromSpace(space, element)):
               element = generateElement(keySize)
        space.append(element)
    return space

def isThereAnEqual(space):
    repeat = 0
    for aux in space:
        repeat = 0
        for aux2 in space:
            if aux == aux2:
                repeat += 1
            if repeat == 2:
                return True
    return False

def qtdlowp():
    lowPrimes =  [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79,83, 89, 97, 101, 103, 107,
                  109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173,179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
                  233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293,307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
                  367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433,439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
                  499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,587, 593, 599, 601, 607, 613, 617, 619, 631, 641,
                  643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719,727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
                  797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863,877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
                  947, 953, 967, 971, 977, 983, 991, 997]
    i = 0
    for x in lowPrimes :
        i += 1
    return (i+1)

    
