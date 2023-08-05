from spyraio.classification import ClassificationModel


class MLPClassifier(ClassificationModel):
    
    
    def compute_model(X_train, y_train, hidden_layer_sizes=(3, 100, 3), 
                      solver='adam', activation='relu'):
        
        from sklearn.neural_network import MLPClassifier

        classifier = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, 
                      solver=solver, activation=activation)
        classifier.fit(X_train, y_train)
        
        return classifier
    
    
    def predict(dt, X):
        y_pred = ClassificationModel.predict_model(dt, X)
        return y_pred
    
    
    def evaluate(y_test, y_pred, accuracy=False):
        evaluate = ClassificationModel.evaluate_model(y_test, y_pred, accuracy)
        return evaluate