
#include <quadTree.h>

QuadTree::QuadTree(uint32_t width,  uint32_t height)
{
  root = new QuadNode(NULL);
  root->x = 0;
  root->y = 0;
  root->width = width;
  root->height = height;
}

QuadTree::~QuadTree()
{
  
}

void QuadTree::setImage(PBMMapImage &src, uint8_t threshold)
{
  _image = src;
  _threshold = threshold;
}

//////////////////////////////////////////////////
void QuadTree::ReduceTree(QuadNode *_node)
{
  std::deque<QuadNode*>::iterator iter;

  if (!_node->valid)
    return;

  if (!_node->leaf)
  {
    unsigned int count = 0;
    int size = _node->children.size();

    for (int i = 0; i < size; i++)
    {
      if (_node->children[i]->valid)
      {
        this->ReduceTree(_node->children[i]);
      }
      if (_node->children[i]->leaf)
        count++;
    }

    if (_node->parent && count == _node->children.size())
    {
      for (iter = _node->children.begin();
           iter != _node->children.end(); ++iter)
      {
        _node->parent->children.push_back(*iter);
        (*iter)->parent = _node->parent;
      }
      _node->valid = false;
    }
    else
    {
      bool done = false;
      while (!done)
      {
        done = true;
        for (iter = _node->children.begin();
             iter != _node->children.end(); ++iter)
        {
          if (!(*iter)->valid)
          {
            _node->children.erase(iter, iter+1);
            done = false;
            break;
          }
        }
      }
    }
  }
  else
  {
    this->Merge(_node, _node->parent);
  }
}

//////////////////////////////////////////////////
void QuadTree::Merge(QuadNode *_nodeA, QuadNode *_nodeB)
{
  std::deque<QuadNode*>::iterator iter;

  if (!_nodeB)
    return;

  if (_nodeB->leaf)
  {
    if (_nodeB->occupied != _nodeA->occupied)
      return;

    if (_nodeB->x == _nodeA->x + _nodeA->width &&
         _nodeB->y == _nodeA->y &&
         _nodeB->height == _nodeA->height)
    {
      _nodeA->width += _nodeB->width;
      _nodeB->valid = false;
      _nodeA->valid = true;

      this->merged = true;
    }

    if (_nodeB->x == _nodeA->x &&
        _nodeB->width == _nodeA->width &&
        _nodeB->y == _nodeA->y + _nodeA->height)
    {
      _nodeA->height += _nodeB->height;
      _nodeB->valid = false;
      _nodeA->valid = true;

      this->merged = true;
    }
  }
  else
  {
    for (iter = _nodeB->children.begin();
         iter != _nodeB->children.end(); ++iter)
    {
      if ((*iter)->valid)
      {
        this->Merge(_nodeA, (*iter));
      }
    }
  }
}


//////////////////////////////////////////////////
void QuadTree::BuildTree(QuadNode *_node)
{
  unsigned int freePixels, occPixels;

  this->GetPixelCount(_node->x, _node->y, _node->width, _node->height,
                      freePixels, occPixels);

  // int diff = labs(freePixels - occPixels);

  if (static_cast<int>(_node->width*_node->height) > 1)
  {
    float newX, newY;
    float newW, newH;

    newX = _node->x;
    newY = _node->y;
    newW = _node->width / 2.0;
    newH = _node->height / 2.0;

    // Create the children for the node
    for (int i = 0; i < 2; i++)
    {
      newX = _node->x;

      for (int j = 0; j < 2; j++)
      {
        QuadNode *newNode = new QuadNode(_node);
        newNode->x = (unsigned int)newX;
        newNode->y = (unsigned int)newY;

        if (j == 0)
          newNode->width = (unsigned int)floor(newW);
        else
          newNode->width = (unsigned int)ceil(newW);

        if (i == 0)
          newNode->height = (unsigned int)floor(newH);
        else
          newNode->height = (unsigned int)ceil(newH);

        _node->children.push_back(newNode);

        this->BuildTree(newNode);

        newX += newNode->width;

        if (newNode->width == 0 || newNode->height == 0)
          newNode->valid = false;
      }

      if (i == 0)
        newY += floor(newH);
      else
        newY += ceil(newH);
    }

    // _node->occupied = true;
    _node->occupied = false;
    _node->leaf = false;
  }
  else if (occPixels == 0)
  {
    _node->occupied = false;
    _node->leaf = true;
  }
  else
  {
    _node->occupied = true;
    _node->leaf = true;
  }
}
uint8_t QuadTree::GetPixel(uint32_t y, uint32_t x)
{
  if (_image.getPixelPlane() == NULL)
    return 0;

  uint8_t *plane = _image.getPixelPlane();
  return plane[y*_image.getWidth() + x];
}

void QuadTree::GetPixelCount(unsigned int xStart, unsigned int yStart,
                                 unsigned int width, unsigned int height,
                                 unsigned int &freePixels,
                                 unsigned int &occPixels)
{
  uint8_t pixColor;

  unsigned int x, y;

  freePixels = occPixels = 0;

  for (y = yStart; y < yStart + height; y++)
  {
    for (x = xStart; x < xStart + width; x++)
    {
      pixColor = this->GetPixel(x, y);

      if (pixColor < this->_threshold)
        freePixels++;
      else
        occPixels++;
    }
  }
}
