from random import shuffle
from sklearn import svm
import os
import numpy as np
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.externals import joblib
import re
from sklearn.neighbors import KNeighborsClassifier

Y = []
X = []
testX = []
dirname = "/Users/Tyler/Documents/GitHub/Bluetrack/data2/"

testRoots =[]
def main():
  for filename in os.listdir(dirname):
    global X,Y,testX,testRoots
    root, ext = os.path.splitext(filename)
    file = dirname + filename
    # Y.append(root);
    features = [];
    with open(file) as f:
      for line in f.readlines():
        line = line.rstrip()
        line = line.replace("(", "")
        line = line.replace(")", "")
        # print line
        # data = re.split(r',\s*(?![^()]*\))', line)
        data = list(line.split(","))[1:]
        data = map(int,data)
        if (len(data) == 18):
          features.append(data)
        elif (len(data) == 16):
          data = [-150,-150]+data
          # print data
          features.append(data)

        else: print root, data

    # print features

    shuffle(features)
    X = X + features
    roots = [root for i in xrange(len(features))]
    Y = Y + roots;
    # testX = testX + features[200:]
    # testRoots += [root for i in xrange(len(features[200:]))]
    
    # testX.append(features[200:])
  
# X = [[0], [1], [2], [3]]
# Y = ['5304 lower_left', '5304 lower_right', '5304 upper_left', '5304 upper_right']
  train_set = np.array(X)
  print train_set.shape
  # nsamples, nx, ny = x.shape
  # d2_train_dataset = x.reshape((nsamples,nx*ny))
  # print x
  # print d2_train_dataset
  # clf = svm.SVC(decision_function_shape='ovo')
  # print clf.fit(train_set, Y) 
  # predictedTest = clf.predict(testX)
  # correct = 0
  # total = 0
  # print len(testX)
  # print len(predictedTest)
  # print len(testRoots)
  # for i,pred in enumerate(predictedTest):
  #   total +=1;
  #   print i
  #   if pred == testRoots[i]:
  #     correct +=1;
  # print "correct: ",correct, "total: ",total
  # clf = NearestCentroid()
  clf = KNeighborsClassifier(n_neighbors=60, weights="distance")
  clf.fit(train_set, Y)
  # predictedTest = clf.predict(testX)
  #print clf.score(testX, testRoots);
  joblib.dump(clf, 'training.pkl') 

if __name__ == '__main__':
  main()
