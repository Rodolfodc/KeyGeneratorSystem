import random
import math

class Fitness:
    def __init__(self, choice = [1], p = 0.8):
        self.choice = choice
        self.num_of_choices = len(choice)
        self.key = None
        self.key_size = 1024 # apenas inicializa com um valor, depois sera alterado para o tamnho da chave em si 
        self.n0 = 0
        self.n1 = 0
        #self.ret_p_value = 0.1
        self.p = p
        #self.returnable_p_value  = None

    def calculate(self, key):
        self.key = (bin(key))
        self.key = self.key[2:]
        self.key_size = len(self.key)
        return self.choose_and_execute_tests()
    

    def choose_and_execute_tests(self):
        if self.num_of_choices == 1:
            if self.choice[0] == 1 :
                return self.frequency_test()
            elif self.choice[0] == 2 :
                return self.runs_test()
        else:
            a = self.frequency_test()
            b = self.runs_test()
            general_p_value = self.generic_p_value(a,b)
            return general_p_value

            
##        elif self.choice == 2 :
##            self.ret_p_value = self.serial_test()
##            
##        elif self.choice == 3 :
##            self.ret_p_value = self.poker_test()
##            
##            
##        else:
##            self.ret_p_value = self.autocorrelation_test()

              

    def frequency_test(self):
        self.n0 = 0
        self.n1 = 0
        for bit in self.key:
            if bit =='0':
                self.n0 += 1
        self.n1 = self.key_size - self.n0
        result = ((self.n0 - self.n1)**2) / self.key_size
        erfc_arg = abs(result)/math.sqrt(self.key_size)
        result = math.erfc(erfc_arg)
        return result

    def serial_test(self):
        for bit in self.key:
            if bit =='0':
                self.n0 += 1
        self.n1 = self.key_size - self.n0
        n00 = 0
        n01 = 0
        n10 = 0
        n11 = 0
        for i in range(self.key_size - 1):
            
            if self.key[i] == '0' :
                if self.key[i+1] == '0':
                    n00 += 1
                else:
                    n01 += 1
            else :
                if self.key[i+1] == '0':
                    n10 += 1
                else:
                    n11 += 1
##        print(n00)
##        print("\nn00 = "+str(n00)+" n01 = "+str(n01)+
##            " n10 = "+str(n10)+" n11 = "+str(n11)+"\n")
##        soma = n00**2 + n01**2 + n10**2 + n11**2
##        print("soma = " + str(soma))
##        result = ( 4 / (self.key_size-1) )*soma
##        print("primeiro membro = " + str(result))
##        result -= (2/self.key_size)*(self.n0**2 + self.n1**2)
##        print("segundo membro = " + str(result))
        result += 1
        return result


    def poker_test(self):
        m = 1
        while( self.key_size/m >= 5*(2**m) ):
            m += 1
        m -= 1
        k = self.key_size//m
        key_parts = []
        start = 0
        end = m
        type_of_substring = []
        ni = []
        
        for i in range(k): # divides the key into k subsequences of length m
            key_parts.append(self.key[start:end])
            start += m
            end += m
           # ni.append(0)
            count = 0

        for number in range(2**m):   # generate all the possible strings of legth m
            aux = bin(number) # get the binary of the number
            aux = aux[2:] # take off the "0b" that python puts in the beginning of the string
            while(len(aux) < m):
                aux = '0' + aux    # complete the binary string (str format) with what it needs to have length m
            type_of_substring.append(aux) # atributes the ganareted string to the list of strings with length m
            ni.append(0)                # add a position to ni because it need to have the same size of number of strings
            
        count = 0
        for substring in type_of_substring :    # loop to count the number of occurences of the ith string type
            for part in key_parts:
                if substring == part:           # if the substring occurs  than 
                    ni[count] += 1              # add it to the respective ni, a variable that indicates the number of occurences of the ith subsrtring
            count += 1

        result_sum = 0
        for i in range(2**m):       # loop to make the sum of all values of ni
            result_sum += (ni[i]**2)
            
        result_test = result_sum * ((2**m) / k)
        result_test -= k
        
        return result_test
        

    def runs_test(self):
        self.n0 = 0
        self.n1 = 0
        for bit in self.key:
            if bit =='1':
                self.n1 += 1
        self.n0 = self.key_size - self.n1
        pi = (self.n1 + 0.0) / (self.key_size + 0.0) #transforma em double
        if math.fabs(pi - 0.5) > (2.0 / math.sqrt(self.key_size)):
            p_value = 0.0
        else:
            V = 1
            for i in range(1,self.key_size):
                if self.key[i] != self.key[i-1] :
                    V = V + 1
            erfc_arg = (math.fabs(V - 2.0 * self.key_size * pi * (1.0-pi)) / (2.0 * pi * (1.0-pi) * math.sqrt(2.0*self.key_size)))
            p_value = math.erfc(erfc_arg)                                                                                                                               
        return p_value
        

    def autocorrelation_test(self):
        d = random.randrange(1, self.key_size)
        n_less_d = self.key_size - d
        ret = 2*( self.calculate_A_for_autocorrelation(d) - ((n_less_d/2) ) ) / math.sqrt(n_less_d)
        return ret


    def calculate_A_for_autocorrelation(self, d):
        soma = 0
        for i in range(self.key_size - d):
            soma = soma + xor(self.key[i], self.key[i+d])
        return soma   


    def generic_p_value(self,a,b):
        #c[] é o vetor a ser analisado m[] o vetor modelo
        #c[0] resultado em run, c[1] resultado em frequencia
        m = [self.p, self.p] #apenas para o teste
        c = [a, b]
        modC = math.sqrt((c[0] * c[0]) + (c[1] * c[1]))
        modM = math.sqrt((m[0] * m[0]) + (m[1] * m[1]))
        dotProd = (c[0]*m[0]) + (c[1] * m[1])
        cosseno = dotProd / (modC *modM)
        raizDedois = math.sqrt(2.00)
        PvalorFinal = modC * cosseno / raizDedois
        return PvalorFinal
    


    

def xor(a ,b):
    a = int(a)
    b = int(b)
    ret = ( ((not a) and b)   or   (a and (not b)) )
    if ret :
        return 1
    return 0


        
        
        
