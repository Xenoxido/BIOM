import matplotlib.pyplot as plt
import math
import numpy as np
import sys

if __name__ == "__main__":
    if(sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        print("You should use it as: python rocExercise.py letter x / letter = {'a', 'b', 'A','B'}, x = float number")
    else:
        x_value = float(sys.argv[2])
        ###################
        #Load & processing files
        ###################
        chosen = sys.argv[1].upper()
        if(chosen == "A"):
            file_clientes = open("scoresA_clientes").readlines()
            file_impostores = open("scoresA_impostores").readlines()
        elif(chosen == "B"):
            file_clientes = open("scoresB_clientes").readlines()
            file_impostores = open("scoresB_impostores").readlines()

        C = len(file_clientes)
        I = len(file_impostores)

        scores_clientes = []
        n_clientes = []
        for i in range(C):
            n, s = file_clientes[i].split(" ")
            n_clientes.append(n)
            scores_clientes.append(s.split("\n")[0])
        scores_impostores = []
        n_impostores = []
        for i in range(I):
            n, s = file_impostores[i].split(" ")
            n_impostores.append(n)
            scores_impostores.append(s.split("\n")[0])

        ###################

        scoresToRoc = [(0.0 , "Null")]
        for i in range(C):
            scoresToRoc.append((float(scores_clientes[i]), "C"))
        for i in range(I):
            scoresToRoc.append((float(scores_impostores[i]), "I"))
        scoresToRoc.append((1.0, "Null"))
        scoresToRoc.sort()
        compressList = []
        for i,j in scoresToRoc:
            if i not in compressList:
                compressList.append(i)
        ############################
        #Plot ROC curve
        ############################
        x = []
        y = []
        fnTotales = []
        for thr in compressList:
            fp = [x for x,y in scoresToRoc if thr <= x and y == "I"] #Los que son impostores y pasan el threshold; Falsos Positivos
            fn = [x for x,y in scoresToRoc if thr > x and y == "C"] #Los que son clientes y no pasa el threshold; Falsos Negativos
            x.append(len(fp)/I)#FP
            fnTotales.append(len(fn)/C)#FN
            y.append(1-(len(fn)/C))#1-FN

        fpTotales = x
        plt.xlabel('FP')
        plt.ylabel('1-FN')    
        plt.plot(x,y)
        plt.show()

        ############################
        #Cruve Area
        ############################
        bestToWorst = [(c, "C") for c in scores_clientes]
        bestToWorst += [(i, "I") for i in scores_impostores]
        bestToWorst.sort()
        bestToWorst.reverse()
        scores_clientes.sort()
        scores_clientes.reverse()
        areaRoc = 0
        j = 0
        for i in range(len(bestToWorst)):
            if bestToWorst[i][1] == "C":
                areaRoc+= (j + 1) / (i + 1)
                j += 1
        areaRoc /= C
        print("Area Roc = ", areaRoc)


        ############################
        #FP(FN = X) y Umbral
        ############################
        FN = 0
        if x_value in fnTotales:
            FN = fnTotales.index(x_value)
        else:
            dif = 1
            for i in range(len(fnTotales)):
                if abs(fnTotales[i] - x_value) < dif:
                    dif = abs(fnTotales[i] - x_value)
                    FN = i

        print("FP(FN = X) = ", fpTotales[FN])
        print("Umbral = ", compressList[FN])

        ############################
        #FN(FP = X) y Umbral
        ############################
        FP = 0
        if x_value in fpTotales:
            FP = fpTotales.index(x_value)
        else:
            dif = 1
            for i in range(len(fpTotales)):
                if abs(fpTotales[i] - x_value) < dif:
                    dif = abs(fpTotales[i] - x_value)
                    FP = i

        print("FN(FP = X) = ", fnTotales[FP])
        print("Umbral = ", compressList[FP])

        ############################
        #FN = FP y Umbral
        ############################
        distancias = []
        for i in range(len(fpTotales)):
            distancias.append(abs(fpTotales[i] - fnTotales[i]))
        print('Umbral(FN = FP) = ', compressList[np.argmin(distancias)])

        ############################
        #D-Prime
        ############################
        nuClientes = sum([float(x) for x in scores_clientes]) / C
        nuImpostores = sum([float(x) for x in scores_impostores]) / I

        desv_clientes = 0
        for i in range(len(scores_clientes)):
            desv_clientes += pow(float(scores_clientes[i]) - nuClientes, 2)
        desv_clientes = math.sqrt(desv_clientes / C)

        desv_impostores = 0
        for i in range(len(scores_impostores)):
            desv_impostores += pow(float(scores_impostores[i]) - nuImpostores, 2)
        desv_impostores = math.sqrt(desv_impostores / C)
        d_prime = (nuClientes - nuImpostores) / math.sqrt(pow(desv_clientes, 2) + pow(desv_impostores, 2))

        print("D-Prime = ", d_prime)
 