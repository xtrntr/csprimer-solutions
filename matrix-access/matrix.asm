section .text
global index
index:
	; rdi: matrix
	; esi: rows
	; edx: cols
	; ecx: rindex
	; r8d: cindex
  ; calculate how many +4 bytes you need to move base on the rindex and cindex
  ; store this value (rindex/ecx * cols/edx * 4 + cindex * 4) in eax
  ; add matrix/rdi, eax
  ; mov rax, matrix/rdi

  imul ecx, edx                 ; rindex * cols
  add ecx, r8d                  ; (rindex * cols) + cindex
  shl rcx, 2                    ; mutiply by 4
  add rcx, rdi                  ; add the offset to rdi
  mov rax, [rcx]                ; dereference address
	ret
