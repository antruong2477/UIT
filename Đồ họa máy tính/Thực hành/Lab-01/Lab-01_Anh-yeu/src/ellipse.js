import { Painter } from "./painter.js";

Painter.prototype.drawEllipseMidpoint = function(center, rx, ry, rgba) {
    let [xc, yc] = center;
    let x = 0, y = ry;
    let rx2 = rx * rx, ry2 = ry * ry;
    let twoRx2 = 2 * rx2, twoRy2 = 2 * ry2;
    let px = 0, py = twoRx2 * y;

    // Vùng 1
    let p1 = ry2 - (rx2 * ry) + (0.25 * rx2);
    while (px <= py) {  // Sửa điều kiện dừng
        this.setPixel(xc + x, yc + y, rgba);
        this.setPixel(xc - x, yc + y, rgba);
        this.setPixel(xc + x, yc - y, rgba);
        this.setPixel(xc - x, yc - y, rgba);

        x++;
        px += twoRy2;

        if (p1 < 0) {
            p1 += ry2 + px;
        } else {
            y--;
            py -= twoRx2;
            p1 += ry2 + px - py;
        }
    }

    // Vùng 2
    let p2 = ry2 * (x + 0.5) * (x + 0.5) + rx2 * (y - 1) * (y - 1) - (rx2 * ry2);
    while (y >= 0) {
        this.setPixel(xc + x, yc + y, rgba);
        this.setPixel(xc - x, yc + y, rgba);
        this.setPixel(xc + x, yc - y, rgba);
        this.setPixel(xc - x, yc - y, rgba);

        y--;
        py -= twoRx2;

        if (p2 > 0) {
            p2 += rx2 - py;
        } else {
            x++;
            px += twoRy2;
            p2 += rx2 - py + px;
        }
    }
};

