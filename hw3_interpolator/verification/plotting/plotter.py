import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots


class Plotter:
    FONT_SIZE = 15
    PNG_WIDTH = 1000
    PNG_HEIGHT = 400
    PNG_HEIGHT_2ROW = 600

    def _save_plot(self, traces, path, png_path=None, include_mathjax=None, **layout_kwargs):
        fig = make_subplots(rows=1, cols=1)
        for trace in traces:
            fig.add_trace(trace, row=1, col=1)
        fig.update_layout(font=dict(size=self.FONT_SIZE), margin=dict(l=40, r=40, t=40, b=40), **layout_kwargs)
        fig.write_html(path, **({"include_mathjax": include_mathjax} if include_mathjax else {}))
        if png_path:
            fig.write_image(png_path, width=self.PNG_WIDTH, height=self.PNG_HEIGHT)

    def _save_plot_2row(self, traces_row1, traces_row2, path, png_path=None, include_mathjax=None, **layout_kwargs):
        fig = make_subplots(rows=2, cols=1)
        for trace in traces_row1:
            fig.add_trace(trace, row=1, col=1)
        for trace in traces_row2:
            fig.add_trace(trace, row=2, col=1)
        fig.update_layout(font=dict(size=self.FONT_SIZE), margin=dict(l=40, r=40, t=40, b=40), **layout_kwargs)
        fig.write_html(path, **({"include_mathjax": include_mathjax} if include_mathjax else {}))
        if png_path:
            fig.write_image(png_path, width=self.PNG_WIDTH, height=self.PNG_HEIGHT_2ROW)

    def plot_signal(self, data, path, png_path=None, x=None, xaxis_title="m", yaxis_title="amplitude", color="blue", name=None):
        self._save_plot(
            traces=[go.Scatter(x=x, y=np.asarray(data), mode="lines", line=dict(color=color), name=name)],
            path=path,
            png_path=png_path,
            xaxis=dict(title=xaxis_title),
            yaxis=dict(title=yaxis_title),
        )

    def plot_complex_signal(self, data, path, png_path=None, x=None, xaxis_title="m"):
        data = np.asarray(data)
        self._save_plot_2row(
            traces_row1=[go.Scatter(x=x, y=data.real, mode="lines", line=dict(color="blue"), name="real")],
            traces_row2=[go.Scatter(x=x, y=data.imag, mode="lines", line=dict(color="orange"), name="imag")],
            path=path,
            png_path=png_path,
            xaxis=dict(title=xaxis_title),
            yaxis=dict(title="real part"),
            xaxis2=dict(title=xaxis_title),
            yaxis2=dict(title="imag part"),
        )

    def plot_two_signals(self, data_a, name_a, data_b, name_b, path, png_path=None, x=None, xaxis_title="m", yaxis_title="amplitude"):
        self._save_plot(
            traces=[
                go.Scatter(x=x, y=np.asarray(data_a), mode="lines", name=name_a),
                go.Scatter(x=x, y=np.asarray(data_b), mode="lines", name=name_b),
            ],
            path=path,
            png_path=png_path,
            xaxis=dict(title=xaxis_title),
            yaxis=dict(title=yaxis_title),
        )

    def plot_two_complex_signals(self, data_a, name_a, data_b, name_b, path, png_path=None, x=None, xaxis_title="m"):
        data_a = np.asarray(data_a)
        data_b = np.asarray(data_b)
        self._save_plot_2row(
            traces_row1=[
                go.Scatter(x=x, y=data_a.real, mode="lines", name=f"{name_a} real"),
                go.Scatter(x=x, y=data_b.real, mode="lines", name=f"{name_b} real"),
            ],
            traces_row2=[
                go.Scatter(x=x, y=data_a.imag, mode="lines", name=f"{name_a} imag"),
                go.Scatter(x=x, y=data_b.imag, mode="lines", name=f"{name_b} imag"),
            ],
            path=path,
            png_path=png_path,
            xaxis=dict(title=xaxis_title),
            yaxis=dict(title="real part"),
            xaxis2=dict(title=xaxis_title),
            yaxis2=dict(title="imag part"),
        )

    def plot_error(self, error, path, png_path=None, x=None, xaxis_title="m", yaxis_title="absolute error", color="red", name="error"):
        self._save_plot(
            traces=[go.Scatter(x=x, y=np.asarray(error), mode="lines", line=dict(color=color), name=name)],
            path=path,
            png_path=png_path,
            xaxis=dict(title=xaxis_title),
            yaxis=dict(title=yaxis_title),
        )

    def plot_interpolation_result(
        self, golden, results, path, png_path=None, x=None,
        golden_err=None, results_err=None, x_err=None,
        xaxis_title=r"$m+\mu$",
    ):
        golden = np.asarray(golden)
        use_separate_err = golden_err is not None and results_err is not None
        fig = make_subplots(rows=3, cols=1)
        for result, name in results:
            result = np.asarray(result)
            fig.add_trace(go.Scatter(x=x, y=result.real, mode="lines", name=f"{name}, real part"), row=1, col=1)
            fig.add_trace(go.Scatter(x=x, y=result.imag, mode="lines", name=f"{name}, imag. part"), row=2, col=1)
        if use_separate_err:
            golden_err = np.asarray(golden_err)
            for result_err, name in results_err:
                error = np.abs(golden_err - np.asarray(result_err))
                fig.add_trace(go.Scatter(x=x_err, y=error, mode="lines", name=f"{name}, abs. error"), row=3, col=1)
        else:
            for result, name in results:
                error = np.abs(golden - np.asarray(result))
                fig.add_trace(go.Scatter(x=x, y=error, mode="lines", name=f"{name}, abs. error"), row=3, col=1)
        fig.update_layout(
            font=dict(size=self.FONT_SIZE),
            margin=dict(l=40, r=40, t=40, b=40),
            xaxis1=dict(title=xaxis_title),
            yaxis=dict(title="real part"),
            xaxis2=dict(title=xaxis_title),
            yaxis2=dict(title="imag. part"),
            xaxis3=dict(title=xaxis_title),
            yaxis3=dict(title="abs. error"),
        )
        fig.write_html(path)
        if png_path:
            fig.write_image(png_path, width=1800, height=600)