class Square {
  int size;
  Position position;

  Square(int size, Position position) {
    this.size = size;
    this.position = position;
  }

  void setSize(int size) {
    this.size = size;
  }

  void setSize(float size) {
    this.size = (int) size;
  }
  
  void setSize(double size) {
    this.size = (int) size;
  }

  int getSize() {
    return size;
  }

  void draw() {
    rect(position.getX(), position.getY(), size, size);
  }

  void setPosition(Position position) {
    this.position = position;
  }

  void setPosition(int x, int y) {
    this.position.setXY(x, y);
  }
}
