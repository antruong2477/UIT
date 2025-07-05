class Ellipse {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext("2d");
        this.isDrawing = false;
        this.start = null;
        this.initEvents();
    }

    initEvents() {
        this.canvas.addEventListener("mousedown", (e) => {
            this.start = this.getMousePos(e);
            this.isDrawing = true;
        });

        this.canvas.addEventListener("mouseup", (e) => {
            if (this.isDrawing) {
                let end = this.getMousePos(e);
                let rx = Math.abs(end.x - this.start.x);
                let ry = Math.abs(end.y - this.start.y);
                this.drawEllipseMidpoint(this.start.x, this.start.y, rx, ry);
                this.isDrawing = false;
            }
        });
    }

    getMousePos(event) {
        let rect = this.canvas.getBoundingClientRect();
        return {
            x: Math.round(event.clientX - rect.left),
            y: Math.round(event.clientY - rect.top)
        };
    }

    drawEllipseMidpoint(xc, yc, rx, ry) {
        let x = 0, y = ry;
        let rx2 = rx * rx, ry2 = ry * ry;
        let p1 = ry2 - (rx2 * ry) + (0.25 * rx2);

        while ((2 * ry2 * x) <= (2 * rx2 * y)) {
            this.plotEllipsePoints(xc, yc, x, y);
            x++;
            if (p1 < 0) {
                p1 += (2 * ry2 * x) + ry2;
            } else {
                y--;
                p1 += (2 * ry2 * x) - (2 * rx2 * y) + ry2;
            }
        }

        let p2 = (ry2 * (x + 0.5) * (x + 0.5)) + (rx2 * (y - 1) * (y - 1)) - (rx2 * ry2);
        while (y >= 0) {
            this.plotEllipsePoints(xc, yc, x, y);
            y--;
            if (p2 > 0) {
                p2 -= (2 * rx2 * y) + rx2;
            } else {
                x++;
                p2 += (2 * ry2 * x) - (2 * rx2 * y) + rx2;
            }
        }
    }

    plotEllipsePoints(xc, yc, x, y) {
        this.setPixel(xc + x, yc + y);
        this.setPixel(xc - x, yc + y);
        this.setPixel(xc + x, yc - y);
        this.setPixel(xc - x, yc - y);
    }

    setPixel(x, y) {
        this.ctx.fillStyle = "black";
        this.ctx.fillRect(x, y, 1, 1);
    }
}

export default Ellipse;