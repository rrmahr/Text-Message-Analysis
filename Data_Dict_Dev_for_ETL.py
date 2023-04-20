# #### Multi-select Multiple Choice Variables




#Create list of QIDs for multi-select variables
multi_select_range = []
for i in data['questions']:
    if ((data['questions'][i]['questionType']['type'] == 'MC') & (data['questions'][i]['questionType']['selector'] == 'MAVR')):
        multi_select_range.append(i)





#Create multi-select variable name list
ms_var_list = []

#Need to select values from the key, value pairs of the choices
for i in multi_select_range:
    for key, value in data['questions'][i]['choices'].items():
        #then need to add that to the data questionName to get the desired variable names
        ms_var_list.append(str(data['questions'][i]['questionName']) + '_' + str(value['recode']))





#Get variable labels
ms_var_label_list = []

#Need to select values from the key, value pairs of the choices
for i in multi_select_range:
    for key, value in data['questions'][i]['choices'].items():
        #then need to add that to the data questionText to get the desired variable labels
        ms_var_label_list.append(str(data['questions'][i]['questionText']) + ' - ' + str(value['choiceText']))





#Create value labels dictionary: For multi-select, value labels will be 1 'Yes', 0 'No'

#Create dictionary with response values and their corresponding labels
ms_inner_dict = {'1': 'Yes', '0': 'No'}

#Create nested dictionary w. var names : values
ms_value_label_dict = {ms_var_list[i] : ms_inner_dict for i in range(len(ms_var_list))}

#Create values df 
ms_rows = []
for key, values in ms_value_label_dict.items():
    for k, v in values.items():
        ms_rows.append([key,k,v])
ms_values_df = pd.DataFrame(ms_rows, columns=["Var_Name", "Value","Value_Label"])





#Create data_dict_df
data_dict_df = pd.DataFrame(columns = ["Var_Name","Var_Label","Value","Value_Label","Data_Type"])

#Add multi-select vars to codebook if any
if len(ms_var_list) > 0:
    #first create a placeholder df with Var_Name & Var_Labels
    p_data_dict_df = pd.concat([pd.Series(x) for x in [ms_var_list, ms_var_label_list]], axis=1).rename(columns={0:"Var_Name",1:"Var_Label"})
    #merge in values df
    p_data_dict_df = pd.merge(p_data_dict_df, ms_values_df, on='Var_Name', how='inner')
    #assign data type -- INT because categorical
    p_data_dict_df['Data_Type'] = "INT"
    #assign question type
    p_data_dict_df['Question_Type'] = "multi-select"

    #merge into data_dict_df
    data_dict_df = pd.concat([data_dict_df,p_data_dict_df])


# #### Multi-select Multiple Choice Other Text Entry Variables




ms_ote_var_list = []
for i in multi_select_range:
    for key, value in data['questions'][i]['choices'].items():
        for key2,value2 in value.items():
            if key2 == 'textEntry':
                ms_ote_var_list.append(str(data['questions'][i]['questionName']) + '_' + str(value['recode']) + '_TEXT')





#Get variable labels
ms_ote_var_label_list = []

#Need to select values from the key, value pairs of the choices
for i in multi_select_range:
    for key, value in data['questions'][i]['choices'].items():
        for key2,value2 in value.items():
            if key2 == 'textEntry':
                ms_ote_var_label_list.append(str(data['questions'][i]['questionText']) + ' - ' + str(value['choiceText'] + ' - TEXT'))





#Create value labels: For mult-select other text entry, value labels will be {nan: 'text'}

#Create dictionary with responses
ms_ote_inner_dict = {np.nan: 'text'}

#Create nested dictionary w. var names : values
ms_ote_value_label_dict = {ms_ote_var_list[i] : ms_ote_inner_dict for i in range(len(ms_ote_var_list))}

#Create values df 
ms_ote_rows = []
for key, values in ms_ote_value_label_dict.items():
    for k, v in values.items():
        ms_ote_rows.append([key,k,v])
ms_ote_values_df = pd.DataFrame(ms_ote_rows, columns=["Var_Name", "Value","Value_Label"])





