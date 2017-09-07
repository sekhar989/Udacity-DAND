import sys
sys.path.append("../tools/")
import numpy
from numpy import mean
import pickle
import pandas
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
#plt.style.use('ggplot')
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn import tree
from sklearn.pipeline import *
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import *
from sklearn.model_selection import *
from sklearn.pipeline import make_pipeline


from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data


features_list = ['poi']

with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

my_dataset = data_dict

print "\nChecking for outliers based on salary more than 1000000.. \n"
for k, v in data_dict.items():
    if v['salary'] != 'NaN' and v['salary'] > 1000000: print k

print "\nTOTAL is not a person. It's a cumulative data of numerical features.\nHence it should be removed. \n"

del data_dict["TOTAL"]
my_dataset = data_dict


### Email
for item in my_dataset:
    person = my_dataset[item]
    if (all([person['from_poi_to_this_person'] != 'NaN',
             person['from_this_person_to_poi'] != 'NaN',
             person['to_messages'] != 'NaN',
             person['from_messages'] != 'NaN'
            ])):
        fraction_from_poi = float(person["from_poi_to_this_person"]) / float(person["to_messages"])
        person["fraction_from_poi"] = fraction_from_poi
        fraction_to_poi = float(person["from_this_person_to_poi"]) / float(person["from_messages"])
        person["fraction_to_poi"] = fraction_to_poi
    else:
        person["fraction_from_poi"] = person["fraction_to_poi"] = 0

### Financial:

for item in my_dataset:
    person = my_dataset[item]
    if (all([person['salary'] != 'NaN',
             person['total_stock_value'] != 'NaN',
             person['exercised_stock_options'] != 'NaN',
             person['bonus'] != 'NaN',
             person['long_term_incentive'] != 'NaN'
            ])):
        person['wealth'] = sum([person[value] for value in ['salary',
                                                            'total_stock_value',
                                                            'exercised_stock_options',
                                                            'bonus',
                                                           'long_term_incentive']])
    else:
        person['wealth'] = 'NaN'


my_features = features_list + ['fraction_from_poi',
                               'fraction_to_poi','wealth',
                               'salary', 'deferral_payments', 'total_payments',
                               'loan_advances', 'bonus',
                               'restricted_stock_deferred', 'deferred_income',
                               'total_stock_value', 'expenses',
                               'exercised_stock_options', 'other',
                               'long_term_incentive',
                               'restricted_stock', 'director_fees',
                               'to_messages',
                               'from_poi_to_this_person',
                               'from_messages', 'from_this_person_to_poi',
                               'shared_receipt_with_poi']



###  *****Feature Selection Function*****

def Selection(data, feature_range, s_features):
    
    data = featureFormat(data, s_features, sort_keys = True)
    labels, features = targetFeatureSplit(data)
    features_iter = []
    
    for i in feature_range:
        
        select = SelectKBest(k = i)
        select.fit(features, labels)
        
        results_list = zip(select.get_support(), my_features[1:], select.scores_)
        results_list = sorted(results_list, key = lambda x: x[2], reverse=True)
        
        iter_feat = [i[1] for i in results_list if i[0] == True]
                
        features_iter.append(iter_feat)
        
        score_list = zip(my_features[:], select.scores_)
        score_list = sorted(score_list, key = lambda x: x[1], reverse=True)
        
    for i in score_list: print i
    return features_iter


### *****Feature Plotting Function******

def Plotting(clf, f_list, input_data):
    
    accuracy = []
    precision = []
    recall = []
    
    for i in f_list:
        feat = ['poi'] + i

        data = input_data
        data = featureFormat(data, feat, sort_keys = True)
        f_labels, f_features = targetFeatureSplit(data)
        
        f_features_train, f_features_test, f_labels_train, f_labels_test = train_test_split(f_features, f_labels, test_size=0.33, random_state=42)
        
        clf.fit(f_features_train, f_labels_train)
        pred = clf.predict(f_features_test)
        
        accuracy.append(accuracy_score(f_labels_test, pred))
        recall.append(recall_score(f_labels_test, pred))
        precision.append(precision_score(f_labels_test, pred))
    
    x = [i + 1 for i in range(len(f_list))]
    y1 = accuracy
    y2 = recall
    y3 = precision
    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    
    ax1.plot(x, y1, c='r', label='Accuracy')
    ax1.plot(x, y2, c='g', label='Recall')
    ax1.plot(x, y3, c='b', label='Precision')
    plt.axis([0, 18, 0, 1])
    plt.grid(True)
    plt.legend(loc='lower right')
    plt.xlabel('Number of "K" in SelectKBest')
    plt.ylabel('Scores')
    plt.title('K vs Accuracy, Recall, Precision')
    plt.show()



