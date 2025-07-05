class DDA {
    constructor(canvas, useKeyboard = false) {
        this.canvas = canvas;
        this.ctx = canvas.getContext("2d");
        this.useKeyboard = useKeyboard;
        this.isDrawing = false;
        this.start = { x: this.canvas.width / 2, y: this.canvas.height / 2 };
        this.current = { ...this.start };
        this.end = null;
        this.lines = []; 
        this.initEvents();
    }
    
    initEvents() {
        if (this.useKeyboard) {
            this.drawPoint(this.start, "red");
            document.addEventListener("keydown", this.handleKeyDown.bind(this));
        } else {
            this.canvas.addEventListener("mousedown", (e) => {
                this.start = this.getMousePos(e);
                this.isDrawing = true;
            });

            this.canvas.addEventListener("mouseup", (e) => {
                if (this.isDrawing) {
                    this.end = this.getMousePos(e);
                    this.lines.push({ start: this.start, end: this.end });
                    this.drawLineDDA(this.start.x, this.start.y, this.end.x, this.end.y);
                    this.isDrawing = false;
                }
            });
        }
    }
    
    handleKeyDown(event) {
        switch (event.key) {
            case "ArrowUp": this.current.y -= 5; break;
            case "ArrowDown": this.current.y += 5; break;
            case "ArrowLeft": this.current.x -= 5; break;
            case "ArrowRight": this.current.x += 5; break;
            case "Enter":
                if (!this.isDrawing) {
                    this.isDrawing = true;
                    this.start = { ...this.current };
                    console.log("Điểm đầu đã chọn:", this.start);
                } else {
                    this.end = { ...this.current };
                    console.log("Điểm cuối đã chọn:", this.end);
                    this.lines.push({ start: this.start, end: this.end });
                    this.isDrawing = false;
                }
                break;
        }
        this.redraw();
    }
    
    redraw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.lines.forEach(line => {
            this.drawLineDDA(line.start.x, line.start.y, line.end.x, line.end.y);
        });
        this.drawPoint(this.current, "red");
        if (this.isDrawing) {
            this.drawPoint(this.start, "blue");
            this.drawLineDDA(this.start.x, this.start.y, this.current.x, this.current.y);
        }
    }
    
    drawPoint(point, color) {
        this.ctx.fillStyle = color;
        this.ctx.fillRect(point.x - 3, point.y - 3, 6, 6);
    }
    
    getMousePos(event) {
        let rect = this.canvas.getBoundingClientRect();
        return {
            x: Math.round(event.clientX - rect.left),
            y: Math.round(event.clientY - rect.top)
        };
    }
    
    drawLineDDA(x0, y0, x1, y1) {
        let dx = x1 - x0;
        let dy = y1 - y0;
        let steps = Math.max(Math.abs(dx), Math.abs(dy));
        let xInc = dx / steps;
        let yInc = dy / steps;
        
        let x = x0;
        let y = y0;
        for (let i = 0; i <= steps; i++) {
            this.setPixel(Math.round(x), Math.round(y));
            x += xInc;
            y += yInc;
        }
    }
    
    setPixel(x, y) {
        this.ctx.fillStyle = "black";
        this.ctx.fillRect(x, y, 1, 1);
    }
}

export default DDA;