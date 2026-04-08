## To Do
- Solve data/valid misalignment between post synthesis result and golden

## Verification
```bash
├── main.py
│   ├── task_q1()
│   ├── task_q2()
│   ├── task_q3()
│   ├── task_q4()
│   ├── task_q5()
│   ├── task_q6()
│   └── task_q8()
│
├── models/
│   ├── filter_coef.py
│   │   └── FilterCoef
│   │       ├── __init__()
│   │       └── _gen()
│   │
│   ├── qntz_model.py
│   │   └── QntzModel
│   │       ├── __init__()
│   │       ├── _scaled_floor()
│   │       ├── quantizer()
│   │       └── quantizer_arr()
│   │
│   ├── fir_filter.py
│   │   ├── Mode(Enum)
│   │   │   └── INPUT, COEF, MULT, ADD
│   │   ├── MaxValSet
│   │   │   ├── __init__()
│   │   │   ├── apply()
│   │   │   ├── _iq_abs_max_ceil()
│   │   │   ├── _find_int_bit()
│   │   │   └── get_int_bit_set()
│   │   └── FirFilter(QntzModel)
│   │       ├── __init__()
│   │       ├── apply()
│   │       └── apply_ref_model()
│   │
│   └── qntz_format.py
│       ├── QntzFormat(@dataclass)
│       │   └── total_bit_width()
│       └── QntzFormatSet(@dataclass)
│           └── fields: input, coef, mult, add
│
├── analysis/
│   ├── simulator.py
│   │   └── Simulator
│   │       ├── __init__()
│   │       ├── run()
│   │       ├── run_reference()
│   │       ├── calc_rmse()
│   │       └── _gen_input()
│   │
│   └── verification.py
│       ├── VeriConfig(@dataclass)
│       │   └── fields: file_name, sim_name, out_dir, latency, multi_col
│       └── FuncVerification
│           ├── __init__()
│           ├── run()
│           └── _read_result()
│
└── plotting/
    └── plotter.py
        └── Plotter
            ├── _save_plot()
            ├── plot_signal()
            ├── plot_two_signals()
            ├── plot_rmse_vs_frac_bit()
            ├── plot_freq_response()
            ├── plot_filter_freq_resp()
            ├── plot_verification()
            └── _calc_mag_resp()
```