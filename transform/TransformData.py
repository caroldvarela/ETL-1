import pandas as pd
import numpy as np

class DataTransform:
    def __init__(self, file):

        self.df = pd.read_csv(file, sep=";")
