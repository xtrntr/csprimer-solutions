int sum(int *nums, int n) {
  int total = 0;
  int incrementer = 4;
  for (int i = 0; i < n; i+= incrementer ) {
    total += nums[i];
    if (i < n) total += nums[i+1];
    if (i < n) total += nums[i+2];
    if (i < n) total += nums[i+3];
  }
  return total;
}
