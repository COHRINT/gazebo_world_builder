/* Extrude a world from an 8-bit PNG */

//LibPNG example code: http://zarb.org/~gc/html/libpng.html
//
/* 
   Goal:
   Read a PNG file
   Create a SDF model files corresponding to the PNG image, with a few parameters
   SDF model consists of a wall segment that is a square, located at each pixel
   Pose is relative to the top-left of the image, in vision frame

*/

#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>

#include <pbmMapImage.h>
#include <quadTree.h>






//////////////////////////////////////////////////
//void MapShape::CreateBoxes(QuadNode * /*_node*/)
//{
  /*TODO: fix this to use SDF
  if (node->leaf)
  {
    if (!node->valid || !node->occupied)
      return;

    std::ostringstream stream;

    // Create the box geometry
    CollisionPtr collision = this->GetWorld()->GetPhysicsEngine()->CreateCollision("box", this->collisionParent->GetLink());
    collision->SetSaveable(false);

    stream << "<gazebo:world xmlns:gazebo =\"http://playerstage.sourceforge.net/gazebo/xmlschema/#gz\" xmlns:collision =\"http://playerstage.sourceforge.net/gazebo/xmlschema/#collision\">";

    float x = (node->x + node->width / 2.0) * this->sdf->Get<double>("scale");
    float y = (node->y + node->height / 2.0) * this->sdf->Get<double>("scale");
    float z = this->sdf->Get<double>("height") / 2.0;
    float xSize = (node->width) * this->sdf->Get<double>("scale");
    float ySize = (node->height) * this->sdf->Get<double>("scale");
    float zSize = this->sdf->Get<double>("height");

    char collisionName[256];
    sprintf(collisionName, "map_collision_%d", collisionCounter++);

    stream << "<collision:box name ='" << collisionName << "'>";
    stream << "  <xyz>" << x << " " << y << " " << z << "</xyz>";
    stream << "  <rpy>0 0 0</rpy>";
    stream << "  <size>" << xSize << " " << ySize << " " << zSize << "</size>";
    stream << "  <static>true</static>";
    stream << "  <visual>";
    stream << "    <mesh>unit_box</mesh>";
    stream << "    <material>" << this->materialP->GetValue() << "</material>";
    stream << "    <size>" << xSize << " "<< ySize << " " << zSize << "</size>";
    stream << "  </visual>";
    stream << "</collision:box>";
    stream << "</gazebo:world>";

    boxConfig->LoadString(stream.str());

    collision->SetStatic(true);
    collision->Load(boxConfig->GetRootNode()->GetChild());

    delete boxConfig;
  }
  else
  {
    std::deque<QuadNode*>::iterator iter;
    for (iter = node->children.begin(); iter != node->children.end(); iter++)
    {
      this->CreateBoxes(*iter);
    }
  }
  */

//////////////////////////////////////////////////


void renderOnePixel(FILE* outFile, float height, uint16_t x, uint16_t y, float scale)
{
  // Write a new Link XML item to the FILE* that represents a 1px by 1px wall
  char baseName[16];
  sprintf(baseName, "Wall_%d_%d", x,y);

  fprintf(outFile, "<collision name='%s_Collision'>\n\t<geometry>\n\t<box>\n", baseName);
  fprintf(outFile, " <size>%f %f %f</size>\n", scale, scale, height);
  fprintf(outFile," </box>\n</geometry>\n<pose frame=''>%f %f 0 0 0 0</pose>\n", x*scale, y*scale);
  fprintf(outFile, "</collision>\n\t<visual name='%s_Visual'>\n<pose frame=''>%f %f 0 0 0 0</pose>\n", baseName, x*scale, y*scale);
  fprintf(outFile, "\t<geometry>\n<box>\n<size>%f %f %f</size>\n", scale, scale, height);
  fprintf(outFile, "</box>\n</geometry>\n<material>\n<script>\n<uri>file://media/materials/scripts/gazebo.material</uri>\n");
  fprintf(outFile,"<name>Gazebo/Grey</name>\n</script>\n<ambient>1 1 1 1</ambient>\n</material>\n");
  fprintf(outFile,"</visual>\n<pose frame=''>%f %f 0 0 -0 0</pose>\n", x*scale, y*scale);
}




void CreateBoxes(QuadNode *node, FILE* outFile, float height, float scale)
{
  if (node->leaf)
  {
    if (!node->valid || !node->occupied)
      return;

    // Create the box geometry
    float x = (node->x + node->width / 2.0) * scale;
    float y = (node->y + node->height / 2.0) * scale;
    float z = height / 2.0;
    float xSize = (node->width) * scale;
    float ySize = (node->height) * scale;
    float zSize = height;
    char baseName[16];
    
    sprintf(baseName, "Wall_%1.1f_%1.1f", x,y);

    fprintf(outFile, "<collision name='%s_Collision'>\n\t<geometry>\n\t<box>\n", baseName);
    fprintf(outFile, " <size>%f %f %f</size>\n", xSize, ySize, zSize);
    fprintf(outFile," </box>\n</geometry>\n<pose frame=''>%f %f %f 0 0 0</pose>\n", x,y,z);
    fprintf(outFile, "</collision>\n\t<visual name='%s_Visual'>\n<pose frame=''>%f %f %f 0 0 0</pose>\n", baseName,
	    x, y, z);
    fprintf(outFile, "\t<geometry>\n<box>\n<size>%f %f %f</size>\n", xSize, ySize, zSize);
    fprintf(outFile, "</box>\n</geometry>\n<material>\n<script>\n<uri>file://media/materials/scripts/gazebo.material</uri>\n");
    fprintf(outFile,"<name>Gazebo/Grey</name>\n</script>\n<ambient>1 1 1 1</ambient>\n</material>\n");
    fprintf(outFile,"</visual>\n");

  }
  else
  {
    std::deque<QuadNode*>::iterator iter;
    for (iter = node->children.begin(); iter != node->children.end(); iter++)
    {
      CreateBoxes(*iter, outFile, height, scale);
    }
  }
}

void processMap(QuadNode *src)
{
  FILE* outFile = fopen("model.sdf","w");
  fprintf(outFile, "<?xml version='1.0'?>\n<sdf version='1.6'>\n<model name='ImageMaze'>\n");
  fprintf(outFile, "<pose frame=''>0 0 0 0 -0 0</pose>\n");
  fprintf(outFile, "<link name='WallLink'>\n");
  CreateBoxes(src, outFile, 1.0, 1.0);
  fprintf(outFile, " \n</link><static>1</static>\n</model>\n</sdf>\n");
  fclose(outFile);
}


QuadTree* MakeQuadTree(PBMMapImage &src)
{
  QuadTree *tree = new QuadTree(src.getWidth(), src.getHeight());
  tree->setImage(src, 127);
  tree->BuildTree(tree->root);

  tree->merged = true;
  while (tree->merged)
  {
    tree->merged = false;
    tree->ReduceTree(tree->root);
  }

  return tree;
}

int main(int argc, char **argv)
{
  PBMMapImage mapImage;
  mapImage.LoadFromPBM(argv[1]);
  QuadTree *tree = MakeQuadTree(mapImage);
  
  processMap(tree->root);
  
  /*
  uint8_t *data = mapImage.getPixelPlane(); 
  for (int i = 0; i<mapImage.getHeight(); i++)
    {
      for (int j = 0; j<mapImage.getWidth(); j++)
	{
	  printf("%u ", data[i*mapImage.getWidth() + j]);
	}
      printf("\n");
    }
  */
  
  return 0;
}
