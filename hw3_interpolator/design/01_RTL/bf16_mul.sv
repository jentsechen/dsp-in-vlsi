module bf16_mul (
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

    logic either_zero;
    assign either_zero = (e_a == 8'd0) || (e_b == 8'd0);

    logic s_out;
    assign s_out = s_a ^ s_b;

    logic [15:0] prod;
    assign prod = {1'b1, m_a} * {1'b1, m_b};

    logic msb15;
    assign msb15 = prod[15];

    logic [7:0] prod_norm;
    assign prod_norm = msb15 ? prod[15:8] : prod[14:7];

    logic signed [9:0] e_out;
    assign e_out = signed'({2'b00, e_a}) + signed'({2'b00, e_b})
                 - (msb15 ? 10'sd126 : 10'sd127);

    logic e_underflow, e_overflow;
    assign e_underflow = (e_out <= 10'sd0);
    assign e_overflow  = (e_out >= 10'sd255);

    logic [7:0] e_final;
    logic [6:0] m_out;
    assign e_final = e_overflow ? 8'd254 : e_out[7:0];
    assign m_out   = prod_norm[6:0];

    assign out = (either_zero || e_underflow) ? '0 : {s_out, e_final, m_out};

endmodule