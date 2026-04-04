module merge_sort_fsm (
    input  logic       clk,
    input  logic       rst_n,
    input  logic       BlkIn,
    output logic       write_en,
    output logic       write_buf_index,
    output logic [1:0] write_cnt,
    output logic       out_valid
);

  typedef enum logic [1:0] {
    IDLE      = 2'b00,
    SortProc  = 2'b01,
    WriteBuf0 = 2'b10,
    WriteBuf1 = 2'b11
  } state_t;

  state_t      current_state, next_state;
  logic [2:0]  sort_proc_cnt;
  logic [1:0]  internal_write_cnt;
  logic [3:0]  blk_cnt;
  logic        first_trans_flag;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) current_state <= IDLE;
    else current_state <= next_state;
  end

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) sort_proc_cnt <= 3'd0;
    else if (current_state == SortProc) sort_proc_cnt <= sort_proc_cnt + 1'b1;
    else sort_proc_cnt <= 3'd0;
  end

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) internal_write_cnt <= 2'd0;
    else if (current_state == WriteBuf0 || current_state == WriteBuf1)
      internal_write_cnt <= internal_write_cnt + 1'b1;
    else internal_write_cnt <= 2'd0;
  end

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) blk_cnt <= 4'd1;
    else if (next_state == IDLE) blk_cnt <= 4'd1;
    else if (BlkIn) blk_cnt <= blk_cnt + 1;
    else if (current_state == WriteBuf0 && next_state == WriteBuf1) blk_cnt <= blk_cnt - 1;
    else if (current_state == WriteBuf1 && next_state == WriteBuf0) blk_cnt <= blk_cnt - 1;
  end

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) first_trans_flag <= '0;
    else if (current_state == SortProc && next_state == WriteBuf0)
      first_trans_flag <= first_trans_flag + 1;
    else if (current_state == WriteBuf0 && next_state == WriteBuf1 && first_trans_flag == 1)
      first_trans_flag <= first_trans_flag - 1;
  end

  always_comb begin
    case (current_state)
      IDLE:     next_state = BlkIn ? SortProc : IDLE;
      SortProc: next_state = (sort_proc_cnt == 3'd4) ? WriteBuf0 : SortProc;
      WriteBuf0: begin
        if (blk_cnt == 0) next_state = IDLE;
        else if (internal_write_cnt == 2'd3) next_state = WriteBuf1;
        else next_state = WriteBuf0;
      end
      WriteBuf1: begin
        if (blk_cnt == 0) next_state = IDLE;
        else if (internal_write_cnt == 2'd3) next_state = WriteBuf0;
        else next_state = WriteBuf1;
      end
      default: next_state = IDLE;
    endcase
  end

  assign write_en        = (current_state == WriteBuf0 || current_state == WriteBuf1);
  assign write_buf_index = (current_state == WriteBuf0) ? 1'b0 : 1'b1;
  assign write_cnt       = internal_write_cnt;
  assign out_valid       = write_en && first_trans_flag == 0 && blk_cnt > 0;

endmodule