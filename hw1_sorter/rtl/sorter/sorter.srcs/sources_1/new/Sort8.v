module Sort8 #(
    parameter WIDTH = 9
) (
    input                       clk,
    input                       rst_n,
    input  signed [WIDTH-1:0]   in0, in1, in2, in3, in4, in5, in6, in7,
    output reg signed [WIDTH-1:0] out0, out1, out2, out3, out4, out5, out6, out7
);

    // Interconnect wires between CAS units and Registers
    wire signed [WIDTH-1:0] w1 [0:7], w2 [0:7], w3 [0:7], w4 [0:7], w5 [0:7], w6 [0:7];
    reg  signed [WIDTH-1:0] r1 [0:7], r2 [0:7], r3 [0:7], r4 [0:7], r5 [0:7];

    // --- STAGE 1: Create 4 bitonic pairs of length 2 ---
    compare_swap #(WIDTH) cs1_0 (in0, in1, 1'b1, w1[0], w1[1]);
    compare_swap #(WIDTH) cs1_1 (in2, in3, 1'b0, w1[2], w1[3]);
    compare_swap #(WIDTH) cs1_2 (in4, in5, 1'b1, w1[4], w1[5]);
    compare_swap #(WIDTH) cs1_3 (in6, in7, 1'b0, w1[6], w1[7]);

    integer i;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for(i=0; i<8; i=i+1) r1[i] <= 0;
        end else begin
            for(i=0; i<8; i=i+1) r1[i] <= w1[i];
        end
    end

    // --- STAGE 2: Merge to 4-groups (Step A) ---
    compare_swap #(WIDTH) cs2_0 (r1[0], r1[2], 1'b1, w2[0], w2[2]);
    compare_swap #(WIDTH) cs2_1 (r1[1], r1[3], 1'b1, w2[1], w2[3]);
    compare_swap #(WIDTH) cs2_2 (r1[4], r1[6], 1'b0, w2[4], w2[6]);
    compare_swap #(WIDTH) cs2_3 (r1[5], r1[7], 1'b0, w2[5], w2[7]);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for(i=0; i<8; i=i+1) r2[i] <= 0;
        end else begin       
            for(i=0; i<8; i=i+1) r2[i] <= w2[i];
        end
    end

    // --- STAGE 3: Merge to 4-groups (Step B) ---
    compare_swap #(WIDTH) cs3_0 (r2[0], r2[1], 1'b1, w3[0], w3[1]);
    compare_swap #(WIDTH) cs3_1 (r2[2], r2[3], 1'b1, w3[2], w3[3]);
    compare_swap #(WIDTH) cs3_2 (r2[4], r2[5], 1'b0, w3[4], w3[5]);
    compare_swap #(WIDTH) cs3_3 (r2[6], r2[7], 1'b0, w3[6], w3[7]);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for(i=0; i<8; i=i+1) r3[i] <= 0;
        end else begin        
            for(i=0; i<8; i=i+1) r3[i] <= w3[i];
        end
    end

    // --- STAGE 4: Final Merge 8-group (Step A: Dist 4) ---
    compare_swap #(WIDTH) cs4_0 (r3[0], r3[4], 1'b1, w4[0], w4[4]);
    compare_swap #(WIDTH) cs4_1 (r3[1], r3[5], 1'b1, w4[1], w4[5]);
    compare_swap #(WIDTH) cs4_2 (r3[2], r3[6], 1'b1, w4[2], w4[6]);
    compare_swap #(WIDTH) cs4_3 (r3[3], r3[7], 1'b1, w4[3], w4[7]);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for(i=0; i<8; i=i+1) r4[i] <= 0;
        end else begin       
            for(i=0; i<8; i=i+1) r4[i] <= w4[i];
        end
    end

    // --- STAGE 5: Final Merge 8-group (Step B: Dist 2) ---
    compare_swap #(WIDTH) cs5_0 (r4[0], r4[2], 1'b1, w5[0], w5[2]);
    compare_swap #(WIDTH) cs5_1 (r4[1], r4[3], 1'b1, w5[1], w5[3]);
    compare_swap #(WIDTH) cs5_2 (r4[4], r4[6], 1'b1, w5[4], w5[6]);
    compare_swap #(WIDTH) cs5_3 (r4[5], r4[7], 1'b1, w5[5], w5[7]);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for(i=0; i<8; i=i+1) r5[i] <= 0;
        end else begin       
            for(i=0; i<8; i=i+1) r5[i] <= w5[i];
        end
    end

    // --- STAGE 6: Final Merge 8-group (Step C: Dist 1) ---
    compare_swap #(WIDTH) cs6_0 (r5[0], r5[1], 1'b1, w6[0], w6[1]);
    compare_swap #(WIDTH) cs6_1 (r5[2], r5[3], 1'b1, w6[2], w6[3]);
    compare_swap #(WIDTH) cs6_2 (r5[4], r5[5], 1'b1, w6[4], w6[5]);
    compare_swap #(WIDTH) cs6_3 (r5[6], r5[7], 1'b1, w6[6], w6[7]);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            {out7,out6,out5,out4,out3,out2,out1,out0} <= 0;
        end else begin
            {out7,out6,out5,out4,out3,out2,out1,out0} <= {w6[0],w6[1],w6[2],w6[3],w6[4],w6[5],w6[6],w6[7]};
        end
    end

endmodule