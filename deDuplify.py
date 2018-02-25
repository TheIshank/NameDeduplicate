import deDupTools as dt
import pandas as pd
import sys

if len(sys.argv)>1:
	inFile = sys.argv[1]
else:
	inFile = "sample_input.csv"

names = pd.read_csv(inFile)
finals = dt.deDuplicate(names)

if '-o' in sys.argv:
	outFile = sys.argv[sys.argv.index('-o')+1]
	finals.loc[1:].to_csv(outFile)
else:
	finals.loc[1:].to_csv("sample_output.csv")
