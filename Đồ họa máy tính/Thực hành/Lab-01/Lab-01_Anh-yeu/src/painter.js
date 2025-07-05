class Painter {
    constructor(context, width, height) {
        this.context = context;
        this.imageData = context.createImageData(width, height);
        this.points = [];
        this.width = width;
        this.height = height;
    }

    getPixelIndex(x, y) {
        if (x < 0 || y < 0 || x >= this.width || y >= this.height)
            return -1;
        return (x + y * this.width) << 2;
    }

    setPixel(x, y, rgba) {
        let pixelIndex = this.getPixelIndex(x, y);
        if (pixelIndex === -1) return;
        for (let i = 0; i < 4; i++) {
            this.imageData.data[pixelIndex + i] = rgba[i];
        }
    }

    updateCanvas() {
        this.context.putImageData(this.imageData, 0, 0);
    }

    drawPoint(p, rgba) {
        let [x, y] = p;
        for (let i = -1; i <= 1; i++)
            for (let j = -1; j <= 1; j++)
                this.setPixel(x + i, y + j, rgba);
        this.updateCanvas(); 
    }

    drawLine(p0, p1, algorithm = "Bresenham") {
        let colorBresenham = [0, 200, 0, 255];
        let colorDDA = [0, 0, 255, 255];

        let lineColor = algorithm === "DDA" ? colorDDA : colorBresenham;

        if (algorithm === "DDA") {
            this.drawLineDDA(p0, p1, lineColor);
        } else {
            this.drawLineBresenham(p0, p1, lineColor);
        }
        this.updateCanvas();
    }
}

export { Painter };
