`timescale 1ns / 1ps

module tb_SelectTopK ();
  parameter int WIDTH = 9;
  parameter int CLK_PERIOD = 10;

  logic clk, rst_n, BlkIn;
  logic signed [WIDTH-1:0] In1, In2, In3, In4, In5, In6, In7, In8;
  logic signed [WIDTH-1:0] SortOut;
  logic        [      1:0] OutRank;

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

  initial clk = 0;
  always #(CLK_PERIOD / 2) clk = ~clk;

  initial begin
    $fsdbDumpfile("fsdb/tb_SelectTopK.fsdb");
    $fsdbDumpvars(0, "+mda");
  end

  int file_ptr, scan_ret;
  int BlkIn_t;
  int In1_t, In2_t, In3_t, In4_t, In5_t, In6_t, In7_t, In8_t;
  initial begin
    rst_n = 0;
    BlkIn = '0;
    In1   = '0;
    In2   = '0;
    In3   = '0;
    In4   = '0;
    In5   = '0;
    In6   = '0;
    In7   = '0;
    In8   = '0;

    #(CLK_PERIOD * 2);
    rst_n = 1;
    #(CLK_PERIOD);

    file_ptr = $fopen("vectors/tb_SelectTopK_input.txt", "r");

    if (file_ptr == 0) begin
      $display("Error: Could not open input file.");
      $finish;
    end

    while (!$feof(
        file_ptr
    )) begin
      scan_ret = $fscanf(
          file_ptr,
          "%d %d %d %d %d %d %d %d %d\n",
          BlkIn_t,
          In1_t,
          In2_t,
          In3_t,
          In4_t,
          In5_t,
          In6_t,
          In7_t,
          In8_t
      );
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

    repeat (15) @(posedge clk);
    BlkIn = '0;
    In1   = '0;
    In2   = '0;
    In3   = '0;
    In4   = '0;
    In5   = '0;
    In6   = '0;
    In7   = '0;
    In8   = '0;
    $finish;
  end

endmodule
