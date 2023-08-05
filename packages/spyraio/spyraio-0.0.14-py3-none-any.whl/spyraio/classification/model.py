class ClassificationModel:
    def __init__(self):
        pass

    
    def predict_model(classifier, X):
        return classifier.predict(X)
    
    
    def evaluate_model(y_test, y_pred, accuracy=False):
        from sklearn.metrics import confusion_matrix
        confusionMatrix = confusion_matrix(y_test, y_pred)
        
        dim = len(confusionMatrix[0])
        
        tcs, fcs = {}, {}
        print(confusionMatrix[0][0])
        
        for x in range(dim):
            tcs['class%d'%(x+1)] = 0
            fcs['class%d'%(x+1)] = 0
            for y in range(dim):
                if x == y:
                    tcs['class%d'%(x+1)] += confusionMatrix[x][y]
                else:
                    fcs['class%d'%(x+1)] += confusionMatrix[x][y]
        
        result = {}        
        for key in tcs.keys():
            result[key] = (tcs[key]/(tcs[key]+fcs[key]))*100
#            print('Accuracy for %s: %.2f'%(key, result[key]))
        
        sumt, sumf = sum(list(tcs.values())), sum(list(fcs.values()))
        result['total'] = sumt/(sumt+sumf)*100
        
        if accuracy:
            return confusionMatrix, result 
        return confusionMatrix
        

        