/* Process a PBM map file and spit out a file containing <pose> tags to embed within SDF */
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include <vector>
#include <time.h>

#include <pbmMapImage.h>
using namespace std;

#define NUM_POINTS 50

typedef struct Point
{
  int x;
  int y;
  Point(int m_x, int m_y) :
    x(m_x), y(m_y) {}
} point_t;

uint8_t free_oct(PBMMapImage &mapImage, int x, int y)
{
  //Check 8-connectedness of the free space so the user can nav around a potential obstacle
  //A 1 in the PBM represents obstacle

  uint8_t *data = mapImage.getPixelPlane();


  //Borders are out
  if (x == 0 || x == mapImage.getWidth()-1)
    return 0;
  if (y == 0 || y == mapImage.getHeight()-1)
    return 0;

  //Next to borders are out
  /*
  if (x == 1 || x == mapImage.getWidth()-2)
    return 0;
  if (y == 1 || y == mapImage.getHeight()-2)
    return 0;
  */
  
  //Check the pixel data, bounds are guaranteed to be good if we make it this far
  //Pixel proper:
  uint8_t freeDirs = 0;
  
  if (data[y*mapImage.getWidth() + x] > 0)
    return 0; //the pixel itself must be good

  // North:
  if (data[(y-1)*mapImage.getWidth() + x] == 0)
    freeDirs++;
  
  //South
  if (data[(y+1)*mapImage.getWidth() + x] == 0)
    freeDirs++;

  //West
  if (data[(y)*mapImage.getWidth() + x - 1] == 0)
    freeDirs++;

  //East
  if (data[(y)*mapImage.getWidth() + x + 1] == 0)
    freeDirs++;
  
  // Northwest:
  if (data[(y-1)*mapImage.getWidth() + x - 1] == 0)
    freeDirs++;
  
  // Northeast:
  if (data[(y-1)*mapImage.getWidth() + x + 1] == 0)
    freeDirs++;

  //Southwest
  if (data[(y+1)*mapImage.getWidth() + x - 1] == 0)
    freeDirs++;
  
  //Southeast
  if (data[(y+1)*mapImage.getWidth() + x + 1] == 0)
    freeDirs++;

  //Clear enough...
  if (freeDirs > 7)
    return 1;
  else
    return 0;
}

int main(int argc, char **argv)
{
  PBMMapImage mapImage;
  mapImage.LoadFromPBM(argv[1]);
  vector<point_t*> freePoints;
  
  uint8_t *data = mapImage.getPixelPlane(); 
  for (int j = 0; j<mapImage.getHeight(); j++)
    {
      for (int i = 0; i<mapImage.getWidth(); i++)
	{
	  if (free_oct(mapImage, i,j)) 
	    {
	      freePoints.push_back(new Point(mapImage.getWidth() - (i + 1), j)); //mirror  y and x
	    }
	}
    }

  printf("Found %d free points to choose from\n", freePoints.size());
  srand(time(NULL));
  
  FILE* outFile = fopen("locations.txt","w");
  int theIndex;
  fprintf(outFile, "x,y\n");
  for (int i=0; i<NUM_POINTS; i++)
    {
      if (freePoints.size() == 0)
	break;
      theIndex = rand() % (freePoints.size()-1);
      point_t* thePoint = freePoints[theIndex];
      freePoints.erase(freePoints.begin() + theIndex);
      fprintf(outFile, "%d,%d\n", thePoint->x, thePoint->y);
      delete thePoint;
    }
  fclose(outFile);
  
  return 0;
}
