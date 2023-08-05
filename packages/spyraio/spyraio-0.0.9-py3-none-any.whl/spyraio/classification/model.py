class ClassificationModel:
    def __init__(self):
        pass

    
    def predict_model(classifier, X):
        return classifier.predict(X)
    
    
    def evaluate_model(y_test, y_pred):
        from sklearn.metrics import confusion_matrix
        confusionMatrix = confusion_matrix(y_test, y_pred)
        
        return confusionMatrix

        