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
    reg signed [WIDTH-1:0]  reg8_set0[0:3][0:7], reg8_set1[0:3][0:7];
    
    wire buf0_write_en;
    wire [1:0] write_cnt;
    merge_sort_fsm fsm0 (clk, rst_n, BlkIn, buf0_write_en, write_cnt);
    
    integer i;
    always @* begin
        if (buf0_write_en) begin
            for(i=0; i<8; i=i+1)  reg8_set0[write_cnt][i] = sort_out[i];
        end else begin
            for(i=0; i<8; i=i+1)  reg8_set1[write_cnt][i] = sort_out[i];
        end
    end
    
//    max_index_finder max0 ();
endmodule
