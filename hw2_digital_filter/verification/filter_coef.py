import numpy as np
import plotly.graph_objs as go
import plotly.offline as pof
from plotly.subplots import make_subplots
from scipy import signal

class FilterCoef:
    def __init__(self, n_taps=25, boundary=2, norm_en=False):
        self.v = self.gen_filter_coef(n_taps=n_taps, boundary=boundary, norm_en=norm_en)
        self.plot_filter_coef()
        self.plot_filter_freq_resp()

    def gen_filter_coef(self, n_taps, boundary, norm_en):
        t = np.linspace(-boundary, boundary, n_taps)
        sinc_out = np.sinc(t)
        if norm_en:
            return sinc_out / sum(sinc_out)
        return sinc_out
        
    def plot_filter_coef(self):
        figure = make_subplots(rows=1, cols=1)
        figure.add_trace(go.Scatter(y=self.v,
                                    marker=dict(color='blue')), row=1, col=1)
        figure.update_layout(
            xaxis=dict(title="index"),
            font=dict(size=20)
        )
        figure.write_html("./figure/filter_coef.html")

    def plot_filter_freq_resp(self):
        w, H = signal.freqz(self.v, worN=8000)
        mag_resp_db = 20*np.log10(np.abs(H))
        max_yaxis_range = np.max(mag_resp_db)+0.5
        phase_resp = np.unwrap(np.angle(H))
        figure = make_subplots(rows=2, cols=1)
        figure.add_trace(go.Scatter(x=w/np.pi, y=mag_resp_db,
                                    marker=dict(color='blue')), row=1, col=1)
        figure.add_hline(
            y=np.max(mag_resp_db) - 3, 
            line_dash="dash", 
            line_color="red", 
            annotation_text="-3dB",
            row=1, col=1
        )
        figure.add_trace(go.Scatter(x=w/np.pi, y=phase_resp,
                                    marker=dict(color='blue')), row=2, col=1)
        figure.update_layout(
            xaxis=dict(title=r"$\text{frequency (}\pi\text{ rad)}$"),
            yaxis=dict(title="magnitude"),
            yaxis_range=[max_yaxis_range-60, max_yaxis_range],
            xaxis2=dict(title=r"$\text{frequency (}\pi\text{ rad)}$"),
            yaxis2=dict(title="phase (rad)"),
            font=dict(size=20)
        )
        figure.write_html("./figure/filter_freq_resp.html", include_mathjax='cdn')
