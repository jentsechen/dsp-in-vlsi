`timescale 1ns/1ps

module tb_poly2_interpolator;

    localparam int N_IN     = 12;  // input samples (lines in interp_input.txt)
    localparam int N_OUT    = 80;  // golden outputs = (N_IN-2) * 8
    localparam int CLK_HALF = 5;   // 10 ns clock period

    logic        clk, rst_n;
    logic        in_valid;
    logic [15:0] in_re, in_im;
    logic        out_valid;
    logic [15:0] out_re, out_im;

    logic [15:0] mem_in_re  [0:N_IN-1];
    logic [15:0] mem_in_im  [0:N_IN-1];
    logic [15:0] mem_g_re   [0:N_OUT-1];
    logic [15:0] mem_g_im   [0:N_OUT-1];

    poly2_interpolator dut (
        .clk      (clk),
        .rst_n    (rst_n),
        .in_valid (in_valid),
        .in_re    (in_re),
        .in_im    (in_im),
        .out_valid(out_valid),
        .out_re   (out_re),
        .out_im   (out_im)
    );

    // --- clock ---
    initial clk = 0;
    always #CLK_HALF clk = ~clk;

    // --- load vectors ---
    // interp_input.txt has two hex values per line: re im
    logic [31:0] raw_input [0:N_IN-1];

    initial begin
        $readmemh("vectors/interp_input.txt",    raw_input);
        $readmemh("vectors/interp_golden_y_re.txt", mem_g_re);
        $readmemh("vectors/interp_golden_y_im.txt", mem_g_im);
        for (int i = 0; i < N_IN; i++) begin
            mem_in_re[i] = raw_input[i][31:16];
            mem_in_im[i] = raw_input[i][15:0];
        end
    end

    // --- drive inputs ---
    int out_idx;

    initial begin
        rst_n    = 0;
        in_valid = 0;
        in_re    = '0;
        in_im    = '0;
        out_idx  = 0;

        @(posedge clk); #1;
        @(posedge clk); #1;
        rst_n = 1;

        for (int i = 0; i < N_IN; i++) begin
            in_re    = mem_in_re[i];
            in_im    = mem_in_im[i];
            in_valid = 1;
            @(posedge clk); #1;
            in_valid = 0;
            // hold input stable for remaining 7 cycles of the group
            repeat (7) @(posedge clk); #1;
        end

        // wait for last outputs to flush
        repeat (4) @(posedge clk);
        $finish;
    end

    // --- check outputs ---
    int pass_cnt, fail_cnt;

    initial begin
        pass_cnt = 0;
        fail_cnt = 0;

        $display("================================================================");
        $display("  POLY2 INTERPOLATOR TESTBENCH  (%0d outputs)", N_OUT);
        $display("================================================================");
        $display("  #    out_re  out_im  g_re    g_im    result");
        $display("----------------------------------------------------------------");
    end

    always @(posedge clk) begin
        if (out_valid && out_idx < N_OUT) begin
            if (out_re === mem_g_re[out_idx] && out_im === mem_g_im[out_idx]) begin
                pass_cnt++;
                $display("  %3d  %h  %h  %h  %h  PASS",
                         out_idx, out_re, out_im, mem_g_re[out_idx], mem_g_im[out_idx]);
            end else begin
                fail_cnt++;
                $display("  %3d  %h  %h  %h  %h  FAIL <<<",
                         out_idx, out_re, out_im, mem_g_re[out_idx], mem_g_im[out_idx]);
            end
            out_idx++;

            if (out_idx == N_OUT) begin
                $display("================================================================");
                if (fail_cnt == 0)
                    $display("  ALL %0d TESTS PASSED", N_OUT);
                else begin
                    $display("  PASSED: %0d / %0d", pass_cnt, N_OUT);
                    $display("  FAILED: %0d / %0d", fail_cnt, N_OUT);
                end
                $display("================================================================");
            end
        end
    end

endmodule