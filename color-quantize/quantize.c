#define RED0 0x00
#define RED1 0x20
#define RED2 0x40
#define RED3 0x60
#define RED4 0x80
#define RED5 0xa0
#define RED6 0xc0
#define RED7 0xe0
#define GREEN0 0x00
#define GREEN1 0x04
#define GREEN2 0x08
#define GREEN3 0x0c
#define GREEN4 0x10
#define GREEN5 0x14
#define GREEN6 0x18
#define GREEN7 0x1c
#define BLUE0 0x00
#define BLUE1 0x01
#define BLUE2 0x02
#define BLUE3 0x03

/*

Problem: branch prediction rates are poor because:
1) 16 possible branches
2) images can be unpredictable - you might get a smooth gradient (e.g. picture of sea), or you could get a picture of random mishmashed colors

Use a lookup table so instead of branch prediction, we load an array lookup instead.

 */


unsigned char RED_LOOKUP[] = {RED0, RED1, RED2, RED3, RED4, RED5, RED6, RED7};
unsigned char GREEN_LOOKUP[] = {GREEN0, GREEN1, GREEN2, GREEN3, GREEN4, GREEN5, GREEN6, GREEN7};
unsigned char BLUE_LOOKUP[] = {BLUE0, BLUE1, BLUE2, BLUE3};

unsigned char quantize(unsigned char red, unsigned char green, unsigned char blue) {
  unsigned char out = 0;
  out += RED_LOOKUP[red / 0x20];   // Assuming red, green, blue values are always < 0x100
  out += GREEN_LOOKUP[green / 0x20];
  out += BLUE_LOOKUP[blue / 0x40];

  return out;
}
