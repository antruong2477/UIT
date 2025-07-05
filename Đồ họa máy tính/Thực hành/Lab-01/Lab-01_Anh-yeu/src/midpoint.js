import { Painter } from "./painter.js";

Painter.prototype.drawCircleMidpoint = function(center, radius) {
    let colorMidpoint = [255, 255, 0, 255]; 

    let [x0, y0] = center;
    let x = radius, y = 0;
    let p = 1 - radius;

    while (x >= y) {
        this.setPixel(x0 + x, y0 + y, colorMidpoint);
        this.setPixel(x0 - x, y0 + y, colorMidpoint);
        this.setPixel(x0 + x, y0 - y, colorMidpoint);
        this.setPixel(x0 - x, y0 - y, colorMidpoint);
        this.setPixel(x0 + y, y0 + x, colorMidpoint);
        this.setPixel(x0 - y, y0 + x, colorMidpoint);
        this.setPixel(x0 + y, y0 - x, colorMidpoint);
        this.setPixel(x0 - y, y0 - x, colorMidpoint);

        y++;
        if (p <= 0) {
            p += 2 * y + 1;
        } else {
            x--;
            p += 2 * (y - x) + 1;
        }
    }

    this.updateCanvas(); 
};

