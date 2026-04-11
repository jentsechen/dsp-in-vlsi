`timescale 1ns/1ps

module tb_bf16_adder;

    localparam int N = 134;  // must match number of lines in vectors/

    logic [15:0] a, b, out;
    logic [15:0] mem_a [0:N-1];
    logic [15:0] mem_b [0:N-1];
    logic [15:0] mem_g [0:N-1];

    bf16_adder dut (
        .a   (a),
        .b   (b),
        .out (out)
    );

    int pass_cnt, fail_cnt;

    initial begin
        $readmemh("vectors/adder_in_a.txt",   mem_a);
        $readmemh("vectors/adder_in_b.txt",   mem_b);
        $readmemh("vectors/adder_golden.txt", mem_g);

        pass_cnt = 0;
        fail_cnt = 0;

        $display("================================================================");
        $display("  BF16 ADDER TESTBENCH  (%0d cases)", N);
        $display("================================================================");
        $display("  #    a       b       out     exp     result");
        $display("----------------------------------------------------------------");

        for (int i = 0; i < N; i++) begin
            a = mem_a[i];
            b = mem_b[i];
            #1;

            if (out === mem_g[i]) begin
                pass_cnt++;
                $display("  %3d  %h  %h  %h  %h  PASS",
                         i, a, b, out, mem_g[i]);
            end else begin
                fail_cnt++;
                $display("  %3d  %h  %h  %h  %h  FAIL <<<",
                         i, a, b, out, mem_g[i]);
                assert (out === mem_g[i])
                    else $error("mismatch at case %0d: a=%h b=%h got=%h exp=%h",
                                i, a, b, out, mem_g[i]);
            end
        end

        $display("================================================================");
        if (fail_cnt == 0) begin
            $display("  ALL %0d TESTS PASSED", N);
        end else begin
            $display("  PASSED: %0d / %0d", pass_cnt, N);
            $display("  FAILED: %0d / %0d", fail_cnt, N);
        end
        $display("================================================================");

        $finish;
    end

endmodule