section .text
global fib
fib:
  ;; rax = return value
  ;; rdi = n
  xor rax, rax
_iter:
  cmp rdi, 0
  jle _done

  cmp rdi, 1
  je _add

  dec rdi
  push rdi                      ; we push here because we want to save the decremented value (n - 1)
  call _iter

  pop rdi                       ; we pop here because this is the point where we want to use decremented value
  dec rdi
  call _iter
_done:
  ret
_add:
  add rax, 1
  ret
