# TriNet_Seismology

## Paper Title

Deep learning inversion of triplicated P waveforms to constrain the 660-km discontinuity

## Code Structure

```text
dl_mtz_vel/
├── data/ # Stores datasets used in the project
├── figure/ # Stores figures that appear in the paper
├── generatedataset/ # Generates datasets containing triplicated phases
│ ├── generatewaveforms/ # Uses the qseis06 program to generate seismograms
│ └── preprocess/ # Processes seismograms for input into TriNet
└── trinet/ # Training and inference of the deep learning model
└── event_20080519/ # Event ID
└── deeplearning/ # Main deep learning workflow
├── dataset_split/ # Split dataset into training, validation, and test sets
└── train/ # Train the model and obtain results on the test set
└── test-real/ # Generate results for real observational data
```
