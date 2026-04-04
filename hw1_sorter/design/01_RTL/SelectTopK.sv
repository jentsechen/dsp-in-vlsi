module SelectTopK #(
    parameter int WIDTH = 9
) (
    input  logic                    clk,
    input  logic                    rst_n,
    input  logic                    BlkIn,
    input  logic signed [WIDTH-1:0] In1,
    In2,
    In3,
    In4,
    In5,
    In6,
    In7,
    In8,
    output logic signed [WIDTH-1:0] SortOut,
    output logic        [      1:0] OutRank
);

  logic signed [WIDTH-1:0] sort_out[8];

  Sort8 #(WIDTH) sort0 (
      .clk  (clk),
      .rst_n(rst_n),
      .in0  (In1),
      .in1  (In2),
      .in2  (In3),
      .in3  (In4),
      .in4  (In5),
      .in5  (In6),
      .in6  (In7),
      .in7  (In8),
      .out0 (sort_out[0]),
      .out1 (sort_out[1]),
      .out2 (sort_out[2]),
      .out3 (sort_out[3]),
      .out4 (sort_out[4]),
      .out5 (sort_out[5]),
      .out6 (sort_out[6]),
      .out7 (sort_out[7])
  );

  logic signed [WIDTH-1:0] reg8_set0[4][8], reg8_set1[4][8];

  logic       write_en, write_buf_index, out_valid;
  logic [1:0] write_cnt;

  merge_sort_fsm fsm0 (
      .clk            (clk),
      .rst_n          (rst_n),
      .BlkIn          (BlkIn),
      .write_en       (write_en),
      .write_buf_index(write_buf_index),
      .write_cnt      (write_cnt),
      .out_valid      (out_valid)
  );

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      for (int i = 0; i < 4; i++)
        for (int j = 0; j < 8; j++) begin
          reg8_set0[i][j] <= '0;
          reg8_set1[i][j] <= '0;
        end
    end else if (write_en) begin
      if (write_buf_index == 0) begin
        for (int j = 0; j < 8; j++) reg8_set0[write_cnt][j] <= sort_out[j];
      end else begin
        for (int j = 0; j < 8; j++) reg8_set1[write_cnt][j] <= sort_out[j];
      end
    end
  end

  logic [2:0] ptr[4];
  logic signed [WIDTH-1:0] merge_in_0, merge_in_1, merge_in_2, merge_in_3;
  logic        [      1:0] max_index;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) ptr <= '{default: '0};
    else if (write_cnt == 2'd3) ptr <= '{default: '0};
    else if (write_en) ptr[max_index] <= ptr[max_index] + 1;
    else ptr <= '{default: '0};
  end

  assign merge_in_0 = write_buf_index ? reg8_set0[0][ptr[0]] : reg8_set1[0][ptr[0]];
  assign merge_in_1 = write_buf_index ? reg8_set0[1][ptr[1]] : reg8_set1[1][ptr[1]];
  assign merge_in_2 = write_buf_index ? reg8_set0[2][ptr[2]] : reg8_set1[2][ptr[2]];
  assign merge_in_3 = write_buf_index ? reg8_set0[3][ptr[3]] : reg8_set1[3][ptr[3]];

  max_index_finder #(WIDTH) max0 (
      .val0     (merge_in_0),
      .val1     (merge_in_1),
      .val2     (merge_in_2),
      .val3     (merge_in_3),
      .max_index(max_index)
  );

  assign SortOut = out_valid ? (write_buf_index ? reg8_set0[max_index][ptr[max_index]] : reg8_set1[max_index][ptr[max_index]]) : '0;
  assign OutRank = out_valid ? write_cnt : 2'd0;

endmodule