#Update data_dict_df with text-entry vars if any
if len(ms_ote_var_list) > 0:
    #first create a placeholder df with Var_Name & Var_Labels
    p_data_dict_df = pd.concat([pd.Series(x) for x in [ms_ote_var_list, ms_ote_var_label_list]], axis=1).rename(columns={0:"Var_Name",1:"Var_Label"})
    #merge in values df
    p_data_dict_df = pd.merge(p_data_dict_df, ms_ote_values_df, on='Var_Name', how='inner')
    #assign data type -- STRING because text entry
    p_data_dict_df['Data_Type'] = "STRING"
    #assign question type
    p_data_dict_df['Question_Type'] = "multi-select text-entry"
    #merge into data_dict_df
    data_dict_df = pd.concat([data_dict_df,p_data_dict_df])


# #### Single-select MC Variables




#Create list of QIDs for single select variables
single_select_range = []
for i in data['questions']:
    if ((data['questions'][i]['questionType']['type'] == 'MC') & (data['questions'][i]['questionType']['selector'] != 'MAVR')):
        single_select_range.append(i)





#Create single-select variable name list
single_var_list = []

#pull from questionNames
for i in single_select_range:
    single_var_list.append(data['questions'][i]['questionName'])





#Get variable labels
single_var_label_list = []

#pull from questionText
for i in single_select_range:
    single_var_label_list.append(data['questions'][i]['questionText'])





#Create list of value and label dictionaries
single_value_label_dict_list = []

#Iterate through the choices
for i in single_select_range:
    single_inner_dict = {}
    for j in data['questions'][i]['choices']:
        #for each, create a dict with the recode value as keys and corresp. choiceText as values (the labels)
        single_inner_dict.update({data['questions'][i]['choices'][j]['recode'] : data['questions'][i]['choices'][j]['choiceText']})
    #add each into a list
    single_value_label_dict_list.append(single_inner_dict)

#Create nested dictionary w. each var name as the keys and each dict in the list created above as the values  
single_value_label_dict = {single_var_list[i] : single_value_label_dict_list[i] for i in range(len(single_var_list))}

#Create values df
single_rows = []
for key, values in single_value_label_dict.items():
    for k, v in values.items():
        single_rows.append([key,k,v])
single_values_df = pd.DataFrame(single_rows, columns=["Var_Name", "Value","Value_Label"])





#Update data_dict_df with single-select vars if any
if len(single_var_list) > 0:
    #first create a placeholder df with Var_Name & Var_Labels
    p_data_dict_df = pd.concat([pd.Series(x) for x in [single_var_list, single_var_label_list]], axis=1).rename(columns={0:"Var_Name",1:"Var_Label"})
    #merge in values df
    p_data_dict_df = pd.merge(p_data_dict_df, single_values_df, on='Var_Name', how='inner')
    #assign data type -- INT because categorical
    p_data_dict_df['Data_Type'] = "INT"
    #assign question type
    p_data_dict_df['Question_Type'] = "single-select"    
    #merge into data_dict_df
    data_dict_df = pd.concat([data_dict_df,p_data_dict_df])


# #### Single-select Multiple Choice Other Text Entry Variables




#Create single-select variable name list
single_var_list = []

#pull from questionNames
for i in single_select_range:
    single_var_list.append(data['questions'][i]['questionName'])





#Create var list
single_ote_var_list = []
for i in single_select_range:
    for key, value in data['questions'][i]['choices'].items():
        for key2,value2 in value.items():
            if key2 == 'textEntry':
                single_ote_var_list.append(str(data['questions'][i]['questionName']) + '_' + str(value['recode']) + '_TEXT')





#Get variable labels
single_ote_var_label_list = []

#Need to select values from the key, value pairs of the choices
for i in single_select_range:
    for key, value in data['questions'][i]['choices'].items():
        for key2,value2 in value.items():
            if key2 == 'textEntry':
                single_ote_var_label_list.append(str(data['questions'][i]['questionText']) + ' - ' + str(value['choiceText'] + ' - TEXT'))





#Create value labels: For mult-select other text entry, value labels will be {nan: 'text'}

#Create dictionary with responses
single_ote_inner_dict = {np.nan: 'text'}

#Create nested dictionary w. var names : values
single_ote_value_label_dict = {single_ote_var_list[i] : single_ote_inner_dict for i in range(len(single_ote_var_list))}

#Create values df 
single_ote_rows = []
for key, values in single_ote_value_label_dict.items():
    for k, v in values.items():
        single_ote_rows.append([key,k,v])
single_ote_values_df = pd.DataFrame(single_ote_rows, columns=["Var_Name", "Value","Value_Label"])





