import sys
sys.path.append("../tools/")

import pickle
import pandas
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
plt.style.use('ggplot')
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn import tree
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import *

# sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi']

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

my_dataset = data_dict

### Task 2: Remove outliers

del data_dict["TOTAL"]
my_dataset = data_dict

### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.

## Email
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
             person['bonus'] != 'NaN'
            ])):
        person['wealth'] = sum([person[field] for field in ['salary',
                                                            'total_stock_value',
                                                            'exercised_stock_options',
                                                            'bonus']])
    else:
        person['wealth'] = 'NaN'

my_features = features_list + ['fraction_from_poi',
                               'fraction_to_poi',
                               'shared_receipt_with_poi',
                               'expenses',
                               'loan_advances',
                               'long_term_incentive',
                               'other',
                               'restricted_stock',
                               'restricted_stock_deferred',
                               'deferral_payments',
                               'deferred_income',
                               'salary',
                               'total_stock_value',
                               'exercised_stock_options',
                               'total_payments',
                               'bonus',
                               'wealth']
# salary = enron_df['salary']
# sorted(salary, reverse = True)

# for k, v in data_dict.items():
#     if v['salary'] != 'NaN' and v['salary'] > 1111258: print k

# for i in data_dict.values():
#     plt.scatter( i['salary'] , i['bonus']  )
#
# plt.xlabel("salary")
# plt.ylabel("bonus")
# plt.show()

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, my_features, sort_keys = True)
labels, features = targetFeatureSplit(data)

# # Scale features
scaler = MinMaxScaler()
features = scaler.fit_transform(features)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.

### GaussianNB
print "\n Running GaussianNB.. Wait for some time \n"
select = SelectKBest()
clf = GaussianNB()

steps = [('feature_selection', select), ('GaussianNB', clf)]

pipeline = Pipeline(steps)

features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.33, random_state=42)

parameters = dict(feature_selection__k = [3,4,5])

cv = GridSearchCV(pipeline, param_grid = parameters, cv = 10)

cv.fit(features_train, labels_train)

pred = cv.predict(features_test)
report = classification_report(labels_test, pred)
accuracy = accuracy_score(labels_test, pred)
results = pandas.DataFrame.from_dict(cv.cv_results_)

results_list = zip(cv.best_estimator_.named_steps['feature_selection'].get_support(), my_features[1:],
                   cv.best_estimator_.named_steps['feature_selection'].scores_)

results_list = sorted(results_list, key = lambda x: x[2], reverse=True)

print '\n GNB Best Estimator:', cv.best_estimator_.steps[1][1]
print'\n GNB Report:', report
print '\n GNB Accuracy:', accuracy

### Random Forest
print "\n Running RandomForestClassifier.. Please Wait for some more time \n"
data = featureFormat(my_dataset, my_features, sort_keys = True)
labels, features = targetFeatureSplit(data)

scaler = MinMaxScaler()
features = scaler.fit_transform(features)

select = SelectKBest()
clf = RandomForestClassifier()

steps = [('feature_selection', select),
        ('random_forest', clf)]

pipeline = Pipeline(steps)

features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.33, random_state=42)

parameters = dict(feature_selection__k = [3,4,5],
                  random_forest__n_estimators=[50, 100, 200],
                  random_forest__min_samples_split=[2, 3, 4, 5, 10])

cv = GridSearchCV(pipeline, param_grid = parameters)

cv.fit(features_train, labels_train)

pred = cv.predict(features_test)

report = classification_report(labels_test, pred)
accuracy = accuracy_score(labels_test, pred)
results = pandas.DataFrame.from_dict(cv.cv_results_)

results_list = zip(cv.best_estimator_.named_steps['feature_selection'].get_support(), my_features[1:],
                   cv.best_estimator_.named_steps['feature_selection'].scores_)

results_list = sorted(results_list, key = lambda x: x[2], reverse=True)

