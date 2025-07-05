import DDA from "./dda.js";
import Bresenham from "./bresenham.js";
import Midpoint from "./midpoint.js";
import Ellipse from "./ellipse.js";

let canvas = document.getElementById("canvas");
let ctx = canvas.getContext("2d");
let algorithmInstance = null;
let useKeyboard = false;

document.getElementById("drawMode").addEventListener("change", (event) => {
    useKeyboard = event.target.value === "keyboard";
    
    const hint = document.getElementById("keyboardHint");
    if (useKeyboard) {
        hint.style.display = "block";
        setTimeout(() => {
            hint.style.display = "none";
        }, 5000);
    } else {
        hint.style.display = "none";
    }

    initializeAlgorithm();
});

function initializeAlgorithm() {
    if (!canvas) {
        console.error("Canvas không tồn tại!");
        return;
    }

    let newCanvas = canvas.cloneNode(true);
    canvas.parentNode.replaceChild(newCanvas, canvas);
    canvas = newCanvas;
    ctx = canvas.getContext("2d");

    let algorithm = document.getElementById("algorithm").value;
    useKeyboard = document.getElementById("drawMode").value === "keyboard";
    
    switch (algorithm) {
        case "ellipse":
            algorithmInstance = new Ellipse(canvas);
            break;
        case "midpoint":
            algorithmInstance = new Midpoint(canvas);
            break;
        case "bresenham":
            algorithmInstance = new Bresenham(canvas, useKeyboard);
            break;
        case "dda":
            algorithmInstance = new DDA(canvas, useKeyboard);
            break;
        default:
            console.error("Thuật toán không hợp lệ:", algorithm);
    }
}


document.getElementById("algorithm").addEventListener("change", () => {
    initializeAlgorithm();
});

document.getElementById("reset").addEventListener("click", () => {
    if (!ctx) {
        console.error("Không thể xóa canvas vì `ctx` là null!");
        return;
    }
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    initializeAlgorithm();
});

initializeAlgorithm();
