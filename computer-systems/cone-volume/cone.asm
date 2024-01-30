default rel

section .data
  pi_approximation dd 3.1415926536  ; Approximation of π as 22/7
  divisor dd 3.0

section .text
global volume
volume:
  ;; 1/3 * 𝜋* r^2 * h cubic units
  ;; xmm0: radius
  ;; xmm1: height
  ;; xmm0: return value
  mulss xmm0, xmm0
  mulss xmm0, xmm1
  movss xmm1, [pi_approximation]
  mulss xmm0, xmm1
  movss xmm1, [divisor]
  divss xmm0, xmm1
 	ret
