# Ethan Wen (ISO) - 2/19/2024
"""## 1. Load Data and Examine the Different Headers/Categories"""
from IPython.display import display
import pandas as pd
raw_incidents = pd.read_excel("incidents_jan_2024.xlsx")

raw_incidents.head()

"""Originally downloaded an excel file to house the incidents. Separated the entire month of Janurary 2024 for data exploration/cleaning to make it easier to apply onto Power BI for more relevant results/metrics."""

print(f'Raw Incidents: {len(raw_incidents)}')
print(f'Columns: {raw_incidents.columns}')

"""In the month of Janurary, 758 incidents were resolved. There are 18 columns/categories for each incident.

## 2. Overview of Categories/Columns
"""

len(raw_incidents["Incident name"].unique())

raw_incidents["Incident name"].unique()

"""There seems to be unique incidents in the ```raw_incidents``` dataframe which we can consolidate. There are different DLP policies so we can total the indices in a dictionary. From there, we can "normalize" the incidents to get a better representation in SOC metrics."""

lst_incidents = list(raw_incidents["Incident name"].unique())
len(lst_incidents)

DLP_incidents = []
for incident in lst_incidents:
    if 'DLP' in incident:
        DLP_incidents.append(incident)
del lst_incidents
# splitting up some of the lists so as to get a distinction in DLP incidents, maybe match email, document, cloud, or number of users
PII_DLP_incidents = []
PCI_DSS_incidents = []
leftover_incidents = []
for incident in DLP_incidents:
    if 'PII' in incident:
        PII_DLP_incidents.append(incident)
    elif 'SSN' in incident:
        PII_DLP_incidents.append(incident)
    elif 'PCI' in incident:
        PCI_DSS_incidents.append(incident)
    else:
        leftover_incidents.append(incident)
del DLP_incidents
# print(f'PII: {PII_DLP_incidents}\n')
print(f'PCI: {PCI_DSS_incidents}\n')
# print(f'leftovers: {leftover_incidents}')
# no leftovers now so we can continue to categorize
del leftover_incidents
email_PII_DLP = []
doc_PII_DLP = []
leftover_PII_DLP = []
for incident in PII_DLP_incidents:
    if 'email' in incident:
        email_PII_DLP.append(incident)
    elif 'document' in incident:
        doc_PII_DLP.append(incident)
    else:
        leftover_PII_DLP.append(incident)
print(f'Email PII DLP: {email_PII_DLP}\n')
print(f'Document PII DLP: {doc_PII_DLP}\n')
print(f'Leftovers: {leftover_PII_DLP}')

"""It seems like the unique DLP emails can be categorized as such with PII for emails, PII for documents, and PCI incidents. This will change when implementing new data - 6 months of incidents - so there could be different categories later on. For now, we can standardize the DLP incident names of the ```raw_incident``` dataframe into <mark>3 categories: "DLP policy (PCI Data Security Standard (PCI DSS)) matched for document" (which can be for cloud purposes), "DLP policy (U.S. Personally Identifiable Information (PII) - Exchange email)", and "DLP policy (U.S. Personally Identifiable Information (PII)) matched for document"</mark>. There could be more categories so the following code will be changed later on in the implementation.

## 3. Replace the unique incidents with the ones created in Step 2

Do so through using the index in the dataframe. Search for the matching incidents with the 3 lists implemented.
"""

unique_DLP_PCI = len(PCI_DSS_incidents) + len(email_PII_DLP) + len(doc_PII_DLP)
print(unique_DLP_PCI)

"""This tells us that calling unique on the incident name should count up to **37 unique incidents + 3 that we created for standardization**."""

PCI_DSS_incidents[0]

raw_incidents.columns

# iterate over the raw_incidents and match over the incident names to those designated in the three lists.
check_list = []
for i in range(len(raw_incidents)):
    check = raw_incidents['Incident name'][i]
    if check in PCI_DSS_incidents:
        raw_incidents.at[i, 'Incident name'] = "DLP policy (PCI Data Security Standard (PCI DSS)) matched for document"
        check_list.append(i)
    elif check in email_PII_DLP:
        raw_incidents.at[i, 'Incident name'] = "DLP policy (U.S. Personally Identifiable Information (PII) - Exchange email)"
        check_list.append(i)
    elif check in doc_PII_DLP:
        raw_incidents.at[i, 'Incident name'] = "DLP policy (U.S. Personally Identifiable Information (PII)) matched for document"
        check_list.append(i)

len(check_list)

"""There may be a discrepancy but its pretty close to the 28 unique incidents. To verify this we call unique on raw_incidents."""

len(raw_incidents['Incident name'].unique())

"""All the unique PCI DSS/DLP incidents are reassigned."""

raw_incidents['Incident name'].unique()

