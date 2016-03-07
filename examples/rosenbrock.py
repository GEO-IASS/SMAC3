from __future__ import division, print_function


#TODO: remove really ugly boilerplate
import logging
import sys
import os
import inspect
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
cmd_folder = os.path.realpath(os.path.join(cmd_folder, ".."))
if cmd_folder not in sys.path:
    sys.path.append(cmd_folder)
    
import numpy as np

from smac.configspace import ConfigurationSpace
from ConfigSpace.hyperparameters import CategoricalHyperparameter, \
    UniformFloatHyperparameter, UniformIntegerHyperparameter
    
from smac.tae.execute_func import ExecuteTAFunc
from smac.scenario.scenario import Scenario
from smac.smbo.smbo import SMBO
from smac.stats.stats import Stats

def rosenbrock_4d(cfg):
    """ The 4 dimensional Rosenbrock function as a toy model
    The Rosenbrock function is well know in the optimization community and
    often serves as a toy problem. It can be defined for arbitrary
    dimensions. The minimium is always at x_i = 1 with a function value of
    zero. All input parameters are continuous, but we will pretent that 
    x2, x3, and x4 can only take integral values. The search domain for
    all x's is the interval [-5, 5].
    """
    x1 = cfg["x1"]
    x2 = cfg["x2"]
    x3 = cfg["x3"]
    x4 = cfg["x4"]

    val = (100 * (x2 - x1 ** 2) ** 2 + (x1 - 1) ** 2 +
           100 * (x3 - x2 ** 2) ** 2 + (x2 - 1) ** 2 +
           100 * (x4 - x3 ** 2) ** 2 + (x3 - 1) ** 2)
    
    return(val)

# register function to be optimize
tae = ExecuteTAFunc(rosenbrock_4d)

# build Configuration Space which defines all parameters and their ranges
cs = ConfigurationSpace()
x1 = UniformFloatHyperparameter("x1", -5, 5, default=5)
cs.add_hyperparameter(x1)
x2 = UniformIntegerHyperparameter("x2", -5, 5, default=5)
cs.add_hyperparameter(x2)
x3 = CategoricalHyperparameter(
    "x3", [5, 2, 0, 1, -1, -2, 4, -3, 3, -5, -4], default=5)
cs.add_hyperparameter(x3)
x4 = UniformIntegerHyperparameter("x4", -5, 5, default=5)
cs.add_hyperparameter(x4)

# example call of the function
# it returns: Status, Cost, Runtime, Additional Infos
def_value = tae.run( cs.get_default_configuration() )[1]
print("Default Value: %.2f" %(def_value))

scenario = Scenario({"run_obj":"quality",
                     "runcount-limit": 200,
                     "instances": [[1]], # Dummy
                     "cs": cs
                     },
                    tae_runner = tae)

#logger = logging.getLogger("Optimizer") # Enable to show Debug outputs

# necessary to use stats options related to scenario information        
Stats.scenario = scenario

# Optimize
smbo = SMBO(scenario=scenario, rng=np.random.RandomState(42))
smbo.run(max_iters=999)

Stats.print_stats()
print("Final Incumbent: %s" %(smbo.incumbent))


