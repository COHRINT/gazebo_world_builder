#ifndef _MAPIMAGE_H_
#define _MAPIMAGE_H_
#include <stdint.h>

class MapImage
{
 public:
  virtual uint8_t *getPixelPlane() = 0;
  virtual uint32_t getHeight() = 0;
  virtual uint32_t getWidth() = 0;
};

#endif
