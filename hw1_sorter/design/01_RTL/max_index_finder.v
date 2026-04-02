module max_index_finder #(
    parameter WIDTH = 9
) (
    input  signed [WIDTH-1:0] val0,
    input  signed [WIDTH-1:0] val1,
    input  signed [WIDTH-1:0] val2,
    input  signed [WIDTH-1:0] val3,
    output reg    [      1:0] max_index
);

  reg signed [WIDTH-1:0] upper_winner;
  reg        [      1:0] upper_idx;
  reg signed [WIDTH-1:0] lower_winner;
  reg        [      1:0] lower_idx;

  always @* begin
    // Stage 1: Compare 0 vs 1
    if (val1 > val0) begin
      upper_winner = val1;
      upper_idx = 2'd1;
    end else begin
      upper_winner = val0;
      upper_idx = 2'd0;
    end

    // Stage 1: Compare 2 vs 3
    if (val3 > val2) begin
      lower_winner = val3;
      lower_idx = 2'd3;
    end else begin
      lower_winner = val2;
      lower_idx = 2'd2;
    end

    // Stage 2: Compare winners
    if (lower_winner > upper_winner) begin
      max_index = lower_idx;
    end else begin
      max_index = upper_idx;
    end
  end

endmodule
