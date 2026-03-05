module bitonic_sort_4 #(parameter WIDTH = 8) (
    input  clk,
    input  rst_n,
    input  [WIDTH-1:0] d0, d1, d2, d3,
    output reg [WIDTH-1:0] s0, s1, s2, s3
);
    // Internal wires for the outputs of the CAS units
    wire [WIDTH-1:0] stage1_out0, stage1_out1, stage1_out2, stage1_out3;
    wire [WIDTH-1:0] stage2_out0, stage2_out1, stage2_out2, stage2_out3;
    wire [WIDTH-1:0] stage3_out0, stage3_out1, stage3_out2, stage3_out3;

    // Pipeline Registers
    reg [WIDTH-1:0] r1_0, r1_1, r1_2, r1_3;
    reg [WIDTH-1:0] r2_0, r2_1, r2_2, r2_3;

    // --- STAGE 1: Generate Bitonic Sequence ---
    compare_swap #(WIDTH) cs1_0 (d0, d1, 1'b1, stage1_out0, stage1_out1);
    compare_swap #(WIDTH) cs1_1 (d2, d3, 1'b0, stage1_out2, stage1_out3);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            {r1_0, r1_1, r1_2, r1_3} <= 0;
        end else begin
            r1_0 <= stage1_out0;
            r1_1 <= stage1_out1;
            r1_2 <= stage1_out2;
            r1_3 <= stage1_out3;
        end
    end

    // --- STAGE 2: Bitonic Merge (Step 1) ---
    compare_swap #(WIDTH) cs2_0 (r1_0, r1_2, 1'b1, stage2_out0, stage2_out2);
    compare_swap #(WIDTH) cs2_1 (r1_1, r1_3, 1'b1, stage2_out1, stage2_out3);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            {r2_0, r2_1, r2_2, r2_3} <= 0;
        end else begin
            r2_0 <= stage2_out0;
            r2_1 <= stage2_out1;
            r2_2 <= stage2_out2;
            r2_3 <= stage2_out3;
        end
    end

    // --- STAGE 3: Bitonic Merge (Step 2 / Final Sort) ---
    compare_swap #(WIDTH) cs3_0 (r2_0, r2_1, 1'b1, stage3_out0, stage3_out1);
    compare_swap #(WIDTH) cs3_1 (r2_2, r2_3, 1'b1, stage3_out2, stage3_out3);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            {s0, s1, s2, s3} <= 0;
        end else begin
            s0 <= stage3_out0;
            s1 <= stage3_out1;
            s2 <= stage3_out2;
            s3 <= stage3_out3;
        end
    end

endmodule