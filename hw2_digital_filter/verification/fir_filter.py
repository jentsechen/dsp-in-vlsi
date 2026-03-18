import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots

class FirFilter:
    def __init__(self, coef):
        assert len(coef) % 2 == 1
        self.coef = coef
        # self.ramp_len = int((len(self.coef)-1) / 2)

    def apply(self, input):
        input_pad = np.concatenate([np.zeros(len(self.coef)-1), input, np.zeros(len(self.coef)-1)])
        output = []
        for i in range(len(input)+len(self.coef)-1):
            output.append(np.sum(input_pad[i:(i+len(self.coef))]*self.coef))
        return np.array(output)

    def apply_ref_model(self, input):
        return np.convolve(a=input, v=self.coef)