from jinja2 import Environment, FileSystemLoader
from flask import Flask
import pandas as pd
import numpy as np
from modules.preprocess import *


dataset = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                   columns=['a', 'b', 'c'])
f= open("generated/showpersons.py", "w+")
f.write("import server\ndef preprocess(params):")
f.close()
params={"dataset":dataset}
f= open("generated/showpersons.py", "a")
f.write("\n\t return server.strToBool({0})".format("'true'"))
f.close()
from generated import showpersons
x=showpersons.preprocess(params)
print(x,type(x))

for x in dataset.columns:
    print(dataset[x])
from importlib import reload
import generated.preProcessActions
generated.preProcessActions=reload(generated.preProcessActions)