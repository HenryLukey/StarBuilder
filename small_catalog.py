import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import pandas as pd

from skyfield.api import Star, load
from skyfield.constants import GM_SUN_Pitjeva_2005_km3_s2 as GM_SUN
from skyfield.data import hipparcos, mpc, stellarium
from skyfield.projections import build_stereographic_projection

with load.open(hipparcos.URL) as f:
    stars = hipparcos.load_dataframe(f)

limiting_magnitude = 6.0

stars = stars.sort_values(by=["magnitude"])
stars = stars.head(9110)

#stars.to_csv("hip_small.dat")
print(stars)
print()
print(len(stars))