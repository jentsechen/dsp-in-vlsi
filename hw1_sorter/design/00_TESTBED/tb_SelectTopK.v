`timescale 1ns / 1ps

module tb_SelectTopK ();
  parameter WIDTH = 9;
  parameter CLK_PERIOD = 10;
  reg clk, rst_n, BlkIn;
  reg signed [WIDTH-1:0] In1, In2, In3, In4, In5, In6, In7, In8;
  wire signed [WIDTH-1:0] SortOut;
  wire        [      1:0] OutRank;

  SelectTopK #(WIDTH) uut (
      .clk    (clk),
      .rst_n  (rst_n),
      .BlkIn  (BlkIn),
      .In1    (In1),
      .In2    (In2),
      .In3    (In3),
      .In4    (In4),
      .In5    (In5),
      .In6    (In6),
      .In7    (In7),
      .In8    (In8),
      .SortOut(SortOut),
      .OutRank(OutRank)
  );

  // Clock generation
  initial clk = 0;
  always #(CLK_PERIOD / 2) clk = ~clk;

  integer k;
  integer file_ptr;
  integer BlkIn_t;
  integer In1_t, In2_t, In3_t, In4_t, In5_t, In6_t, In7_t, In8_t;
  initial begin
    // Initialize
    rst_n = 0;
    In1   = 0;
    In2   = 0;
    In3   = 0;
    In4   = 0;
    In5   = 0;
    In6   = 0;
    In7   = 0;
    In8   = 0;
    BlkIn = 0;

    #(CLK_PERIOD * 2);
    rst_n = 1;
    #(CLK_PERIOD);

    file_ptr = $fopen("input.txt", "r");

    if (file_ptr == 0) begin
      $display("Error: Could not open input file.");
      $finish;
    end

    while (!$feof(
        file_ptr
    )) begin
      $fscanf(file_ptr, "%d %d %d %d %d %d %d %d %d\n", BlkIn_t, In1_t, In2_t, In3_t, In4_t, In5_t,
              In6_t, In7_t, In8_t);
      @(posedge clk);
      BlkIn <= BlkIn_t;
      In1   <= In1_t;
      In2   <= In2_t;
      In3   <= In3_t;
      In4   <= In4_t;
      In5   <= In5_t;
      In6   <= In6_t;
      In7   <= In7_t;
      In8   <= In8_t;
    end

    $fclose(file_ptr);

    @(posedge clk);
    BlkIn <= 0;
    In1   <= 0;
    In2   <= 0;
    In3   <= 0;
    In4   <= 0;
    In5   <= 0;
    In6   <= 0;
    In7   <= 0;
    In8   <= 0;
    //        repeat (12) @(posedge clk);
  end

endmodule
