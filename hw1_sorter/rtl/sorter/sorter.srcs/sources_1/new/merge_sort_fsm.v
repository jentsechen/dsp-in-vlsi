module merge_sort_fsm (
    input clk,
    input rst_n,
    input BlkIn,
    output write_en,
    output write_buf_index,
    output [1:0] write_cnt,
    output out_valid
);

    localparam IDLE      = 2'b00;
    localparam SortProc  = 2'b01;
    localparam WriteBuf0 = 2'b10;
    localparam WriteBuf1 = 2'b11;

    reg [1:0] current_state, next_state;
    reg [2:0] sort_proc_cnt;
    reg [1:0] internal_write_cnt;
    reg [3:0] blk_cnt; // Maximum of 16 blocks are supported
    reg first_trans_flag;

    // BLOCK 1: State Register
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            current_state <= IDLE;
        else
            current_state <= next_state;
    end

    // Counter Logic: Sort Process
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            sort_proc_cnt <= 3'd0;
        end else if (current_state == SortProc) begin
            sort_proc_cnt <= sort_proc_cnt + 1'b1;
        end else begin
            sort_proc_cnt <= 3'd0; // Reset counter when not in SortProc
        end
    end

    // Counter Logic: Write Counter
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            internal_write_cnt <= 2'd0;
        end else if (current_state == WriteBuf0 || current_state == WriteBuf1) begin
            internal_write_cnt <= internal_write_cnt + 1'b1;
        end else begin
            internal_write_cnt <= 2'd0; // Reset counter when not writing
        end
    end
    
    // Counter Logic: Block Counter
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n || next_state == IDLE) begin
            blk_cnt <= 4'd1;
        end else if (BlkIn) begin
            blk_cnt <= blk_cnt + 1;
        end else if (current_state == WriteBuf0 && next_state == WriteBuf1) begin
            blk_cnt <= blk_cnt - 1;
        end else if (current_state == WriteBuf1 && next_state == WriteBuf0) begin
            blk_cnt <= blk_cnt - 1;
        end else begin
            blk_cnt <= blk_cnt;
        end
    end
    
    // Counter Logic: First Transition Flag
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            first_trans_flag <= 0;
        end else if (current_state == SortProc && next_state == WriteBuf0) begin
            first_trans_flag <= first_trans_flag + 1;
        end else if (current_state == WriteBuf0 && next_state == WriteBuf1 && first_trans_flag==1) begin
            first_trans_flag <= first_trans_flag - 1;
        end else begin
            first_trans_flag <= first_trans_flag;
        end
    end

    // BLOCK 2: Next State Logic
    always @* begin
        case (current_state)
            IDLE: begin
                if (BlkIn) next_state = SortProc;
                else       next_state = IDLE;
            end
            SortProc: begin
                // Check against the actual register name
                if (sort_proc_cnt == 3'd4) next_state = WriteBuf0;
                else                       next_state = SortProc;
            end
            WriteBuf0: begin
                if (blk_cnt == 0)                    next_state = IDLE;
                else if (internal_write_cnt == 2'd3) next_state = WriteBuf1;
                else                                 next_state = WriteBuf0;
            end
            WriteBuf1: begin
                if (blk_cnt == 0)                    next_state = IDLE;
                else if (internal_write_cnt == 2'd3) next_state = WriteBuf0;
                else                                 next_state = WriteBuf1;
            end
            default: next_state = IDLE;
        endcase
    end

    // Assignments
    assign write_en = (current_state == WriteBuf0 || current_state == WriteBuf1);
    assign write_buf_index = (current_state == WriteBuf0) ? 0 : 1;
    assign write_cnt     = internal_write_cnt;
    assign out_valid = (current_state == WriteBuf0 || current_state == WriteBuf1) && first_trans_flag==0 && blk_cnt>0;
endmodule