from random import shuffle
from sklearn import svm
import os
import numpy as np
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.externals import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
Y = []
X = []
testX = []
testRoots =[]
dirname = "/Users/Tyler/Documents/GitHub/Bluetrack/data2/"
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
          data.append(data[2]-data[0]);

          # data.append(data[1]-data[0]);          
          features.append(data)

        elif (len(data) == 16):
          data = [-150,-150]+data + [0]
          # print data
          features.append(data)

        else: print root, data

        # print data
        # features.append(data)
    # print features
    shuffle(features)

    X = X + features[:30]
    roots = [root for i in xrange(30)]
    Y = Y + roots;
    testX = testX + features[30:]
    testRoots += [root for i in xrange(len(features[30:]))]
    
    # testX.append(features[200:])
    

# X = [[0], [1], [2], [3]]
# Y = ['5304 lower_left', '5304 lower_right', '5304 upper_left', '5304 upper_right']
  # print len(X)
  # print len(Y)
  train_set = np.array(X)
  print train_set.shape
  # nsamples, nx, ny = x.shape
  # d2_train_dataset = x.reshape((nsamples,nx*ny))
  # print x
  # print d2_train_dataset
  # clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(11,4), random_state=1)
  clf = KNeighborsClassifier(n_neighbors=60, weights="distance")
  clf.fit(train_set, Y)
  predictedTest = clf.predict(testX)
  correct = 0
  total = 0
  print clf.score(testX,testRoots)
  # print len(testX)
  # print len(predictedTest)
  # print len(testRoots)
  # for i,pred in enumerate(predictedTest):
  #   total +=1;
  #   # print i
  #   if pred == testRoots[i]:
  #     correct +=1;
  # print "correct: ",correct, "total: ",total
  # clf = NearestCentroid()
  # clf.fit(train_set, Y)

  # predictedTest = clf.predict(testX)
  # correct = 0
  # total = 0
  # print len(testX)
  # print len(predictedTest)
  # print len(testRoots)
  # for i,pred in enumerate(predictedTest):
  #   total +=1;
  #   # print i
  #   if pred == testRoots[i]:
  #     correct +=1;
  #   else:
  #     print pred,"|||" ,testRoots[i]
  # print "correct: ",correct, "total: ",total
if __name__ == '__main__':
  main()
