export function getPosOnCanvas(x, y) {
    let bbox = canvas.getBoundingClientRect();
    return [
        Math.floor((x - bbox.left) * (canvas.width / bbox.width) + 0.5),
        Math.floor((y - bbox.top) * (canvas.height / bbox.height) + 0.5)
    ];
}

export function doMouseMove(e) {
    if (state === 0 || state === 2) return;
    let p = getPosOnCanvas(e.clientX, e.clientY);
    painter.draw(p);
}

export function doMouseDown(e) {
    if (state === 2 || e.button !== 0) return;
    let p = getPosOnCanvas(e.clientX, e.clientY);
    painter.addPoint(p);
    painter.draw(p);
    if (state === 0) state = 1;
}

export function doKeyDown(e) {
    if (state === 2) return;
    let keyId = e.keyCode || e.which;
    if (keyId === 27 && state === 1) { // ESC key
        state = 2;
        painter.draw(painter.points[painter.points.length - 1]); // Xóa đường màu đỏ
    }
}