#Update data_dict_df with text-entry vars if any
if len(single_ote_var_list) > 0:
    #first create a placeholder df with Var_Name & Var_Labels
    p_data_dict_df = pd.concat([pd.Series(x) for x in [single_ote_var_list, single_ote_var_label_list]], axis=1).rename(columns={0:"Var_Name",1:"Var_Label"})
    #merge in values df
    p_data_dict_df = pd.merge(p_data_dict_df, single_ote_values_df, on='Var_Name', how='inner')
    #assign data type -- STRING because text entry
    p_data_dict_df['Data_Type'] = "STRING"
    #assign question type
    p_data_dict_df['Question_Type'] = "single-select text-entry"
    #merge into data_dict_df
    data_dict_df = pd.concat([data_dict_df,p_data_dict_df])


# #### Text Entry Variables - Not Form




#Create list of QIDs for Text Entry variables
te_range = []
for i in data['questions']:
    if ((data['questions'][i]['questionType']['type'] == 'TE') & (data['questions'][i]['questionType']['selector'] != 'FORM')):
        te_range.append(i)





#Create text entry variable name list
te_var_list = []

#pull from questionName
for i in te_range:
    te_var_list.append(data['questions'][i]['questionName'])





#Get variable labels
te_var_label_list = []

#pull from questionText
for i in te_range:
    te_var_label_list.append(data['questions'][i]['questionText'])





#Create value labels: For text entry, value labels will be {'': 'text'}

#Create dictionary with responses
te_inner_dict = {np.nan: 'text'}

#Create nested dictionary w. var names : values
te_value_label_dict = {te_var_list[i] : te_inner_dict for i in range(len(te_var_list))}

#Create values df 
te_rows = []
for key, values in te_value_label_dict.items():
    for k, v in values.items():
        te_rows.append([key,k,v])
te_values_df = pd.DataFrame(te_rows, columns=["Var_Name", "Value","Value_Label"])





#Update data_dict_df with text-entry vars if any
if len(te_var_list) > 0:
    #first create a placeholder df with Var_Name & Var_Labels
    p_data_dict_df = pd.concat([pd.Series(x) for x in [te_var_list, te_var_label_list]], axis=1).rename(columns={0:"Var_Name",1:"Var_Label"})
    #merge in values df
    p_data_dict_df = pd.merge(p_data_dict_df, te_values_df, on='Var_Name', how='inner')
    #assign data type -- STRING because text entry
    p_data_dict_df['Data_Type'] = "STRING"
    #assign question type
    p_data_dict_df['Question_Type'] = "text-entry"
    #merge into data_dict_df
    data_dict_df = pd.concat([data_dict_df,p_data_dict_df])


# #### Text Entry Variables - Form




#Create list of QIDs for Text Entry - Form variables
te_form_range = []
for i in data['questions']:
    if ((data['questions'][i]['questionType']['type'] == 'TE') & (data['questions'][i]['questionType']['selector'] == 'FORM')):
        te_form_range.append(i)





#Create TE form variable name list
te_form_var_list = []

#Need to select key from the key, value pairs of the choices
for i in te_form_range:
    for key, value in data['questions'][i]['choices'].items():
        #then need to add that to the data questionName to get the desired variable names
        te_form_var_list.append(str(data['questions'][i]['questionName']) + '_' + str(key))





#Get variable labels
te_form_var_label_list = []

#Need to select value descriptions from the key, value pairs of the choices
for i in te_form_range:
    for key, value in data['questions'][i]['choices'].items():
        #then need to add that to the data questionText to get the desired variable labels
        te_form_var_label_list.append(str(data['questions'][i]['questionText']) + ' - ' + str(value['description']))





#Create dictionary with responses
te_form_inner_dict = {np.nan: 'text'}

#Create nested dictionary w. var names : values
te_form_value_label_dict = {te_form_var_list[i] : te_form_inner_dict for i in range(len(te_form_var_list))}

#Create values df 
te_form_rows = []
for key, values in te_form_value_label_dict.items():
    for k, v in values.items():
        te_form_rows.append([key,k,v])
te_form_values_df = pd.DataFrame(te_form_rows, columns=["Var_Name", "Value","Value_Label"])





