import sys
import getopt
import os
import math
import operator
import numpy as np
class Turney:
  class TrainSplit:
    """Represents a set of training/testing data. self.train is a list of Examples, as is self.test. 
    """
    def __init__(self):
      self.train = []
      self.test = []

  class Example:
    """Represents a document with a label. klass is 'pos' or 'neg' by convention.
       words is a list of strings.
    """
    def __init__(self):
      self.klass = ''
      self.words = []


  def __init__(self):
    """Turney initialization"""    
    self.numFolds = 10
    self.dic={}
    self.hit_great=0
    self.hit_poor=0
    

  #############################################################################
  # TODO TODO TODO TODO TODO 
  # Implement the Turney classifier 

  def classify(self, words):
    words=[word.split('_')[0] for word in words]
    score=0
    for i in range (0,len(words)-2):
      if (words[i],words[i+1]) in self.dic:
        score+=self.dic[(words[i],words[i+1])][0]
    if score>3:
      return 'pos'
    else:
      return 'neg'
  

  def addExample(self, words):
    for i in range(0,len(words)-2):
      if(words[i]=="great"):
        self.hit_great+=1
      elif (words[i]=="poor"):
        self.hit_poor+=1
      if (words[i],words[i+1]) in self.dic:
        great=0
        poor=0
        if i<10:
          start=0
        else:
          start=i-10
        if i+10>len(words)-1:
          end=len(words)-1
        else:
          end=i+10
        near=words[start:end]
        if "great" in near:
          self.dic[(words[i],words[i+1])][1]+=1
        if "poor" in near:
          self.dic[(words[i],words[i+1])][2]+=1
      

  def extract(self, split):
    for example in split.test:
      words=example.words
      words=[word.split('_') for word in words]
      for k in range(0,len(words)-2):
        if( words[k][1]=="JJ" and words[k+1][1]=="JJ" and words[k+2][1]!="NN" and words[k+2][1]!="NNS"):
          self.dic[(words[k][0],words[k+1][0])]=[0,0.1,0.1]
        elif( words[k][1]=="JJ" and words[k+1][1]=="NN" ) or ( words[k][1]=="JJ" and words[k+1][1]=="NNS" ):
          self.dic[(words[k][0],words[k+1][0])]=[0,0.1,0.1]
        elif( words[k][1]=="NN" and words[k+1][1]=="JJ" and words[k+2][1]!="NN" and words[k+2][1]!="NNS") or ( words[k][1]=="NNS" and words[k+1][1]=="JJ" and words[k+2][1]!="NN" and words[k+2][1]!="NNS"):
          self.dic[(words[k][0],words[k+1][0])]=[0,0.1,0.1]
        elif( words[k][1]=="RB" and words[k+1][1]=="JJ" and words[k+2][1]!="NN" and words[k+2][1]!="NNS") or ( words[k][1]=="RBR" and words[k+1][1]=="JJ" and words[k+2][1]!="NN" and words[k+2][1]!="NNS") or ( words[k][1]=="RBS" and words[k+1][1]=="JJ" and words[k+2][1]!="NN" and words[k+2][1]!="NNS"):
          self.dic[(words[k][0],words[k+1][0])]=[0,0.1,0.1]
 
  
  def train(self, split):
      """
      * TODO 
      * iterates through data examples
      """
      self.extract(split)
      total=0
      for example in split.train:
          words = example.words
          words=[word.split('_')[0] for word in words]
          self.addExample(words)
      for key in self.dic:
        if self.dic[key][1]==0.1 and self.dic[key][2]==0.1:
          self.dic[key][0]=0
        else:
          self.dic[key][0]=np.log2([(self.dic[key][1]*self.hit_poor)/(self.dic[key][2]*self.hit_great)])[0]

          
  # END TODO (Modify code beyond here with caution)
  #############################################################################
  
  
  def readFile(self, fileName):
    """
     * Code for reading a file.  you probably don't want to modify anything here, 
     * unless you don't like the way we segment files.
    """
    contents = []
    f = open(fileName)
    for line in f:
      contents.append(line)
    f.close()
    result = self.segmentWords('\n'.join(contents)) 
    return result

  
  def segmentWords(self, s):
    """
     * Splits lines on whitespace for file reading
    """
    return s.split()

  
  def trainSplit(self, trainDir):
    """Takes in a trainDir, returns one TrainSplit with train set."""
    split = self.TrainSplit()
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    for fileName in posTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
      example.klass = 'pos'
      split.train.append(example)
    for fileName in negTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
      example.klass = 'neg'
      split.train.append(example)
    return split


  def crossValidationSplits(self, trainDir):
    """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
    splits = [] 
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    #for fileName in trainFileNames:
    for fold in range(0, self.numFolds):
      split = self.TrainSplit()
      for fileName in posTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      for fileName in negTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
        example.klass = 'neg'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      splits.append(split)
    return splits
  

def test10Fold(args):
  pt = Turney()
  
  splits = pt.crossValidationSplits(args[0])
  avgAccuracy = 0.0
  fold = 0
  for split in splits:
    classifier = Turney()
    accuracy = 0.0
    classifier.train(split)
    for example in split.test:
      words = example.words
      guess = classifier.classify(words)
      if example.klass == guess:
        accuracy += 1.0
    accuracy = accuracy / len(split.test)
    avgAccuracy += accuracy
    print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy) 
    fold += 1
  avgAccuracy = avgAccuracy / fold
  print '[INFO]\tAccuracy: %f' % avgAccuracy
    
    
def classifyDir(trainDir, testDir):
  classifier = Turney()
  trainSplit = classifier.trainSplit(trainDir)
  classifier.train(trainSplit)
  testSplit = classifier.trainSplit(testDir)
  #testFile = classifier.readFile(testFilePath)
  accuracy = 0.0
  for example in testSplit.train:
    words = example.words
    guess = classifier.classify(words)
    if example.klass == guess:
      accuracy += 1.0
  accuracy = accuracy / len(testSplit.train)
  print '[INFO]\tAccuracy: %f' % accuracy
    
def main():
  (options, args) = getopt.getopt(sys.argv[1:], '')
  if len(args) == 2:
    classifyDir(args[0], args[1])
  elif len(args) == 1:
    test10Fold(args)

if __name__ == "__main__":
    main()
