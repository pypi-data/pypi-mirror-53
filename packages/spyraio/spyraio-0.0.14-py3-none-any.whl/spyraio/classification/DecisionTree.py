from spyraio.classification import ClassificationModel


class DecisionTreeClassifier(ClassificationModel):
#    def __init__(self):
#        self.model = None
    
    
    def compute_model(X_train, y_train, criterion='gini', max_depth=None, 
                      max_leaf_nodes=None):
        
        from sklearn.tree import DecisionTreeClassifier

        classifier = DecisionTreeClassifier(criterion=criterion, 
                                            max_depth=max_depth,
                                            max_leaf_nodes=max_leaf_nodes)
        classifier.fit(X_train, y_train)
        
        return classifier
    
    
    def predict(dt, X):
        y_pred = ClassificationModel.predict_model(dt, X)
        return y_pred
    
    
    def evaluate(y_test, y_pred, accuracy=False):
        evaluate = ClassificationModel.evaluate_model(y_test, y_pred, accuracy)
        return evaluate
    
    
    def save_dot(dt, features, classes):
        from sklearn.tree import DecisionTreeClassifier, export_graphviz
#        import time
        
#        dotfilename = 'dotfile-%s.dot'%str(time.time()).split(('.'))[0]
        dotfilename = 'dotfile.dot'
        with open(dotfilename, 'w') as dotfile:
            export_graphviz(dt, out_file=dotfile, feature_names=features,
                            class_names=classes,
                             impurity=False, filled=True)
        