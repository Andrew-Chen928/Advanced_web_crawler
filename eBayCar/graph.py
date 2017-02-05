# import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')

x,y = np.loadtxt('text2.csv',
                 unpack=True,
                 delimiter = ',')

# plt.plot(x,y)
width = 1.5
plt.bar(y, x, width=width, align='center', linewidth=1, edgecolor="green")
plt.title('Wiper sale info demmo', fontsize=14, fontweight='bold')
plt.ylabel('Sold Amount', fontsize=12, fontweight='bold')
plt.xlabel('Price', fontsize=12, fontweight='bold')
plt.savefig('wiper_demo.png')
# plt.show()
