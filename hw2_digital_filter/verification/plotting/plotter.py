import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from scipy import signal


class Plotter:
    FONT_SIZE  = 15
    PNG_WIDTH  = 1000
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

    def plot_signal(self, data, path, png_path=None, xaxis_title="n", color="blue"):
        self._save_plot(
            traces=[go.Scatter(y=data, mode="lines", line=dict(color=color))],
            path=path,
            png_path=png_path,
            xaxis=dict(title=xaxis_title),
        )

    def plot_two_signals(self, data_a, name_a, data_b, name_b, path, xaxis_title="n"):
        self._save_plot(
            traces=[
                go.Scatter(y=data_a, name=name_a),
                go.Scatter(y=data_b, name=name_b),
            ],
            path=path,
            xaxis=dict(title=xaxis_title),
        )

    def plot_rmse_vs_frac_bit(self, frac_bit_list, error, path, png_path=None):
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(
            go.Scatter(x=frac_bit_list, y=error, mode="lines", line=dict(color="blue")),
            row=1, col=1,
        )
        fig.add_hline(
            y=2**-11,
            annotation_text="2⁻¹¹",
            annotation_font_color="red",
            line_dash="dash",
            line_color="red",
        )
        fig.update_layout(
            xaxis=dict(title="word length (bit)"),
            yaxis=dict(title="RMSE"),
            margin=dict(l=40, r=40, t=40, b=40),
            font=dict(size=self.FONT_SIZE),
        )
        fig.write_html(path)
        if png_path:
            fig.write_image(png_path, width=self.PNG_WIDTH, height=self.PNG_HEIGHT)

    def plot_freq_response(self, coef_ft, coef_fx, path, error_path, png_path=None, error_png_path=None):
        norm_w, mag_db_ft, max_range = self._calc_mag_resp(coef_ft)
        _, mag_db_fx, _ = self._calc_mag_resp(coef_fx)

        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(go.Scatter(x=norm_w, y=mag_db_ft, name="floating point", marker=dict(color="blue")), row=1, col=1)
        fig.add_trace(go.Scatter(x=norm_w, y=mag_db_fx, name="fixed-point", marker=dict(color="green")), row=1, col=1)
        fig.add_hline(y=np.max(mag_db_ft) - 3, line_dash="dash", line_color="red", annotation_text="-3dB")
        fig.update_layout(
            xaxis=dict(title=r"$\text{frequency (}\pi\text{ rad)}$"),
            yaxis=dict(title="magnitude (dB)"),
            yaxis_range=[max_range - 60, max_range],
            margin=dict(l=40, r=40, t=40, b=40),
            font=dict(size=self.FONT_SIZE),
        )
        fig.write_html(path, include_mathjax="cdn")
        if png_path:
            fig.write_image(png_path, width=self.PNG_WIDTH, height=self.PNG_HEIGHT)

        mag_db_error = mag_db_fx - mag_db_ft
        n_passband = int(8000 * 0.14)
        self._save_plot(
            traces=[go.Scatter(x=norm_w, y=mag_db_error, name="error", marker=dict(color="orange"))],
            path=error_path,
            png_path=error_png_path,
            include_mathjax="cdn",
            xaxis=dict(title=r"$\text{frequency (}\pi\text{ rad)}$"),
            yaxis=dict(title="magnitude (dB)"),
            xaxis_range=[0, 0.14],
            yaxis_range=[
                np.min(mag_db_error[:n_passband]) - 1e-6,
                np.max(mag_db_error[:n_passband]) + 1e-6,
            ],
        )

    def plot_filter_freq_resp(self, coef, path, png_path=None):
        w, H = signal.freqz(coef, worN=8000)
        mag_resp_db = 20 * np.log10(np.abs(H))
        phase_resp = np.unwrap(np.angle(H))
        max_yaxis_range = np.max(mag_resp_db) + 0.5
        norm_w = w / np.pi

        fig = make_subplots(rows=2, cols=1)
        fig.add_trace(go.Scatter(x=norm_w, y=mag_resp_db, marker=dict(color="blue"), showlegend=False), row=1, col=1)
        fig.add_hline(y=np.max(mag_resp_db) - 3, line_dash="dash", line_color="red", annotation_text="-3dB", row=1, col=1)
        fig.add_trace(go.Scatter(x=norm_w, y=phase_resp, marker=dict(color="blue"), showlegend=False), row=2, col=1)
        fig.update_layout(
            xaxis=dict(title=r"$\text{frequency (}\pi\text{ rad)}$"),
            yaxis=dict(title="magnitude (dB)"),
            yaxis_range=[max_yaxis_range - 60, max_yaxis_range],
            xaxis2=dict(title=r"$\text{frequency (}\pi\text{ rad)}$"),
            yaxis2=dict(title="phase (rad)"),
            margin=dict(l=40, r=40, t=40, b=40),
            font=dict(size=self.FONT_SIZE),
        )
        fig.write_html(path, include_mathjax="cdn")
        if png_path:
            fig.write_image(png_path, width=self.PNG_WIDTH, height=self.PNG_HEIGHT_2ROW)

    def plot_verification(self, golden, result, sim_name, path, error, error_path, png_path=None, error_png_path=None):
        self._save_plot(
            traces=[
                go.Scatter(y=golden, name="floating point"),
                go.Scatter(y=result, name=sim_name),
            ],
            path=path,
            png_path=png_path,
            xaxis=dict(title="n"),
        )
        self._save_plot(
            traces=[go.Scatter(y=error, name="error")],
            path=error_path,
            png_path=error_png_path,
            xaxis=dict(title="n"),
        )

    def _calc_mag_resp(self, coef):
        w, H = signal.freqz(coef, worN=8000)
        mag_resp_db = 20 * np.log10(np.abs(H))
        return w / np.pi, mag_resp_db, np.max(mag_resp_db) + 0.5