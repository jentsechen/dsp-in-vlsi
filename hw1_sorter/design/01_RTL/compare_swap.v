module compare_swap #(
    parameter WIDTH = 9
) (
    input  signed [WIDTH-1:0] a,
    input  signed [WIDTH-1:0] b,
    input                     asc,
    output signed [WIDTH-1:0] low,
    output signed [WIDTH-1:0] high
);
  wire a_gt_b;
  wire swap;

  // Only one hardware comparator instantiated here
  assign a_gt_b = (a > b);

  // Use XOR logic to decide the swap:
  // If asc=1, swap if a > b.
  // If asc=0, swap if a <= b (which is !a_gt_b).
  assign swap = asc ^ !a_gt_b;

  assign low = swap ? b : a;
  assign high = swap ? a : b;
endmodule