best_scores = cv.best_estimator_.named_steps['feature_selection'].scores_
best_scores = sorted([round(x, 3) for x in best_scores], reverse = True)

print '\n RF Best Estimator:', cv.best_estimator_.steps[1][1]
print'\n RF Report:', report
print '\n RF Accuracy:', accuracy


### SVC
print "\n Running SVC.. Almost done.. Please Wait for some more time \n"
data = featureFormat(my_dataset, my_features, sort_keys = True)
labels, features = targetFeatureSplit(data)

scaler = MinMaxScaler()
features = scaler.fit_transform(features)

select = SelectKBest()
clf = SVC()

steps = [('feature_selection', select), ('svc', clf)]

pipeline = Pipeline(steps)

features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.33, random_state=42)

parameters = dict(feature_selection__k = [3,4,5],
                  svc__kernel = ["rbf", "linear"],
                  svc__C = [1, 10, 50, 100, 200])

cv = GridSearchCV(pipeline, param_grid = parameters, cv = 10)

cv.fit(features_train, labels_train)

pred = cv.predict(features_test)

report = classification_report( labels_test, pred)
accuracy = accuracy_score(labels_test, pred)

results = pandas.DataFrame.from_dict(cv.cv_results_)

results_list = zip(cv.best_estimator_.named_steps['feature_selection'].get_support(), my_features[1:],
                   cv.best_estimator_.named_steps['feature_selection'].scores_)

results_list = sorted(results_list, key = lambda x: x[2], reverse=True)

best_scores = cv.best_estimator_.named_steps['feature_selection'].scores_
best_scores = sorted([round(x, 3) for x in best_scores], reverse = True)

print '\n SVC Best Estimator:', cv.best_estimator_.steps[1][1]
print'\n SVC Report:', report
print '\n SVC Accuracy:', accuracy


print "Choosing GNB as per the recall & precision score..."

## Final Features as per SelectKBest

print '\n Final Features as per SelectKBest..'

from sklearn.model_selection import *
from sklearn.metrics import *

my_features = features_list + ['fraction_to_poi','salary','bonus']
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.525, random_state=42)

print '\n Running GNB.. \n'

#clf = SVC(C = 10, kernel = 'rbf')
clf = GaussianNB()

clf.fit(features_train, labels_train)
pred = clf.predict(features_test)

report = classification_report(labels_test, pred)
accuracy = accuracy_score(labels_test, pred)

#print '\n', "SVC(C = 10, kernel = 'rbf') Accuracy:", accuracy
#print '\n', "SVC(C = 10, kernel = 'rbf') Report:", report

print '\n', "GNB Accuracy:", accuracy
print '\n', "GNB Report:", report

print '\n', "GNB Confusion Matrix:", confusion_matrix(labels_test, pred)

print '\n'
print '\n'
print '\n'
print '\n'
print '\n Running KFold (10 Fold) Evaluation..'

kf = KFold(n_splits= 10)

my_features = features_list + ['fraction_to_poi','salary','bonus']

data = featureFormat(my_dataset, my_features, sort_keys = True)

labels, features = targetFeatureSplit(data)

for train, test in kf.split(features):
        accuracy = []
        features_train = []
        features_test  = []
        labels_train   = []
        labels_test    = []
        for ii in train:
            features_train.append( features[ii] )
            labels_train.append( labels[ii] )
            clf.fit(features_train, labels_train)
        for jj in test:
            features_test.append( features[jj] )
            labels_test.append( labels[jj] )
            pred = clf.predict(features_test)
            accuracy.append(accuracy_score(labels_test, pred))
#            print confusion_matrix(labels_test, pred)
print accuracy
print "\n Mean Accuracy:\n", mean(accuracy)
### Task 5: Tune your classifier to achieve better than .3 precision and recall
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info:
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
#
# from sklearn.cross_validation import train_test_split
# features_train, features_test, labels_train, labels_test = \
#     train_test_split(features, labels, test_size=0.3, random_state=42)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, my_features)
