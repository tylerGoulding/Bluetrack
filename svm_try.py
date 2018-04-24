from random import shuffle
from sklearn import svm
import os
import numpy as np
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


Y = []
X = []
testX = []
testroots = []
dirname = "C:\\Users\\Fatema Almeshqab\\Desktop\\Bluetrack\\data\\"
for filename in os.listdir(dirname):
    root, ext = os.path.splitext(filename)
    file = dirname + filename
    # Y.append(root);
    features = [];
    with open(file) as f:
      for line in f.readlines():
        line = line.rstrip()
        data = list(line.split(","))[1:]
        data = map(int,data)
        features.append(data)
    # print features
    shuffle(features)
    X = X + features[:200]
    roots = [root for i in xrange(200)]
    Y = Y + roots;
    testX = testX + features[200:]
    testroots += [root for i in xrange(len(features[200:]))]
    # testX.append(features[100:])
    
# X = [[0], [1], [2], [3]]
# Y = ['5304 lower_left', '5304 lower_right', '5304 upper_left', '5304 upper_right']
train_set = np.array(X)
clf = svm.SVC();
clf.fit(train_set, Y) 
predicted_values =  clf.predict(testX);
print clf.score(testX, testroots);

clf = NearestCentroid()
clf.fit(train_set, Y)
predicted_values =  clf.predict(testX);

#for predicted_val in predicted_values:
#    print predicted_val;
print clf.score(testX, testroots);

neigh = KNeighborsClassifier()
neigh.fit(train_set, Y);
predicted_values =  neigh.predict(testX);
print neigh.score(testX, testroots);

logreg = LogisticRegression(multi_class='multinomial', solver='newton-cg');
logreg.fit(train_set, Y)
print logreg.score(testX, testroots)

clf = DecisionTreeClassifier().fit(train_set, Y);
print clf.score(testX, testroots);

lda = LinearDiscriminantAnalysis()
lda.fit(train_set, Y);
print lda.score(testX, testroots);



# correct = 0
# total = 0
# count = 0
# for i,pred in enumerate(predicted_values):
#     total +=1;
#     if pred == testroots[i]:
#         correct +=1;
#     elif ((pred[0:4]==testroots[i][0:4]) and (pred[5:10]!=testroots[i][5:10])):
#         count += 1;
#         print pred, testroots[i];
#     elif (pred[0:4]!=testroots[i][0:4]):
#         count += 1;
#         print pred, testroots[i];

# print "correct: ",correct, "total: ",total
# print count 
# print correct/float(total);
# print total - correct - count;
# print count/float(total);
