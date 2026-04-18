`timescale 1ns / 1ps

`define SYN_SDF_FILE "../02_SYN/Netlist/SelectTopK_syn.sdf"

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
    `ifdef RTL
      $fsdbDumpfile("fsdb/tb_SelectTopK.fsdb");
      $fsdbDumpvars(0, "+mda");
    `endif
    `ifdef GATE
      $sdf_annotate(`SYN_SDF_FILE, uut);
      $fsdbDumpfile("fsdb/tb_SelectTopK.fsdb");
      $fsdbDumpvars(0, "+mda");
    `endif
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

  int                      gold_ptr, gold_scan;
  int                      gold_val             [4];
  int                      pass_cnt, fail_cnt;
  logic signed [WIDTH-1:0] captured             [4];
  logic signed [WIDTH-1:0] SortOut_d;
  logic        [      1:0] OutRank_d;

  initial begin
    gold_ptr = $fopen("vectors/tb_SelectTopK_golden.txt", "r");
    if (gold_ptr == 0) begin
      $display("[CHECKER] Error: Cannot open golden file.");
      $finish;
    end

    pass_cnt  = 0;
    fail_cnt  = 0;
    SortOut_d = '0;
    OutRank_d = '0;

    @(posedge rst_n);

    forever begin
      @(posedge clk);
      #1;

      if (OutRank == 2'd1 && OutRank_d == 2'd0) begin
        captured[0] = SortOut_d;
        captured[1] = SortOut;
      end else if (OutRank == 2'd2 && OutRank_d == 2'd1) begin
        captured[2] = SortOut;
      end else if (OutRank == 2'd3 && OutRank_d == 2'd2) begin
        captured[3] = SortOut;
        gold_scan = $fscanf(gold_ptr, "%d %d %d %d\n",
                            gold_val[0], gold_val[1], gold_val[2], gold_val[3]);
        if (captured[0] === gold_val[0] && captured[1] === gold_val[1] &&
            captured[2] === gold_val[2] && captured[3] === gold_val[3]) begin
          $display("[CHECKER] Block %0d PASS  got: %4d %4d %4d %4d",
                   pass_cnt + fail_cnt,
                   captured[0], captured[1], captured[2], captured[3]);
          pass_cnt++;
        end else begin
          $display("[CHECKER] Block %0d FAIL  got: %4d %4d %4d %4d  exp: %4d %4d %4d %4d",
                   pass_cnt + fail_cnt,
                   captured[0], captured[1], captured[2], captured[3],
                   gold_val[0], gold_val[1], gold_val[2], gold_val[3]);
          fail_cnt++;
        end
      end

      SortOut_d = SortOut;
      OutRank_d = OutRank;
    end
  end

  final begin
    $display("[CHECKER] ----------------------------------------");
    if (fail_cnt == 0)
      $display("[CHECKER] All %0d blocks PASSED.", pass_cnt);
    else
      $display("[CHECKER] %0d / %0d blocks FAILED.", fail_cnt, pass_cnt + fail_cnt);
    $display("[CHECKER] ----------------------------------------");
  end

endmodule
