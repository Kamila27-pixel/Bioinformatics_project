import numpy as np
from sklearn.ensemble import RandomForestClassifier

class DNAClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=10)

        X_train = np.array([
            [1, 10, 10, 1], [2, 12, 11, 2],
            [10, 1, 2, 11], [12, 2, 1, 10]
        ])
        y_train = np.array([1, 1, 0, 0])
        self.model.fit(X_train, y_train)

    def predict_coding(self, sequence):
        seq = sequence.upper()
        features = [seq.count('A'), seq.count('C'), seq.count('G'), seq.count('T')]
        prediction = self.model.predict([features])
        
        if prediction[0] == 1:
            return "High coding potential"
        else:
            return "Low coding potential"
