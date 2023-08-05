from spyraio.classification import ModelClassification


class DecisionTreeClassifier(ModelClassification):
    def __init__(self):
        print('hello')
    
    
    def compute_model(X_train, y_train, criterion='gini', max_depth=None, 
                      max_leaf_nodes=None):
        from sklearn.tree import DecisionTreeClassifier

        classifier = DecisionTreeClassifier(criterion=criterion, 
                                            max_depth=max_depth,
                                            max_leaf_nodes=max_leaf_nodes)
        classifier.fit(X_train, y_train)

        return classifier
    