"""## 4. Check the importance/frequency of the incidents with the corresponding 40 incident names & Removing unnecessary categories"""

incident_freq = {}
# iterate over the raw_incidents and add up frequency through key-value pairs for a display
for i in range(len(raw_incidents)):
    temp = raw_incidents['Incident name'][i]
    if temp not in incident_freq:
        incident_freq[temp] = 1
    else:
        incident_freq[temp] += 1
print(incident_freq)

import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
x = list(incident_freq.items())
x = [list(i) for i in x]
incident_freq_df = pd.DataFrame(x, columns=['Incident Name', 'Counts'])
incident_freq_df.sort_values(by='Counts', inplace = True, ascending=False)
sns.set_style("whitegrid")
incident_fig, ax = plt.subplots(figsize=(10, 10))
sns.barplot(x='Counts', y='Incident Name', data=incident_freq_df).set(title='Incident Frequency')
ax.bar_label(ax.containers[0])
plt.show()

"""When looking at the incidents, it seems like alot of the incidents overlap in terms of categorization such as the email reported incidents. However, they are slightly different from each other so I will leave them in for the sake of clarity."""

raw_incidents.head()

raw_incidents['Investigation state'].unique()

raw_incidents['Categories'].unique()

raw_incidents['Service sources'].unique()

raw_incidents['Detection sources'].unique()

raw_incidents['Data sensitivity'].unique()

raw_incidents['Status'].unique()

raw_incidents['Determination'].unique()

raw_incidents['Device groups'].unique()

"""Deleting some columns that are repetitive/not useful: **Data sensitivity** (only contains NaN values), **Status** (all incidents are resolved), and **Device groups** (not that useful - one can distinguish through incident name)."""

filtered_incidents = raw_incidents.drop(['Data sensitivity', 'Status', 'Device groups'], axis=1)

filtered_incidents.head()

"""### 5. Next Steps (Replace values with "-" to NaN values, Converting time from first to last activity, Creating new column called Time Elapsed, Perhaps doing something with Impacted Assets)"""

import numpy as np

filtered_incidents = filtered_incidents.replace('-', np.nan)

filtered_incidents.head()

"""The time dates on first activity and last activity are in ISO 8601."""

from datetime import datetime
result = datetime.fromisoformat('2024-01-31T22:36:02.000Z') - datetime.fromisoformat('2024-01-31T22:36:02.000Z')

"""Convert the ISO 8601 times to actual datetime from the two columns: 'First activity' and 'Last activity'"""

for i in range(len(filtered_incidents)):
    filtered_incidents.at[i, 'First activity'] = datetime.fromisoformat(filtered_incidents['First activity'][i])
    filtered_incidents.at[i, 'Last activity'] = datetime.fromisoformat(filtered_incidents['Last activity'][i])

"""Now the times are listed in the **current format (Year-Month-Day) and (Hour-Minutes-Seconds-Milliseconds)**. We can now create a new column that will hopefully get us more insights into these incidents."""

filtered_incidents['Time Elapsed'] = (filtered_incidents['Last activity'] - filtered_incidents['First activity'])

print(filtered_incidents['Time Elapsed'][0:20])

for i in range(len(filtered_incidents)):
    filtered_incidents.at[i, 'Time Elapsed'] = filtered_incidents['Time Elapsed'][i].total_seconds()

print(filtered_incidents['Time Elapsed'].unique())

"""Seems like hours or minutes may be a better indication of time for these incidents. For now, choosing **hours** as a measurement instead of seconds seems to be the best choice."""

filtered_incidents['Time Elapsed'] = filtered_incidents['Time Elapsed']/3600
for i in range(len(filtered_incidents)):
    filtered_incidents.at[i, 'Time Elapsed'] = round(filtered_incidents['Time Elapsed'][i], 2)

max(filtered_incidents['Time Elapsed'].unique())

"""This was a good measurement since it seemed like the max amount of time was less than 24 hours."""

print(filtered_incidents['Impacted assets'].unique())

"""After reviewing the different strings in the filtered incidents, there seemed to be some patterns in place.
1. Accounts: (Last Name, First Name) or (Department),Mailboxes: (Last Name, First Name) or (Department)
2. Accounts: (Last Name, First Name) or (Department),Apps: (Application)
3. undefined: (email address)
4. Mailboxes: (email address)
5. Accounts: (Last Name, First Name)
6. undefined: (email address)  
...etc
"""

test_impacted_assets = filtered_incidents['Impacted assets'][0:5]

print(test_impacted_assets)

"""Trying to split up the people/assets/organizations impacted by the incident. We can organize this into 4 columns: people impacted, devices, email addresses, and applications."""

type(test_impacted_assets)

test_df = test_impacted_assets.to_frame()

