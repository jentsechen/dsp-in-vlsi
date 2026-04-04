module compare_swap #(
    parameter int WIDTH = 9
) (
    input  logic signed [WIDTH-1:0] a,
    input  logic signed [WIDTH-1:0] b,
    input  logic                    asc,
    output logic signed [WIDTH-1:0] low,
    output logic signed [WIDTH-1:0] high
);
  logic a_gt_b;
  logic swap;

  assign a_gt_b = (a > b);
  assign swap   = asc ^ !a_gt_b;

  assign low  = swap ? b : a;
  assign high = swap ? a : b;
endmodule