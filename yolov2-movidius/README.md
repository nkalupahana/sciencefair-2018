# Introduction
The TinyYolo V2 network can be used for object recognition and classification.  See [https://pjreddie.com/darknet/yolov2/](https://pjreddie.com/darknet/yolov2/) for more information on this network.
The provided Makefile does the following
1. Clones the Darkflow repo.
2. Downloads the Tiny Yolo v2 cfg and weights files.
3. Converts the cfg and weights files to a Tensorflow pb file.
3. Profiles and Compiles the network using the Neural Compute SDK.

# Makefile
Provided Makefile has various targets that help with the above mentioned tasks.

## make help
Shows available targets

## make all
Runs profile, compile.

## make profile
Runs the provided network on the NCS and generates per layer statistics that are helpful for understanding the performance of the network on the Neural Compute Stick.

## make compile
Uses the network description and the trained weights files to generate a Movidius internal 'graph' format file.  This file is later used for loading the network on to the Neural Compute Stick and executing the network.

## make clean
Removes all the temporary files that are created by the Makefile

## search_bing_api.py
This Python file downloads a ton of images for an image dataset by running a given search term term against the Bing Image Search API.
