`timescale 1ns/1ps

module fir_filter_tb;
    parameter INPUT_INT  = 1;  
    parameter INPUT_FRAC = 13;
    parameter COEF_INT   = 1;
    parameter COEF_FRAC  = 15;
    parameter MULT_INT    = 1;
    parameter MULT_FRAC   = 18;
    parameter ADD_INT    = 3;
    parameter ADD_FRAC   = 18;
    
    parameter INPUT_WIDTH = INPUT_INT + INPUT_FRAC + 1;
    parameter COEF_WIDTH  = COEF_INT + COEF_FRAC + 1;
    parameter MULT_WIDTH   = MULT_INT + MULT_FRAC + 1;
    parameter ADD_WIDTH  = ADD_INT + ADD_FRAC + 1;
    // 2. Signals
    logic clk;
    logic rst_n;
    logic signed [INPUT_WIDTH-1:0]   FilterIn;
    logic signed [ADD_WIDTH-1:0]  FilterOut;
    logic ValidIn, ValidOut;

    // 3. Instantiate Unit Under Test (UUT)
    fir_filter #(
    .INPUT_INT(INPUT_INT), .INPUT_FRAC(INPUT_FRAC), .COEF_INT(COEF_INT), .COEF_FRAC(COEF_FRAC),
    .MULT_INT(MULT_INT), .MULT_FRAC(MULT_FRAC), .ADD_INT(ADD_INT), .ADD_FRAC(ADD_FRAC)
    ) uut (
        .clk(clk),
        .rst_n(rst_n),
        .FilterIn(FilterIn),
        .ValidIn(ValidIn),
        .FilterOut(FilterOut),
        .ValidOut(ValidOut)
    );

    // 4. Clock Generation (100MHz)
    initial clk = 0;
    always #5 clk = ~clk;

    // 5. Stimulus Procedure
    integer in_file_ptr, FilterIn_t;
    initial begin
        // Initialize
        rst_n   = 0;
        FilterIn = 0;
        ValidIn = 0;

        // Reset sequence
        #20 rst_n = 1;
        #10;
        
        in_file_ptr = $fopen("input.txt", "r");
        if (in_file_ptr == 0) begin
            $display("Error: Could not open input file.");
            $finish;
        end
        
        while (!$feof(in_file_ptr)) begin
            $fscanf(in_file_ptr, "%d\n", FilterIn_t);
            @(posedge clk);
            FilterIn <= FilterIn_t;
            ValidIn <= 1;
        end
        
        @(posedge clk);
        FilterIn <= 0; ValidIn <= 0;
        repeat (30) @(posedge clk);

//        $finish;
    end
    
//    integer out_file_ptr;
//    initial begin
//        out_file_ptr = $fopen("output.txt", "r");
//        if (out_file_ptr == 0) begin
//            $display("Error: Could not open output file.");
//            $finish;
//        end
//    end
    
//    always @(posedge clk) begin
//        if (ValidOut && out_file_ptr != 0) begin
//            $fdisplay(out_file_ptr, "%d\n", FilterOut);
//        end
//    end
    
    always @(posedge clk) begin
        if (ValidOut) begin
            $display("%d", FilterOut);
        end
    end

endmodule