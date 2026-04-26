module cordic #(
    parameter int N          = 10,
    parameter int XY_FRAC    = 12,
    parameter int THETA_FRAC = 10,
    parameter int PI_INT     = 3217,
    parameter int THETA_E [0:N-1] = '{804, 475, 251, 127, 64, 32, 16, 8, 4, 2}
) (
    input  logic                          clk,
    input  logic                          rst_n,
    input  logic                          in_valid,
    input  logic signed [XY_FRAC+1:0]    x_in,
    input  logic signed [XY_FRAC+1:0]    y_in,
    output logic                          out_valid,
    output logic signed [THETA_FRAC+2:0] phase_out
);

    localparam int THETA_W = THETA_FRAC + 2;
    localparam int OUT_W   = THETA_FRAC + 3;
    localparam int STEP_W  = $clog2(N + 1);

    function automatic logic signed [THETA_W-1:0] theta_lut(
        input logic [STEP_W-1:0] i
    );
        logic signed [THETA_W-1:0] val;
        val = THETA_E[i];
        return val;
    endfunction

    logic signed [XY_FRAC+1:0]  x_r, y_r;
    logic signed [THETA_W-1:0]  theta_r;
    logic signed [OUT_W-1:0]    theta_off_r;
    logic        [STEP_W-1:0]   step_r;
    logic                       busy_r;

    logic                       rotate_cw;
    logic signed [XY_FRAC+1:0]  x_sh, y_sh;
    logic signed [XY_FRAC+1:0]  x_nxt, y_nxt;
    logic signed [THETA_W-1:0]  theta_nxt;

    assign rotate_cw = ~y_r[XY_FRAC+1];
    assign y_sh      = y_r >>> step_r;
    assign x_sh      = x_r >>> step_r;
    assign x_nxt     = rotate_cw ? (x_r + y_sh) : (x_r - y_sh);
    assign y_nxt     = rotate_cw ? (y_r - x_sh) : (y_r + x_sh);
    assign theta_nxt = rotate_cw ? (theta_r + theta_lut(step_r))
                                 : (theta_r - theta_lut(step_r));

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            x_r         <= '0;
            y_r         <= '0;
            theta_r     <= '0;
            theta_off_r <= '0;
            step_r      <= '0;
            busy_r      <= 1'b0;
            out_valid   <= 1'b0;
            phase_out   <= '0;
        end else begin
            out_valid <= 1'b0;

            if (!busy_r && in_valid) begin
                if (x_in[XY_FRAC+1]) begin
                    x_r         <= -x_in;
                    y_r         <= -y_in;
                    theta_off_r <= y_in[XY_FRAC+1] ? -OUT_W'(PI_INT) : OUT_W'(PI_INT);
                end else begin
                    x_r         <= x_in;
                    y_r         <= y_in;
                    theta_off_r <= '0;
                end
                theta_r <= '0;
                step_r  <= '0;
                busy_r  <= 1'b1;
            end else if (busy_r) begin
                x_r     <= x_nxt;
                y_r     <= y_nxt;
                theta_r <= theta_nxt;
                step_r  <= step_r + 1'b1;

                if (step_r == STEP_W'(N - 1)) begin
                    busy_r    <= 1'b0;
                    out_valid <= 1'b1;
                    phase_out <= $signed({theta_nxt[THETA_W-1], theta_nxt}) + theta_off_r;
                end
            end
        end
    end

endmodule
