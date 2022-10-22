// get canvas 2D context object
const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");
const info = document.querySelector("p");

const GLOBALS = {
  click: { x: undefined, y: undefined },
  mouse: { x: undefined, y: undefined },
  mouseDown: { x: undefined, y: undefined },
  mouseUp: { x: undefined, y: undefined },
  distance: (a, b) =>
    Math.sqrt(Math.pow(b.x - a.x, 2) + Math.pow(b.y - a.y, 2)), //  formula: √ (x2 − x1)^2 + (y2 − y1)^2
  angle: (a, b) => Math.atan2(b.y - a.y, b.x - a.x) // formula: atan2(y2 - y1, x2 - x1)
  // Globally accessable helper functions for calculating angle and distance between two points
};
// use GLOBALS to keep track of mouse actions, and have them accessable by every sprite

const PROPS = [];

const CHARS = [];

// function for applying any initial settings
function init() {
  // apply a fullscreen fit
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  // register event listeners to store mouse actions and coordinates inside GLOBALS, so that they can be accessed by sprites that need them.

  /*window.addEventListener("click", (e) => {
    GLOBALS.mouseUp.x = GLOBALS.mouseDown.x = GLOBALS.mouse.x = GLOBALS.click.x =
      e.pageX;
    GLOBALS.mouseUp.y = GLOBALS.mouseDown.y = GLOBALS.mouse.y = GLOBALS.click.y =
      e.pageY;
  });*/

  /*function tStart(e) {
    GLOBALS.mouseUp.x = undefined;
    GLOBALS.mouseUp.y = undefined;
    GLOBALS.mouseDown.x = GLOBALS.mouse.x = e.pageX || e.touches[0]?.pageX;
    GLOBALS.mouseDown.y = GLOBALS.mouse.y = e.pageY || e.touches[0]?.pageY;
  }

  function tEnd(e) {
    GLOBALS.mouseDown.x = GLOBALS.mouse.x = undefined;
    GLOBALS.mouseDown.y = GLOBALS.mouse.y = undefined;
  }

  function tMove(e) {
    GLOBALS.mouse.x = e.pageX || e.touches[0]?.pageX;
    GLOBALS.mouse.y = e.pageY || e.touches[0]?.pageY;
  }*/
  // add listeners for both mobile and desktop (for demonstration purposes)

  /*window.addEventListener("touchstart", tStart);
  window.addEventListener("mousedown", tStart);
  window.addEventListener("touchend", tEnd);
  window.addEventListener("mouseup", tEnd);
  window.addEventListener("touchmove", tMove);
  window.addEventListener("mousemove", tMove);*/
}

// function for rendering background elements
function renderBackground() {}

// function for rendering prop objects in PROPS
function renderProps() {}

// function for rendering character objects in CHARS
function renderCharacters() {}

/* CLASS FOR JOYSTICKS */
class Joystick {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.distance = { x: 0, y: 0 };
    this.angle = 0;
  }
  render() {
    // display distance property before every render
    /*info.innerText = `directionX: ${this.distance.x || 0}, directionY: ${
      this.distance.y || 0
    }, angle: ${this.angle}(radians)`;*/

    let { x, y } = this;
    let { distance, angle } = GLOBALS;
    ctx.beginPath();
    ctx.lineWidth = 2;
    ctx.arc(x, y, 70, 0, 2 * Math.PI);
    ctx.stroke();
    ctx.beginPath();
    // logic for keeping thumbstick inside the circle
    if (
      distance(GLOBALS.mouse, this) < 70 &&
      distance(GLOBALS.mouseDown, this) < 70
    ) {
      ctx.arc(GLOBALS.mouse.x, GLOBALS.mouse.y, 40, 0, 2 * Math.PI);
      this.angle = angle(GLOBALS.mouse, this);
      this.distance.x = GLOBALS.mouse.x - this.x;
      this.distance.y = GLOBALS.mouse.y - this.y;
    } else if (
      distance(GLOBALS.mouse, this) > 70 &&
      distance(GLOBALS.mouseDown, this) < 70
    ) {
      let { x, y } = GLOBALS.mouse;
      let d = distance(GLOBALS.mouse, this) - 70,
        ok = false;
      while (ok === false) {
        if (x < this.x) {
          x++;
        } else {
          x--;
        }
        if (y < this.y) {
          y++;
        } else {
          y--;
        }
        if (distance({ x: x, y: y }, this) < 70) {
          ok = true;
        }
      }
      ctx.arc(x, y, 40, 0, 2 * Math.PI);
      this.distance.x = x - this.x;
      this.distance.y = y - this.y;
      this.angle = angle({ x: x, y: y }, this);
    } else {
      ctx.arc(x, y, 40, 0, 2 * Math.PI);
      this.distance.x = x - this.x;
      this.distance.y = y - this.y;
      this.angle = angle({ x: x, y: y }, this);
    }

    ctx.stroke();
    ctx.fillStyle = "gray";
    ctx.globalAlpha = 0.7;
    ctx.fill();
  }
}

// function for rendering onscreen controls
let stick = new Joystick(window.innerWidth / 2, window.innerHeight / 2);
function renderControls() {
  stick.render();
}

// main function to be run for rendering frames
function startFrames() {
  // erase entire canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // render each type of entity in order, relative to layers
  renderBackground();
  renderProps();
  renderCharacters();
  renderControls();

  // rerun function (call next frame)
  window.requestAnimationFrame(startFrames);
}

init(); // initialize game settings
startFrames(); // start running frames
