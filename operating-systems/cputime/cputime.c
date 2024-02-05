#define _GNU_SOURCE
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <stdio.h>
#include <unistd.h>
#include <sched.h>

#define SLEEP_SEC 3
#define NUM_MULS 100000000
#define NUM_MALLOCS 100000
#define MALLOC_SIZE 1000

// TODO define this struct
struct profile_times {
  pid_t pid;
  int cpu_num;
  clock_t processor_start;
  struct timespec real_start;
};

// TODO populate the given struct with starting information
void profile_start(struct profile_times *t) {
  t->pid = getpid();
  t->cpu_num = sched_getcpu();
  t->processor_start = clock();
  clock_gettime(CLOCK_REALTIME, &t->real_start);
}

// TODO given starting information, compute and log differences to now
void profile_log(struct profile_times *t) {
  struct timespec end;
  double elapsed;
  clock_gettime(CLOCK_REALTIME, &end);
  elapsed = end.tv_sec - t->real_start.tv_sec;
  elapsed += (end.tv_nsec - t->real_start.tv_nsec) / 1000000000.0;
  printf("[PID %d, CPU %d]: Processor time: %.2f, Real time: %.2f\n",
         t->pid,
         t->cpu_num,
         ((double) clock() - t->processor_start) / CLOCKS_PER_SEC,
         elapsed);
}

int main(int argc, char *argv[]) {
  struct profile_times t;

  // TODO profile doing a bunch of floating point muls
  float x = 1.0;
  profile_start(&t);
  printf("Float operation section\n");
  for (int i = 0; i < NUM_MULS; i++)
    x *= 1.1;
  profile_log(&t);

  // TODO profile doing a bunch of mallocs
  profile_start(&t);
  printf("Malloc section\n");
  void *p;
  for (int i = 0; i < NUM_MALLOCS; i++)
    p = malloc(MALLOC_SIZE);
  profile_log(&t);

  // TODO profile sleeping
  profile_start(&t);
  printf("Sleep section\n");
  sleep(SLEEP_SEC);
  profile_log(&t);
}
