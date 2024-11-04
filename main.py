from fastapi import FastAPI, Request
import pandas as pd
import os

app = FastAPI()

# Initialize empty dataset file if it doesn't exist
if not os.path.exists("interaction_data.csv"):
    pd.DataFrame(columns=["mouse_movement", "click_speed", "device_orientation",
                          "scroll_depth", "time_on_page", "label"]).to_csv("interaction_data.csv", index=False)

@app.post("/collect_data")
async def collect_data(request: Request):
    data = await request.json()

    # Extract and format the data for saving
    mouse_movement = str(data['mouse_movement'])
    click_speed = str(data['click_speed'])
    device_orientation = data['device_orientation']
    scroll_depth = data['scroll_depth']
    time_on_page = data['time_on_page']
    label = data['label']

    # Append to CSV
    new_data = pd.DataFrame([{
        "mouse_movement": mouse_movement,
        "click_speed": click_speed,
        "device_orientation": device_orientation,
        "scroll_depth": scroll_depth,
        "time_on_page": time_on_page,
        "label": label
    }])
    new_data.to_csv("interaction_data.csv", mode='a', header=False, index=False)
    
    return {"status": "success", "message": "Data collected successfully"}
