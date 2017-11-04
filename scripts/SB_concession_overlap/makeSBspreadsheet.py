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



## combine them all

aa =  SBC.nombre + SBC.nombres + " " + SBC.apellidos
aa = aa.str.replace('10','')
aa = aa.str.strip()

## get rid of the "10" values that represent NA, 
## that came from qgis, not sure why

nom = aa

## and I think that worked.

nom.unique()

len(nom)

len(nom.unique())


## append this combined name to SBC 

SBC['ComboName'] = nom

SBC[['ComboName', 'nombre']].head()

SBC[['ComboName', 'nombres', 'apellidos']].tail()

## looks okay. Can we do this with the SB dataframe also?

bb =  SB.nombre + SB.nombres + " " + SB.apellidos
bb = bb.str.replace('10','').str.strip()
SB['ComboName'] = bb

## get rid of repeats, this will be our first column of our new df:
nom = nom.unique()

########### area of each BP:#########

## in HA
SBarea = [ SB[SB.ComboName == i ].area.iloc[0]/10000 for i in nom ]

########### now how do we get the identity of concessions in each?#########

## function to collect names of concessions:

def getconcIDs(cn):
    SBs = SBC.groupby('ComboName')
    bb = SBs.get_group(cn)
    conc_ids = list(bb.nam)
    return(conc_ids)

## try it out:

cn = 'ASOCIACION COFRADIA HUACUPAMBA'

cn = 'HOOVER SANTIAGO JIMENEZ GRANDA'

getconcIDs(cn)

## seems to work

## use it, turn lists into strings
CIDS = [ getconcIDs(i) for i in nom ]
concIDs = pd.Series(CIDS).apply(lambda x : (', '.join(x)))



########### and for the combined areas of concessions?#########


def getconcArea(sn):
    SBs = SBC.groupby('ComboName')
    bb = SBs.get_group(sn)
    concArea_Hai = sum(bb.area)/10000 ## convert to Ha
    return(concArea_Hai)

sn = 'COMUNA GUAMBUZARI'

sn = 'ASOCIACION DE CENTROS SHUAR TAYUNTS'
getconcArea(sn)

## seems okay

## so for each BP:
concArea_Ha = [ getconcArea(i) for i in nom ]


########### now calculate % underconcession:#########

perConc = np.array(concArea_Ha) / np.array(SBarea)

########### add convenio id ###############

convenio = [ SB[SB.ComboName == i ].convenio for i in nom ]

####### make df #########

df = pd.concat([pd.Series(nom), \
    pd.Series(convenio),\
    pd.Series(SBarea),\
    pd.Series(concIDs),\
    pd.Series(concArea_Ha),\
    pd.Series(perConc),\
    ], keys = [ \
        'nom', \
        'convenio', \
        'SBarea', \
        'concIDs', \
        'concArea_Ha', \
        'perConc', \
        ], axis = 1)

## sanity checks
## seems ok

df.to_csv('SB_percent_concessioned.csv')

## 
