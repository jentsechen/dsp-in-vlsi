module fir_filter_paral_2 #(
    localparam TAPS = 25,
    parameter INPUT_INT  = 1,  parameter INPUT_FRAC = 13,
    parameter COEF_INT   = 1,  parameter COEF_FRAC  = 15,
    parameter MULT_INT   = 1,  parameter MULT_FRAC  = 18,
    parameter ADD_INT    = 3,  parameter ADD_FRAC   = 18,
    
    localparam INPUT_WIDTH = INPUT_INT + INPUT_FRAC + 1,
    localparam COEF_WIDTH  = COEF_INT + COEF_FRAC + 1,
    localparam MULT_WIDTH  = MULT_INT + MULT_FRAC + 1,
    localparam ADD_WIDTH   = ADD_INT + ADD_FRAC + 1,
    localparam LATENCY     = 9
)(
    input  logic                   clk,
    input  logic                   rst_n,
    input  logic signed [INPUT_WIDTH-1:0] FilterIn0, FilterIn1, // Two inputs per cycle
    input  logic                   ValidIn,
    output logic signed [ADD_WIDTH-1:0]   FilterOut0, FilterOut1, // Two outputs per cycle
    output logic                   ValidOut
);

    // --- 1. Coefficient LUT ---
    localparam logic signed [COEF_WIDTH-1:0] COEF_LUT [0:TAPS-1] = '{
        -17'sd1,   -17'sd2845, -17'sd5420, -17'sd6954, -17'sd6775,
        -17'sd4471, 17'sd0,     17'sd6258,  17'sd13549, 17'sd20860,
         17'sd27098,17'sd31291, 17'sd32768, 17'sd31291, 17'sd27098,
         17'sd20860,17'sd13549, 17'sd6258,  17'sd0,    -17'sd4471,
        -17'sd6775, -17'sd6954, -17'sd5420, -17'sd2845, -17'sd1
    };

    // --- 2. Parallel Delay Lines ---
    // We need to store samples in pairs. For 2-parallel, each delay line 
    // effectively moves at half the sample rate.
    logic signed [INPUT_WIDTH-1:0] delay0 [0:(TAPS/2)]; 
    logic signed [INPUT_WIDTH-1:0] delay1 [0:(TAPS/2)];

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for (int i = 0; i <= TAPS/2; i++) begin
                delay0[i] <= '0;
                delay1[i] <= '0;
            end
        end else if (ValidIn) begin
            delay0[0] <= FilterIn0;
            delay1[0] <= FilterIn1;
            for (int i = 1; i <= TAPS/2; i++) begin
                delay0[i] <= delay0[i-1];
                delay1[i] <= delay1[i-1];
            end
        end
    end

    // --- 3. Multiplication (Polyphase Decomposition) ---
    logic signed [MULT_WIDTH-1:0] prod0 [0:TAPS-1];
    logic signed [MULT_WIDTH-1:0] prod1 [0:TAPS-1];

    always_ff @(posedge clk) begin
        for (int i = 0; i < TAPS; i++) begin
            automatic logic signed [INPUT_WIDTH+COEF_WIDTH-1:0] f_prod0, f_prod1;
            localparam lsb = INPUT_FRAC + COEF_FRAC - MULT_FRAC;
            localparam msb = lsb + MULT_WIDTH - 1;

            // Output 0 logic: x0*h0 + x(-1)*h1 + x(-2)*h2 ...
            // If i is even, use delay0. If i is odd, use delay1 from previous cycle.
            if (i % 2 == 0) 
                f_prod0 = delay0[i/2] * COEF_LUT[i];
            else 
                f_prod0 = delay1[i/2+1] * COEF_LUT[i]; // delay1[0] is x(-1) relative to FilterIn0

            // Output 1 logic: x1*h0 + x0*h1 + x(-1)*h2 ...
            if (i % 2 == 0)
                f_prod1 = delay1[i/2] * COEF_LUT[i];
            else
                f_prod1 = delay0[i/2] * COEF_LUT[i];

            prod0[i] <= f_prod0[msb:lsb];
            prod1[i] <= f_prod1[msb:lsb];
        end
    end

    // --- 4. Accumulation ---
    logic signed [ADD_WIDTH-1:0] sum0, sum1;
    always_comb begin
        sum0 = '0;
        sum1 = '0;
        for (int i = 0; i < TAPS; i++) begin
            sum0 = sum0 + prod0[i];
            sum1 = sum1 + prod1[i];
        end
    end

    // --- 5. Output and Valid Logic ---
    localparam SHIFT = MULT_FRAC - ADD_FRAC;
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            FilterOut0 <= '0;
            FilterOut1 <= '0;
        end else begin
            FilterOut0 <= sum0 >>> SHIFT;
            FilterOut1 <= sum1 >>> SHIFT;
        end
    end

    reg [LATENCY-1:0] v_pipe;
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) v_pipe <= '0;
        else        v_pipe <= {v_pipe[LATENCY-2:0], ValidIn};
    end
    assign ValidOut = v_pipe[LATENCY-1];

endmodule