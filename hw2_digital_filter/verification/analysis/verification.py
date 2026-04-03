from dataclasses import dataclass
from pathlib import Path
import numpy as np
from analysis.simulator import Simulator
from plotting.plotter import Plotter

FRAC_SCALE = 2 ** 18


@dataclass
class VeriConfig:
    file_name: str
    sim_name:  str
    out_dir:   str
    latency:   int  = 0
    multi_col: bool = False


class FuncVerification:
    def __init__(self, data_dir: Path, diagram_dir: Path):
        self.data_dir    = data_dir
        self.diagram_dir = diagram_dir
        self.sim         = Simulator()
        self.plotter     = Plotter()

    def run(self, config: VeriConfig):
        out = self.diagram_dir / config.out_dir
        out.mkdir(parents=True, exist_ok=True)

        result = self._read_result(config.file_name, config.latency, config.multi_col)
        error  = np.concatenate([
            [None] * config.latency,
            self.sim.output[config.latency:] - result[config.latency:],
        ])

        self.plotter.plot_verification(
            golden=self.sim.output, result=result, sim_name=config.sim_name,
            path=out / f"{config.file_name}.html",
            error=error,
            error_path=out / f"{config.file_name}_error.html",
            png_path=out / f"{config.file_name}.png",
            error_png_path=out / f"{config.file_name}_error.png",
        )

    def _read_result(self, file_name, latency, multi_col):
        values = []
        with open(self.data_dir / f"{file_name}.txt") as f:
            for line in f:
                line = line.strip()
                if line:
                    if multi_col:
                        values += [int(v) / FRAC_SCALE for v in line.split()]
                    else:
                        values.append(int(line) / FRAC_SCALE)
        result = np.array(values, dtype=object)
        if latency > 0:
            result = np.concatenate([[None] * latency, result])
        return result