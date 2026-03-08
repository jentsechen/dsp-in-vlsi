module SelectTopK # (
    parameter WIDTH = 9
)  (
    input  clk,
    input  rst_n,
    input  BlkIn,
    input  signed [WIDTH-1:0]  In1, In2, In3, In4, In5, In6, In7, In8,
    output signed [WIDTH-1:0]  SortOut,
    output [1:0]  OutRank
    );
    wire signed [WIDTH-1:0] sort_out[7:0];
    Sort8 #(WIDTH) sort0 (clk, rst_n, In1, In2, In3, In4, In5, In6, In7, In8, sort_out[0], sort_out[1], sort_out[2], sort_out[3], sort_out[4], sort_out[5], sort_out[6], sort_out[7]);
    reg signed [WIDTH-1:0]  reg8_set0[3:0][7:0], reg8_set1[3:0][7:0];
    
    wire write_en, write_buf_index, out_rank_valid;
    wire [1:0] write_cnt;
    merge_sort_fsm fsm0 (clk, rst_n, BlkIn, write_en, write_buf_index, write_cnt, out_rank_valid);
    
    integer i, j;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            // Nested loops to clear all 4 sets of 8 registers
            for (i = 0; i < 4; i = i + 1) begin
                for (j = 0; j < 8; j = j + 1) begin
                    reg8_set0[i][j] <= 0;
                    reg8_set1[i][j] <= 0;
                end
            end
        end else begin
            // Use non-blocking assignments (<=) for sequential logic
            if (write_en) begin
                if (write_buf_index==0) begin
                    for (j = 0; j < 8; j = j + 1) begin
                        reg8_set0[write_cnt][j] <= sort_out[7-j];
                    end
                end else begin
                    for (j = 0; j < 8; j = j + 1) begin
                        reg8_set1[write_cnt][j] <= sort_out[7-j];
                    end
                end
            end else begin
                for (i = 0; i < 4; i = i + 1) begin
                    for (j = 0; j < 8; j = j + 1) begin
                        reg8_set0[i][j] <= reg8_set0[i][j];
                        reg8_set1[i][j] <= reg8_set1[i][j];
                    end
                end              
            end
        end
    end
    
    reg [2:0] ptr [3:0];
    wire [1:0] max_index;
    
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n || write_cnt==2'd3) begin
            for(i=0; i<4; i=i+1) ptr[i] <= 0;
        end else if (write_en) begin
            ptr[max_index] <= ptr[max_index] + 1;
        end else begin
            for(i=0; i<4; i=i+1) ptr[i] <= 0;
        end        
    end
    
    wire [WIDTH-1:0] merge_in_0, merge_in_1, merge_in_2, merge_in_3;
    assign merge_in_0 = (write_buf_index==0) ? reg8_set1[0][ptr[0]] : reg8_set0[0][ptr[0]]; // read buf. 0 when write buf. 1
    assign merge_in_1 = (write_buf_index==0) ? reg8_set1[1][ptr[1]] : reg8_set0[1][ptr[1]]; // read buf. 0 when write buf. 1
    assign merge_in_2 = (write_buf_index==0) ? reg8_set1[2][ptr[2]] : reg8_set0[2][ptr[2]]; // read buf. 0 when write buf. 1
    assign merge_in_3 = (write_buf_index==0) ? reg8_set1[3][ptr[3]] : reg8_set0[3][ptr[3]]; // read buf. 0 when write buf. 1
    max_index_finder #(WIDTH) max0 (merge_in_0, merge_in_1, merge_in_2, merge_in_3, max_index);
    assign SortOut = (write_buf_index==0) ? reg8_set1[max_index][ptr[max_index]] : reg8_set0[max_index][ptr[max_index]]; // read buf. 0 when write buf. 1
    assign OutRank = (out_rank_valid) ? write_cnt : 2'd0;
endmodule
