"""File 18ordinalLogit.py

:author: Michel Bierlaire, EPFL
:date: Mon Sep  9 08:08:40 2019

 Example of an ordinal logit model.
 This is just to illustrate the syntax, as the data are not ordered. 
 But the example assume, for the sake of it, that they are 1->2->3
 Three alternatives: Train, Car and Swissmetro
 SP data
"""
import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.distributions as dist

# Read the data
df = pd.read_csv("swissmetro.dat",sep='\t')
database = db.Database("swissmetro",df)

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
B_TIME = Beta('B_TIME',0,None,None,0)
B_COST = Beta('B_COST',0,None,None,0)

# Parameters for the ordered logit. 
# tau1 <= 0
tau1	 = Beta('tau1',-1,None,0,0)
# delta2 >= 0
delta2	 = Beta('delta2',2,0,None,0)
tau2 = tau1 + delta2


# Definition of new variables
TRAIN_COST =  TRAIN_CO   * (  GA   ==  0  )

# Definition of new variables: adding columns to the database 
TRAIN_TT_SCALED = DefineVariable('TRAIN_TT_SCALED',\
                                 TRAIN_TT / 100.0,database)
TRAIN_COST_SCALED = DefineVariable('TRAIN_COST_SCALED',\
                                   TRAIN_COST / 100,database)

#  Utility
U = B_TIME * TRAIN_TT_SCALED + B_COST * TRAIN_COST_SCALED 

# Associate each discrete indicator with an interval.
#   1: -infinity -> tau1
#   2: tau1 -> tau2
#   3: tau2 -> +infinity
ChoiceProba = {
    1: 1-dist.logisticcdf(U-tau1),
    2: dist.logisticcdf(U-tau1)- dist.logisticcdf(U-tau2),
    3: dist.logisticcdf(U-tau2) }

# Definition of the model. This is the contribution of each
# observation to the log likelihood function.
logprob = log(Elem(ChoiceProba,CHOICE))

# Define level of verbosity
import biogeme.messaging as msg
logger = msg.bioMessage()
logger.setSilent()
#logger.setWarning()
#logger.setGeneral()
#logger.setDetailed()

# Create the Biogeme object
biogeme  = bio.BIOGEME(database,logprob)
biogeme.modelName = "18ordinalLogit"

# Estimate the parameters
results = biogeme.estimate()
pandasResults = results.getEstimatedParameters()
print(pandasResults)



