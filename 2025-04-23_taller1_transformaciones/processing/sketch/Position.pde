class Position {
  private int x;
  private int y;


  Position(int x, int y) {
    this.x = x;
    this.y = y;
  }

  Position(Position p) {
    this.x = p.getX();
    this.y = p.getY();
  }

  Position(float x, float y) {
    this.x = (int) x;
    this.y = (int) y;
  }

  Position() {
    this.x = 0;
    this.y = 0;
  }

  public int getX() {
    return x;
  }
  public int getY() {
    return y;
  }

  public void setX(int x) {
    this.x = x;
  }

  public void setY(int y) {
    this.y = y;
  }

  public void setXY(int x, int y) {
    this.x = x;
    this.y = y;
  }

  public void setXY(Position p) {
    this.x = p.getX();
    this.y = p.getY();
  }
}
