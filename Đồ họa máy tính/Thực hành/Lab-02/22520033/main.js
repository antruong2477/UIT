const canvas = document.getElementById("webglCanvas");
const gl = canvas.getContext("webgl");

if (!gl) {
    console.error("WebGL không được hỗ trợ!");
}

// Shader đỉnh (vertex shader)
const vertexShaderSource = `
    attribute vec2 a_position;
    uniform vec2 u_translation;
    uniform float u_angle;
    uniform vec2 u_scale;
    uniform vec2 u_pivot; // Tâm quay

    void main() {
        float rad = radians(u_angle);
        mat2 rotation = mat2(cos(rad), -sin(rad), sin(rad), cos(rad));

        vec2 pos = (a_position - u_pivot) * u_scale;
        vec2 rotatedPos = rotation * pos + u_pivot;
        gl_Position = vec4(rotatedPos + u_translation, 0, 1);
    }
`;

// Shader màu (fragment shader)
const fragmentShaderSource = `
    precision mediump float;
    void main() {
        gl_FragColor = vec4(1.0, 0.7, 0.8, 1.0);
    }
`;

function createShader(gl, type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        console.error("Lỗi biên dịch shader:", gl.getShaderInfoLog(shader));
        gl.deleteShader(shader);
        return null;
    }
    return shader;
}

// Tạo shader
const vertexShader = createShader(gl, gl.VERTEX_SHADER, vertexShaderSource);
const fragmentShader = createShader(gl, gl.FRAGMENT_SHADER, fragmentShaderSource);

// Tạo chương trình WebGL
const program = gl.createProgram();
gl.attachShader(program, vertexShader);
gl.attachShader(program, fragmentShader);
gl.linkProgram(program);
if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    console.error("Lỗi liên kết chương trình:", gl.getProgramInfoLog(program));
}
gl.useProgram(program);

// Lấy vị trí biến trong shader
const positionAttributeLocation = gl.getAttribLocation(program, "a_position");
const translationUniformLocation = gl.getUniformLocation(program, "u_translation");
const angleUniformLocation = gl.getUniformLocation(program, "u_angle");
const scaleUniformLocation = gl.getUniformLocation(program, "u_scale");
const pivotUniformLocation = gl.getUniformLocation(program, "u_pivot");

const aVertices = new Float32Array([
    -0.55, -0.30,  -0.45, -0.30,  -0.35, 0.30,  
    -0.55, -0.30,  -0.45, -0.30,  -0.32, 0.30,  
    -0.32, 0.3,  -0.35, 0.3,  -0.4, 0.0,  //

    -0.35, 0.30,  -0.25, -0.30,  -0.15, -0.30,
    -0.32, 0.30,  -0.25, -0.30,  -0.15, -0.30,
    -0.32, 0.3,  -0.35, 0.3,  -0.28, 0.0,  //

    -0.4, 0.00,  -0.28, 0.00,  -0.4, 0.07,
    -0.4, 0.07,  -0.28, 0.00,  -0.28, 0.07
]);

const nVertices = new Float32Array([
    0.15, -0.3,  0.2, -0.3,  0.15, 0.0,
    0.2, -0.3,  0.2, 0.0,  0.15, 0.0,
    0.15, -0.3,  0.2, 0.0,  0.20, -0.15,

    0.35, -0.3,  0.4, -0.3,  0.35, 0.0,
    0.4, -0.3,  0.4, 0.0,  0.35, 0.0,
    0.35, -0.3,  0.4, 0.0,  0.4, -0.15,

    0.15, 0.0, 0.15, -0.05, 0.4,0.0,
    0.4, 0.0, 0.4,-0.05, 0.15,-0.05,
    // Dấu móc
    0.15, 0.0, 0.15, -0.05, 0.1,-0.05,
    0.4, -0.3, 0.4, -0.25, 0.44, -0.22,
]);

// Tạo buffer cho chữ A
const aBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, aBuffer);
gl.bufferData(gl.ARRAY_BUFFER, aVertices, gl.STATIC_DRAW);

