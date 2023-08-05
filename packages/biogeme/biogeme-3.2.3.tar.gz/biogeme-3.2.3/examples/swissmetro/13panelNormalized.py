"""File 13panelNormalized.py

:author: Michel Bierlaire, EPFL
:date: Sun Sep  8 19:20:13 2019

 Example of a mixture of logit models, using Monte-Carlo integration.
 The agent effect, accounting for serial correlation, is included.
 The term with the smallest variance has been normalized. 
 The datafile is organized as panel data.
 Three alternatives: Train, Car and Swissmetro
 SP data
"""
import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models

# Read the data
df = pd.read_csv("swissmetro.dat",sep='\t')
database = db.Database("swissmetro",df)

# Data is organized as panel data. The variable ID identifies each individual.
database.panel("ID")

# The Pandas data structure is available as database.data. Use all the
# Pandas functions to invesigate the database
#print(database.data.describe())

# The following statement allows you to use the names of the variable
# as Python variable.
from headers import *

# Removing some observations can be done directly using pandas.
#remove = (((database.data.PURPOSE != 1) & (database.data.PURPOSE != 3)) | (database.data.CHOICE == 0))
#database.data.drop(database.data[remove].index,inplace=True)

# Here we use the "biogeme" way for backward compatibility
exclude = (( PURPOSE != 1 ) * (  PURPOSE   !=  3  ) +  ( CHOICE == 0 )) > 0
database.remove(exclude)

# Parameters to be estimated
ASC_CAR = Beta('ASC_CAR',0,None,None,0)
ASC_TRAIN = Beta('ASC_TRAIN',0,None,None,0)
ASC_SM = Beta('ASC_SM',0,None,None,1)
B_TIME = Beta('B_TIME',0,None,None,0)
B_COST = Beta('B_COST',0,None,None,0)
SIGMA_CAR = Beta('SIGMA_CAR',0,None,None,0)
SIGMA_SM = Beta('SIGMA_SM',0,None,None,1)
SIGMA_TRAIN = Beta('SIGMA_TRAIN',0,None,None,0)

# Define random parameters, normally distributed across individuals,
# designed to be used for Monte-Carlo simulation
EC_CAR = SIGMA_CAR * bioDraws('EC_CAR','NORMAL')
EC_SM = SIGMA_SM * bioDraws('EC_SM','NORMAL')
EC_TRAIN = SIGMA_TRAIN * bioDraws('EC_TRAIN','NORMAL')

# Definition of new variables
SM_COST =  SM_CO   * (  GA   ==  0  ) 
TRAIN_COST =  TRAIN_CO   * (  GA   ==  0  )

# Definition of new variables: adding columns to the database 
TRAIN_TT_SCALED = DefineVariable('TRAIN_TT_SCALED',\
                                 TRAIN_TT / 100.0,database)
TRAIN_COST_SCALED = DefineVariable('TRAIN_COST_SCALED',\
                                   TRAIN_COST / 100,database)
SM_TT_SCALED = DefineVariable('SM_TT_SCALED', SM_TT / 100.0,database)
SM_COST_SCALED = DefineVariable('SM_COST_SCALED', SM_COST / 100,database)
CAR_TT_SCALED = DefineVariable('CAR_TT_SCALED', CAR_TT / 100,database)
CAR_CO_SCALED = DefineVariable('CAR_CO_SCALED', CAR_CO / 100,database)

# Definition of the utility functions
V1 = ASC_TRAIN + B_TIME * TRAIN_TT_SCALED + B_COST * TRAIN_COST_SCALED + EC_TRAIN
V2 = ASC_SM + B_TIME * SM_TT_SCALED + B_COST * SM_COST_SCALED + EC_SM
V3 = ASC_CAR + B_TIME * CAR_TT_SCALED + B_COST * CAR_CO_SCALED + EC_CAR

# Associate utility functions with the numbering of alternatives
V = {1: V1,
     2: V2,
     3: V3}

# Associate the availability conditions with the alternatives
CAR_AV_SP =  DefineVariable('CAR_AV_SP',CAR_AV  * (  SP   !=  0  ),database)
TRAIN_AV_SP =  DefineVariable('TRAIN_AV_SP',TRAIN_AV  * (  SP   !=  0  ),database)
av = {1: TRAIN_AV_SP,
      2: SM_AV,
      3: CAR_AV_SP}

# Conditional to the random variables, the likelihood of one observation is
# given by the logit model (called the kernel)
obsprob = models.logit(V,av,CHOICE)

# Conditional to the random variables, the likelihood of all observations for
# one individual (the trajectory) is the product of the likelihood of
# each observation.
condprobIndiv = PanelLikelihoodTrajectory(obsprob)

# We integrate over the random variables using Monte-Carlo
logprob = log(MonteCarlo(condprobIndiv))

# Define level of verbosity
import biogeme.messaging as msg
logger = msg.bioMessage()
#logger.setSilent()
#logger.setWarning()
logger.setGeneral()
#logger.setDetailed()

# Create the Biogeme object
biogeme  = bio.BIOGEME(database,logprob,numberOfDraws=500)
biogeme.modelName = "13panelNormalized"

# Estimate the parameters. 
results = biogeme.estimate()
pandasResults = results.getEstimatedParameters()
print(pandasResults)



