module fir_filter #(
    localparam TAPS = 25,
    parameter INPUT_INT  = 1,  parameter INPUT_FRAC = 13,
    parameter COEF_INT   = 1,  parameter COEF_FRAC  = 15,
    parameter MULT_INT    = 1,  parameter MULT_FRAC   = 18,
    parameter ADD_INT    = 3,  parameter ADD_FRAC   = 18,
    
    localparam INPUT_WIDTH = INPUT_INT + INPUT_FRAC + 1,
    localparam COEF_WIDTH  = COEF_INT + COEF_FRAC + 1,
    localparam MULT_WIDTH   = MULT_INT + MULT_FRAC + 1,
    localparam ADD_WIDTH  = ADD_INT + ADD_FRAC + 1
)(
    input  logic                   clk,
    input  logic                   rst_n,
    input  logic signed [INPUT_WIDTH-1:0] FilterIn,
    output logic signed [ADD_WIDTH-1:0]   FilterOut
);

    // --- 1. Coefficient LUT Definition ---
    // Use 'localparam' so it cannot be changed from outside the module
    localparam logic signed [COEF_WIDTH-1:0] COEF_LUT [0:TAPS-1] = '{
        -17'sd1,
        -17'sd2845,
        -17'sd5420,
        -17'sd6954,
        -17'sd6775,
        -17'sd4471,
        17'sd0,
        17'sd6258,
        17'sd13549,
        17'sd20860,
        17'sd27098,
        17'sd31291,
        17'sd32768,
        17'sd31291,
        17'sd27098,
        17'sd20860,
        17'sd13549,
        17'sd6258,
        17'sd0,
        -17'sd4471,
        -17'sd6775,
        -17'sd6954,
        -17'sd5420,
        -17'sd2845,
        -17'sd1
    };
//    localparam logic signed [COEF_WIDTH-1:0] COEF_LUT [0:TAPS-1] = '{
//    16'sd1, 16'sd0, 16'sd0, 16'sd0, 16'sd0, 16'sd0, 16'sd0, 16'sd0, 16'sd0, 16'sd0
//    , 16'sd0, 16'sd0, 16'sd0, 16'sd0, 16'sd0, 16'sd0, 16'sd0, 16'sd0, 16'sd0, 16'sd0
//    , 16'sd0, 16'sd0, 16'sd0, 16'sd0, 16'sd0};
//    logic signed [COEF_WIDTH-1:0] COEF_LUT [0:TAPS-1];
//    initial begin
//        // Use $readmemh for hex values or $readmemb for binary
//        $readmemh("coef.txt", COEF_LUT);
//    end

    // 2. Delay Line
    logic signed [INPUT_WIDTH-1:0] delay_pipeline [0:TAPS-1];

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for (int i = 0; i < TAPS; i++) delay_pipeline[i] <= '0;
        end else begin
            delay_pipeline[0] <= FilterIn;
            for (int i = 1; i < TAPS; i++) delay_pipeline[i] <= delay_pipeline[i-1];
        end
    end

    // 3. Multiplication Stage (Using LUT)
    logic signed [MULT_WIDTH-1:0] product [0:TAPS-1];
    
    always_ff @(posedge clk) begin
        for (int i = 0; i < TAPS; i++) begin
            // References the localparam LUT instead of an input port
//            product[i] <= delay_pipeline[i] * COEF_LUT[i];
            automatic logic signed [INPUT_WIDTH+COEF_WIDTH-1:0] full_prod = delay_pipeline[i] * COEF_LUT[i];
            localparam lsb = INPUT_FRAC+COEF_FRAC-MULT_FRAC;
            product[i] <= full_prod[INPUT_WIDTH+COEF_WIDTH-(INPUT_INT+1+COEF_INT+1-MULT_INT-1)-1:lsb];
        end
    end

    // 4. Accumulation
    logic signed [ADD_WIDTH-1:0] sum;
    always_comb begin
        sum = '0;
        for (int i = 0; i < TAPS; i++) sum = sum + product[i];
    end

    // 5. Output Scaling
    localparam SHIFT = MULT_FRAC - ADD_FRAC;
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) FilterOut <= '0;
        else        FilterOut <= sum >>> SHIFT;
    end

endmodule