// Tạo buffer cho chữ N 
const nBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, nBuffer);
gl.bufferData(gl.ARRAY_BUFFER, nVertices, gl.STATIC_DRAW);


// Giá trị mặc định của các biến
let translateX = 0, translateY = 0, angle = 0, scaleX = 1, scaleY = 1;
let pivotAX = -0.35, pivotAY = -0.1; 
let pivotNX = 0.275, pivotNY = -0.15; 

// Thao tác lên A or N or both
let selectedObject = "both"; // Mặc định là cả hai
document.getElementById("objectSelect").addEventListener("change", function () {
    selectedObject = this.value;
    draw();
});


// Cập nhật giá trị khi người dùng thay đổi thanh trượt
document.getElementById("translateX").oninput = (e) => { translateX = parseFloat(e.target.value); draw(); };
document.getElementById("translateY").oninput = (e) => { translateY = parseFloat(e.target.value); draw(); };
document.getElementById("angle").oninput = (e) => { angle = parseFloat(e.target.value); draw(); };
document.getElementById("scaleX").oninput = (e) => { scaleX = parseFloat(e.target.value); draw(); };
document.getElementById("scaleY").oninput = (e) => { scaleY = parseFloat(e.target.value); draw(); };

document.querySelectorAll('input[type="range"]').forEach(slider => {
    slider.addEventListener('input', function () {
        let min = this.min;
        let max = this.max;
        let val = this.value;
        let percentage = ((val - min) / (max - min)) * 100;
        this.style.background = `linear-gradient(to right, dodgerblue 0%, dodgerblue ${percentage}%, #ccc ${percentage}%, #ccc 100%)`;

        this.nextElementSibling.textContent = this.value;
    });

    slider.dispatchEvent(new Event('input'));
});

