section .text
global pangram
pangram:
	; rdi: source string
  ; rax: to return a boolean, 1 for true and 0 for false
  ; edx: contain the char for each iteration
  ; ecx: bitset
  ;
  xor ecx, ecx
  xor rax, rax
_loop:
  cmp byte [rdi], 0             ; check for null character
  je _done
  movzx edx, byte [rdi]         ; read character into edx, zero extend
  inc rdi                       ; move to next character
  cmp edx, 64                   ; continue from start of loop if character is smaller than '@'
  jl _loop
  bts ecx, edx                  ; bit and set
  jmp _loop
_done:
  cmp ecx, 0x07fffffe           ; compare bitset with 0x07fffffe
  sete al                       ; set EAX to 1 if equal, 0 otherwise
  ret
