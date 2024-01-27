section .text
global binary_convert
binary_convert:
  ;  rdi contains the string
  ;  rax contains output
  ;  edx contains character
  xor rax, rax
_loop:
  cmp byte [rdi], 0              ; check for null character
  je _done
  movzx edx, byte [rdi]
  inc rdi
  shl rax, 1
  cmp edx, '1'                   ; assume only 1 and 0 are inputs
  je _increment
  jmp _loop
_increment:
  inc rax
  jmp _loop
_done:
	ret
