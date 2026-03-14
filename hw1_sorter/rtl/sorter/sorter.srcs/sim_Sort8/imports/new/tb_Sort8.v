`timescale 1ns / 1ps

module tb_Sort8();
    parameter WIDTH = 9;
    parameter CLK_PERIOD = 10;
    reg clk, rst_n;
    reg signed [WIDTH-1:0] in0, in1, in2, in3, in4, in5, in6, in7;
    wire signed [WIDTH-1:0] out0, out1, out2, out3, out4, out5, out6, out7;

    Sort8 #(WIDTH) uut (
        .clk(clk), .rst_n(rst_n),
        .in0(in0), .in1(in1), .in2(in2), .in3(in3),
        .in4(in4), .in5(in5), .in6(in6), .in7(in7),
        .out0(out0), .out1(out1), .out2(out2), .out3(out3),
        .out4(out4), .out5(out5), .out6(out6), .out7(out7)
    );

    initial clk = 0;
    always #(CLK_PERIOD/2) clk = ~clk;
    
    integer file_ptr;
    integer in0_t, in1_t, in2_t, in3_t, in4_t, in5_t, in6_t, in7_t;
    initial begin
        // Initialize
        rst_n = 0;
        in0 = 0;  in1 = 0;  in2 = 0;  in3 = 0;  in4 = 0;  in5 = 0; in6 = 0;  in7 = 0;
        
        #(CLK_PERIOD * 2);
        rst_n = 1;
        #(CLK_PERIOD);
        
        file_ptr = $fopen("input.txt", "r");
        
        if (file_ptr == 0) begin
            $display("Error: Could not open input file.");
            $finish;
        end
        
        while (!$feof(file_ptr)) begin
            $fscanf(file_ptr, "%d %d %d %d %d %d %d %d\n", in0_t, in1_t, in2_t, in3_t, in4_t, in5_t, in6_t, in7_t);
            @(posedge clk);
            in0<=in0_t; in1<=in1_t; in2<=in2_t; in3<=in3_t; in4<=in4_t; in5<=in5_t; in6<=in6_t; in7<=in7_t;
        end
        
        $fclose(file_ptr);
        
        @(posedge clk);
        in0 = 0;  in1 = 0;  in2 = 0;  in3 = 0;  in4 = 0;  in5 = 0; in6 = 0;  in7 = 0;
    end

endmodule