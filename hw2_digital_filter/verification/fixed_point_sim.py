import numpy as np
import plotly.graph_objs as go
import plotly.offline as pof
from plotly.subplots import make_subplots
from scipy import signal
from filter_coef import FilterCoef
from fir_filter import FirFilter

class FixedPointSim:
    def __init__(self):
        self.filter_coef = FilterCoef().v
        self.input = self.gen_input()
        self.plot_input()
        filter = FirFilter(self.filter_coef)
        self.ref_output = filter.apply_ref_model(self.input)
        self.output = filter.apply(self.input)
        self.plot_output()
        
    def gen_input(self):
        n = np.arange(0, 144)
        return np.cos(-2*np.pi/128*n) - np.cos(2*np.pi*n/4)

    def plot_input(self):
        figure = make_subplots(rows=1, cols=1)
        figure.add_trace(go.Scatter(y=self.input,
                                    marker=dict(color='blue')), row=1, col=1)
        figure.update_layout(
            xaxis=dict(title="index"),
            font=dict(size=20)
        )
        figure.write_html("./figure/input.html")

    # def apply_filter(self):
    #     filter = FirFilter(self.filter_coef)
    #     return filter.apply_ref_model(self.input)
    
    def plot_output(self):
        figure = make_subplots(rows=1, cols=1)
        # figure.add_trace(go.Scatter(y=self.input,
        #                             marker=dict(color='blue')), row=1, col=1)
        # figure.add_trace(go.Scatter(y=self.ref_output[12:-12],
        #                             marker=dict(color='red')), row=1, col=1)
        figure.add_trace(go.Scatter(y=self.ref_output,
                                    marker=dict(color='red')), row=1, col=1)
        figure.add_trace(go.Scatter(y=self.output,
                                    mode='lines',
                                    line=dict(
                                    color='orange',
                                    dash='dash'
                                )), row=1, col=1)
        figure.update_layout(
            xaxis=dict(title="index"),
            font=dict(size=20)
        )
        figure.write_html("./figure/output.html")
