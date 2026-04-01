`timescale 1ns/1ps

module fir_filter_paral_2_tb;
    // 1. Parameters (matching the module)
    parameter INPUT_INT  = 1;  
    parameter INPUT_FRAC = 13;
    parameter COEF_INT   = 1;
    parameter COEF_FRAC  = 15;
    parameter MULT_INT   = 1;
    parameter MULT_FRAC  = 18;
    parameter ADD_INT    = 3;
    parameter ADD_FRAC   = 18;
    
    parameter INPUT_WIDTH = INPUT_INT + INPUT_FRAC + 1;
    parameter COEF_WIDTH  = COEF_INT + COEF_FRAC + 1;
    parameter MULT_WIDTH  = MULT_INT + MULT_FRAC + 1;
    parameter ADD_WIDTH   = ADD_INT + ADD_FRAC + 1;

    // 2. Signals
    logic clk;
    logic rst_n;
    // Parallel signals
    logic signed [INPUT_WIDTH-1:0] FilterIn0, FilterIn1;
    logic signed [ADD_WIDTH-1:0]   FilterOut0, FilterOut1;
    logic ValidIn, ValidOut;

    // 3. Instantiate Unit Under Test (UUT)
    fir_filter_paral_2 #(
        .INPUT_INT(INPUT_INT), .INPUT_FRAC(INPUT_FRAC), 
        .COEF_INT(COEF_INT),   .COEF_FRAC(COEF_FRAC),
        .MULT_INT(MULT_INT),   .MULT_FRAC(MULT_FRAC), 
        .ADD_INT(ADD_INT),     .ADD_FRAC(ADD_FRAC)
    ) uut (
        .clk(clk),
        .rst_n(rst_n),
        .FilterIn0(FilterIn0),
        .FilterIn1(FilterIn1),
        .ValidIn(ValidIn),
        .FilterOut0(FilterOut0),
        .FilterOut1(FilterOut1),
        .ValidOut(ValidOut)
    );

    // 4. Clock Generation (100MHz)
    initial clk = 0;
    always #5 clk = ~clk;

    // 5. Stimulus Procedure
    integer in_file_ptr;
    integer val0, val1; // Temporary storage for two samples

    initial begin
        // Initialize
        rst_n    = 0;
        FilterIn0 = 0;
        FilterIn1 = 0;
        ValidIn   = 0;

        // Reset sequence
        #20 rst_n = 1;
        #10;
        
        // Open the input file
        // Ensure input.txt has at least two samples per line or read sequentially
        in_file_ptr = $fopen("input.txt", "r");
        if (in_file_ptr == 0) begin
            $display("Error: Could not open input file.");
            $finish;
        end
        
        // Process two samples per clock cycle
        while (!$feof(in_file_ptr)) begin
            // Read two consecutive values from the file
            // Note: If your file has one value per line, $fscanf will find the next one
            if ($fscanf(in_file_ptr, "%d\n", val0) == 1) begin
                if (!$feof(in_file_ptr)) begin
                    $fscanf(in_file_ptr, "%d\n", val1);
                end else begin
                    val1 = 0; // Pad with zero if there's an odd number of samples
                end
                
                @(posedge clk);
                FilterIn0 <= val0;
                FilterIn1 <= val1;
                ValidIn   <= 1;
            end
        end
        
        // End of data
        @(posedge clk);
        FilterIn0 <= 0; 
        FilterIn1 <= 0; 
        ValidIn   <= 0;
        
        // Allow time for the pipeline to empty
        repeat (30) @(posedge clk);

        $display("Simulation finished.");
        $fclose(in_file_ptr);
        $finish;
    end
    
    // 6. Monitor Output
    // Since we output two samples per cycle, we display both
    always @(posedge clk) begin
        if (ValidOut) begin
//            $display("Time: %0t | Out0: %d | Out1: %d", $time, FilterOut0, FilterOut1);
            $display("%d %d", FilterOut0, FilterOut1);
        end
    end

endmodule