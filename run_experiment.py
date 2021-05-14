#!/usr/bin/env python
# coding: utf-8

# # cadCAD Experiment
# Over 500 timesteps, money comes in to the system each timestep and is distributed to delegators according to the proportion of shares they have bought.  The share price and number are tied to a bonding curve.  
# 
# They purchase shares in the system according to their belief of the future revenue streams.

# In[1]:


# if this crashes, run this:
# pip install ipython-autotime

# from IPython.conftest import get_ipython
# get_ipython().run_line_magic('load_ext', 'autotime')
# get_ipython().run_line_magic('load_ext', 'autoreload')
# get_ipython().run_line_magic('autoreload', '2')
import sys
from tabulate import tabulate
import pandas as pd
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor

sys.path.append("..")


# In[2]:



from model.run import run

# df = run()


# In[3]:


# from cadCAD_tools import profile_run

from model.psub import psubs
from model.state import genesis_state
from model.config import simulation_config, exp
from model.config import params

TIMESTEPS = len(simulation_config[0]['T'])
SAMPLES = simulation_config[0]['N'] 
# df = run()

exec_mode = ExecutionMode()

local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=local_proc_ctx, configs=exp.configs)

raw_result, _, _ = run.execute()
df = pd.DataFrame(raw_result)

print(tabulate(df, headers='keys', tablefmt='psql'))
exit()

# df = profile_run(genesis_state,
#                  params,
#                  psubs,
#                  TIMESTEPS,
#                  SAMPLES)


# In[4]:


# from cadCAD_tools.profiling.visualizations import visualize_substep_impact

# visualize_substep_impact(df, relative=True)


# In[5]:


max_substep = max(df.substep)
print(max_substep)
df = df[df.substep==max_substep].reset_index()
print(df.substep.unique())


# In[6]:


import pickle
pickle.dump(df, open('experiment.p', 'wb'))


# In[38]:


# df.substep[0:20]
# data frame with:
# simulation, subset, timestep, substep
df1 = df[["simulation", "subset", "run", "timestep", "substep"]]


# In[39]:


df1.timestep.unique()


# In[ ]:





# In[50]:


df1.substep.unique()


# In[48]:


# df where timestep == 1
# simulation_config = configuration.utils.config_sim({
#     'T': range(2000),
#     'N': 1,
#     'M': params
# })

df1[((df1.timestep == 1) & (df1.run == 1) & (df1.subset == 0))]

