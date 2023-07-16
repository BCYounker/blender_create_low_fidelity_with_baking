# Blender Low-Fidelity Model Creator

This project offers a bpy Python script that aids in the operation of Blender to generate low-fidelity models from high detail inputs. It performs complex tasks such as mesh reduction, texture mapping, and baking.

## Overview

The aim of this Python script is to simplify and automate the conversion of high-detail Blender models into a more manageable format, reducing the surface detail from 4 million points down to just 6 thousand for provided ply file. This makes it a highly useful tool for 3D modelers, artists, and developers who are working with heavy, complex 3D models and need to downscale them for performance or compatibility reasons.

![surface4M](https://typora-bochen.oss-cn-hongkong.aliyuncs.com/Typora/surface4M.png)

![surface6k](https://typora-bochen.oss-cn-hongkong.aliyuncs.com/Typora/surface6k.png)

*Above: On the left is a model with 4 million surface points. On the right is the same model after being processed by the script, reduced to 6 thousand surface points.*

I used this to autonomously convert a batch of high-fidelity models into low-fidelity models.

![batch](https://typora-bochen.oss-cn-hongkong.aliyuncs.com/Typora/batch.png)

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed on your machine:

- The latest version of [Blender](https://www.blender.org/download/).
- Python 3.6 or higher.

### Preparation

The script uses a .ply file as input. The one used in this project is reconstructed from a non-public dataset, so you'll need to replace this with your own personal .ply file.

### Installation

1. Clone the repository.
2. Navigate to the cloned directory.
3. Make sure to configure your Python path in Blender.

### Running the Script

Execute the `run.py` script to start the operation.

## Usage

This bpy script is perfect for individuals working with heavy 3D models in Blender and need a simplified version of the same. The resultant low-fidelity model maintains the essential features of the original model, making it suitable for rendering, 3D printing, and more.

## License

If you want to use this, please star this project.
