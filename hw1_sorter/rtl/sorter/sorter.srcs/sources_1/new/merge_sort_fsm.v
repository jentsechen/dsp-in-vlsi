module merge_sort_fsm (
    input clk,
    input rst_n,
    input BlkIn,
    output buf0_write_en,
    output [1:0] write_cnt
);

    // 1. Define State Encodings (Localparams are best here)
    localparam IDLE       = 2'b00;
    localparam SortProc   = 2'b01;
    localparam WriteBuf0  = 2'b10;
    localparam WriteBuf1  = 2'b11;

    reg [1:0] current_state, next_state;

    // BLOCK 1: State Register (Sequential)
    // Updates the current state on every clock edge
    always @(posedge clk or posedge rst_n) begin
        if (!rst_n)
            current_state <= IDLE;
        else
            current_state <= next_state;
    end
    
    //
    reg [2:0] currect_sort_proc_cnt, next_sort_proc_cnt;
    always @* begin
        next_sort_proc_cnt = (current_state == SortProc) ? (currect_sort_proc_cnt + 1) : currect_sort_proc_cnt;
    end
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            currect_sort_proc_cnt <= 0;
        end else begin
            currect_sort_proc_cnt <= next_sort_proc_cnt;
        end
    end
    
    //
    reg [2:0] currect_write_cnt, next_write_cnt;
    always @* begin
        next_write_cnt = ((current_state == WriteBuf0) || (current_state == WriteBuf1)) ? (currect_write_cnt + 1) : currect_write_cnt;
    end
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            currect_write_cnt <= 0;
        end else begin
            currect_write_cnt <= next_write_cnt;
        end
    end

    // BLOCK 2: Next State Logic (Combinational)
    // Determines what the "next_state" should be based on inputs
    always @* begin
        case (current_state)
            IDLE: begin
                if (BlkIn) next_state = SortProc;
                else       next_state = IDLE;
            end
            SortProc: begin
                if (sort_proc_cnt==3'd6) next_state = WriteBuf0;
                else next_state = SortProc;
            end
            WriteBuf0: begin
                if (write_cnt==2'd3) next_state = WriteBuf1;
                else next_state = WriteBuf0;
            end
            WriteBuf1: begin
                if (write_cnt==2'd3) next_state = WriteBuf0;
                else next_state = WriteBuf1;
            end
            default: next_state = IDLE;
        endcase
    end
    
    assign buf0_write_en = (current_state == WriteBuf0);
    assign write_cnt = currect_write_cnt;

endmodule