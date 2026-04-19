import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots


class Plotter:
    FONT_SIZE = 15
    PNG_WIDTH = 1000
    PNG_HEIGHT = 400

    def _save_plot(self, traces, path, png_path=None, **layout_kwargs):
        fig = make_subplots(rows=1, cols=1)
        for trace in traces:
            fig.add_trace(trace, row=1, col=1)
        fig.update_layout(font=dict(size=self.FONT_SIZE), margin=dict(l=40, r=40, t=40, b=40), **layout_kwargs)
        fig.write_html(path)
        if png_path:
            fig.write_image(png_path, width=self.PNG_WIDTH, height=self.PNG_HEIGHT)

    def plot_signal(self, data, path, png_path=None, x=None, xaxis_title="N", yaxis_title="S(N)", color="blue", hlines=None):
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(go.Scatter(x=x, y=np.asarray(data), mode="lines+markers", marker=dict(size=5), line=dict(color=color), showlegend=False), row=1, col=1)
        if hlines:
            for hl in hlines:
                fig.add_hline(
                    y=hl["y"],
                    annotation_text=hl.get("annotation_text", ""),
                    annotation_font_color=hl.get("color", "black"),
                    line_dash=hl.get("dash", "dash"),
                    line_color=hl.get("color", "black"),
                )
        fig.update_layout(
            font=dict(size=self.FONT_SIZE),
            margin=dict(l=40, r=40, t=40, b=40),
            showlegend=False,
            xaxis=dict(title=xaxis_title),
            yaxis=dict(title=yaxis_title),
        )
        fig.write_html(path)
        if png_path:
            fig.write_image(png_path, width=self.PNG_WIDTH, height=self.PNG_HEIGHT)