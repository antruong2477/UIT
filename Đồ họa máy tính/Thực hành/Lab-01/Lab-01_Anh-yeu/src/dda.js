import { Painter } from "./painter.js";

Painter.prototype.drawLineDDA = function(p0, p1, rgba) {
    let [x0, y0] = p0;
    let [x1, y1] = p1;
    let dx = x1 - x0, dy = y1 - y0;
    if (dx === 0 && dy === 0) return;

    if (Math.abs(dy) <= Math.abs(dx)) {
        if (x1 < x0) {
            [x0, x1] = [x1, x0];
            [y0, y1] = [y1, y0];
        }
        let k = dy / dx;
        let y = y0;
        for (let x = x0; x <= x1; x++) {
            this.setPixel(x, Math.floor(y + 0.5), rgba);
            y += k;
        }
    } else {
        if (y1 < y0) {
            [x0, x1] = [x1, x0];
            [y0, y1] = [y1, y0];
        }
        let k = dx / dy;
        let x = x0;
        for (let y = y0; y <= y1; y++) {
            this.setPixel(Math.floor(x + 0.5), y, rgba);
            x += k;
        }
    }
};
