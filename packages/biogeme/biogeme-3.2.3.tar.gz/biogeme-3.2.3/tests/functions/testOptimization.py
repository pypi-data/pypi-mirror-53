import unittest
import random as rnd
import biogeme.biogeme as bio
import biogeme.database as db
import biogeme.optimization as opt
import pandas as pd
import numpy as np
from biogeme.expressions import *

def rosenbrock(x,hessian=False):
    n = len(x)
    f = sum(100.0 * (x[i+1]-x[i]**2)**2 + (1.0-x[i])**2 for i in range(n-1))
    g = np.zeros(n)
    for i in range(n-1):
        g[i] = g[i] - 400 * x[i] * (x[i+1]-x[i]**2)  - 2 * (1-x[i])
        g[i+1] = g[i+1] + 200 * (x[i+1]-x[i]**2)
    if hessian:
        H = np.zeros((n,n))
        for i in range(n-1):
            H[[i],[i]] = H[[i],[i]] - 400 * x[i+1] + 1200 * x[i]**2 + 2
            H[[i+1],[i]] = H[[i+1],[i]] - 400 * x[i]
            H[[i],[i+1]] = H[[i],[i+1]] - 400 * x[i]
            H[[i+1],[i+1]] = H[[i+1],[i+1]] + 200
        return f,g,H
    else:
        return f,g,None

class testOptimization(unittest.TestCase):
    def setUp(self):
        np.random.seed(90267)
        rnd.seed(90267)
        df = pd.DataFrame({'Person':[1,1,1,2,2],
                   'Exclude':[0,0,1,0,1],
                   'Variable1':[1,2,3,4,5],
                   'Variable2':[10,20,30,40,50],
                   'Choice':[1,2,3,1,2],
                   'Av1':[0,1,1,1,1],
                   'Av2':[1,1,1,1,1],
                   'Av3':[0,1,1,1,1]})
        myData = db.Database('test',df)
        
        Choice=Variable('Choice')
        Variable1=Variable('Variable1')
        Variable2=Variable('Variable2')
        beta1 = Beta('beta1',0,None,None,0)
        beta2 = Beta('beta2',0,None,None,0)
        V1 = beta1 * Variable1
        V2 = beta2 * Variable2
        V3 = 0
        V ={1:V1,2:V2,3:V3}

        likelihood = bioLogLogit(V,av=None,choice=Choice)
        self.myBiogeme = bio.BIOGEME(myData,likelihood)
        self.myBiogeme.modelName = 'simpleExample'


    def testSchnabelEskow(self):
        A = np.array([[0.3571,-0.1030,0.0274,-0.0459],[-0.1030,0.2525,0.0736,-0.3845],[0.0274,0.0736,0.2340,-0.2878],[-0.0459,-0.3845,-0.2878,0.5549]])
        L,E,P = opt.schnabelEskow(A)
        self.assertAlmostEqual(L[0,0],0.7449161,5)
        diff = P @ L @ L.T @ P.T - E - A
        for i in list(diff.flatten()):
            self.assertAlmostEqual(i,0.0,5)

    def testSchnabelEskow2(self):
        A = np.array([[1890.3,-1705.6,-315.8,3000.3],[-1705.6,1538.3,284.9,-2706.6],[-315.8,284.9,52.5,-501.2],[3000.3,-2706.6,-501.2,4760.8]])        
        L,E,P = opt.schnabelEskow(A)
        self.assertAlmostEqual(L[0,0],6.89985507e+01,5)
        diff = P @ L @ L.T @ P.T - E - A
        for i in list(diff.flatten()):
            self.assertAlmostEqual(i,0.0,5)

    def testLineSearch(self):
        x = np.array([-1.5,1.5])
        def function(x):
            f,g,h = rosenbrock(x)
            return f,g
        f,g = function(x)
        alpha,nfev = opt.lineSearch(function,x,-g)
        self.assertAlmostEqual(alpha,0.0009765625)

    def testNewton(self):
        x0 = np.array([-1.5,1.5])
        xstar,nit,nfev,msg = opt.newtonLineSearch(rosenbrock,x0)
        for i in list(xstar):
            self.assertAlmostEqual(i,1,4)

    def testNewtonTrustRegion(self):
        x0 = np.array([-1.5,1.5])
        xstar,nit,nfev,msg = opt.newtonTrustRegion(rosenbrock,x0)
        for i in list(xstar):
            self.assertAlmostEqual(i,1,4)
        
    def testBioScipy(self):
        results = self.myBiogeme.estimate()
        beta = results.getBetaValues()
        self.assertAlmostEqual(beta['beta1'],0.144546,3)
        self.assertAlmostEqual(beta['beta2'],0.023502,3)

    def testBioNewtonLineSearch(self):
        results = self.myBiogeme.estimate(algorithm=opt.newtonLineSearchForBiogeme)
        beta = results.getBetaValues()
        self.assertAlmostEqual(beta['beta1'],0.144546,3)
        self.assertAlmostEqual(beta['beta2'],0.023502,3)

    def testBioCfsqp(self):
        results = self.myBiogeme.estimate(algorithm=None)
        beta = results.getBetaValues()
        self.assertAlmostEqual(beta['beta1'],0.144546,3)
        self.assertAlmostEqual(beta['beta2'],0.023502,3)

    def testBioNewtonTrustRegion(self):
        results = self.myBiogeme.estimate(algorithm=opt.newtonTrustRegionForBiogeme)
        beta = results.getBetaValues()
        self.assertAlmostEqual(beta['beta1'],0.144546,3)
        self.assertAlmostEqual(beta['beta2'],0.023502,3)
        
if __name__ == '__main__':
    unittest.main()