### *****Classifier Tuning Function*****

def Grid(clf, data, selected_features, parameters, iterations = 20):

    data = featureFormat(data, selected_features, sort_keys = True)
    labels, features = targetFeatureSplit(data)

    for i in range(iterations):

        features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.33, random_state=42)
        pipeline = make_pipeline(clf)

        cv = GridSearchCV(pipeline, param_grid = parameters)
        cv.fit(features_train,labels_train)
        pred = cv.predict(features_test)

        print "\nIteration Num.:", (i + 1)
        print "\nBest Paramters:", cv.best_params_
        print "\nReport:\n", classification_report(labels_test, pred)



### ******Validation Function*****

def Classifer(clf, data, features, iterations = 100):

    data = featureFormat(data, features, sort_keys = True)
    labels, features = targetFeatureSplit(data)

    for i in range(iterations):
        kf = KFold(n_splits = 3, shuffle = False)
        clf = clf

        accuracy = []
        precision = []
        recall = []
        print "\nIteration Num.:", (i + 1)

        for train, test in kf.split(features):
            features_train = []
            features_test  = []
            labels_train   = []
            labels_test    = []

            for m in train:
                features_train.append( features[m] )
                labels_train.append( labels[m] )

            for n in test:
                features_test.append( features[n] )
                labels_test.append( labels[n] )
                clf.fit(features_train, labels_train)
                pred = clf.predict(features_test)
            accuracy.append(accuracy_score(labels_test, pred))
            precision.append(precision_score(labels_test, pred))
            recall.append(recall_score(labels_test, pred))

    print "\nMean Accuracy:", mean(accuracy)
    print "\nMean Precision:", mean(precision)
    print "\nMean Recall:", mean(recall)


print "\n*******************************************************************\n"
print "\nRunning Feature Selection..\n"

feature_range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12, 13, 14, 15, 16, 17, 18]
kbest_features = Selection(my_dataset, feature_range, my_features)

Plotting(GaussianNB(), kbest_features, my_dataset)

#my_features = ["poi"] + kbest_features[6]

data = featureFormat(my_dataset, my_features, sort_keys = True)
labels, features = targetFeatureSplit(data)

print '\nRunning Final Feature Selection of 7 features..\n'

select = SelectKBest(k = 7)
select.fit(features, labels)

results_list = zip(select.get_support(), my_features[1:], select.scores_)
results_list = sorted(results_list, key = lambda x: x[2], reverse=True)
for i in results_list: print i
my_features = features_list + [i[1] for i in results_list if i[0] == True]

print '\n'
print "Final Selected features..\n"
for i in my_features[1:]: print i

#print "\n*******************************************************************\n"
#print "\nRunning GaussianNB.. Wait for some time \n"
#params = dict()
#Grid(GaussianNB(), my_dataset, my_features, params)

#print "\nRunning GaussianNB.. Wait for some time \n"
#clf = GaussianNB()
#Classifer(clf, my_dataset , my_features, iterations = 20)

#print "\n*******************************************************************\n"

#print "\nRunning RandomForestClassifier.. Please Wait for some more time \n"
#
#params = dict(randomforestclassifier__n_estimators=[10, 20, 50, 100],
#              randomforestclassifier__min_samples_split=[2, 3, 4, 5])
#
#Grid(RandomForestClassifier(), my_dataset, my_features, params)

#print "\nRunning Final RandomForestClassifier.. Please Wait for some more time \n"
#
#clf = RandomForestClassifier(n_estimators = 20, min_samples_split = 2)
#Classifer(clf, my_dataset , my_features, iterations = 20)

#print "\n*******************************************************************\n"

#print "\nRunning SVC.. Almost done.. Please Wait for some more time \n"
#
#params = dict(svc__kernel = ['rbf'],
#              svc__C = [1, 10, 20 ,30, 50])
#Grid(SVC(), my_dataset, my_features, params)

#print "\nRunning SVC.. Wait for some more time \n"
#clf = SVC(C = 1, kernel = 'rbf')
#Classifer(clf, my_dataset , my_features, iterations = 20)

print "\n*******************************************************************\n"

print "\nRunning Final GaussianNB.. Final Run..\n"
clf = GaussianNB()
Classifer(clf, my_dataset , my_features)

dump_classifier_and_data(clf, my_dataset, my_features)