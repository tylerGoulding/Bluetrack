from random import shuffle
from sklearn import svm
import os
import numpy as np
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.externals import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
import platform
import re
from scipy import stats
import ast
from sklearn.svm import SVC
from collections import Counter 


#### facilitate programming between Project Memebers
dirname_tyler = "/Users/Tyler/Documents/GitHub/Bluetrack/data3/"
dirname_fatema = "C:\\Users\\Fatema Almeshqab\\Desktop\\Bluetrack\\data3\\"
if platform.system() == 'Darwin':
  dirname = dirname_tyler
else:
  dirname = dirname_fatema

mac_list = ["b8:27:eb:b6:43:f8", "b8:27:eb:d3:4c:7f","b8:27:eb:cd:4b:81","b8:27:eb:ee:32:b8","b8:27:eb:e7:50:37","b8:27:eb:63:a1:e3"]
Y = []
X = []
testX = []
testRoots =[]

# Validity checks
valid_types = ['region','room','region_given_room']
valid_rooms = ['5300','5302','5304']
  
def generateSets(dataDict, granularity = "region",ignore_node=-1, room = ""):

  if granularity not in valid_types:
    return -1;
  if (granularity == 'region_given_room') and room not in valid_rooms:
    return -1;
  trainX = []
  trainY = []
  testX  = []
  testY  = []
  testY_full =[]

  for position in dataDict.keys():
    if granularity == 'region':
      data_pos = position;
    elif granularity == 'room':
      data_pos = position.split("_")[0]
    else:
      data_pos = position;

    data = dataDict[position];
    shuffle(data);
    for i,moment in enumerate(data):
      feat = []
      if [] not in moment:
        for j, nodeRSSI in enumerate(moment):
          if (j == ignore_node):
            continue;
          mean    = np.mean(nodeRSSI);
          median  = np.median(nodeRSSI);
          minRSSI = min(nodeRSSI);
          maxRSSI = max(nodeRSSI); 
          feat += [mean , median]
        if (i < 50):
          trainX.append(feat);
          trainY.append(data_pos);
        else:
          testX.append(feat);
          testY.append(data_pos);
          testY_full.append(position);
  return trainX, trainY, testX, testY,testY_full

def generate_room_specific_classifiers(dataDict):
  dict5300 = dict((k,dataDict[k]) for k in dataDict.keys() if "5300" in k)
  X, Y, testX, testY,_ = generateSets(dict5300);
  train_set = np.array(X)
  clf5300 = KNeighborsClassifier(n_neighbors=60, weights="distance").fit(train_set, Y); #SVC(kernel='linear', C=2).fit(train_set, Y)

  dict5302 = dict((k,dataDict[k]) for k in dataDict.keys() if "5302" in k)
  X, Y, testX, testY,_ = generateSets(dict5302);
  train_set = np.array(X)

  clf5302 =  KNeighborsClassifier(n_neighbors=60, weights="distance").fit(train_set, Y); #SVC(kernel='linear', C=2).fit(train_set, Y)
  train_set = np.array(X)

  dict5304 = dict((k,dataDict[k]) for k in dataDict.keys() if "5304" in k)
  X, Y, testX, testY,_ = generateSets(dict5304);
  train_set = np.array(X)

  clf5304 = KNeighborsClassifier(n_neighbors=60, weights="distance").fit(train_set, Y); # SVC(kernel='linear', C=2).fit(train_set, Y)
  train_set = np.array(X)

  return clf5300,clf5302,clf5304

      
def main():
  global X,Y,testX,testRoots
  rawData = {}
  regions = [];
  for filename in os.listdir(dirname):
    root, ext = os.path.splitext(filename)
    regions.append(root);
    # if (filename == "5302_middle_3.txt"): 
    #   continue
    file = dirname + filename
    features = [];
    room_level_Y = [];
    rawData[root] = [];
    with open(file) as f:
      for line in f.readlines():
        if line[0].isdigit():   
          continue;       
        else:
          parts = ast.literal_eval(line)
          parts.sort(key=lambda x: mac_list.index(x[0]))
          raw_list = [x[1] for x in parts];
          rawData[root].append(raw_list)     


  clf5300,clf5302,clf5304 = generate_room_specific_classifiers(rawData);   
  ########
  ## Testing on all 11 regions
  ########

  X, Y, testX, testY,_ = generateSets(rawData);
  train_set = np.array(X)
  # print train_set
  # clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(11,4), random_state=1)
  clf = KNeighborsClassifier(n_neighbors=60, weights="distance")
  clf.fit(train_set, Y)
  predictedTest = clf.predict(testX)
  print "knn - region"
  print clf.score(testX,testY)

  correct = 0
  total = 0
  odd = 0
  wrong_regions = []
  for i,pred in enumerate(predictedTest):
    total +=1;
    # print i
    if pred == testY[i]:
      correct +=1;
    else:
      wrong_regions.append((pred,testY[i]));
      #print pred,"|||" ,testY[i]
  print "correct: ",correct, "total: ",total
  print "wrong: ", total-correct;

  print "wrong values based on region"
  percentages = [];
  for region, true_region in set(wrong_regions):
    count = wrong_regions.count((region, true_region));
    if (count > 2):
      percentages.append(((region, true_region), count)) #/testY.count(true_region)));

  percentages.sort(key=lambda x: x[1], reverse=True);
  print percentages

  clf = SVC(kernel='linear', C=2).fit(train_set, Y)
  predictedTest = clf.predict(testX)
  print "svc - region"
  print clf.score(testX,testY)

  ########
  ## Testing on room level (3 values)
  ########
  X, Y, testX, testY, testY_full = generateSets(rawData,"room");
  train_set = np.array(X)

  clf = SVC(kernel='linear', C=2).fit(train_set, Y)
  predictedTest = clf.predict(testX)
  print "svc - room"
  print clf.score(testX,testY)

  clf = KNeighborsClassifier(n_neighbors=12, weights="distance")
  clf.fit(train_set, Y)
  predictedTest = clf.predict(testX)
  print "knn - room"
  print clf.score(testX,testY)
  correct5300 = 0
  total5300 = 0
  correct5302 = 0
  total5302 = 0
  correct5304 = 0
  total5304 = 0
  for event,result in zip(testX,testY_full):
    event = [event]
    room = clf.predict(event)[0];
    # print room
    if room == "5300":
      pred = clf5300.predict(event);
      # print pred
      # print result
      if pred == result:
        correct5300 +=1;
      total5300 +=1;
    elif room == "5302":
      pred =clf5302.predict(event);
      if pred == result:
        correct5302 +=1;
      total5302 +=1;
    elif room == "5304":
      pred = clf5304.predict(event);
      if pred == result:
        correct5304 +=1;
      total5304 +=1;

  print "---------------"
  print "5300"
  print "correct: ",correct5300, "total: ",total5300
  print "accuracy: ", correct5300*100/float(total5300)
  print "---------------"
  print "5302"
  print "correct: ",correct5302, "total: ",total5302
  print "accuracy: ", correct5302*100/float(total5302)
  print "---------------"
  print "5304"
  print "correct: ",correct5304, "total: ",total5304
  print "accuracy: ", correct5304*100/float(total5304)

  # correct = 0
  # total = 0
  # print len(testX)
  # print len(predictedTest)
  # print len(testY)
  # for i,pred in enumerate(predictedTest):
  #   total +=1;
  #   # print i
  #   if pred == testY[i]:
  #     correct +=1;
  #   else:
  #     print pred,"|||" ,testY[i]
  # print "correct: ",correct, "total: ",total
if __name__ == '__main__':
  main()
