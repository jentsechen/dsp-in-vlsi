module bf16_add (
    input  logic [15:0] a,
    input  logic [15:0] b,
    output logic [15:0] out
);

    logic        s_a;
    logic [7:0]  e_a;
    logic [6:0]  m_a;
    logic        s_b;
    logic [7:0]  e_b;
    logic [6:0]  m_b;

    assign s_a = a[15];
    assign e_a = a[14:7];
    assign m_a = a[6:0];
    assign s_b = b[15];
    assign e_b = b[14:7];
    assign m_b = b[6:0];

    logic both_zero;
    assign both_zero = (e_a == 8'd0) && (e_b == 8'd0);

    logic [7:0] sig_a, sig_b;
    assign sig_a = {1'b1, m_a};
    assign sig_b = {1'b1, m_b};

    logic        a_ge_b;
    logic [7:0]  exp_diff, e_aligned;
    assign a_ge_b    = (e_a >= e_b);
    assign exp_diff  = a_ge_b ? (e_a - e_b) : (e_b - e_a);
    assign e_aligned = a_ge_b ? e_a : e_b;

    logic [7:0] sig_a_sh, sig_b_sh;
    assign sig_a_sh = a_ge_b ? sig_a : (sig_a >> exp_diff);
    assign sig_b_sh = a_ge_b ? (sig_b >> exp_diff) : sig_b;

    logic signed [8:0] val_a, val_b;
    assign val_a = s_a ? (-signed'({1'b0, sig_a_sh})) : signed'({1'b0, sig_a_sh});
    assign val_b = s_b ? (-signed'({1'b0, sig_b_sh})) : signed'({1'b0, sig_b_sh});

    logic signed [9:0] val_sum;
    assign val_sum = 10'(val_a) + 10'(val_b);

    logic        s_out, sum_zero;
    logic [9:0]  mag;
    assign s_out    = val_sum[9];
    assign mag      = s_out ? (~val_sum[9:0] + 10'd1) : val_sum[9:0];
    assign sum_zero = (val_sum == '0);

    logic [3:0] msb_pos;
    always_comb begin
        priority if      (mag[8]) msb_pos = 4'd8;
        else if (mag[7]) msb_pos = 4'd7;
        else if (mag[6]) msb_pos = 4'd6;
        else if (mag[5]) msb_pos = 4'd5;
        else if (mag[4]) msb_pos = 4'd4;
        else if (mag[3]) msb_pos = 4'd3;
        else if (mag[2]) msb_pos = 4'd2;
        else if (mag[1]) msb_pos = 4'd1;
        else             msb_pos = 4'd0;
    end

    logic [3:0] shift_r, shift_l;
    assign shift_r = (msb_pos > 4'd7) ? (msb_pos - 4'd7) : 4'd0;
    assign shift_l = (msb_pos < 4'd7) ? (4'd7 - msb_pos) : 4'd0;

    logic [9:0] mag_norm;
    assign mag_norm = (msb_pos > 4'd7) ? (mag >> shift_r) :
                      (msb_pos < 4'd7) ? (mag << shift_l) : mag;

    logic signed [9:0] e_adj;
    assign e_adj = signed'({2'b00, e_aligned})
                 + signed'({6'b000000, shift_r})
                 - signed'({6'b000000, shift_l});

    logic e_underflow, e_overflow;
    assign e_underflow = (e_adj <= 10'sd0);
    assign e_overflow  = (e_adj >= 10'sd255);

    logic [7:0] e_out;
    logic [6:0] m_out;
    assign e_out = e_overflow ? 8'd254 : e_adj[7:0];
    assign m_out = mag_norm[6:0];

    assign out = (both_zero || sum_zero || e_underflow) ? '0 : {s_out, e_out, m_out};

endmodule