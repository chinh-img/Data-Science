# Trình dự đoán gender dựa trên thông số chiều cao, cân nặng,size giày
from sklearn import tree # scikit-learn là library có nhiều cho ML
from sklearn.metrics import mean_absolute_error, accuracy_score # Sai số tuyệt đối
# [height, weight, shoe size]
X = [[181, 80, 44], [177, 70, 43], [160, 60, 83], [154,54,37],
     [166, 65, 40], [190, 90, 47], [175, 64, 39], [177, 70, 40], [159, 55, 37],
     [171,75,42], [181,85,43]]

Y = ['male', 'female', 'female', 'female', 'male', 'male', 
     'male', 'female', 'male', 'female', 'male']

clf = tree.DecisionTreeClassifier()

clf = clf.fit(X, Y)

prediction = clf.predict([[160, 60, 40], [172, 45, 32]])
# Machine Learning decistion tree based
print("Học máy dự đoán: ")
print(prediction)
# Sai số tuyệt đối của dự đoán ML
# MAE = mean_absolute_error(X, prediction)
# print(MAE)

# calculate accuracy 
true_labels = ['male', 'female']
acc = accuracy_score(true_labels, prediction) # Cần 2 labels phải có cùng length
print(acc)
