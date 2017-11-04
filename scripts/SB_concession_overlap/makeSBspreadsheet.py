## let's look at some of pandas cleanup methods

import os
import csv
import numpy as np
import pandas as pd


## just read in from spreadsheet:

SBC = pd.read_csv('SB_conc_overlap.csv')
SB = pd.read_csv('SBs.csv')
C = pd.read_csv('Concessions_g.csv')


## what are the goals? 

## a spreadsheet that lists all SBs, and the concessions that touch 
## them, the area of each SB, the area of Concession within them
## and the resulting percent of SB affected by concessions


## can we get a list of all affected SBs?

## we want a column that gives the name if a colective, 
## and the owner namer if individual:

## get colectivas


########### add convenio id ###############

## let's use convenio as our hashable id 

## get a list of all convenios with a concession
## on it:

len(SBC.convenio)

convenio = SBC.convenio.unique()

len(convenio) ## 994

########## add owner/name ##################

## combine owners/names to the master dfs

aa =  SBC.nombre + SBC.nombres + " " + SBC.apellidos
aa = aa.str.replace('10','')
aa = aa.str.strip()
SBC['ComboName'] = aa
## get rid of the "10" values that represent NA, 
## that came from qgis, not sure why



SBC[['ComboName', 'nombre']].head()

SBC[['ComboName', 'nombres', 'apellidos']].tail()

SBC[SBC.convenio == 'MAE-PSB-I-2012-C-021']

## looks okay. Can we do this with the SB dataframe also?

bb =  SB.nombre + SB.nombres + " " + SB.apellidos
bb = bb.str.replace('10','').str.strip()
SB['ComboName'] = bb

## check
SB[['ComboName', 'nombre']].head()
SB[['ComboName', 'nombres', 'apellidos']].tail()

## now get a column of names/owners for each unique convenio:

comboName = [ SB[SB.convenio == i ].ComboName.iloc[0] for i in convenio ]

## looks right...



########### area of each BP:#########

## in HA
SBarea = [ SB[SB.convenio == i ].area.iloc[0]/10000 for i in convenio ]

###########  identity of concessions in each #########

## function to collect names of concessions:

def getconcIDs(cn):
    SBs = SBC.groupby('convenio')
    bb = SBs.get_group(cn)
    conc_ids = list(bb.nam)
    return(conc_ids)

## try it out:

cn = 'MAE-PSB-I-2011-C-006'

getconcIDs(cn)

## seems to work

## use it, turn lists into strings
CIDS = [ getconcIDs(i) for i in convenio ]
concIDs = pd.Series(CIDS).apply(lambda x : (', '.join(x)))


########### and for the combined areas of concessions?#########


def getconcArea(sn):
    SBs = SBC.groupby('convenio')
    bb = SBs.get_group(sn)
    concArea_Hai = sum(bb.area)/10000 ## convert to Ha
    return(concArea_Hai)


sn = 'MAE-PSB-I-2012-C-006'
getconcArea(sn)

## seems okay

## so for each BP:
concArea_Ha = [ getconcArea(i) for i in convenio ]


########### now calculate % underconcession:#########

perConc = np.array(concArea_Ha) / np.array(SBarea)


####### make df #########

df = pd.concat([pd.Series(comboName), \
    pd.Series(convenio),\
    pd.Series(SBarea),\
    pd.Series(concIDs),\
    pd.Series(concArea_Ha),\
    pd.Series(perConc),\
    ], keys = [ \
        'comboName', \
        'convenio', \
        'SBarea', \
        'concIDs', \
        'concArea_Ha', \
        'perConc', \
        ], axis = 1)

## sanity checks
## seems ok


n = 'MAE-PSB-I-2011-I-055'

SB[SB.convenio == n]

df.to_csv('SB_percent_concessioned.csv')

## 
