#ifndef _PBM_MAPIMAGE_H_
#define _PBM_MAPIMAGE_H_


#include <stdint.h>


#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

class PBMMapImage
{
 public:
  PBMMapImage();
  ~PBMMapImage();
  void LoadFromPBM(const char* fileName);
  uint8_t *getPixelPlane();
  uint32_t getHeight();
  uint32_t getWidth();
   
 private:
  uint32_t width;
  uint32_t height;
  uint8_t *data;
  
};

#endif
