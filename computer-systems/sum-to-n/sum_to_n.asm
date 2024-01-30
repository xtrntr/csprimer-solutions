;   Which register contains the argument (n)? RDI
;   In which register will the return value be placed? rax
;   What instruction is used to do the addition? add
;   What instruction(s) can be used to construct the loop? 

section .text
global sum_to_n
sum_to_n:
  xor rax, rax                  ; rax is return value 
  mov rcx, 1                    ; rcx is used to store the counter. when rcx is less than rdi/n, increment rax by rcx and increment rcx by 1
  cmp rdi, 0                    ; will fail for negative numbers ;_;
  jle done
loop:
  add rax, rcx                  ; increment rax by rcx
  inc rcx                       ; increment rcx by 1
  cmp rcx, rdi                  ; check if rcx/counter is smaller than rdi/n
  jle loop                      ; jump to add if rcx is smaller than rdi/n
done:
	ret
  
