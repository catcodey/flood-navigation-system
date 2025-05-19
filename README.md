## Flood-Free Routte Identification and Optimization Using Satellite Imagery and Machine Learning

This is a flood navigation system built using the concept of segmentation on satellite imagery 
All links for datasets and kaggle notebooks have been mentioned in About.  
The installation and instructions on how to run the project is given in Usage.  

###  About
This project was inspired by the Chennai 2015 floods.  
We build a system integrates the foll. 4 concepts water segmentation, elevation-based filtering, road segmentation and shortest path(breadth first search).  
The goal is to create a map-like visualiation where we identify  as many low lying regions as possible and try to find the shortest path to the nearest elevation points of these regions.  

🔶 Water segmentation  
- YOLOV11-m for water segmenatation
- Trained on Custom Google earth imagery [Water seg dataset](https://universe.roboflow.com/reaserch/flood-area-segmentation-biizb)
- Trained on Kaggle [Kaggle notebook](https://www.kaggle.com/code/bhavnab/flood-segmentation/edit)

🔶 Road segmentation
- Beefy U-nets
- Trined on DeepGlobe road extraction dataset [Road extrn dataset](https://www.kaggle.com/datasets/balraj98/deepglobe-road-extraction-dataset)
- Trained on Kaggle [Kaggle notebook](https://www.kaggle.com/code/bhavnab/road-segmentation-using-satellite-images-u-net/edit)


### Usage

- Navigate to project folder using cd cmd.
- create a virtual env of python version 3.11 here. it works only with this python version
- activate the venv using the foll cmd
   - source .3.11venv/bin/activate
- run the requirements.txt in this venv.
- After this open 2 seperate terminals in vs code. Activate the venvs in these 2 terminals.  
- Type the foll cmds in the first terminal. 
    - cd backend (navigating to main.py directory)
    - uvicorn main:app --host 0.0.0.0 --port 8000 --reload    
-Type the foll cmds in the 2nd terminal
  - cd frontend
  - cd src
  - the above 2 cmds will navigate u to the App.js directory
  - npm start
-Thats it!

**NOTE: You execute the uvicorn and npm start commands ONLY inside the directories of the main.py and app.js files in seperate terminals. Otherwise it will not work. Thats what those cd cmds are for.**

