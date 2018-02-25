# NameDeduplicate
Finding unique entries in a list containing first name, last name, gender and date of births of various people
## Intro
Variation in names leads to difficulty in identifying a unique person and hence deduplication  of records is an unsolved challenge. 
DeDuplication becomes significantly easier if additional information such as date of birth and gender is known. A similar problem has been targeted in this project where entries which are identified as same are merged together and recurrent occurrences are eliminated.

## How to use?
If you wish to try it out on your own dataset follow these steps:

1. Clone the repository

2. Open your favourite command line interface

3. Navigate to the cloned folder

4. Copy the desired data file and run the following command: `python deDuplify.py "Name of your file in csv format without quotes"`. 
Make sure the inputfile you wish to include is present in the cloned folder and is of the csv format. If not specified explicitly, the script will use the name.csv file as input.
For example:`python deDuplify.py mixedNames.csv`

5. The output will be provided in the form of `unique_output.csv` in the same folder as the script. If you wish to get the output file with some specific name then use -o flag as follows: `python deDuplify.py names.csv -o name2.csv` :tada:
6. If you wish to dive in the technicalities of this script, checkout the [Name DeDuplicator.ipynb](Name%20DeDuplicator.ipynb)
7. If you are here for evaluation please download the :sparkles: [Apporach.ppsx](Approach.ppsx) :sparkles: file

Note: The input csv should contain the following attributes - "ln", "fn", "dob", "gn" signifying the last name, first name, date of birth and gender of the person
