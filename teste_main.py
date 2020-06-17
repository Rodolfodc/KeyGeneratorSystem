import rabinM
import os
import particle
import json


def main():

    
    execution = 0
    #buscar pelo diretorio de execucoes, se nao existir criar um
    #* e execution eh mantido 0 se nao, execution eh atualizado
    
    if not os.path.exists("\keyGeneratorSystem"):
        os.mkdir(r"\keyGeneratorSystem")
        os.mkdir(r"\keyGeneratorSystem\system_execution")
        os.mkdir(r"\keyGeneratorSystem\generated_keys")
        os.mkdir(r"\keyGeneratorSystem\generated_spaces")
        os.mkdir(r"\keyGeneratorSystem\generated_swarms")
        os.mkdir(r"\keyGeneratorSystem\previous_settings")
        f = open(r"\keyGeneratorSystem\system_execution\exec_number.txt","w")
        aux = str(execution)
        f.write(aux)
        f.close()
    else:
        f = open(r"\keyGeneratorSystem\system_execution\exec_number.txt","r")
        aux = f.read()
        execution = int(aux)
        execution += 1
        f.close()
    del aux
    del f

##------------------------------------------------------------------------------------------------------------------------------------------------------
    
    #inicializacao com valores default
    ne   = 30
    np   = 10
    C1   = 2
    C2   = 2
    W    = 0.5
    Vmax = 15
    iMax = 500
    n    = 1024
    p    = 0.8
    flag = False
    swarm = None
    space = None
    fitness = 1
    #1-frequency test
    #2-serial test
    #3-run test 
    #4-poker test
    #5-autocorrelation test
    

