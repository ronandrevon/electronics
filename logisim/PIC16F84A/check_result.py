#! /bin/python3
import sys
import pandas as pd 

args = sys.argv
file = args[1]
#file='run/mem_test.pic.txt'


# import result file keep only end of instructions, convert W,RA,RB to integers
df = pd.read_csv(file,sep='\t',dtype='str',names=['clk','W','sw','RA','RB','PC'])
df1 = df.loc[df['clk']=='1'][['W','sw','RA','RB','PC']]

for col in ['W','RA','RB'] : 
    df1[col] = list(map(lambda s:int(s.replace(' ',''),2),df1[col] ))
df1['PC'] = list(map(lambda s:hex(int(s.replace(' ',''),2)), df1['PC'] ))

df1.index=range(df1.shape[0])
print(df1)