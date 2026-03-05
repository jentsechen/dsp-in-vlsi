module compare_swap #(parameter WIDTH = 8) (
    input  [WIDTH-1:0] in0, in1,
    input              asc, // 1 for ascending, 0 for descending
    output [WIDTH-1:0] out0, out1
);
    wire swap = (asc) ? (in0 > in1) : (in0 < in1);

    assign out0 = swap ? in1 : in0;
    assign out1 = swap ? in0 : in1;
endmodule