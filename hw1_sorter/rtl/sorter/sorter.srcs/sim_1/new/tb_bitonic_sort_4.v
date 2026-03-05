`timescale 1ns / 1ps

module tb_bitonic_sort_4();

    parameter WIDTH = 8;
    parameter CLK_PERIOD = 10; // 100MHz clock

    // Inputs
    reg clk;
    reg rst_n;
    reg [WIDTH-1:0] d0, d1, d2, d3;
    
    // Outputs
    wire [WIDTH-1:0] s0, s1, s2, s3;

    // Instantiate the Pipelined Module
    bitonic_sort_4 #(WIDTH) uut (
        .clk(clk),
        .rst_n(rst_n),
        .d0(d0), .d1(d1), .d2(d2), .d3(d3),
        .s0(s0), .s1(s1), .s2(s2), .s3(s3)
    );

    // Clock Generation
    initial clk = 0;
    always #(CLK_PERIOD/2) clk = ~clk;

    initial begin
        // Initialize Inputs
        rst_n = 0;
        d0 = 0; d1 = 0; d2 = 0; d3 = 0;

        // Reset Sequence
        #(CLK_PERIOD * 2);
        rst_n = 1;
        @(posedge clk);

        // --- DATA INPUT PHASE ---
        // Case 1: Already Sorted (Input at T=0)
        d0 = 10; d1 = 20; d2 = 30; d3 = 40;
        @(posedge clk);

        // Case 2: Reverse Sorted (Input at T=1)
        d0 = 99; d1 = 66; d2 = 33; d3 = 11;
        @(posedge clk);

        // Case 3: Random Order (Input at T=2)
        d0 = 45; d1 = 12; d2 = 88; d3 = 0;
        @(posedge clk);

        // Case 4: Duplicate Values (Input at T=3)
        d0 = 15; d1 = 15; d2 = 5; d3 = 15;
        @(posedge clk);
        
        // Clear inputs to see the pipeline flush
        d0 = 0; d1 = 0; d2 = 0; d3 = 0;

        // --- LATENCY WAIT ---
        // Since latency is 3 cycles, we wait for the results to propagate
        repeat(5) @(posedge clk);

        $display("Simulation Finished.");
        $finish;
    end

    // Monitor Output (Adjusted to show which cycle we are on)
    always @(posedge clk) begin
        if (rst_n) begin
            $display("Time=%0t | In: [%d %d %d %d] | Out: [%d %d %d %d]", 
                     $time, d0, d1, d2, d3, s0, s1, s2, s3);
        end
    end

endmodule