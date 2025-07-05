class Midpoint {
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
                let radius = Math.sqrt((end.x - this.start.x) ** 2 + (end.y - this.start.y) ** 2);
                this.drawCircleMidpoint(this.start.x, this.start.y, Math.round(radius));
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

    drawCircleMidpoint(xc, yc, r) {
        let x = r, y = 0;
        let p = 1 - r;
        this.drawCirclePixels(xc, yc, x, y);

        while (x > y) {
            y++;
            if (p <= 0) {
                p += 2 * y + 1;
            } else {
                x--;
                p += 2 * (y - x) + 1;
            }
            this.drawCirclePixels(xc, yc, x, y);
        }
    }

    drawCirclePixels(xc, yc, x, y) {
        this.setPixel(xc + x, yc + y);
        this.setPixel(xc - x, yc + y);
        this.setPixel(xc + x, yc - y);
        this.setPixel(xc - x, yc - y);
        this.setPixel(xc + y, yc + x);
        this.setPixel(xc - y, yc + x);
        this.setPixel(xc + y, yc - x);
        this.setPixel(xc - y, yc - x);
    }

    setPixel(x, y) {
        this.ctx.fillStyle = "black";
        this.ctx.fillRect(x, y, 1, 1);
    }
}

export default Midpoint;