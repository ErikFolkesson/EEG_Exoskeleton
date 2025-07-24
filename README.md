# Introduction

The aim of this project is to develop a classifier for Motor Imagery (MI) EEG signals, with a focus on applications for stroke patients. The classifier leverages neural network models to distinguish between different imagined movements, supporting rehabilitation and assistive technologies.

## Dataset
Dataset used: https://www.bbci.de/competition/iv/#dataset1 - specifically "Data sets 2a". Full paper can be found here: https://www.bbci.de/competition/iv/desc_2a.pdf. 

Summary of the dataset: 
The dataset contains data from 9 subjects. It collects data using a cue based Motor Imagery (MI). 

The dataset contains 4 tasks, which are imagination of movement of: 
- left hand (class 1)
- right hand (class 2)
- both feet (class 3)
- tongue (class 4)

Each subject was recorded in two sessions on two different days. Each session is comprised of 6 runs which are separated by short breaks. Each run consists of 48 trials, 12 for each class. This means each session contains 288 trials. At the start of each session a recoding of roughly 5 minutes was done to estimate the EOG influence. A cue happens at second 2, telling the subject what body part to imagine moving. The subject then imagines moving the body part until second 6. 

Signals were recorded with a sampling rate of 250 Hz. A bandpass-filter filtered out signals outside of 0.5-100 Hz. Sensitivity of the amplifier was set to 100 $\mu V$. A notch filter at 50 Hz was also applied to remove line noise. 

3 EOG channels were also recorded. Sampling rate of 250 Hz. Same bandpass and notch filter. Sensitivity of amplifier was set to 1 mV. 

## Project Structure

The project is organized as follows:

- `data/`: Contains raw and processed EEG data.
  - `raw_data/`: Original dataset files.
  - `processed_data/`: Preprocessed data ready for analysis.
- `logs/`: Stores training and evaluation logs.
- `models/`: Saved model checkpoints and related files.
- `notebooks/`: Jupyter notebooks for exploration, model development, and analysis.
- `src/`: Source code for data handling, preprocessing, feature extraction, modeling, and utilities.
  - `data/`: Data loading and management.
  - `feature_extractors/`: Feature extraction methods.
  - `models/`: Neural network and classifier implementations.
  - `pre_processors/`: Signal preprocessing routines.
  - `utils/`: Helper functions for data and visualization.