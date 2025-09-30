import os
import pandas as pd

folder_name = 'database'
file_name = 'rf.csv'
file_path = os.path.join(folder_name, file_name)
df_rf = pd.read_csv(file_path)

folder_name = 'database'
file_name = 'rf.csv'
file_path = os.path.join(folder_name, file_name)
merged_df = pd.read_csv(file_path)

merged_final['year_month'] = merged_final['date'].dt.to_period('M')
df_rf['year_month'] = df_rf['date'].dt.to_period('M')

merged_df = pd.merge(merged_final, df_rf, on='year_month', how='left')
merged_df.drop(columns=['year_month'], inplace=True)

print(merged_df)