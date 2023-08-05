# coding: utf-8

desc={"ref": {"C0": 'Smirnov, G. S. & Stegailov, V. V. Toward Determination of the New Hydrogen Hydrate Clathrate Structures. J Phys Chem Lett 4, 3560-3564 (2013); Strobel, Timothy A et al. “Hydrogen-Stuffed, Quartz-Like Water Ice.” Journal of the American Chemical Society 138.42 (2016): 13786–13789.',
              "Ice 17": 'del Rosso, Leonardo, Milva Celli, and Lorenzo Ulivi. “Ice XVII as a Novel Material for Hydrogen Storage.” Challenges 8.1 (2017): 3.'},
      "usage": "No options available.",
      "brief": "Ice XVII."
      }

density = 0.88     #default density

bondlen = 1.2

coord="relative"

cell="""
2.66453550129  4.69111124482  2.55091895393
"""

waters="""
0.677211836339 -0.109412115924 0.692291816468
-0.127211837083 0.159412115985 0.192291816964
0.0250000004322 0.00787072277433 0.525000000221
0.372788162852 -0.109412116231 0.357708184099
0.524999999997 0.0421292775959 0.0249999994379
0.177211837459 0.159412115799 -0.142291817189
0.177211836341 0.390587884076 0.692291816467
0.372788162918 0.659412115985 0.192291816965
0.525000000434 0.507870722774 0.525000000221
-0.127211837147 0.390587883769 0.357708184099
0.0249999999983 0.542129277596 0.0249999994377
0.67721183746 0.659412115799 -0.142291817189
"""

from genice.cell import cellvectors
cell = cellvectors(a=2.66453550129,
                   b=4.69111124482,
                   c=2.55091895393)
