# Microwave Imaging
Rohde &amp; Schwarz Microwave Imaging for HackaTUM 2022

## Inspiration
In our project, we aim to help automate large-scale waste separation. Current solutions utilize lasers and cameras to classify unsorted waste. Although they are able to achieve high precision, these systems require the object to be clearly seen. Since the majority of waste is unsorted, the preprocessing step relies heavily on the manual action from human workers: waste needs to be extracted from the plastic bags or cardboard boxes, cleaned and evenly distributed along the sorting line. 

We propose a solution that utilizes both microwave imaging and deep learning. Our goal is to create a real-time visualization and identification of unwanted materials in scenarios where traditional methods would not be able to see them, for example due to them being in a trash bag. Our solution proved to be effective in differentiating between paper, plastic, and metal, by achieving an f1-score of 81%

Our application works as follows:

- A user takes a trash bag filled with a combination of paper, plastic, and metal

- The resulting data gets inputted into our application

- A resulting 3d visualization (256x256x64) and an image with bounding boxes around the objects (identifying them as either plastic, paper, or metal)

- The user can then remove the unwanted items for the recycling process, and continue.

## What it does

We show that microwave imaging provides a better alternative to laser sensing and cameras since it has a signal on common types of waste, such as plastic, metal, and organic. Furthermore, it can “look inside” thin materials like cardboard boxes and plastic bags. 

For this purpose, we collected and labeled a dataset of 341 images of plastic bottles, metal cans and paper, covered by a plastic bag from the sensor to prevent visual contact. The data shows that the signal is strong enough for the microwave sensor to be used in production.

The raw data from the sensor is a set of about 20 256х256 images. We preprocessed the data by calculating the mean of all 2d images, reducing dimensionality with Principal Component Analysis algorithm, and downscaling the data to 64х64 format. We made the dataset publicly available. 

We trained a computer vision model to detect 3 types of waste in an image: plastic, metal, paper. The model was deployed on Vertex AI.
We made an app where the user can upload photo and get predictions. See youtube video.


## How we built it

Our team consists of 4 people, so we were able to divide the tasks equally: two members worked on data preparation and augmentation, one deployed and trained the computer vision model, one worked on the interactive demo. For the preprocessing step, we used python and scikit-learn. The ML model was deployed on Vertex AI.. For the frontend and interactive demo, we used React.

## Challenges we ran into

1) Data collection - we decided to manually collect the dataset, so we spent a lot of time on making images of various combinations of common household waste.

2) Data preparation - the imaging data had a custom format. Although we were provided the functions to work with it, they were not fully documented. It was challenging to get used to the new framework.

3) Interactive demo - we finished training the model only at the end of Day 2 of the hackathon. It took us all night to make the interactive demo.

## Accomplishments that we're proud of

- Creating a microwave image recognition model with an 81% f1 score.

- Creating a 3d model visualization of the scans we took

- Creating the user interface and backend in order to achieve a smooth experience for finding the items in the scan

Utilizing various effective preprocessing techniques

## What we learned

- We learned advanced image recognition and data augmentation techniques

- Team building process and effectively working together in order to develop the entire solution

- Brainstorming for creative and innovative ideas

## Team

- Daniel von Eschwege
- Jordi van Setten
- Kristóf András Sándor 
- Aleksei Zhuravlev