# split by colon - ':'
check_entities = ['Accounts', 'Mailboxes', 'undefined', 'Apps']
apps = ['Microsoft Exchange Online', 'Microsoft OneDrive for Business', 'Microsoft SharePoint Online', 'Microsoft Power BI', 'Microsoft 365', 'Service Mailbox', 'COI Support', 'UT System Vulnerability Manager', 'ftp']

def sorting_data(test_df):
    # add the new columns
    test_df['people_impacted'] = np.nan
    test_df['devices_impacted'] = np.nan
    test_df['emails_impacted'] = np.nan
    test_df['apps_impacted'] = np.nan
    for idx, value in test_df['Impacted assets'].items():
        # skipping NaN values in Impacted assets
        if pd.isna(value) == False:
            temp_list = value.split(':')
            # we know that the first element in the list will be an "entity" the name that I have given for the different columns
            # check the entries into the temp_list and add to either people_impacted, devices, emails, and or apps.
            people_impacted = [] # should be the else option
            devices_impacted = [] # should contain .local
            emails_impacted = [] # should contain @
            apps_impacted = [] # should be in the apps
            people = [] # arranged in full names
            for k in temp_list:
                # i is the next entry - most likely a list
                entry_list = k.split(',')
                for j in entry_list:
                    j = j.strip()
                    if j in apps:
                        apps_impacted.append(j)
                    elif '@' in j:
                        emails_impacted.append(j)
                    elif '.local' in j:
                        devices_impacted.append(j)
                    # additional rule to get all devices into the list
                    elif 'utsystem.edu' in j:
                        devices_impacted.append(j)
                    else:
                        people_impacted.append(j)
            # error with usernames - first example - index 75
            # error - Institute for Transformational Learning
            print(people_impacted)
            usernames = {'snash':'Nash, Sean', 'ITL Info':'Info, ITL', 'Office of Talent and Innovation':'Talent_and_Innovation, Office_of'}
            # replace the username with the full name
            for username in usernames.keys():
                if username in people_impacted:
                    print('Yes')
            for username in usernames.keys():
                for i in range(1, len(people_impacted)):
                    print(username)
                    print(i)
                    if people_impacted[i] == username:
                       #  print('Yes')
                        people_impacted[i] = usernames[username]
                        # splitting the element into 2
                        split_items = people_impacted[i].split(', ')
                        people_impacted = people_impacted[0:1] + people_impacted[1:i] + split_items
            # after sorting the four different types of data/things impacted into the lists - we can try to arrange the names to full names in the list "people"
            counter = 0
            full_name = ''
            # skip the check_entities
            for s in people_impacted:
                if s not in check_entities and counter == 0:
                    full_name = s
                    counter += 1
                elif s not in check_entities and counter == 1:
                    full_name = s + ' ' + full_name
                    counter = 0
                    people.append(full_name)
                    full_name = ''

            # remove duplicate names that show up under the different entities/columns
            people = list(set(people))

            # after getting the completed lists of data - we can reassign them as a value back into test_df and leave them as nan values if empty
            # we should assign the lists as strings - convert before putting into the column
            if people != []:
                new_str = ', '.join([str(ele) for ele in people])
                test_df.at[idx, 'people_impacted'] = new_str
            if devices_impacted != []:
                new_str = ', '.join([str(ele) for ele in devices_impacted])
                test_df.at[idx, 'devices_impacted'] = new_str
            if emails_impacted != []:
                new_str = ', '.join([str(ele) for ele in emails_impacted])
                test_df.at[idx, 'emails_impacted'] = new_str
            if apps_impacted != []:
                new_str = ', '.join([str(ele) for ele in apps_impacted])
                test_df.at[idx, 'apps_impacted'] = new_str
    return test_df

display(sorting_data(test_df))

print(len(filtered_incidents['Impacted assets'].unique()))

"""We should test this over different sections or go over it sequentially to make sure that this process doesn't get messed up."""

test_impacted_assets = filtered_incidents['Impacted assets'][5:20]
test_df = test_impacted_assets.to_frame()
# printing every row - data is gettng cutoff
for asset in test_df['Impacted assets']:
    print(asset)

"""Trying the same method on it but should have the same results."""

display(test_df)

display(sorting_data(test_df))

test_impacted_assets = filtered_incidents['Impacted assets'][20:40]
test_df = test_impacted_assets.to_frame()
for asset in test_df['Impacted assets']:
    print(asset)

display(sorting_data(test_df).loc[[38,39]])

