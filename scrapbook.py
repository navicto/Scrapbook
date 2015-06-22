#sort vitals_data so numerical features are first and categorical at the end
columns = vitals_data.columns.tolist()
#remove numeric features for cardiac rhythm (it's a numerical attr. they shouldn't have been created in the first place)
rhythm_numeric = [attr for attr in columns if 'Rhythm' in attr]
rhythm_numeric.remove('Cardiac_Rhythm_FLAG') #this is categorical and we do need it
columns = [attr for attr in columns if attr not in rhythm_numeric]
#Only categorical attrs are vitals FLAGS, DATE, and READMITTED
categorical = [col for col in columns if 'FLAG' in col]
categorical += ['DATE', 'READMITTED']
numerical = list(set(columns) - set(categorical))
sorted_columns = numerical + categorical #Desired order of the features
#sort dataframes
vitals_data = vitals_data[sorted_columns]