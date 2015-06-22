__author__ = 'Victor'
from os.path import expanduser, join, split
import sys
home_dir = expanduser('~')
sys.path.append(join(home_dir, 'PycharmProjects', 'HospitalReadmission'))
from weka_utils.arff import propagate_bins


source_path = '/Users/Victor/Box Sync/Psiquiatrico/data/arff/e1_depressiondataset_training_v2_filtered_discretized.arff'
target_path = '/Users/Victor/Box Sync/Psiquiatrico/data/arff/Interview 2/e2_depressiondataset_final.arff'

out_path = '/Users/Victor/Box Sync/Psiquiatrico/data/arff/Interview 2/e2_depressiondataset_final_discretized.arff'

propagate_bins.map_arff(source_path=source_path, target_path=target_path, out_path=out_path)
