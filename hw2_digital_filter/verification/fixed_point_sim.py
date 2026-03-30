import numpy as np
import plotly.graph_objs as go
import plotly.offline as pof
from plotly.subplots import make_subplots
from scipy import signal
from filter_coef import FilterCoef
from fir_filter import FirFilter, QntzFormat, QntzFormatSet, Mode


class FixedPointSim:
    def __init__(self):
        self.filter_coef = FilterCoef().v
        self.input = self.gen_input()
        self.plot_input()
        self.filter = FirFilter(self.filter_coef)
        self.ref_output = self.filter.apply_ref_model(input=self.input)
        self.output = self.filter.apply(
            input=self.input, qntz_format_set=QntzFormatSet(), det_int_bit_en=True
        )
        self.plot_output()
        self.filter.max_val_sel.get_int_bit_set()

    def gen_input(self):
        n = np.arange(0, 144)
        return np.cos(-2 * np.pi / 128 * n) - np.cos(2 * np.pi * n / 4)

    def plot_input(self):
        figure = make_subplots(rows=1, cols=1)
        figure.add_trace(
            go.Scatter(y=self.input, marker=dict(color="blue")), row=1, col=1
        )
        figure.update_layout(xaxis=dict(title="index"), font=dict(size=20))
        figure.write_html("./figure/input.html")

    def plot_output(self):
        figure = make_subplots(rows=1, cols=1)
        figure.add_trace(
            go.Scatter(y=self.input * sum(self.filter.coef), marker=dict(color="blue")),
            row=1,
            col=1,
        )
        figure.add_trace(
            go.Scatter(y=self.ref_output, marker=dict(color="red")), row=1, col=1
        )
        figure.add_trace(
            go.Scatter(
                y=self.output, mode="lines", line=dict(color="orange", dash="dash")
            ),
            row=1,
            col=1,
        )
        figure.update_layout(xaxis=dict(title="index"), font=dict(size=20))
        figure.write_html("./figure/output.html")

    def plot_qntz_anal(self, mode: Mode, qntz_format_set: QntzFormatSet):
        output_ft = self.filter.apply(input=self.input, qntz_format_set=QntzFormatSet())
        qntz_format_set_iter = qntz_format_set
        frac_bit_list = np.arange(9, 21)
        error = []
        for f in frac_bit_list:
            if mode == Mode.INPUT:
                qntz_format_set_iter.input.frac_bit = f
            elif mode == Mode.COEF:
                qntz_format_set_iter.coef.frac_bit = f
            elif mode == Mode.MULT:
                qntz_format_set_iter.mult.frac_bit = f
            else:  # mode == Mode.ADD
                qntz_format_set_iter.add.frac_bit = f
            output_fx = self.filter.apply(
                input=self.input, qntz_format_set=qntz_format_set_iter
            )
            error.append(self.calc_rmse(output_fx, output_ft))
        figure = make_subplots(rows=1, cols=1)
        figure.add_trace(
            go.Scatter(
                x=frac_bit_list,
                y=error,
                mode="lines",
                line=dict(color="blue", dash="solid"),
            ),
            row=1,
            col=1,
        )
        figure.add_hline(
            y=2**-11,
            annotation_text="2⁻¹¹",
            annotation_font_color="red",
            line_dash="dash",
            line_color="red",
            row=1,
            col=1,
        )
        figure.update_layout(
            xaxis=dict(title="word length"),
            # yaxis=dict(title="RMSE (log scale)", type="log"),
            yaxis=dict(title="RMSE"),
            font=dict(size=20),
        )
        figure.write_html(f"./figure/qntz_result_{str(mode.name).lower()}.html")

    def plot_qntz_result(self, qntz_format_set: QntzFormatSet):
        output_ft = self.filter.apply(input=self.input, qntz_format_set=QntzFormatSet())
        output_fx = self.filter.apply(input=self.input, qntz_format_set=qntz_format_set)
        figure = make_subplots(rows=2, cols=1)
        figure.add_trace(
            go.Scatter(y=output_ft, name="floating point"),
            row=1,
            col=1,
        )
        figure.add_trace(
            go.Scatter(y=output_fx, name="fixed-point"),
            row=1,
            col=1,
        )
        figure.add_trace(
            go.Scatter(y=output_fx - output_ft, name="error"),
            row=2,
            col=1,
        )
        figure.update_layout(font=dict(size=20))
        figure.write_html("./figure/qntz_result.html")

    def calc_rmse(self, a, b):
        assert len(a) == len(b)
        return np.sqrt(np.sum((a - b) ** 2) / len(b))
