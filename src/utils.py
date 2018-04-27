import math
import itertools
import numpy
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score


#Use this file to store functions and utils that are common to all the models

class modelutils:
    @staticmethod
    def mixture_of_experts(s_list, v_list):
        op = 0.0
        s_denom = sum([math.exp(s) for s in s_list])
        if len(v_list) == 0:
            return 0
        maxv = max(v_list)

        v_list = [v/float(maxv) for v in v_list]


        for s,v in zip(s_list, v_list):  
            confidence = math.exp(s)/float(s_denom)
            vote = None
            if v == 0.0:
                vote = 0.0
            else:
                vote = 1.0/(1 + math.exp(-v))
                
                op += (confidence * vote)
        return op


    @staticmethod
    def evaluate(model, testX, testY):
        predY = [model.predict(x) for x in testX]

        print("******************************************************************************")
        print("\t\t\t\t\tEvaluation on Test Set")
        print("******************************************************************************")
       
        print("Accuracy : ")
        print(accuracy_score(testY, predY))

        print("\nClassiifcation Scores")
        print(classification_report(testY, predY))

        print("\nConfusion Matrix")
        print(confusion_matrix(testY, predY))



        
