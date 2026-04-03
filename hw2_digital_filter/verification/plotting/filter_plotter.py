import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from scipy import signal
from plotting.plotter import Plotter


class FilterPlotter(Plotter):
    def plot_filter_coef(self, coef, path, png_path=None):
        self._save_plot(
            traces=[go.Scatter(y=coef, marker=dict(color="blue"))],
            path=path,
            png_path=png_path,
            xaxis=dict(title="n"),
        )

    def plot_filter_freq_resp(self, coef, path, png_path=None):
        w, H = signal.freqz(coef, worN=8000)
        mag_resp_db = 20 * np.log10(np.abs(H))
        phase_resp = np.unwrap(np.angle(H))
        max_yaxis_range = np.max(mag_resp_db) + 0.5
        norm_w = w / np.pi

        fig = make_subplots(rows=2, cols=1)
        fig.add_trace(go.Scatter(x=norm_w, y=mag_resp_db, marker=dict(color="blue"), showlegend=False), row=1, col=1)
        fig.add_hline(
            y=np.max(mag_resp_db) - 3,
            line_dash="dash",
            line_color="red",
            annotation_text="-3dB",
            row=1, col=1,
        )
        fig.add_trace(go.Scatter(x=norm_w, y=phase_resp, marker=dict(color="blue"), showlegend=False), row=2, col=1)
        fig.update_layout(
            xaxis=dict(title=r"$\text{frequency (}\pi\text{ rad)}$"),
            yaxis=dict(title="magnitude (dB)"),
            yaxis_range=[max_yaxis_range - 60, max_yaxis_range],
            xaxis2=dict(title=r"$\text{frequency (}\pi\text{ rad)}$"),
            yaxis2=dict(title="phase (rad)"),
            font=dict(size=self.FONT_SIZE),
        )
        fig.write_html(path, include_mathjax="cdn")
        if png_path:
            fig.write_image(png_path)