#ifndef __QUADTREE_H_
#define __QUADTREE_H_

#include <deque>
#include <stdio.h>
#include <math.h>
#include <string>
#include <pbmMapImage.h>


class QuadNode
    {
      /// \brief Constructor
      /// \param[in] _parent Parent quad tree node.
      public: QuadNode(QuadNode *_parent)
              : x(0), y(0), width(0), height(0)
              {
                parent = _parent;
                occupied = false;
                leaf = true;
                valid = true;
              }

      /// \brief Destructor.
      public: ~QuadNode()
              {
                std::deque<QuadNode*>::iterator iter;
                for (iter = children.begin(); iter != children.end(); ++iter)
                    delete (*iter);
              }

      /// \brief Print this quad tree node, and all its children.
      /// \param[in] _space String of spaces that formats the printfs.
      public: void Print(std::string _space)
              {
                std::deque<QuadNode*>::iterator iter;

                printf("%sXY[%d %d] WH[%d %d] O[%d] L[%d] V[%d]\n",
                    _space.c_str(), x, y, width, height, occupied, leaf, valid);
                _space += "  ";
                for (iter = children.begin(); iter != children.end(); ++iter)
                  if ((*iter)->occupied)
                    (*iter)->Print(_space);
              }

      /// \brief X and Y location of the node.
      public: uint32_t x, y;

      /// \brief Width and height of the node.
      public: uint32_t width, height;

      /// \brief Parent node.
      public: QuadNode *parent;

      /// \brief Children nodes.
      public: std::deque<QuadNode*> children;

      /// \brief True if the node is occupied
      public: bool occupied;

      /// \brief True if the node is a leaf.
      public: bool leaf;

      /// \brief True if the node is valid.
      public: bool valid;
    };

class QuadTree
{
 public:
  QuadNode *root;
  QuadTree(uint32_t width, uint32_t height);
  ~QuadTree();
  void setImage(PBMMapImage &src, uint8_t threshold);
  void ReduceTree(QuadNode *_node);
  void Merge(QuadNode *_nodeA, QuadNode *_nodeB);
  void BuildTree(QuadNode *_node);
  bool merged;
  void GetPixelCount(unsigned int xStart, unsigned int yStart,
		     unsigned int width, unsigned int height,
		     unsigned int &freePixels,
		     unsigned int &occPixels);
  uint8_t GetPixel(uint32_t x, uint32_t y);
 private:
  PBMMapImage _image;
  uint8_t _threshold;
  
};

#endif