#Update data_dict_df with text entry vars if any
if len(te_form_var_list) > 0:
    #first create a placeholder df with Var_Name & Var_Labels
    p_data_dict_df = pd.concat([pd.Series(x) for x in [te_form_var_list, te_form_var_label_list]], axis=1).rename(columns={0:"Var_Name",1:"Var_Label"})
    #merge in values df
    p_data_dict_df = pd.merge(p_data_dict_df, te_form_values_df, on='Var_Name', how='inner')
    #assign data type -- STRING for text entry
    p_data_dict_df['Data_Type'] = "STRING"
    #assign question type
    p_data_dict_df['Question_Type'] = "text-entry form"
    #merge into data_dict_df
    data_dict_df = pd.concat([data_dict_df,p_data_dict_df])


# #### Matrix Variables - Not TE
# * For Matrix Variables where the selector is not TE




#Create list of QIDs for matrix (non-text entry) variables
matrix_range = []
for i in data['questions']:
    if ((data['questions'][i]['questionType']['type'] == 'Matrix') & (data['questions'][i]['questionType']['selector'] != 'TE')):
        matrix_range.append(i)





#Create matrix variable name list
matrix_var_list = []

#Need to select value -- recode value from the key, value pairs of the subQuestions (statements/rows of the matrix)
for i in matrix_range:
    for key, value in data['questions'][i]['subQuestions'].items():
        #then need to add that to the QID to get variable importid
        matrix_var_list.append(str(i) + '_' + str(value['recode']))

#Then rename the importid with the question export tag from api_q_dict created above
matrix_var_list = [api_q_dict.get(item,item) for item in matrix_var_list] 





#Get variable labels
matrix_var_label_list = []

#Need to select value -- choiceText from the key, value pairs of the subQuestions (statements/rows of the matrix)
for i in matrix_range:
    for key, value in data['questions'][i]['subQuestions'].items():
        #then need to add that to the data questionText to get the desired variable labels
        matrix_var_label_list.append(str(data['questions'][i]['questionText']) + ' - ' + str(value['choiceText']))





#Create list of value and label dictionaries
matrix_value_label_dict_list = []

#Iterate through the questions and then the choices
for i in matrix_range:
    matrix_inner_dict = {}
    for k in data['questions'][i]['subQuestions'].items():
        for j in data['questions'][i]['choices']:
            #for each, create a dict with the recode value as keys and corresp. choiceText as values (the labels)
            matrix_inner_dict.update({data['questions'][i]['choices'][j]['recode'] : data['questions'][i]['choices'][j]['choiceText']})
        #add each into a list
        matrix_value_label_dict_list.append(matrix_inner_dict)


#Create nested dictionary w. var names : {the dict created above}  
matrix_value_label_dict = {matrix_var_list[i] : matrix_value_label_dict_list[i] for i in range(len(matrix_var_list))}

#Create values df
matrix_rows = []
for key, values in matrix_value_label_dict.items():
    for k, v in values.items():
        matrix_rows.append([key,k,v])
matrix_values_df = pd.DataFrame(matrix_rows, columns=["Var_Name", "Value","Value_Label"])





#Update data_dict_df with matrix vars if any
if len(matrix_var_list) > 0:
    #first create a placeholder df with Var_Name & Var_Labels
    p_data_dict_df = pd.concat([pd.Series(x) for x in [matrix_var_list, matrix_var_label_list]], axis=1).rename(columns={0:"Var_Name",1:"Var_Label"})
    #merge in values df
    p_data_dict_df = pd.merge(p_data_dict_df, matrix_values_df, on='Var_Name', how='inner')
    #assign data type -- INT because categorical
    p_data_dict_df['Data_Type'] = "INT"
    #assign question type
    p_data_dict_df['Question_Type'] = "matrix"
    #merge into data_dict_df
    data_dict_df = pd.concat([data_dict_df,p_data_dict_df])


# #### Matrix Variables - Text Entry
# * For Matrix Variables where the selector is TE (text entry)
# * No value labels




#Create list of QIDs for matrix te variables
matrix_te_range = []
for i in data['questions']:
    if ((data['questions'][i]['questionType']['type'] == 'Matrix') & (data['questions'][i]['questionType']['selector'] == 'TE')):
        matrix_te_range.append(i)





#Create matrix variable name list
matrix_te_var_list = []

#Need to select value -- recode value from the key, value pairs of the subQuestions (statements/matrix rows)
for i in matrix_te_range:
    for key, value in data['questions'][i]['subQuestions'].items():
        #and select the key from the key, value pairs of the choices
        for key2, value2 in data['questions'][i]['choices'].items():
            #then need to add each of those to the QID to get variable importid
            matrix_te_var_list.append(str(i) + '_' + str(value['recode']) + "_" + str(key2))

