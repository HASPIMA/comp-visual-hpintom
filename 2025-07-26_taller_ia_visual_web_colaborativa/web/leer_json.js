// web/script.js
fetch("resultados/deteccion_0.json")
  .then(res => res.json())
  .then(data => {
    const tbody = document.getElementById("tbody0");
    data.objects.forEach(obj => {
      const row = `<tr>
        <td>${obj.class}</td>
        <td>${(obj.confidence * 100).toFixed(1)}%</td>
        <td>(${obj.x}, ${obj.y}, ${obj.w}, ${obj.h})</td>
      </tr>`;
      tbody.innerHTML += row;
    });
  });
fetch("resultados/deteccion_1.json")
  .then(res => res.json())
  .then(data => {
    const tbody = document.getElementById("tbody1");
    data.objects.forEach(obj => {
      const row = `<tr>
        <td>${obj.class}</td>
        <td>${(obj.confidence * 100).toFixed(1)}%</td>
        <td>(${obj.x}, ${obj.y}, ${obj.w}, ${obj.h})</td>
      </tr>`;
      tbody.innerHTML += row;
    });
  });
fetch("resultados/deteccion_2.json")
  .then(res => res.json())
  .then(data => {
    const tbody = document.getElementById("tbody2");
    data.objects.forEach(obj => {
      const row = `<tr>
        <td>${obj.class}</td>
        <td>${(obj.confidence * 100).toFixed(1)}%</td>
        <td>(${obj.x}, ${obj.y}, ${obj.w}, ${obj.h})</td>
      </tr>`;
      tbody.innerHTML += row;
    });
  });
fetch("resultados/deteccion_3.json")
  .then(res => res.json())
  .then(data => {
    const tbody = document.getElementById("tbody3");
    data.objects.forEach(obj => {
      const row = `<tr>
        <td>${obj.class}</td>
        <td>${(obj.confidence * 100).toFixed(1)}%</td>
        <td>(${obj.x}, ${obj.y}, ${obj.w}, ${obj.h})</td>
      </tr>`;
      tbody.innerHTML += row;
    });
  });
fetch("resultados/deteccion_4.json")
  .then(res => res.json())
  .then(data => {
    const tbody = document.getElementById("tbody4");
    data.objects.forEach(obj => {
      const row = `<tr>
        <td>${obj.class}</td>
        <td>${(obj.confidence * 100).toFixed(1)}%</td>
        <td>(${obj.x}, ${obj.y}, ${obj.w}, ${obj.h})</td>
      </tr>`;
      tbody.innerHTML += row;
    });
  });