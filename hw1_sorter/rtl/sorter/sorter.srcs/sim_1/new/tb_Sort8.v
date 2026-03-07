`timescale 1ns / 1ps

module tb_Sort8();

    parameter WIDTH = 9;
    parameter CLK_PERIOD = 10;

    reg clk;
    reg rst_n;
    reg signed [WIDTH-1:0] in [0:7];
    wire signed [WIDTH-1:0] out [0:7];

    // Connect to the module ports
    Sort8 #(WIDTH) uut (
        .clk(clk), .rst_n(rst_n),
        .in0(in[0]), .in1(in[1]), .in2(in[2]), .in3(in[3]),
        .in4(in[4]), .in5(in[5]), .in6(in[6]), .in7(in[7]),
        .out0(out[0]), .out1(out[1]), .out2(out[2]), .out3(out[3]),
        .out4(out[4]), .out5(out[5]), .out6(out[6]), .out7(out[7])
    );

    // Scoreboard / Latency Buffer to track inputs through the 6-stage pipeline
    reg signed [WIDTH-1:0] history [0:5][0:7]; 
    integer i, j;

    // Clock generation
    initial clk = 0;
    always #(CLK_PERIOD/2) clk = ~clk;

    // Test Procedure
    initial begin
        // Initialize
        rst_n = 0;
        for (i = 0; i < 8; i = i + 1) in[i] = 0;
        
        #(CLK_PERIOD * 2);
        rst_n = 1;
        #(CLK_PERIOD);

        // Feed 20 sets of random signed data
//        repeat (20) begin
//            @(posedge clk);
//            for (i = 0; i < 8; i = i + 1) begin
//                in[i] = $random % 256; // Generates signed values between -255 and 255
//            end
//        end
        @(posedge clk);
        in[0] = 8;
        in[1] = 26;
        in[2] = 10;
        in[3] = 21;
        in[4] = 17;
        in[5] = 93;
        in[6] = 11;
        in[7] = 25;

        // Wait for pipeline to flush
        repeat (7) @(posedge clk);
        
        $display("Test Complete. Check waveforms for sorted order.");
        $finish;
    end

    // Shift history buffer every clock to track pipeline latency (6 stages)
    always @(posedge clk) begin
        if (rst_n) begin
            // Shift history
            for (i = 5; i > 0; i = i - 1) begin
                for (j = 0; j < 8; j = j + 1) begin
                    history[i][j] <= history[i-1][j];
                end
            end
            // Load current input into head of history
            for (j = 0; j < 8; j = j + 1) begin
                history[0][j] <= in[j];
            end
        end
    end

    // Simple Self-Checking Monitor
    // Checks if out[n] <= out[n+1]
    always @(negedge clk) begin
        if (rst_n && out[0] !== 9'shxxx) begin // Skip if output is still unknown
            if ((out[0] <= out[1]) && (out[1] <= out[2]) && (out[2] <= out[3]) &&
                (out[3] <= out[4]) && (out[4] <= out[5]) && (out[5] <= out[6]) && 
                (out[6] <= out[7])) begin
                $display("TIME: %0t | SUCCESS: [%d, %d, %d, %d, %d, %d, %d, %d]", 
                          $time, out[0], out[1], out[2], out[3], out[4], out[5], out[6], out[7]);
            end else begin
                $display("TIME: %0t | ERROR: Sort order failed! Out: [%d, %d, %d, %d, %d, %d, %d, %d]", 
                          $time, out[0], out[1], out[2], out[3], out[4], out[5], out[6], out[7]);
            end
        end
    end

endmodule