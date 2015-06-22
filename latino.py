__author__ = 'Victor'

import pandas as pd
import numpy as np
from weka_utils.arff import to_arff

def expand_columns(data, columns):
    #columns to expand
    to_expand = data.loc[:, columns]
    unchanged = list(set(data.columns) - set(columns))
    unchanged = data.loc[:, unchanged]
    #get unique values in columns to expand
    values = set()
    for col in columns:
        values = set.union(set(to_expand[col].unique().tolist()), values)
    values = [val for val in values if not pd.isnull(val)]
    #create new dataframe
    expanded = pd.DataFrame(columns=values,  index=data.index)
    #check if row has any of the values of new columns
    for value in values:
        test = pd.Series({i:False for i in data.index})
        for col in columns:
            test = test | (data[col] == value)
        expanded[value] = test

    return (pd.concat([unchanged, expanded], axis=1), values)

def column_counts(data, columns, count_name):
    new_data = data.copy()
    new_data[count_name] = np.nan
    #iterate over rows
    for row in new_data.index:
        count = 0
        for col in columns:
            if data.loc[row, col]:
                count += 1
        new_data.loc[row, count_name] = count

    return new_data

def age_group(data, age_attr, age_ranges, new_label):
    ages = data[age_attr]
    new_ages = []
    for age in ages:
        found_group = False
        for age_range in age_ranges:
            if (age >= age_range[0]) and (age < age_range[1]):
                new_ages += [age_ranges[age_range]]
                found_group = True
                break
        if not found_group:
            new_ages += [np.nan]
    data[new_label] = new_ages


def main():
    dataset = '/Users/Victor/Box Sync/DBMI/7.Summer 2015/CongresoLatino/e2depressiondataset.csv'
    depre = pd.read_csv(dataset, index_col=0)
    #remove null columns:
    null_attrs = []
    for col in depre.columns:
        if depre[~depre[col].isnull()].empty:
            del depre[col]
            null_attrs += [col]

    #change missing values
    depre = depre.replace({'NA':np.nan})
    #columns with medications:
    expand_cols = ['f7_p10a_', 'f7_p10a3', 'f7_p10a7', 'f7_p1001', 'f7_p1005', 'f7_p1009', 'f7_p1013']
    expand_cols = [attr for attr in expand_cols if attr in depre.columns] #remove column if not in dataset
    expanded_depre, new_cols = expand_columns(data=depre, columns=expand_cols)
    print expanded_depre.head()
    depre_withCount = column_counts(data=expanded_depre, columns=new_cols, count_name='N_meds')
    print depre_withCount.head()
    #create age group:
    age_groups = {(0.0001, 18) : '0to18', (18, 45) : '18to45', (45, 65) : '45to65', (65, np.inf) : '65orGreater'}
    age_group(data=depre_withCount, age_attr='edad', age_ranges=age_groups, new_label='getario')
    #create work hours
    depre_withCount['horastrabajo'] = depre_withCount['f6_p6'] / (4 * depre_withCount['f6_p3'])
    #rename columns so they match the first dataset:
    mapping = pd.read_csv('/Users/Victor/Box Sync/DBMI/7.Summer 2015/CongresoLatino/mapping.csv')
    mapping = mapping[~mapping['from'].isnull()]
    map_index = {}
    for entry in mapping.index:
        map_index[mapping.loc[entry, 'from']] = mapping.loc[entry, 'to']
    depre_withCount = depre_withCount.rename(columns=map_index)
    #save to arff
    out_path = '/Users/Victor/Box Sync/DBMI/7.Summer 2015/CongresoLatino/e2depressiondataset_expanded_plusAgeGroup.csv'
    attr_spec = {}
    for col in depre_withCount.columns:
        if not depre_withCount[col]._get_numeric_data().empty:
            attr_spec[col] = 'NUMERIC'

    # to_arff.dataframe2ARFF(data=depre_withCount,attr_spec=attr_spec,out_path=out_path)
    #put class at the end
    columns = set(depre_withCount.columns) - set(["f7_p9a"])
    columns = list(columns) + ["f7_p9a"]
    depre_withCount = depre_withCount[columns]
    depre_withCount.to_csv(out_path + '.csv')
    #save list of removed features:
    out_path = '/Users/Victor/Box Sync/DBMI/7.Summer 2015/CongresoLatino/removed_from_e2depressiondataset.txt'
    with open(out_path, 'w') as out_null:
        for attr in null_attrs:
            print>>out_null, attr


if __name__ == '__main__':
    main()