"""**Row 38** of the dataframe is different from the other rows before. The impacted assets in accounts that aren't names are **Service Mailbox, COI Support, UT System Vulnerability Manager, and ftp**.  
**Row 39** of the dataframe is also different from the other rows - it contains an email address but doesn't get put into the emails_impacted column.

To fix this we can put Service Mailbox, COI Support, UT System Vulnerability Manager, and ftp into the apps list. The nessus.utsystem.edu seems to be a device rather than an email address. We can include this with an additional elif statement.

<mark>*Update was succesful in the change and the impacted assets are placed in the various categories</mark>
"""

test_impacted_assets = filtered_incidents['Impacted assets'][40:100]
test_df = test_impacted_assets.to_frame()
for asset in test_df['Impacted assets']:
    print(asset)

"""There may be an error due to the undefined row in the following test_df - snash. We can try to go ahead and sort that though.

Got an error - perhaps because of the nan value on row 43.
"""

display(test_df.loc[[43]])

"""Writing another if statement to ignore NaN values in **Impacted assets** could resolve this issue.

<mark>*Update fixed the NaN error - check to see if there are any other errors in the sorting</mark>

Seems to be a error in row 75 with **snash** missing from the Impacted Assets
"""

print(test_df.loc[[75]])

"""Seems like **snash** probably corresponds to the user, Sean Nash. Perhaps we can store everything else into usernames as well after sorting everything else and deal with that later (changing usernames into full names maybe)."""

test_df = test_df.loc[[75]]
print(test_df)

# drop the columns that aren't impacted assets for the test
# test_df = test_df.drop(['people_impacted', 'devices_impacted', 'emails_impacted', 'apps_impacted'], axis = 1)

for asset in test_df['Impacted assets']:
    print(asset)

for idx, value in test_df['Impacted assets'].items():
    temp_list = value.split(':')
    # we know that the first element in the list will be an "entity" the name that I have given for the different columns
    # check the entries into the temp_list and add to either people_impacted, devices, emails, and or apps.
    people_impacted = [] # should be the else option
    devices_impacted = [] # should contain .local
    emails_impacted = [] # should contain @
    apps_impacted = [] # should be in the apps
    people = [] # arranged in full names
    misc = [] # new list for miscellaneous - usernames
    for k in temp_list[1:]:
    # i is the next entry - most likely a list
        entry_list = k.split(',')
        for j in entry_list:
            j = j.strip()
            if j in apps:
                apps_impacted.append(j)
            elif '@' in j:
                emails_impacted.append(j)
            elif '.local' in j:
                devices_impacted.append(j)
            # additional rule to get all devices into the list
            elif 'utsystem.edu' in j:
                devices_impacted.append(j)
            else:
                people_impacted.append(j)

print(apps_impacted)
print(emails_impacted)
print(devices_impacted)
print(people_impacted)

test_df = filtered_incidents['Impacted assets'][75:76]
test_df = test_df.to_frame()

print(test_df)

sorting_data(test_df)

"""Works for now but definitely needs to be tweaked around in order to make the function better in case of multiple usernames.

<mark>*Update fixed the username Sean Nash error and put it into people_impacted</mark>
"""

test_impacted_assets = filtered_incidents['Impacted assets'][100:150]
test_df = test_impacted_assets.to_frame()
for asset in test_df['Impacted assets']:
    print(asset)

# sorting_data(test_df)

"""Issue in row 103 - ITL Info should still be in the people section."""

test_df = filtered_incidents['Impacted assets'][103:104]
test_df = test_df.to_frame()

print(test_df)

sorting_data(test_df)

"""<mark>*Update - fixed the ITL Info Issue</mark>

Commenting out - checking over all the rows as a check.
"""

# test_df = filtered_incidents['Impacted assets'][150:200]
# test_df = test_df.to_frame()

# sorting_data(test_df)

# test_df = filtered_incidents['Impacted assets'][200:250]
# test_df = test_df.to_frame()

# sorting_data(test_df)

# test_df = filtered_incidents['Impacted assets'][250:300]
# test_df = test_df.to_frame()

# sorting_data(test_df)

# test_df = filtered_incidents['Impacted assets'][300:350]
# test_df = test_df.to_frame()

# sorting_data(test_df)

# test_df = filtered_incidents['Impacted assets'][350:400]
# test_df = test_df.to_frame()

# sorting_data(test_df)

test_df = filtered_incidents['Impacted assets'][460:461]
test_df = test_df.to_frame()
sorting_data(test_df)

"""Problems: row 460, row 482  

Accounts: Adler, Karen,Ruiz-Esparza, Yvette,Bennett, Jean,UT System Public Affairs,Office of Talent and Innovation,Mailboxes: OES, Careers,Burgdorf, Barry D.,Bennett, Jean,UT System Public Affairs,Frazier, Catherine

Comments on the error - trying to lower the amount of iterations across the different one liner - not normal full names. This would help with the additional entities **UT System Public Affairs, Office of Talent and Innovation, and OES**.
"""

