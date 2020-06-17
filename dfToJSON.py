import numpy as np 
import pandas as pd   
data = np.array([['1', '2'], ['3', '4']])   
dataFrame = pd.DataFrame(data, columns = ['col1', 'col2']) 
print(dataFrame)
json = dataFrame.to_json('temp.json', orient='records', lines=True) 
print(json) 