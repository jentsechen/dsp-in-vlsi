`timescale 1ns / 1ps

module tb_SelectTopK();
    parameter WIDTH = 9;
    parameter CLK_PERIOD = 10;
    reg clk, rst_n, BlkIn;
    reg signed [WIDTH-1:0] In1, In2, In3, In4, In5, In6, In7, In8;
    wire signed [WIDTH-1:0] SortOut;
    wire [1:0] OutRank;
    
    SelectTopK #(WIDTH) uut (
        .clk(clk), .rst_n(rst_n), .BlkIn(BlkIn),
        .In1(In1), .In2(In2), .In3(In3), .In4(In4), .In5(In5), .In6(In6), .In7(In7), .In8(In8),
        .SortOut(SortOut), .OutRank(OutRank)
    );
    
    // Clock generation
    initial clk = 0;
    always #(CLK_PERIOD/2) clk = ~clk;
    
    integer k;
    initial begin
        // Initialize
        rst_n = 0;
        In1 = 0;  In2 = 0;  In3 = 0;  In4 = 0;  In5 = 0;  In6 = 0;  In7 = 0;  In8 = 0; BlkIn = 0;
        
        #(CLK_PERIOD * 2);
        rst_n = 1;
        #(CLK_PERIOD);
        
//        for (k = 0; k < 8; k = k + 1) begin
//            @(posedge clk);
//            // Pulse BlkIn only on the very first cycle to start the FSM
//            BlkIn <= (k == 0); 
            
//            // Assign values (1-8, 9-16, ..., 57-64)
//            In1 <= (k * 8) + 1;
//            In2 <= (k * 8) + 2;
//            In3 <= (k * 8) + 3;
//            In4 <= (k * 8) + 4;
//            In5 <= (k * 8) + 5;
//            In6 <= (k * 8) + 6;
//            In7 <= (k * 8) + 7;
//            In8 <= (k * 8) + 8;
//        end
        @(posedge clk);
        BlkIn <= 1;
        In1 <= 1;  In2 <= 2;  In3 <= 3;  In4 <= 29;  In5 <= 27;  In6 <= 32;  In7 <= 28;  In8 <= 8;

        // Set 1: Values 9-16
        @(posedge clk);
        BlkIn <= 0;
        In1 <= 9;  In2 <= 10; In3 <= 11; In4 <= 12; In5 <= 13; In6 <= 14; In7 <= 15; In8 <= 16;

        // Set 2: Values 17-24
        @(posedge clk);
        BlkIn <= 0;
        In1 <= 17; In2 <= 18; In3 <= 19; In4 <= 20; In5 <= 21; In6 <= 22; In7 <= 23; In8 <= 24;

        // Set 3: Values 25-32
        @(posedge clk);
        BlkIn <= 0;
        In1 <= 4; In2 <= 5; In3 <= 6; In4 <= 7; In5 <= 25; In6 <= 30; In7 <= 31; In8 <= 26;

        // Set 4: Values 33-40
        @(posedge clk);
        BlkIn <= 1;
        In1 <= 33; In2 <= 34; In3 <= 35; In4 <= 36; In5 <= 37; In6 <= 38; In7 <= 39; In8 <= 40;

        // Set 5: Values 41-48
        @(posedge clk);
        BlkIn <= 0;
        In1 <= 41; In2 <= 42; In3 <= 43; In4 <= 44; In5 <= 45; In6 <= 46; In7 <= 47; In8 <= 48;

        // Set 6: Values 49-56
        @(posedge clk);
        BlkIn <= 0;
        In1 <= 49; In2 <= 50; In3 <= 51; In4 <= 52; In5 <= 53; In6 <= 54; In7 <= 55; In8 <= 56;

        // Set 7: Values 57-64
        @(posedge clk);
        BlkIn <= 0;
        In1 <= 57; In2 <= 58; In3 <= 59; In4 <= 60; In5 <= 61; In6 <= 62; In7 <= 63; In8 <= 64;

        // --- 3. End of Burst ---
        @(posedge clk);
        BlkIn <= 0;
        In1 <= 0; In2 <= 0; In3 <= 0; In4 <= 0; In5 <= 0; In6 <= 0; In7 <= 0; In8 <= 0;
        repeat (12) @(posedge clk);
    end

endmodule
