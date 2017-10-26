## let's look at some of pandas cleanup methods

import os
import csv
import numpy as np
import pandas as pd

## did we ever make a json file out of our bp_conc 
## spreadsheet? dunno. 

## just read in from spreadsheet:

BPC = pd.read_csv('../mining_data/BP_Conc_Intersect_g.csv')
BP = pd.read_csv('../mining_data/BP_g.csv')
C = pd.read_csv('../mining_data/Concessions_g.csv')


## what are the goals? 
## a spreadsheet with concessions by territory, sorted by size
## a spreadshhet of BPs affected by concessions, sorted by area affected

## lotsa other stuff. But gotta be real in the goals

## so for today? get the locations split out on both pandas, export as csvs
## put them and the map of loscedros on the website

## so back to the basics - how do we split this column into two?

PROV = BPC['ubicacion'].apply(lambda x : x.split(';'))

## or 

PROV = BPC['ubicacion'].str.split(';')

PROV[0][0]

## but to get at the elements of this list?

PROV1 = [ a[0].split(':')[1].strip() for a in PROV ]
PROV2 = [ a[1].split(':')[1].strip() for a in PROV ]

## as long as the indices line up, we can do this:
BPC['Prov'] = PROV1
BPC['Cant'] = PROV2

## repeat all that for the BP df:

## not working#########
PROV = BP['ubicacion'].str.split(';')
PROV1 = [ a[0].split(':')[1].strip() for a in PROV ]
PROV2 = [ a[1].split(':')[1].strip() for a in PROV ]
BP['Prov'] = PROV1
BP['Cant'] = PROV2
## not working#########

## aside, roo wants LC's number:

BP = BP.set_index('nombre')
BP.loc['LOS CEDROS']
BP = BP.reset_index()

## okay, how do we group the BP/concession chart by BP?

## can we get a list of all affected BPs?
noms = BPC.nombre.unique()

## have a feeling this would be a lot easier with a database
## oh well, just spit this out. Set up dbs later

##noms is our first column. we also want the BP code...
BPcode = [ BP[BP.nombre == i ].cod_bosq_m.iloc[0] for i in noms ]

########### area of each BP:#########

BParea_Ha = [ BP[BP.nombre == i ].area_ha.iloc[0] for i in noms ]

########### now how do we get the identity of concessions in each?#########

## function to collect names of concessions:
def getconcIDs(nom):
    BPs = BPC.groupby('nombre')
    bb = BPs.get_group(nom)
    conc_ids = list(bb.nam)
    return(conc_ids)

## so for each BP:
concIDs = [ getconcIDs(i) for i in noms ]

## how can we convert our concession ids to strings,
## join into a single cell of a spreadsheet?

## a function to get rid of empty decimal of a concID if necessary:
def cleanzero(i): ## uses a float
    i = str(i)
    if float(i) % 1 == 0: ## if there is a decimal
        dec = i.find('.') ## find decimal
        zoop = i[:dec] ## remove
    else: zoop = str(i)
    return(zoop)

## nest into another function, that can handle a list, and joins?
def cleanallzeros(lst): 
    if type(lst) is list: ## if it's a list of numbers
        clz = [ cleanzero(str(j)) for j in lst ]
        clzs = ", ".join(clz)
    elif type(lst) is float: ## if its a scalar 
        clzs = cleanzero(str(lst))
    return(clzs)

## apply this to all of the lists in concIDs
concIDs = pd.Series(concIDs).apply(cleanallzeros)

########### and for the combined areas of concessions?#########


def getconcArea(nom):
    BPs = BPC.groupby('nombre')
    bb = BPs.get_group(nom)
    concArea_Hai = sum(bb.area)/10000 ## convert to Ha
    return(concArea_Hai)

## so for each BP:
concArea_Ha = [ getconcArea(i) for i in noms ]

########### now calculate % underconcession:#########

perConc = np.array(concArea_Ha) / np.array(BParea_Ha)

####### province information for each BP #########

## locations, province and canton
BPub = [ list(BP[BP.nombre == i ].ubicacion)[0] for i in noms ]

len(BPub)

## split it up:

ublist = pd.Series(BPub).str.split(';')

## take out just the first elemnent of resulting lists
BPprov = [ a[0].split(':')[1].strip() for a in ublist ]


## did this work?
df = pd.concat([pd.Series(noms), \
        pd.Series(BPcode), \
        pd.Series(BPprov), \
        pd.Series(concIDs), \
        pd.Series(concArea_Ha), \
        pd.Series(BParea_Ha), \
        pd.Series(perConc), \
    ], keys = [ \
        'noms', \
        'BPcode', \
        'BPprov', \
        'concIDs', \
        'concArea_Ha', \
        'BParea_Ha', \
        'perConc', \
        ], axis = 1)

## sanity checks
## seems ok

df.to_csv('BP_percent_concessioned.csv')