##-------------------------------------------------------------------------------------------------------------------------------------------------------

    resp = input("\n\nDeseja utilizar um espaco de busca gerado anteriormente ?(s/n): ")
    if resp.upper() == 'S':
        files_list = []  #lista que contera os nomes dos arquivos do diretorio
        for roots, dirs, files in os.walk(r"\keyGeneratorSystem\generated_swarms"): # apenas eh utilizado files, que contem os nomes dos arquivos do diretorio em questao
            files_list = files  # atribuicao da lista de arquivos a variavel. como nao ha subdiretorios soh a atribuiacao eh suficiente
        if files_list:
            if files_list > 1:
                print("Os espacos arquivados sao:\n")
                i=1
                for file in files_list:  # apresentacao dos arquivos do diretorio
                    print(str(i)+"_____ "+file)
                    i += 1
                resp = input("\nInsira a opcao desejada: ")
                while(int(resp) > len(files_list)  and  int(resp) < 0):
                    resp = input("\nOpcao invalida!\nInsira uma opcao entre as dadas: ")
            else:
                resp = "1"
                print("Foi encontrado apenas um espaco arquivado")
            file = open("\\keyGeneratorSystem\\generated_spaces\\"+files_list[int(resp)-1],"r")
            #ler arquivo e atribuir ao enxame
            #**discutir sobre como deve ser arquivado o enxame, as chaves o espaco e as configuracoes, se deve pode ser tudo txt ou deve ser um tipo especifico**
            space = json.load(file)
            print("Espaco carregado!\n")
            file.close()
        else:
            print(r"Não há espacos arquivados!!!\n")

    

    

    resp = input("Deseja utilizar um enxame anteriormente gerado ?(s/n): ")
    if resp.upper() == 'S':
        files_list = []  #lista que contera os nomes dos arquivos do diretorio
        for roots, dirs, files in os.walk(r"\keyGeneratorSystem\generated_swarms"): # apenas eh utilizado files, que contem os nomes dos arquivos do diretorio em questao
            files_list = files  # atribuicao da lista de arquivos a variavel. como nao ha subdiretorios soh a atribuiacao eh suficiente
        if files_list:
            if files_list > 1:
                print("Os enxames arquivados sao:\n")
                i=1
                for file in files_list:  # apresentacao dos arquivos do diretorio
                    print(str(i)+"_____ "+file)
                    i += 1
                resp = input("\nInsira a opcao desejada: ")
                while(int(resp) > len(files_list)  and  int(resp) < 0):
                    resp = input("\nOpcao invalida!\nInsira uma opcao entre as dadas: ")
            else:
                resp = "1"
            file = open("\\keyGeneratorSystem\\generated_swarms\\"+files_list[int(resp)-1],"r")
            #ler arquivo e atribuir ao enxame
            #**discutir sobre como deve ser arquivado o enxame, as chaves o espaco e as configuracoes, se deve pode ser tudo txt ou deve ser um tipo especifico**
            swarm = json.load(file)# verificar a utilizacao do jason para swarm, tonar a classe PSO e a classe Particle serializavel para jason
            print("Enxame carregado!\n")
            file.close()
            if space and (len(space) < len(swarm)) :
                swarm = swarm[:(len(space)//2)]
                print("O enxame e maior que o espaco de busca, por padrao so se considera o numero de particulas equivalente a metade do numero de elementos")
                print("As particulas consideradas vao de 0 a ne/2 no enxame")
        else:
            print(r"Não há enxames arquivados!!!\n")


   
    resp = input("Deseja carregar uma configuracao feita anteriormente ?(s/n): ")
    if resp.upper() == 'S':
        files_list = []  #lista que contera os nomes dos arquivos do diretorio
        for roots, dirs, files in os.walk(r"\keyGeneratorSystem\previous_settings"): # apenas eh utilizado files, que contem os nomes dos arquivos do diretorio em questao
            files_list = files  # atribuicao da lista de arquivos a variavel. como nao ha subdiretorios soh a atribuiacao eh suficiente
        if files_list:
            if files_list > 1:
                print("As configuracoes encontradas sao:\n")
                i=1
                for file in files_list:  # apresentacao dos arquivos do diretorio
                    print(str(i)+"_____ "+file)
                    i += 1
                resp = input("\nInsira a opcao desejada: ")
                while(int(resp) > len(files_list)  and  int(resp) < 0):
                    resp = input("\nOpcao invalida!\nInsira uma opcao entre as dadas: ")
            else:
                resp = '1'
            file = open("\\keyGeneratorSystem\\previous_settings\\"+files_list[int(resp)-1],"r")
            #ler arquivo e atribuir ao enxame
            #**discutir sobre como deve ser arquivado o enxame, as chaves o espaco e as configuracoes, se deve pode ser tudo txt ou deve ser um tipo especifico**
            swarm = json.load(file)
            print("configuracao carregada!\n")
            file.close()
        else:
            print(r"Não há enxames arquivados!!!\n")
    else:
        resp = input("\n\nVai utilizar a configuracao default ?(s/n): ")
        if resp.upper() == 'N':
            print("\n\n\nSe nao deseja configurar um determinado parametro digite d e ele assumira o valor padrao ou , se houver, o valor carregado:\n")
            resp = input("\nNumero de elementos a serem gerados (ne): ")
            if resp.upper() != 'D' :
                ne = int(resp)
            resp = input("\nNumero de particulas do enxame (np): ")
            if resp.upper() != 'D' :
                np = int(resp)
            resp = input("\nValor do coeficiente de cognicao do enxame (C1): ")
            if resp.upper() != 'D' :
                C1 = int(resp)
            resp = input("\nValor do coeficiente social do enxame (C2): ")
            if resp.upper() != 'D' :
                C2 = int(resp)
            resp = input("\nValor do coeficiente de inercia (W): ")
            if resp.upper() != 'D' :
                W = float(resp)
            resp = input("\nO fator de constricao (F) sera valido?(s/n): ")
            if resp.upper() != 'D' :
                if resp.upper() == 'S':
                    flag = True
            resp = input("\nNumero de iteracoes maximas para o enxame: ")
            if resp.upper() != 'D' :
                iMax = int(resp)
            resp = input("\nVelocidade Maxima para o enxame: ")
            if resp.upper() != 'D' :
                Vmax = int(resp)
            resp = input("\nTamanho da chave (em bits): ")
            if resp.upper() != 'D' :
                n = int(resp)
            resp = input("\nPatamar para o fitness: ")
            if resp.upper() != 'D' :
                p = float(resp)
            print("\nQual fitness sera utilizada?\n\n  1-Teste de frequencia\n  2-Teste serial\n  3- Teste de run\n 4- Teste de Poker\n  5- Teste de autocorrelacao\n")
            resp = input("\nOpcao: ")
            if resp.upper() != 'D' :
                fitness = int(resp)
            ##falta salvar a configuracao realizada em arquivo - como sera salvo ?

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#space generation
    if not space :
        space = rabinM.generateSpace(ne, n)
        print("Espaco gerado!!\n")
#PSO execution
    pso = particle.PSO(np, ne, C1, C2, W, Vmax, iMax, flag, fitness, p, space)
    if swarm:
        pso.set_swarm = swarm
    best_key = pso.execution()#best_key contains the element with best n
    print("Chave encontrada:\n\n\n")
    print("tam = %d"%len(best_key))
    print("p = %d\n"%best_key[0])
    print("q = %d\n"%best_key[1])
    print("e = %d\n"%best_key[2])
    print("n = %d\n"%best_key[3])
    print("avaliacao = %f\n"%best_key[4])
    d = rabinM.generateDFromElement(best_key)
    print("d = "+str(d[5])+"\n")
    #verificacoes sobre o que o usuario deseja salvar e em qual formato- ainda a ser feito.
    

if __name__ == "__main__":
    main()