function draw() {
    gl.clearColor(1, 1, 1, 1);
    gl.clear(gl.COLOR_BUFFER_BIT);

    if (selectedObject === "both") {
        // Ảnh hưởng cả hai chữ
        gl.uniform2f(translationUniformLocation, translateX, translateY);
        gl.uniform1f(angleUniformLocation, angle);
        gl.uniform2f(scaleUniformLocation, scaleX, scaleY);

        // Vẽ chữ A
        gl.uniform2f(pivotUniformLocation, pivotAX, pivotAY);
        gl.bindBuffer(gl.ARRAY_BUFFER, aBuffer);
        gl.vertexAttribPointer(positionAttributeLocation, 2, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(positionAttributeLocation);
        gl.drawArrays(gl.TRIANGLES, 0, aVertices.length / 2);

        // Vẽ chữ N
        gl.uniform2f(pivotUniformLocation, pivotNX, pivotNY);
        gl.bindBuffer(gl.ARRAY_BUFFER, nBuffer);
        gl.vertexAttribPointer(positionAttributeLocation, 2, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(positionAttributeLocation);
        gl.drawArrays(gl.TRIANGLES, 0, nVertices.length / 2);
    } 
    else if (selectedObject === "A") {
        // Chỉ thay đổi chữ A, giữ nguyên chữ N
        gl.uniform2f(translationUniformLocation, translateX, translateY);
        gl.uniform1f(angleUniformLocation, angle);
        gl.uniform2f(scaleUniformLocation, scaleX, scaleY);
        gl.uniform2f(pivotUniformLocation, pivotAX, pivotAY);

        gl.bindBuffer(gl.ARRAY_BUFFER, aBuffer);
        gl.vertexAttribPointer(positionAttributeLocation, 2, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(positionAttributeLocation);
        gl.drawArrays(gl.TRIANGLES, 0, aVertices.length / 2);

        // Vẽ chữ N nhưng không thay đổi
        gl.uniform2f(translationUniformLocation, 0, 0);
        gl.uniform1f(angleUniformLocation, 0);
        gl.uniform2f(scaleUniformLocation, 1, 1);
        gl.uniform2f(pivotUniformLocation, pivotNX, pivotNY);

        gl.bindBuffer(gl.ARRAY_BUFFER, nBuffer);
        gl.vertexAttribPointer(positionAttributeLocation, 2, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(positionAttributeLocation);
        gl.drawArrays(gl.TRIANGLES, 0, nVertices.length / 2);
    } 
    else if (selectedObject === "N") {
        // Chỉ thay đổi chữ N, giữ nguyên chữ A
        gl.uniform2f(translationUniformLocation, translateX, translateY);
        gl.uniform1f(angleUniformLocation, angle);
        gl.uniform2f(scaleUniformLocation, scaleX, scaleY);
        gl.uniform2f(pivotUniformLocation, pivotNX, pivotNY);

        gl.bindBuffer(gl.ARRAY_BUFFER, nBuffer);
        gl.vertexAttribPointer(positionAttributeLocation, 2, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(positionAttributeLocation);
        gl.drawArrays(gl.TRIANGLES, 0, nVertices.length / 2);

        // Vẽ chữ A nhưng không thay đổi
        gl.uniform2f(translationUniformLocation, 0, 0);
        gl.uniform1f(angleUniformLocation, 0);
        gl.uniform2f(scaleUniformLocation, 1, 1);
        gl.uniform2f(pivotUniformLocation, pivotAX, pivotAY);

        gl.bindBuffer(gl.ARRAY_BUFFER, aBuffer);
        gl.vertexAttribPointer(positionAttributeLocation, 2, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(positionAttributeLocation);
        gl.drawArrays(gl.TRIANGLES, 0, aVertices.length / 2);
    }
}

const sliders = [
    { id: "translateX", output: "valTranslateX" },
    { id: "translateY", output: "valTranslateY" },
    { id: "angle", output: "valAngle" },
    { id: "scaleX", output: "valScaleX" },
    { id: "scaleY", output: "valScaleY" }
];

// Lắng nghe sự kiện thay đổi và cập nhật giá trị
sliders.forEach(slider => {
    const input = document.getElementById(slider.id);
    const output = document.getElementById(slider.output);
    
    input.addEventListener("input", () => {
        output.textContent = input.value;
    });
});
// Vẽ lần đầu
draw();

let autoMoveInterval, autoRotateInterval;
let moving = false, rotating = false;

// Hàm tự động di chuyển theo hình vuông
function autoMoveSquare() {
    if (moving) {
        moving = false;
        return;
    }
    moving = true;

    let step = 0;
    const stepSize = 0.1; 
    const positions = [
        { x: -0.1, y: 0.1 }, { x: 0.1, y: 0.1 },
        { x: 0.1, y: -0.1 }, { x: -0.1, y: -0.1 }
    ];
    
    let target = positions[step]; 

    function move() {
        if (!moving) return;

        translateX += (target.x - translateX) * stepSize;
        translateY += (target.y - translateY) * stepSize;

        draw();

        if (Math.abs(target.x - translateX) < 0.001 && Math.abs(target.y - translateY) < 0.001) {
            step = (step + 1) % positions.length;
            target = positions[step];
        }

        requestAnimationFrame(move);
    }

    move();
}

// Tự động xoay mượt
let lastTime = 0;
function smoothRotate(timestamp) {
    if (!rotating) return;

    if (!lastTime) lastTime = timestamp;
    let deltaTime = (timestamp - lastTime) / 1000; 
    lastTime = timestamp;

    angle = (angle + deltaTime * 90) % 360; // Quay 90 độ mỗi giây (có thể điều chỉnh)
    draw();

    requestAnimationFrame(smoothRotate);
}
function autoRotate() {
    if (rotating) {
        rotating = false;
        return;
    }
    rotating = true;
    requestAnimationFrame(smoothRotate);
}

// Hàm reset về vị trí ban đầu
function resetTransform() {
    clearInterval(autoMoveInterval);
    clearInterval(autoRotateInterval);
    moving = false;
    rotating = false;

    // Reset các giá trị biến đổi
    translateX = 0;
    translateY = 0;
    angle = 0;
    scaleX = 1;
    scaleY = 1;
    draw();
}

// Thêm sự kiện cho nút
document.getElementById("autoMove").addEventListener("click", autoMoveSquare);
document.getElementById("autoRotate").addEventListener("click", autoRotate);
document.getElementById("reset").addEventListener("click", resetTransform);
