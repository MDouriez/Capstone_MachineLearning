# Casptone_MachineLearning

Authors: Marie Douriez, Ludovic Thea

Contains code used for data analysis

- **csv files**: contains csv files of processed data collected in Ludovic's house. <br />
-- *X_1st_batch.csv*:  data collected just before Springbreak <br />
--*X_2nd_batch.csv* : data collected just after Springbreak <br />
--*y.csv, y_alldata.csv*:  labels (activities) <br />
--*presence.csv*: presence features used to model Ludovic's housemates actions <br />

- **utils files**: contains files to handle csv files (open, split, merge...) and plot data <br />
--*processFile.py*: opens csv file <br />
--*plot.py*: plot data without dates <br />
--*plot_withdates.py*: plot data with dates <br />
--*split_newfile.py*: split one csv file into multiple files for each value recorded <br />
--*merge_files.py*: merge multiple csv files together <br />

- **event detection**: files for events detection <br />
--*mattress.ipynb*: sleeping detection <br />
--*shower stove detection.ipynb*: for shower/stove activity detection <br />
--*plot_lever3.py*: script used to detect the usage of a toilet flush <br />

- **activity recognition**: files to process data, create final matrices and perform some analysis <br />
--*annotations.py*: creates labels vector from csv files of annotations <br />
--*featurize.ipynb*: for each sensor file, creates features <br />
--*create_X.py*: concatenate all features for all sensors and create final matrix X <br />
--*Data_analysis_clean.ipynb*: performs analysis (Random Forest, OneVsRestClassifier, confusion matrices...) <br />
