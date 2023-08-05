from spyraio.classification import ClassificationModel


class SVMClassifier(ClassificationModel):
#    def __init__(self):
#        self.model = None
    
    
    def compute_model(X_train, y_train, kernel='rbf', degree=3, gamma='scale'):
        
        from sklearn.svm import SVC

        classifier = SVC(kernel=kernel, degree=degree, gamma=gamma)
        classifier.fit(X_train, y_train)
        
        return classifier
    
    
    def predict(dt, X):
        y_pred = ClassificationModel.predict_model(dt, X)
        return y_pred
    
    
    def evaluate(y_test, y_pred, accuracy=False):
        evaluate = ClassificationModel.evaluate_model(y_test, y_pred, accuracy)
        return evaluate