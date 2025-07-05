import { Painter } from "./painter.js";
import { getPosOnCanvas } from "./events.js";
import "./dda.js";
import "./bresenham.js";
import "./midpoint.js";
import "./ellipse.js";

var canvas = document.getElementById("canvas");
var context = canvas.getContext("2d");

var width = canvas.width;
var height = canvas.height;

var painter = new Painter(context, width, height);
var isEllipseMode = false;
var drawing = false; // Flag to indicate drawing in progress

// Lấy thuật toán từ dropdown
var algorithmSelect = document.getElementById("algorithmSelect");
var selectedAlgorithm = algorithmSelect.value;

algorithmSelect.addEventListener("change", function () {
    selectedAlgorithm = algorithmSelect.value;
});

// Xử lý khi nhấn nút "Vẽ Ellipse"
document.getElementById("drawEllipse").addEventListener("click", function () {
    isEllipseMode = !isEllipseMode; // Bật/Tắt chế độ ellipse khi nhấn
    this.classList.toggle("active", isEllipseMode); // Thay đổi màu nút
    console.log("Chế độ vẽ Ellipse:", isEllipseMode ? "Bật" : "Tắt");
});

// Xử lý sự kiện chuột để vẽ
canvas.addEventListener("mousedown", function (e) {
    if (e.button !== 0) return; 

    if (!drawing) {
        let p = getPosOnCanvas(e.clientX, e.clientY, canvas);
        painter.points = [p]; // Reset ngay lập tức khi bắt đầu vẽ
        painter.drawPoint(p, [225, 0, 100, 255]);
        console.log("Điểm bắt đầu:", painter.points);
        drawing = true; 
    } else {
        let p = getPosOnCanvas(e.clientX, e.clientY, canvas);
        painter.points.push(p);
        painter.drawPoint(p, [225, 0, 100, 255]); 
        console.log("Điểm kết thúc:", painter.points);

        let [x0, y0] = painter.points[0];
        let [x1, y1] = painter.points[1];

        if (isEllipseMode) {
            let xc = Math.round((x0 + x1) / 2);
            let yc = Math.round((y0 + y1) / 2);
            let rx = Math.abs(x1 - x0) / 2;
            let ry = Math.abs(y1 - y0) / 2;
            console.log(`Vẽ Ellipse: (${xc}, ${yc}), Rx = ${rx}, Ry = ${ry}`);
            painter.drawEllipseMidpoint([xc, yc], rx, ry, [255, 165, 0, 255]);
        } else {
            if (selectedAlgorithm === "DDA") {
                console.log("Vẽ đường bằng DDA");
                painter.drawLine(painter.points[0], painter.points[1], selectedAlgorithm);
            } else if (selectedAlgorithm === "Bresenham") {
                console.log("Vẽ đường bằng Bresenham");
                painter.drawLine(painter.points[0], painter.points[1], selectedAlgorithm);
            } else if (selectedAlgorithm === "Midpoint") {
                console.log("Vẽ đường tròn bằng Midpoint");
                let radius = Math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2);
                painter.drawCircleMidpoint(painter.points[0], Math.round(radius));
            } else {
                console.error("Thuật toán không hợp lệ:", selectedAlgorithm);
            }
        }

        setTimeout(() => {
            painter.points = [];
            drawing = false;
        }, 0);
    }
});


document.getElementById("reset").addEventListener("click", function () {
    context.clearRect(0, 0, canvas.width, canvas.height);
    painter = new Painter(context, width, height);
    drawing = false; 
    isEllipseMode = false;
});

document.addEventListener("keydown", function (e) {
    if (drawing && e.key === "Escape") {
        drawing = false;
        painter.points = [];
        context.clearRect(0, 0, canvas.width, canvas.height);
    }
});