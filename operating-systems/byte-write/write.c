#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
  FILE *file;
  unsigned char random_byte;
  struct stat filestat;
  char *filename = "tmp";

  file = fopen(filename, "wb");
  if (file == NULL) {
    perror("Error opening file");
    return 1;
  }

  long long size;
  long long blocks;


  printf("IO Block: %ld bytes\n", (long) filestat.st_blksize);
  printf("Device: %lxh/%ldd\n", (long) filestat.st_dev, (long) filestat.st_dev);
  printf("Inode: %ld\n", (long) filestat.st_ino);
  printf("Links: %ld\n", (long) filestat.st_nlink);
  printf("Access: %o\n", filestat.st_mode);
  printf("UID: %d   GID: %d\n", filestat.st_uid, filestat.st_gid);
  printf("--------------------\n\n");

  for (int i = 0; i < 32000; i++) {
    random_byte = (unsigned char)rand();
    if (fwrite(&random_byte, sizeof(random_byte), 1, file) == 1) {
      if (stat(filename, &filestat)) {
        perror("Error calling stat on file");
        return 1;
      }

      if (size != filestat.st_size) {
        printf("Size changed from: %lld bytes to %lld bytes when writing byte #%d\n", blocks, (long long) filestat.st_size, i);
      }
      size = filestat.st_size;

      if (blocks != filestat.st_blocks) {
        printf("Allocated blocks changed from: %lld to %lld when writing byte #%d\n", blocks, (long long) filestat.st_blocks, i);
      }
      blocks = filestat.st_blocks;
    }
  }

  fclose(file);
}
