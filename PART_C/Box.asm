// Box.asm  -  K = 67
// Black box while any key is pressed, white when released.
// Start row 67, 20 rows tall, width = 16*((67 mod 4)+1) = 64 px = 4 words.
// Start address = 16384 + 32*67 = 18528

(LOOP)
  @KBD
  D=M
  @BLACK
  D;JNE
  @color
  M=0            // no key -> white
  @DRAW
  0;JMP
(BLACK)
  @color
  M=-1           // key    -> black
(DRAW)
  @18528         // 16384 + 32*K
  D=A
  @addr
  M=D            // addr = first word of current row
  @20            // rows tall
  D=A
  @rows
  M=D
(ROW)
  @4             // width in words
  D=A
  @cols
  M=D
  @addr
  D=M
  @p
  M=D            // p = pointer within this row
(COL)
  @color
  D=M
  @p
  A=M
  M=D            // RAM[p] = color
  @p
  M=M+1
  @cols
  M=M-1
  D=M
  @COL
  D;JGT
  @32
  D=A
  @addr
  M=D+M          // next row: addr += 32
  @rows
  M=M-1
  D=M
  @ROW
  D;JGT
  @LOOP
  0;JMP
