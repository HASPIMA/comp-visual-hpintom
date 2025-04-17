void setup () {
  size(400, 400);
}

float newSize( float prevSize) {
  float d = dist(width/2, height/2, mouseX, mouseY);
  float maxDist = dist(0, 0, width/2, height/2);
  return prevSize + map(d, 0, maxDist, -maxDist + 100, maxDist);
}

void  draw() {
  background(204);

  int size1 = 50;
  int size2 = 100;
  int size3 = 20;

  fill(0);
  Square s1 = new Square(size1, new Position(1, 2));
  Square s2 = new Square(size2, new Position(3, 4));

  // Constrain the mouse position to keep the square within bounds
  float constrainedX = constrain(mouseX, size3/2, width - size3/2 );
  float constrainedY = constrain(mouseY, size3/2, height - size3/2);
  Square s3 = new Square(size2, new Position(constrainedX, constrainedY));

  // First square
  pushMatrix();
  rectMode(CORNER);
  fill(0);

  rotate(sin(frameCount * 0.01 + mouseY * 0.1));

  s1.setSize(newSize(size1));
  s1.draw();
  popMatrix();


  // Second square
  pushMatrix();
  rectMode(CENTER);
  fill(255, 0, 0);

  translate(width/2, height/2);
  rotate(cos(frameCount * 0.1 + mouseX * 0.02));

  s2.draw();
  popMatrix();

  // Third square - follows mouse and rotates
  pushMatrix();
  rectMode(CENTER);
  fill(0, 0, 255);

  translate(constrainedX, constrainedY);
  rotate(frameCount * 0.05);

  s3.draw();
  popMatrix();
}