#Then rename the importid with the question export tag from api_q_dict created above
matrix_te_var_list = [api_q_dict.get(item,item) for item in matrix_te_var_list] 





#Get variable labels
matrix_te_var_label_list = []

#Need to select value -- choiceText from the key, value pairs of the subQuestions
for i in matrix_te_range:
    for key, value in data['questions'][i]['subQuestions'].items():
        #and select the value -- choiceText from the key, value pairs of the choices
        for key2, value2 in data['questions'][i]['choices'].items():
            #then need to add both of those to the questionText to get the desired variable labels
            matrix_te_var_label_list.append(str(data['questions'][i]['questionText']) + ' - ' + str(value['choiceText'])+ ' - ' + str(value2['choiceText']))





#Create dictionary with responses, nan : 'text' because text entry
matrix_te_inner_dict = {np.nan: 'text'}

#Create nested dictionary w. var names : values
matrix_te_value_label_dict = {matrix_te_var_list[i] : matrix_te_inner_dict for i in range(len(matrix_te_var_list))}

#Create values df 
matrix_te_rows = []
for key, values in matrix_te_value_label_dict.items():
    for k, v in values.items():
        matrix_te_rows.append([key,k,v])
matrix_te_values_df = pd.DataFrame(matrix_te_rows, columns=["Var_Name", "Value","Value_Label"])





#Update data_dict_df with matrix text entry vars if any
if len(matrix_te_var_list) > 0:
    #first create a placeholder df with Var_Name & Var_Labels
    p_data_dict_df = pd.concat([pd.Series(x) for x in [matrix_te_var_list, matrix_te_var_label_list]], axis=1).rename(columns={0:"Var_Name",1:"Var_Label"})
    #merge in values df
    p_data_dict_df = pd.merge(p_data_dict_df, matrix_te_values_df, on='Var_Name', how='inner')
    #assign data type -- STRING because text entry (may need to edit later)
    p_data_dict_df['Data_Type'] = "STRING"
    #assign question type
    p_data_dict_df['Question_Type'] = "matrix"
    #merge into data_dict_df
    data_dict_df = pd.concat([data_dict_df,p_data_dict_df])


# #### SBS (Side by Side) Variables - Not TE
# * For SBS Variables where the selector is not TE




#Create list of QIDs for all sbs vars
sbs_range = []
for i in data['questions']:
    if (data['questions'][i]['questionType']['type'] == 'SBS'):
        sbs_range.append(i)

#Select != 'TE' from columns -- question type
sbs_nte_range = []
for i in sbs_range:
     for key, value in data['questions'][i]['columns'].items(): 
        if (data['questions'][i]['columns'][key]['questionType']['selector'] != 'TE'):
            sbs_nte_range.append(i)

#Remove duplicates
sbs_nte_range_dup = []
[sbs_nte_range_dup.append(i) for i in sbs_nte_range if i not in sbs_nte_range_dup]
sbs_nte_range = sbs_nte_range_dup





#Create side by side non-text entry variable name list
sbs_nte_var_list = []

#Need to select key from the key, value pairs of the columns
for i in sbs_nte_range:
    for key, value in data['questions'][i]['columns'].items():
        #Select only non-text entry columns
        if (data['questions'][i]['columns'][key]['questionType']['selector'] != 'TE'):
            #and select key from the key, value pairs of the subQuestions
            for key2, value2 in data['questions'][i]['subQuestions'].items():
                #then need to add both of those to the QID to get variable importid
                sbs_nte_var_list.append(str(i) + '#' + str(key) + "_" + str(key2))

#Then rename the importid with the question export tag from api_q_dict created above
sbs_nte_var_list = [api_q_dict.get(item,item) for item in sbs_nte_var_list]    





#Get variable labels
sbs_nte_var_label_list = []

#Need to select value -- questionText from the key, value pairs of the columns
for i in sbs_nte_range:
    for key, value in data['questions'][i]['columns'].items():
        #Select only non-text entry columns
        if (data['questions'][i]['columns'][key]['questionType']['selector'] != 'TE'):
            #and select value -- choiceText from the key, value pairs of the subQuestions (statements/rows)
            for key2, value2 in data['questions'][i]['subQuestions'].items():
                #then need to concatenate those to get the desired variable label
                sbs_nte_var_label_list.append(str(value['questionText']) + ' - ' + str(value2['choiceText']))
  





