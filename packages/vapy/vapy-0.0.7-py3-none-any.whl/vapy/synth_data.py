
import random
import numpy as np
import matplotlib.pyplot as plt

types = ['a', 'b', 'c']
colors = {'a': '#1b9e77','b': '#d95f02','c': '#7570b3'}

x = np.linspace(0, 1, 15)
y = np.linspace(0, 1, 15)

d = []
for xv in x:
    for yv in y:
        d.append(tuple((xv,yv, random.choice(types))))


print(d)
xx, yy = np.meshgrid(x,y)

cc = np.random.choice(list(colors.values()), 15*15)


plt.scatter(xx,yy, c=cc)
plt.show()