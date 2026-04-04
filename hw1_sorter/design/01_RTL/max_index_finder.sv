module max_index_finder #(
    parameter int WIDTH = 9
) (
    input  logic signed [WIDTH-1:0] val0,
    input  logic signed [WIDTH-1:0] val1,
    input  logic signed [WIDTH-1:0] val2,
    input  logic signed [WIDTH-1:0] val3,
    output logic        [      1:0] max_index
);

  logic signed [WIDTH-1:0] upper_winner;
  logic        [      1:0] upper_idx;
  logic signed [WIDTH-1:0] lower_winner;
  logic        [      1:0] lower_idx;

  always_comb begin
    if (val1 > val0) begin
      upper_winner = val1;
      upper_idx    = 2'd1;
    end else begin
      upper_winner = val0;
      upper_idx    = 2'd0;
    end

    if (val3 > val2) begin
      lower_winner = val3;
      lower_idx    = 2'd3;
    end else begin
      lower_winner = val2;
      lower_idx    = 2'd2;
    end

    if (lower_winner > upper_winner) max_index = lower_idx;
    else max_index = upper_idx;
  end

endmodule