# Create values list
sbs_nte_value_label_dict_list = []

for i in sbs_nte_range:
    # Iterate through the key, value pairs of the columns
    for key, value in data['questions'][i]['columns'].items():
        #Select only non-text entry columns
        if (data['questions'][i]['columns'][key]['questionType']['selector'] != 'TE'):
            #Create an empty dictionary
            sbs_nte_inner_dict = {}
            # Then iterate through value -- choices for each column
            for key2, value2 in value['choices'].items():
                # Add the recode value and its corresponding label to the dictionary
                sbs_nte_inner_dict.update({value2['recode'] : value2['choiceText']})
            # Then add each dictionary of values and labels to a list for each statement/row
            for j in range(len(data['questions'][i]['subQuestions'])): 
                sbs_nte_value_label_dict_list.append(sbs_nte_inner_dict)

#Create nested dictionary w. var names : values   
sbs_nte_value_label_dict = {sbs_nte_var_list[i] : sbs_nte_value_label_dict_list[i] for i in range(len(sbs_nte_var_list))}





#Create sbs nte values df
sbs_nte_rows = []
for key, values in sbs_nte_value_label_dict.items():
    for k, v in values.items():
        sbs_nte_rows.append([key,k,v])

sbs_nte_values_df = pd.DataFrame(sbs_nte_rows, columns=["Var_Name", "Value","Value_Label"])





#Update data_dict_df with side by side non-text entry vars if any
if len(sbs_nte_var_list) > 0:
    #first create a placeholder df with Var_Name & Var_Labels
    p_data_dict_df = pd.concat([pd.Series(x) for x in [sbs_nte_var_list, sbs_nte_var_label_list]], axis=1).rename(columns={0:"Var_Name",1:"Var_Label"})
    #merge in values df
    p_data_dict_df = pd.merge(p_data_dict_df, sbs_nte_values_df, on='Var_Name', how='inner')
    #assign data type -- INT because categorical
    p_data_dict_df['Data_Type'] = "INT"
    #assign question type
    p_data_dict_df['Question_Type'] = "side-by-side"
    #merge into data_dict_df
    data_dict_df = pd.concat([data_dict_df,p_data_dict_df])


# #### SBS (Side by Side) Variables - Text Entry
# * For side by side variables where the selector is TE




#Create list of QIDs for all sbs var columns where the selector is TE
sbs_te_range = []
for i in sbs_range:
     for key, value in data['questions'][i]['columns'].items(): 
            if (data['questions'][i]['columns'][key]['questionType']['selector'] == 'TE'):
                sbs_te_range.append(i)
            
#Remove duplicates
sbs_te_range_dup = []
[sbs_te_range_dup.append(i) for i in sbs_te_range if i not in sbs_te_range_dup]
sbs_te_range = sbs_te_range_dup





#Create side by side text-entry variable name list
sbs_te_var_list = []

#Need to select key from the key, value pairs of the columns
for i in sbs_te_range:
    for key, value in data['questions'][i]['columns'].items():
        #Select only text entry columns
        if (data['questions'][i]['columns'][key]['questionType']['selector'] == 'TE'):
            #and select key from key, value pairs of the subQuestions (statements/rows)
            for key2, value2 in data['questions'][i]['subQuestions'].items():
                #then add both of those and a trailing _1 to the QID to get the variable importid
                sbs_te_var_list.append(str(i) + '#' + str(key) + "_" + str(key2) + "_1")

#Then rename the importid with the question export tag from the api var list (df)
sbs_te_var_list = [api_q_dict.get(item,item) for item in sbs_te_var_list] 





#Get variable labels
sbs_te_var_label_list = []

#Need to select value -- questionText from the key, value pairs of the columns
for i in sbs_te_range:
    for key, value in data['questions'][i]['columns'].items():
        #Select only text entry columns
        if (data['questions'][i]['columns'][key]['questionType']['selector'] == 'TE'):
            #and select value -- choiceText from the key, value pairs of the subQuestions (statements/rows)
            for key2, value2 in data['questions'][i]['subQuestions'].items():
                #then need to concatenate those to get the desired variable label
                sbs_te_var_label_list.append(str(value['questionText']) + ' - ' + str(value2['choiceText']))





