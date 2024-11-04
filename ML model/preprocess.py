import pandas as pd
from ast import literal_eval

# Load the collected dataset
data = pd.read_csv("interaction_data.csv")

# Convert string representations of lists back to lists
data['mouse_movement'] = data['mouse_movement'].apply(literal_eval)
data['click_speed'] = data['click_speed'].apply(literal_eval)

# Feature Engineering
# Example: Summarize mouse movement and click speed by calculating their lengths and averages
data['mouse_movement_count'] = data['mouse_movement'].apply(len)
data['mouse_movement_avg'] = data['mouse_movement'].apply(lambda x: sum(p['time'] for p in x) / len(x) if x else 0)
data['click_speed_avg'] = data['click_speed'].apply(lambda x: sum(x) / len(x) if x else 0)

# Finalize features for modeling
final_data = data[['mouse_movement_count', 'mouse_movement_avg', 'click_speed_avg', 
                   'device_orientation', 'scroll_depth', 'time_on_page', 'label']]

# Save the processed data for training
final_data.to_csv("processed_interaction_data.csv", index=False)
