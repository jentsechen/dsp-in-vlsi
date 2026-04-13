module poly2_interpolator (
    input  logic        clk,
    input  logic        rst_n,
    input  logic        in_valid,
    input  logic [15:0] in_re,
    input  logic [15:0] in_im,
    output logic        out_valid,
    output logic [15:0] out_re,
    output logic [15:0] out_im
);

  // --- mu counter: resets on in_valid, counts 0..7 each clock cycle ---
  // Generates BF16 mu = cnt/8 via lookup table.

  logic [2:0] mu_cnt;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) mu_cnt <= '0;
    else if (in_valid) mu_cnt <= '0;
    else mu_cnt <= mu_cnt + 3'd1;
  end

  logic [15:0] mu_r;

  always_comb begin
    case (mu_cnt)
      3'd0: mu_r = 16'h0000;  // 0/8 = 0.0
      3'd1: mu_r = 16'h3E00;  // 1/8 = 0.125
      3'd2: mu_r = 16'h3E80;  // 2/8 = 0.25
      3'd3: mu_r = 16'h3EC0;  // 3/8 = 0.375
      3'd4: mu_r = 16'h3F00;  // 4/8 = 0.5
      3'd5: mu_r = 16'h3F20;  // 5/8 = 0.625
      3'd6: mu_r = 16'h3F40;  // 6/8 = 0.75
      3'd7: mu_r = 16'h3F60;  // 7/8 = 0.875
    endcase
  end

  // --- 3-sample shift register ---
  // sr[0] = x[m+2] (newest), sr[1] = x[m+1], sr[2] = x[m] (oldest)
  // Advances on in_valid_r (one cycle after in_valid).

  logic [15:0] sr_re[0:2], sr_im[0:2];

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      sr_re[0] <= '0;
      sr_re[1] <= '0;
      sr_re[2] <= '0;
      sr_im[0] <= '0;
      sr_im[1] <= '0;
      sr_im[2] <= '0;
    end else if (in_valid) begin
      sr_re[0] <= in_re;
      sr_re[1] <= sr_re[0];
      sr_re[2] <= sr_re[1];
      sr_im[0] <= in_im;
      sr_im[1] <= sr_im[0];
      sr_im[2] <= sr_im[1];
    end
  end

  // --- Fill counter: saturates at 3, gates out_valid ---

  logic [1:0] fill_cnt;
  logic       sr_full;

  assign sr_full = (fill_cnt == 2'd3);

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) fill_cnt <= '0;
    else if (in_valid && !sr_full) fill_cnt <= fill_cnt + 2'd1;
  end

  // --- BF16 multiply-by-0.5: decrement exponent, clamp to 0 on underflow ---

  logic [15:0] hx0_re, hx0_im, hx2_re, hx2_im;

  assign hx0_re = (sr_re[2][14:7] <= 8'd1) ? 16'h0000 : {sr_re[2][15], sr_re[2][14:7]-8'd1, sr_re[2][6:0]};
  assign hx0_im = (sr_im[2][14:7] <= 8'd1) ? 16'h0000 : {sr_im[2][15], sr_im[2][14:7]-8'd1, sr_im[2][6:0]};
  assign hx2_re = (sr_re[0][14:7] <= 8'd1) ? 16'h0000 : {sr_re[0][15], sr_re[0][14:7]-8'd1, sr_re[0][6:0]};
  assign hx2_im = (sr_im[0][14:7] <= 8'd1) ? 16'h0000 : {sr_im[0][15], sr_im[0][14:7]-8'd1, sr_im[0][6:0]};

  // --- BF16 negate x[m] and x[m+1]: flip sign bit, keep zero as zero ---

  logic [15:0] nx0_re, nx0_im, nx1_re, nx1_im;

  assign nx0_re = (sr_re[2][14:7] == 8'd0) ? 16'h0000 : {~sr_re[2][15], sr_re[2][14:0]};
  assign nx0_im = (sr_im[2][14:7] == 8'd0) ? 16'h0000 : {~sr_im[2][15], sr_im[2][14:0]};
  assign nx1_re = (sr_re[1][14:7] == 8'd0) ? 16'h0000 : {~sr_re[1][15], sr_re[1][14:0]};
  assign nx1_im = (sr_im[1][14:7] == 8'd0) ? 16'h0000 : {~sr_im[1][15], sr_im[1][14:0]};

  // --- Farrow branch v(2) = 0.5*x[m] - x[m+1] + 0.5*x[m+2] ---

  logic [15:0] v2a_re, v2a_im, v2_re, v2_im;

  // --- BF16 negate v(2): declared after v2_re/v2_im ---

  logic [15:0] nv2_re, nv2_im;

  assign nv2_re = (v2_re[14:7] == 8'd0) ? 16'h0000 : {~v2_re[15], v2_re[14:0]};
  assign nv2_im = (v2_im[14:7] == 8'd0) ? 16'h0000 : {~v2_im[15], v2_im[14:0]};

  bf16_add u_v2a_re (
      .a  (hx0_re),
      .b  (nx1_re),
      .out(v2a_re)
  );
  bf16_add u_v2a_im (
      .a  (hx0_im),
      .b  (nx1_im),
      .out(v2a_im)
  );
  bf16_add u_v2_re (
      .a  (v2a_re),
      .b  (hx2_re),
      .out(v2_re)
  );
  bf16_add u_v2_im (
      .a  (v2a_im),
      .b  (hx2_im),
      .out(v2_im)
  );

  // --- Farrow branch v(1) = x[m+1] - x[m] - v(2) ---

  logic [15:0] v1a_re, v1a_im, v1_re, v1_im;

  bf16_add u_v1a_re (
      .a  (sr_re[1]),
      .b  (nx0_re),
      .out(v1a_re)
  );
  bf16_add u_v1a_im (
      .a  (sr_im[1]),
      .b  (nx0_im),
      .out(v1a_im)
  );
  bf16_add u_v1_re (
      .a  (v1a_re),
      .b  (nv2_re),
      .out(v1_re)
  );
  bf16_add u_v1_im (
      .a  (v1a_im),
      .b  (nv2_im),
      .out(v1_im)
  );

  // --- Horner evaluation: y = x[m] + mu*(v(1) + mu*v(2)) ---

  logic [15:0] t2_re, t2_im, t1_re, t1_im, t3_re, t3_im, yc_re, yc_im;

  bf16_mul u_t2_re (
      .a  (mu_r),
      .b  (v2_re),
      .out(t2_re)
  );
  bf16_mul u_t2_im (
      .a  (mu_r),
      .b  (v2_im),
      .out(t2_im)
  );
  bf16_add u_t1_re (
      .a  (v1_re),
      .b  (t2_re),
      .out(t1_re)
  );
  bf16_add u_t1_im (
      .a  (v1_im),
      .b  (t2_im),
      .out(t1_im)
  );
  bf16_mul u_t3_re (
      .a  (mu_r),
      .b  (t1_re),
      .out(t3_re)
  );
  bf16_mul u_t3_im (
      .a  (mu_r),
      .b  (t1_im),
      .out(t3_im)
  );
  bf16_add u_yc_re (
      .a  (sr_re[2]),
      .b  (t3_re),
      .out(yc_re)
  );
  bf16_add u_yc_im (
      .a  (sr_im[2]),
      .b  (t3_im),
      .out(yc_im)
  );

  // --- Output registers ---

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      out_valid <= '0;
      out_re    <= '0;
      out_im    <= '0;
    end else begin
      out_valid <= sr_full;
      out_re    <= yc_re;
      out_im    <= yc_im;
    end
  end

endmodule
