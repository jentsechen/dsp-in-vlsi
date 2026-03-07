module compare_swap #(parameter WIDTH = 9) (
    input  signed [WIDTH-1:0] a,
    input  signed [WIDTH-1:0] b,
    input                     asc, // 1 for Ascending, 0 for Descending
    output signed [WIDTH-1:0] low,
    output signed [WIDTH-1:0] high
);
    wire swap;
    // For ascending: swap if a > b. For descending: swap if a < b.
    assign swap = asc ? (a > b) : (a < b);

    assign low  = swap ? b : a;
    assign high = swap ? a : b;
endmodule