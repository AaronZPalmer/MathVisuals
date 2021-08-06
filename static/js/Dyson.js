
const canvas = document.getElementById("canvas");
var ctx = canvas.getContext('2d');

const bus_png = new Image();
bus_png.src = "/static/images/bus.png"; // can also be a remote URL e.g. http://
// bus_png.onload = function() {
//    context.drawImage(bus_png,0,0);
// };

window.addEventListener('resize', resize);
// document.addEventListener('mousemove', draw);
// document.addEventListener('mousedown', getPosition);
// document.addEventListener('mouseenter', setPosition);

var intervalId = window.setInterval(function(){
  getPosition()
}, 100);


function getPosition() {
  fetch('/bus_sim')
      .then(function (response) {
          return response.json();
      }).then(function (text) {
          positions = text.positions
          N = text.N
          image_width = bus_png.width * canvas.width / N / 600
          image_height = bus_png.height * canvas.height / N / 600
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          for(let i  = 0; i < N; i++) {
            ctx.drawImage(bus_png, positions[i] * canvas.width / 5 + canvas.width / 2 - image_width, canvas.height / 2 - image_height, image_width, image_height)
          }
          // console.log(positions);
          // console.log(N); 
          //  console.log(canvas.width); 
      });
  // ctx.drawImage(bus_png,pos.x,pos.y)
}

function setVals() {
  form_data = document.getElementById("setValForm");
  N = form_data[0].value
  sigma = form_data[1].value
  C = form_data[2].value
  fetch('/bus_sim', {

    // Declare what type of data we're sending
    headers: {
      'Content-Type': 'application/json'
    },

    // Specify the method
    method: 'POST',

    // A JSON payload
    body: JSON.stringify({
        "N": N,
        "sigma": sigma,
        "C": C
    })
  });
  universality_class = 2/3*(sigma ** 2 + Math.sqrt(sigma **4+6*C))/sigma/sigma
  document.getElementById("universalityClass").innerHTML = "universality class (beta / sigma^2) = " + universality_class.toString();
}

function resize() {
  ctx.canvas.width = window.innerWidth;
  ctx.canvas.height = window.innerHeight;
}

