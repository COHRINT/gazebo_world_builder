#include <pbmMapImage.h>
PBMMapImage::PBMMapImage()
{
  data = NULL;
}

PBMMapImage::~PBMMapImage()
{
  if (data)
    free(data);
}
uint32_t PBMMapImage::getHeight()
{
  return height;
}

uint32_t PBMMapImage::getWidth()
{
  return width;
}

uint8_t* PBMMapImage::getPixelPlane()
{
  return data;
}
void PBMMapImage::LoadFromPBM(const char* fileName)
{
  FILE* fin = fopen(fileName,"r");
  //First line: magic number

  char *theLine = NULL;
  size_t bufSize = 0;


  getline(&theLine, &bufSize, fin);

  if (strcmp(theLine, "P1") == 0)
    {
      printf("Bad magic number: %s\n", theLine);
      return;
    }

  //Next: width and height
  fscanf(fin, "%u %u\n", &width, &height);

  //Allocate mem
  data = (uint8_t*) malloc(width*height*sizeof(uint8_t));

  for (int i = 0; i<height; i++)
    {
      getline(&theLine, &bufSize, fin);
      for (int j = 0; j<width; j++)
	{
	  sscanf(&theLine[j*2], "%hhu", &data[i*width + j]);
	  if (data[i*width + j] > 0)
	    data[i*width + j] = 255;
	}
    }
  free(theLine);
  fclose(fin);
}
