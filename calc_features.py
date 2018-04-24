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

mac_list = ["b8:27:eb:b6:43:f8", "b8:27:eb:d3:4c:7f","b8:27:eb:cd:4b:81","b8:27:eb:ee:32:b8","b8:27:eb:e7:50:37","b8:27:eb:63:a1:e3"]
Y = []
X = []
testX = []
testRoots =[]
dirname_tyler = "/Users/Tyler/Documents/GitHub/Bluetrack/data3/"
dirname_fatema = "C:\\Users\\Fatema Almeshqab\\Desktop\\Bluetrack\\data3\\"

if platform.system() == 'Darwin':
  dirname = dirname_tyler
else:
  dirname = dirname_fatema

valid_types = ['region','room','region_given_room']
valid_rooms = ['5300','5302','5304']
  
def generateSets(dataDict, granularity = "region",room = ""):
  if granularity not in valid_types:
    return -1;
  if (granularity == 'region_given_room') and room not in valid_rooms:
    return -1;
  trainX = []
  trainY = []
  testX  = []
  testY  = []
  for position in dataDict.keys():
    if granularity == 'region':
      data_pos = position;
    elif granularity == 'room':
      data_pos = position.split("_")[0]
    data = dataDict[position];
    shuffle(data);
    # print position
    for i,moment in enumerate(data):
      # print i
      # print moment
      feat = []
      if [] in moment:
        continue
      else:
        for j, nodeRSSI in enumerate(moment):
            #if (j == 0): continue;
            # nodeRSSI = np.array(nodeRSSI);
            mean    = np.mean(nodeRSSI);
            minRSSI = min(nodeRSSI);
            maxRSSI = max(nodeRSSI);
            var     = np.var(nodeRSSI);
            mode    = stats.mode(np.array(nodeRSSI)); 
            median = np.median(nodeRSSI);     
            feat += [mean , median] #, minRSSI, maxRSSI] #, int(mode[0])];
        # print len(feat) # should be 30 features long
        # print feat
        if (i < 60):
          trainX.append(feat);
          trainY.append(data_pos);
        else:
          testX.append(feat);
          testY.append(data_pos);

  return trainX, trainY, testX, testY
      
      
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
  ########
  ## Testing on all 11 regions
  ########
  X, Y, testX, testY = generateSets(rawData);
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
  X, Y, testX, testY = generateSets(rawData,"room");
  train_set = np.array(X)
  # clf = NearestCentroid();
  # clf.fit(train_set, Y);
  # print clf.score(testX,testY)
  
  clf = KNeighborsClassifier(n_neighbors=12, weights="distance")
  clf.fit(train_set, Y)
  predictedTest = clf.predict(testX)
  print "knn - room"
  print clf.score(testX,testY)

  clf = SVC(kernel='linear', C=2).fit(train_set, Y)
  predictedTest = clf.predict(testX)
  print "svc - room"
  print clf.score(testX,testY)

  # correct = 0
  # odd = 0;
  # previous_room = "";
  # for i, point in enumerate(testX):
  #   current_room = clf.predict([point])[0];
  #   if (previous_room == ""):
  #     previous_room = current_room;
  #   else:
  #     if (((previous_room[0:4] == '5302') and  (current_room[0:4] == '5304')) or
  #         ((previous_room[0:4] == '5304') and  (current_room[0:4] == '5302'))):
  #       #print previous_room, testY[i]; 
  #       #continue;
  #     else:
  #       previous_room = current_room 

  #   if (previous_room == testY[i]):
  #     correct += 1;
  #   print previous_room, testY[i];
  # print correct;

if __name__ == '__main__':
  main()
