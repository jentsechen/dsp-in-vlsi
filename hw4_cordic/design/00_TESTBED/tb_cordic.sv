`timescale 1ns/1ps

module tb_cordic;

    localparam int N          = 10;
    localparam int XY_FRAC    = 12;
    localparam int THETA_FRAC = 10;
    localparam int PAT_NUM    = 4;

    localparam int XY_W    = XY_FRAC + 2;    // 14
    localparam int THETA_W = THETA_FRAC + 3; // 13
    localparam int TIMEOUT = 200;

    logic                        clk, rst_n;
    logic                        in_valid;
    logic signed [XY_W-1:0]     x_in, y_in;
    logic                        out_valid;
    logic signed [THETA_W-1:0]  phase_out;

    cordic #(
        .N(N),
        .XY_FRAC(XY_FRAC),
        .THETA_FRAC(THETA_FRAC)
    ) dut (
        .clk      (clk),
        .rst_n    (rst_n),
        .in_valid (in_valid),
        .x_in     (x_in),
        .y_in     (y_in),
        .out_valid(out_valid),
        .phase_out(phase_out)
    );

    initial clk = 0;
    always #5 clk = ~clk;

    logic [XY_W-1:0]    pat_x      [0:PAT_NUM-1];
    logic [XY_W-1:0]    pat_y      [0:PAT_NUM-1];
    logic [THETA_W-1:0] pat_golden [0:PAT_NUM-1];

    integer pass_cnt, fail_cnt, wait_cnt;

    initial begin
        $readmemh("./vectors/x_in.txt",         pat_x);
        $readmemh("./vectors/y_in.txt",         pat_y);
        $readmemh("./vectors/theta_golden.txt", pat_golden);

        rst_n    = 0;
        in_valid = 0;
        x_in     = '0;
        y_in     = '0;
        repeat (2) @(negedge clk);
        rst_n = 1;
        @(negedge clk);

        pass_cnt = 0;
        fail_cnt = 0;

        for (int i = 0; i < PAT_NUM; i++) begin
            @(negedge clk);
            in_valid = 1;
            x_in     = pat_x[i];
            y_in     = pat_y[i];
            @(negedge clk);
            in_valid = 0;
            x_in     = '0;
            y_in     = '0;

            wait_cnt = 0;
            while (!out_valid) begin
                @(negedge clk);
                wait_cnt++;
                if (wait_cnt > TIMEOUT) begin
                    $display("TIMEOUT waiting for out_valid on pattern %0d", i);
                    $finish;
                end
            end

            if (phase_out === $signed(pat_golden[i])) begin
                $display("PASS [%0d]  x=%0d  y=%0d  phase_out=%0d  golden=%0d",
                    i, $signed(pat_x[i]), $signed(pat_y[i]),
                    $signed(phase_out), $signed(pat_golden[i]));
                pass_cnt++;
            end else begin
                $display("FAIL [%0d]  x=%0d  y=%0d  phase_out=%0d  golden=%0d",
                    i, $signed(pat_x[i]), $signed(pat_y[i]),
                    $signed(phase_out), $signed(pat_golden[i]));
                fail_cnt++;
            end
        end

        $display("-----------------------------");
        if (fail_cnt == 0)
            $display("ALL PASS  (%0d/%0d)", pass_cnt, PAT_NUM);
        else
            $display("RESULT: %0d PASS  %0d FAIL  (total %0d)", pass_cnt, fail_cnt, PAT_NUM);
        $finish;
    end

endmodule
