# Maulwurf ⛏️
 Track and visualize caves in Star Citizen

## Setup ⚙️
#### 1. Install python
#### 2. Install modules
```py
pip3 install keyboard
pip3 install pyperclip
pip3 install pynput
pip3 install numpy
pip3 install matplotlib
pip3 install ntplib
```
#### 3. Clone this repo

## Usage
### Meteorology Mapper
#### 1. Convert your .txt file to a json file using the ``txt_to_json.py``script
#### 3. Render the new .json file using the ``visualizer.py``script
### Terrain Mapper
#### 1. Fly to a cave in Star Citizen
#### 2. Run "tracker.py" in the console
#### 3. Go to a location on a planet
- Doesn't matter if its a cave or on the surface
#### 4. Press "Q" when done to save
#### 6. Run "visualizer.py" and specify the name of the planet
