__author__ = 'Victor'
from os.path import expanduser, join, split
import sys
home_dir = expanduser('~')
sys.path.append(join(home_dir, 'PycharmProjects', 'WekaPy'))
from weka_utils.arff import reorder
from weka_utils.arff import rm_features

test_path = '/Users/Victor/Desktop/psiquiatrico/e2_depressiondataset_final_discretized.arff'
train_path = '/Users/Victor/Desktop/psiquiatrico/e1_depressiondataset_training_v2_filtered_discretized.arff'

out_path = '/Users/Victor/Desktop/psiquiatrico/e1_depressiondataset_training_v2_filtered_discretized_removedAttrsNotInTraining.arff'

#get features in training
training_attrs = set(reorder.arff_features(train_path))
test_attrs = set(reorder.arff_features(test_path))

remove_attrs = set.intersection(training_attrs, test_attrs)

#get remove command
weka_cp = '/Users/Victor/Desktop/weka-3-7-12/weka.jar'
rm_cl = rm_features.rm_features(source=train_path,out_path=out_path,rm_by='name', features=remove_attrs,reverse=True,cp=weka_cp, heap='8g')
rm_cl.execute(verbose=True, shell=True)



print 5