const canvas = document.getElementById('input_canvas');
const ctx = canvas.getContext('2d');
Clear();
mouseDown = false;

function ProcessMouse(event) {
  let rect = canvas.getBoundingClientRect();
  let x = parseInt(event.clientX - rect.left);
  let y = parseInt(event.clientY - rect.top);
  if (mouseDown) {
    ctx.beginPath();
    ctx.arc(x, y, 10, 0, 2 * Math.PI);
    ctx.fillStyle = 'white';
    ctx.fill();
  }
}

function Status(s) {
  if (s == 1) {
    mouseDown = true;
  } else {
    mouseDown = false;
  }
}

function SubmitData() {
  const pixel_data = ctx.getImageData(0, 0, 280, 280).data;
  let compact = [];
  for (let i = 0; i < pixel_data.length; i += 4) {
    if (pixel_data[i] > 100) {
      compact.push(1);
    } else {
      compact.push(0);
    }
  }
  let ultradense = [];
  for (let y = 0; y < 28; y++) {
    for (let x = 0; x < 28; x++) {
      let sum = 0;
      for (let y10 = 0; y10 < 10; y10++) {
        for (let x10 = 0; x10 < 10; x10++) {
          sum += compact[(y * 10 + y10) * 280 + (x * 10 + x10)];
        }
      }
      const average = parseInt((sum * 9) / 100);
      ultradense.push(average);

      ctx.fillStyle = 'rgb(' + parseInt(28.3 * average) + ',' + parseInt(28.3 * average) + ',' + parseInt(28.3 * average) + ')';
      ctx.fillRect(x * 10, y * 10, 10, 10);
    }
  }
  console.log(ultradense);
  let response = fetch('/mnist/getnumber?x=' + ultradense.join('')).then(rawdata => {
    rawdata.json().then(jsondata => {
      console.log(jsondata);
      let output = '';
      jsondata.probability.forEach(p => {
        output += '<td>' + parseFloat(parseInt(p * 10000)) / 100 + '%</td>';
      });
      document.getElementById('data').innerHTML = output;
    });
  });
}

function Clear() {
  ctx.fillStyle = '#000000';
  ctx.fillRect(0, 0, 280, 280);

  for (let i = 1; i < 28; i++) {
    ctx.strokeStyle = '#333333';
    ctx.moveTo(0, i * 10);
    ctx.lineTo(280, i * 10);
    ctx.stroke();

    ctx.moveTo(i * 10, 0);
    ctx.lineTo(i * 10, 280);
    ctx.stroke();
  }
}
