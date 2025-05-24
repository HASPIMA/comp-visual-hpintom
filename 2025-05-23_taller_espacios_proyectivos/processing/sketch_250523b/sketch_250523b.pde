float angle = 0;

void setup() {
  size(600, 600, P3D);
  smooth(8);
}

void draw() {
  background(220);

  if (keyPressed) {
    if (key == 'o' || key == 'O') {
      ortho(-width/2, width/2, -height/2, height/2, 0.1, 1000);
      fill(0);
      text("Proyección Ortográfica (Presiona 'p' para Perspectiva)", 10, 20);
    } else if (key == 'p' || key == 'P') {
      perspective(PI/3.0, float(width)/float(height), 0.1, 1000);
      fill(0);
      text("Proyección Perspectiva (Presiona 'o' para Ortográfica)", 10, 20);
    }
  } else {
    perspective(PI/3.0, float(width)/float(height), 0.1, 1000);
    fill(0);
    text("Proyección Perspectiva (Presiona 'o' para Ortográfica)", 10, 20);
  }

  translate(width/2, height/2, 0);
  rotateY(angle);
  rotateX(angle * 0.3);

  noStroke();

  // Cubo lejano
  pushMatrix();
  translate(-100, 0, -100);
  fill(255, 100, 0);
  box(80);
  popMatrix();

  // Esfera central
  pushMatrix();
  translate(0, 0, 0);
  fill(0, 150, 255);
  sphere(60);
  popMatrix();

  // Cono cercano
  pushMatrix();
  translate(100, 0, 100);
  fill(100, 255, 100);
  drawCone(40, 100);
  popMatrix();

  angle += 0.01;
}

// Función para dibujar un cono simple
void drawCone(float radius, float height) {
  int sides = 32;
  float angleStep = TWO_PI / sides;

  beginShape(TRIANGLE_FAN);
  vertex(0, -height/2, 0); // Punta del cono (arriba)

  for (int i = 0; i <= sides; i++) {
    float x = radius * cos(i * angleStep);
    float z = radius * sin(i * angleStep);
    vertex(x, height/2, z);
  }

  endShape();
}