#Create dictionary with responses
sbs_te_inner_dict = {np.nan: 'text'}

#Create nested dictionary w. var names : values
sbs_te_value_label_dict = {sbs_te_var_list[i] : sbs_te_inner_dict for i in range(len(sbs_te_var_list))}

#Create values df 
sbs_te_rows = []
for key, values in sbs_te_value_label_dict.items():
    for k, v in values.items():
        sbs_te_rows.append([key,k,v])
sbs_te_values_df = pd.DataFrame(sbs_te_rows, columns=["Var_Name", "Value","Value_Label"])





#Update data_dict_df with side by side text entry vars if any
if len(sbs_te_var_list) > 0:
    #first create a placeholder df with Var_Name & Var_Labels
    p_data_dict_df = pd.concat([pd.Series(x) for x in [sbs_te_var_list, sbs_te_var_label_list]], axis=1).rename(columns={0:"Var_Name",1:"Var_Label"})
    #merge in values df
    p_data_dict_df = pd.merge(p_data_dict_df, sbs_te_values_df, on='Var_Name', how='inner')
    #assign data type -- INT because categorical
    p_data_dict_df['Data_Type'] = "INT"
    #assign question type
    p_data_dict_df['Question_Type'] = "side-by-side"
    #merge into data_dict_df
    data_dict_df = pd.concat([data_dict_df,p_data_dict_df])


# ### Embedded Data
# * Add each embedded data variable to the data dictionary
# * Will add to values data_dict_df after, as there will be manual labeling needed




#Create Embedded Data Vars list
ED_var_list = []

for i in range(len(data['embeddedData'])):
    ED_var_list.append(data['embeddedData'][i]['name'])





#Update data_dict_df with embedded data -- just var name for now
if len(ED_var_list) > 0:
    #first create a placeholder df with Var_Name
    p_data_dict_df = pd.concat([pd.Series(x) for x in [ED_var_list]], axis=1).rename(columns={0:"Var_Name"})
    #assign question type
    p_data_dict_df['Question_Type'] = "embedded data"
    #merge into data_dict_df
    data_dict_df = pd.concat([data_dict_df,p_data_dict_df])


# ## Step 3: Clean Data Dictionary <a class="anchor" id="3"></a>

# #### Variable order
# * Get variable order from responses dataset
# * Merge with data dictionary
# * Sort data dictionary




#Create Var_Order variable to have consistent order of variables between codebook and df

#Create list of columns
column_list = df.columns.to_list()

#Get order from columns
var_order = []
[var_order.append(i + 1) for i in range(len(column_list))]

#Create a df with columns & their order
var_order_df = pd.DataFrame({'Var_Name': column_list, 'Var_Order':var_order})

#Merge into data_dict_df - outer to see if any errors occured
data_dict_df = pd.merge(data_dict_df, var_order_df, on='Var_Name', how='outer')

#Check work
#view(data_dict_df)





#Sort data_dict_df by 'Value' then 'Var_Order'
data_dict_df['Value'] = data_dict_df['Value'].apply(pd.to_numeric, errors='coerce')
data_dict_df['Var_Order'] = data_dict_df['Var_Order'].apply(pd.to_numeric)
data_dict_df = data_dict_df.sort_values(by=['Var_Order','Var_Name','Value'])

#Reorder variables
data_dict_df = data_dict_df[['Var_Name','Var_Label','Value','Value_Label','Data_Type','Var_Order','Question_Type']]





#Reset the index of the data dictionary
data_dict_df = data_dict_df.reset_index().drop(columns='index')


# #### Clean up variable & value labels




#Functions to strip html
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

#Clean up variable & value labels
def clean_label(x):
    #Remove HTML
    clean_x = strip_tags(x)
    #Remove line breaks
    clean_x = re.sub(r'\n', ' ', clean_x)
    #Remove extra white space (2+)
    clean_x = re.sub(r'\s{2,}', ' ', clean_x)
    #then remove leading white space
    clean_x  = re.sub(r'^\s','', clean_x)
    #finally remove trailing white space
    clean_x = re.sub(r'\s$','', clean_x)
    return clean_x
    
data_dict_df['Var_Label'] = [clean_label(i) for i in data_dict_df['Var_Label'].astype(str)]
data_dict_df['Value_Label'] = [clean_label(i) for i in data_dict_df['Value_Label'].astype(str)]








