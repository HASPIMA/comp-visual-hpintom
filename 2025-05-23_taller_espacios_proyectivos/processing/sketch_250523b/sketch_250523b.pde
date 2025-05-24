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

  // Esfera lejana (naranja)
  pushMatrix();
  translate(-100, 0, -100);
  fill(255, 165, 0);
  sphere(60);
  popMatrix();

  // Esfera central (azul)
  pushMatrix();
  translate(0, 0, 0);
  fill(0, 150, 255);
  sphere(60);
  popMatrix();

  // Esfera cercana (verde)
  pushMatrix();
  translate(100, 0, 100);
  fill(0, 255, 100);
  sphere(60);
  popMatrix();

  angle += 0.01;
}
