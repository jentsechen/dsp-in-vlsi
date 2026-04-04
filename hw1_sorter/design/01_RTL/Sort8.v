module Sort8 #(
    parameter int WIDTH = 9
) (
    input  logic                    clk,
    input  logic                    rst_n,
    input  logic signed [WIDTH-1:0] in0,
    in1,
    in2,
    in3,
    in4,
    in5,
    in6,
    in7,
    output logic signed [WIDTH-1:0] out0,
    out1,
    out2,
    out3,
    out4,
    out5,
    out6,
    out7
);

  logic signed [WIDTH-1:0] w1[8], w2[8], w3[8], w4[8], w5[8], w6[8];
  logic signed [WIDTH-1:0] r1[8], r2[8], r3[8], r4[8], r5[8];

  compare_swap #(WIDTH) cs1_0 (
      .a   (in0),
      .b   (in1),
      .asc (1'b1),
      .low (w1[0]),
      .high(w1[1])
  );
  compare_swap #(WIDTH) cs1_1 (
      .a   (in2),
      .b   (in3),
      .asc (1'b0),
      .low (w1[2]),
      .high(w1[3])
  );
  compare_swap #(WIDTH) cs1_2 (
      .a   (in4),
      .b   (in5),
      .asc (1'b1),
      .low (w1[4]),
      .high(w1[5])
  );
  compare_swap #(WIDTH) cs1_3 (
      .a   (in6),
      .b   (in7),
      .asc (1'b0),
      .low (w1[6]),
      .high(w1[7])
  );

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) r1 <= '{default: '0};
    else r1 <= w1;
  end

  compare_swap #(WIDTH) cs2_0 (
      .a   (r1[0]),
      .b   (r1[2]),
      .asc (1'b1),
      .low (w2[0]),
      .high(w2[2])
  );
  compare_swap #(WIDTH) cs2_1 (
      .a   (r1[1]),
      .b   (r1[3]),
      .asc (1'b1),
      .low (w2[1]),
      .high(w2[3])
  );
  compare_swap #(WIDTH) cs2_2 (
      .a   (r1[4]),
      .b   (r1[6]),
      .asc (1'b0),
      .low (w2[4]),
      .high(w2[6])
  );
  compare_swap #(WIDTH) cs2_3 (
      .a   (r1[5]),
      .b   (r1[7]),
      .asc (1'b0),
      .low (w2[5]),
      .high(w2[7])
  );

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) r2 <= '{default: '0};
    else r2 <= w2;
  end

  compare_swap #(WIDTH) cs3_0 (
      .a   (r2[0]),
      .b   (r2[1]),
      .asc (1'b1),
      .low (w3[0]),
      .high(w3[1])
  );
  compare_swap #(WIDTH) cs3_1 (
      .a   (r2[2]),
      .b   (r2[3]),
      .asc (1'b1),
      .low (w3[2]),
      .high(w3[3])
  );
  compare_swap #(WIDTH) cs3_2 (
      .a   (r2[4]),
      .b   (r2[5]),
      .asc (1'b0),
      .low (w3[4]),
      .high(w3[5])
  );
  compare_swap #(WIDTH) cs3_3 (
      .a   (r2[6]),
      .b   (r2[7]),
      .asc (1'b0),
      .low (w3[6]),
      .high(w3[7])
  );

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) r3 <= '{default: '0};
    else r3 <= w3;
  end

  compare_swap #(WIDTH) cs4_0 (
      .a   (r3[0]),
      .b   (r3[4]),
      .asc (1'b1),
      .low (w4[0]),
      .high(w4[4])
  );
  compare_swap #(WIDTH) cs4_1 (
      .a   (r3[1]),
      .b   (r3[5]),
      .asc (1'b1),
      .low (w4[1]),
      .high(w4[5])
  );
  compare_swap #(WIDTH) cs4_2 (
      .a   (r3[2]),
      .b   (r3[6]),
      .asc (1'b1),
      .low (w4[2]),
      .high(w4[6])
  );
  compare_swap #(WIDTH) cs4_3 (
      .a   (r3[3]),
      .b   (r3[7]),
      .asc (1'b1),
      .low (w4[3]),
      .high(w4[7])
  );

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) r4 <= '{default: '0};
    else r4 <= w4;
  end

  compare_swap #(WIDTH) cs5_0 (
      .a   (r4[0]),
      .b   (r4[2]),
      .asc (1'b1),
      .low (w5[0]),
      .high(w5[2])
  );
  compare_swap #(WIDTH) cs5_1 (
      .a   (r4[1]),
      .b   (r4[3]),
      .asc (1'b1),
      .low (w5[1]),
      .high(w5[3])
  );
  compare_swap #(WIDTH) cs5_2 (
      .a   (r4[4]),
      .b   (r4[6]),
      .asc (1'b1),
      .low (w5[4]),
      .high(w5[6])
  );
  compare_swap #(WIDTH) cs5_3 (
      .a   (r4[5]),
      .b   (r4[7]),
      .asc (1'b1),
      .low (w5[5]),
      .high(w5[7])
  );

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) r5 <= '{default: '0};
    else r5 <= w5;
  end

  compare_swap #(WIDTH) cs6_0 (
      .a   (r5[0]),
      .b   (r5[1]),
      .asc (1'b1),
      .low (w6[0]),
      .high(w6[1])
  );
  compare_swap #(WIDTH) cs6_1 (
      .a   (r5[2]),
      .b   (r5[3]),
      .asc (1'b1),
      .low (w6[2]),
      .high(w6[3])
  );
  compare_swap #(WIDTH) cs6_2 (
      .a   (r5[4]),
      .b   (r5[5]),
      .asc (1'b1),
      .low (w6[4]),
      .high(w6[5])
  );
  compare_swap #(WIDTH) cs6_3 (
      .a   (r5[6]),
      .b   (r5[7]),
      .asc (1'b1),
      .low (w6[6]),
      .high(w6[7])
  );

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) {out7, out6, out5, out4, out3, out2, out1, out0} <= '0;
    else
      {out7, out6, out5, out4, out3, out2, out1, out0} <= {
        w6[0], w6[1], w6[2], w6[3], w6[4], w6[5], w6[6], w6[7]
      };
  end

endmodule