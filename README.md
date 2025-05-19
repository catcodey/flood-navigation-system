## Flood-Free Routte Identification and Optimization Using Satellite Imagery and Machine Learning

This is a flood navigation system built using the concept of segmentation on satellite imagery 
All links for datasets and kaggle notebooks have been mentioned in About.  
The installation and instructions on how to run the project is given in Usage.  

###  About
This project was inspired by the Chennai 2015 floods.  
We build a system integrates the foll 4 concepts water segmentation, elevation-based filtering, road segmentation and shortest path(bfs).  
The goal is to create a map-like visualiation where we identify  as many low lying regions as possible and try to find the shortest path to the nearest elevation points of these regions.  

🔶 Water segmentation  
- YOLOV11-m for water segmenatation
- Trained on Custom Google earth imagery [Water seg dataset](https://universe.roboflow.com/reaserch/flood-area-segmentation-biizb)
- Trained on Kaggle [Kaggle notebook](https://www.kaggle.com/code/bhavnab/flood-segmentation/edit)

🔶 Road segmenatation
- Beefy U-nets
- Trined on DeepGlobe road extraction dataset [Road extrn dataset](https://www.kaggle.com/datasets/balraj98/deepglobe-road-extraction-dataset)
- Trained on Kaggle [Kaggle notebook](https://www.kaggle.com/code/bhavnab/road-segmentation-using-satellite-images-u-net/edit)

  
### Usage
