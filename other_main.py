import particle
import rabinM

def main():
    space = []
    num_of_elements = 30
    key_size = 1024
    num_of_particles = 10
    C1 = 2
    C2 = 2
    W = 0.5
    Vmax = 15
    iMax = 100
    flag = False
    fitness = 1
    best_element = []
    key = []
    p = 0.8 # patamar desejado do p-valor
    print("\n___________________________Bem vindo ao gerador de chaves____________________________\n")
    key_size = int(input("\nDigite o tamanho o chave a ser gerada: "))
    num_of_elements = int(input(r"Digite o numero de elementos do espaco a ser gerado: "))
    print("\nGerando espaco...")
    space = rabinM.generateSpace(num_of_elements, key_size)
    print("\nEspaco gerado!")
    num_of_particles = int(input("\nNumero de particulas: "))
    C1 = float(input("C1: "))
    C2 = float(input("C2: "))
    W = float(input("W(coefiente de inercia): "))
    Vmax = int(input("Velocidade maxima: "))
    iMax = int(input("Numero de iteracoes maximas: "))
    flag = input("Coef. de consticao sera valido?(s/n): ")
    if flag.upper() == 'S' or flag.upper() == "SIM":
        flag = True
    else:
        flag = False
    fitness = int(input("Escolha UMA fitness ou as duas(digite 12 neste caso):\n1-frequencia\n2-runs\n\nopcao: "))
    if fitness == 12:
        fitness = [1,2]
    elif fitness == 1:
        fitness = [1]
    else:
        fitness = [2]
    pso = particle.PSO(num_of_particles, num_of_elements, C1, C2, W, Vmax, iMax, flag, fitness, p, space)
    best_element = pso.execution()
    print("Melhor elemento encntrado!! :D ")
    d = rabinM.generateDFromElement(best_element)
    key = best_element[2:4]
    key.append(d[5])
    print(key)


if __name__ == '__main__' :
    main()
    
    
    
    
