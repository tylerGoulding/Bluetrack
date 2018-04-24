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
testRoots =[]
dirname_tyler = "/Users/Tyler/Documents/GitHub/Bluetrack/data3/"
dirname_fatema = "C:\\Users\\Fatema Almeshqab\\Desktop\\Bluetrack\\data3\\"

# if platform.system() == 'Darwin':
#   dirname = dirname_tyler
# else:
#   dirname = dirname_fatema

valid_types = ['region','room','region_given_room']
  
def generateSets(dataDict, type = "region"):
  trainX = []
  trainY = []
  testX  = []
  testY  = []
  for position in dataDict.keys():
    if type == 'region':
      data_pos = position;
    elif type == 'room':
      data_pos = position.split("_")[0]

    data = dataDict[position];
    shuffle(data);
    print position
    for i,moment in enumerate(data):
      # print i
      # print moment
      feat = []
      if [] in moment:
        continue
      else:
        for nodeRSSI in moment:
            # nodeRSSI = np.array(nodeRSSI);
            mean    = np.mean(nodeRSSI);
            minRSSI = min(nodeRSSI);
            maxRSSI = max(nodeRSSI);
            var     = np.var(nodeRSSI);
            mode    = stats.mode(np.array(nodeRSSI));      
            feat += [mean, minRSSI, maxRSSI, var, int(mode[0])];
        # print len(feat) # should be 30 features long
        # print feat
        if (i < 50):
          trainX.append(feat);
          trainY.append(position);
        else:
          testX.append(feat);
          testY.append(position);

testRoots =[]
def main():
  for filename in os.listdir(dirname_fatema):
    global X,Y,testX,testRoots
    root, ext = os.path.splitext(filename)
    file = dirname_fatema + filename
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
  X, Y, testX, testY = generateSets(rawData);
  print len(X)
  train_set = np.array(X)
  # print train_set
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
  # clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(11,4), random_state=1)
  clf = NearestCentroid();
  clf.fit(train_set, Y);
  print clf.score(testX,testY)
  
  clf = KNeighborsClassifier(n_neighbors=60, weights="distance")
  clf.fit(train_set, Y)
  predictedTest = clf.predict(testX)
  correct = 0
  total = 0
  print clf.score(testX,testY)
  # print len(testX)
  # print len(predictedTest)
  # print len(testRoots)
  # for i,pred in enumerate(predictedTest):
  #   total +=1;
  #   print i
  #   if pred == testRoots[i]:
  #     correct +=1;
    # total +=1;
    # print i
    # if pred == testRoots[i]:
      # correct +=1;
  # print "correct: ",correct, "total: ",total
  # clf = NearestCentroid()
  clf = KNeighborsClassifier(n_neighbors=60, weights="distance")
  clf.fit(train_set, Y)
  # print clf.score()
  joblib.dump(clf, 'training.pkl') 
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
