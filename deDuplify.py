import deDupTools as dt
import pandas as pd
import sys

# inFile = input("Enter input file name: ")
# try:
# 	pd.read_csv(inFile)

# except FileNotFoundError:
# 	exit()

inFile = sys.argv[1]

names = pd.read_csv(inFile)
finals = dt.deDuplicate(names)

if '-o' in sys.argv:
	outFile = sys.argv[sys.argv.index('-o')+1]
	finals.loc[1:].to_csv(outFile)
else:
	finals.loc[1:].to_csv("unique_output.csv")
