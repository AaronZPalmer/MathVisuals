
const canvas = document.getElementById("canvas");
var ctx = canvas.getContext('2d');

const koala_png = new Image();
koala_png.src = "/static/images/koala.png"; // can also be a remote URL e.g. http://
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


  fetch('/koala_sim')
      .then(function (response) {
          return response.json();
      }).then(function (text) {

          x_positions = text.x_positions
          y_positions = text.y_positions

          N = text.N

          ctx.clearRect(0, 0, canvas.width, canvas.height);

          image_width = koala_png.width * canvas.width / Math.sqrt(N) / 2500
          image_height = koala_png.height * canvas.width / Math.sqrt(N) / 2500
          if (text.circumcircles == true){

            num_circles= text.num_circles
            radii = text.radii
            x_center = text.x_center
            y_center = text.y_center

            for(let i  = 0; i < N; i++) {
              ctx.drawImage(koala_png,x_positions[i] * canvas.width / 10 + canvas.width / 2 - image_width / 2, y_positions[i] * canvas.height / 10 + canvas.height / 2 - image_height / 2, image_width, image_height)
            } 
            ctx.strokeStyle = "#FF0000";
            // ctx.beginPath();
            // ctx.ellipse(canvas.width / 2,canvas.height / 2, 1* canvas.width / 10, 1 * canvas.height / 10, 0, 0, 2 * Math.PI);
            // ctx.stroke();
            for(let i  = 0; i < num_circles; i++) {
              ctx.beginPath();
              ctx.ellipse(x_center[i] * canvas.width / 10 + canvas.width / 2,y_center[i] * canvas.height / 10 + canvas.height / 2, radii[i]* canvas.width / 10, radii[i] * canvas.height / 10, 0, 0, 2 * Math.PI);
              ctx.stroke();
            }  
            // console.log(radii)
            // console.log(x_center)
            // console.log(y_center)
            // console.log(num_circles)
            // console.log("balls")
             
          } else {
  
            for(let i  = 0; i < N; i++) {
              ctx.drawImage(koala_png,x_positions[i] * canvas.width / 10 + canvas.width / 2 - image_width / 2, y_positions[i] * canvas.height / 10 + canvas.height / 2 - image_height / 2, image_width, image_height)
            }
          }
          // console.log(x_positions);
          // console.log(N); 
          //  console.log(canvas.width); 
      });
}

function setVals() {
  form_data = document.getElementById("setValForm");
  N = form_data[0].value
  sigma = form_data[1].value
  C = form_data[2].value
  var checkBox = document.getElementById("myCheck");
  fetch('/koala_sim', {

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
        "C": C,
        "circumcircles": checkBox.checked
    })
  });
}

function resize() {
  ctx.canvas.width = window.innerWidth;
  ctx.canvas.height = window.innerHeight;
}

