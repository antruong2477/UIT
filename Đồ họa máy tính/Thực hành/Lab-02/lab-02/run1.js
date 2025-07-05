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
    void main() {
        float rad = radians(u_angle);
        mat2 rotation = mat2(cos(rad), -sin(rad), sin(rad), cos(rad));
        vec2 scaledPos = a_position * u_scale;
        vec2 rotatedPos = rotation * scaledPos;
        gl_Position = vec4(rotatedPos + u_translation, 0, 1);
    }
`;

// Shader màu (fragment shader)
const fragmentShaderSource = `
    precision mediump float;
    void main() {
        gl_FragColor = vec4(0.2, 0.8, 1.0, 1.0); // Màu xanh dương nhạt
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

// Dữ liệu tọa độ đỉnh cho chữ "F"
const fVertices = new Float32Array([
    // Cột dọc
    0, 0,   0.1, 0,   0, 0.6,
    0, 0.6, 0.1, 0,   0.1, 0.6,

    // Thanh ngang trên
    0, 0.5, 0.4, 0.5, 0, 0.6,
    0, 0.6, 0.4, 0.5, 0.4, 0.6,

    // Thanh ngang giữa
    0, 0.25, 0.3, 0.25, 0, 0.35,
    0, 0.35, 0.3, 0.25, 0.3, 0.35
]);

// Tạo buffer và nạp dữ liệu vào GPU
const positionBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
gl.bufferData(gl.ARRAY_BUFFER, fVertices, gl.STATIC_DRAW);
gl.enableVertexAttribArray(positionAttributeLocation);
gl.vertexAttribPointer(positionAttributeLocation, 2, gl.FLOAT, false, 0, 0);

// Giá trị mặc định của các biến
let translateX = 0, translateY = 0, angle = 0, scaleX = 1, scaleY = 1;

// Cập nhật giá trị khi người dùng thay đổi thanh trượt
document.getElementById("translateX").oninput = (e) => { translateX = parseFloat(e.target.value); draw(); };
document.getElementById("translateY").oninput = (e) => { translateY = parseFloat(e.target.value); draw(); };
document.getElementById("angle").oninput = (e) => { angle = parseFloat(e.target.value); draw(); };
document.getElementById("scaleX").oninput = (e) => { scaleX = parseFloat(e.target.value); draw(); };
document.getElementById("scaleY").oninput = (e) => { scaleY = parseFloat(e.target.value); draw(); };

// Hàm vẽ
function draw() {
    gl.clearColor(1, 1, 1, 1);
    gl.clear(gl.COLOR_BUFFER_BIT);

    gl.uniform2f(translationUniformLocation, translateX, translateY);
    gl.uniform1f(angleUniformLocation, angle);
    gl.uniform2f(scaleUniformLocation, scaleX, scaleY);

    gl.drawArrays(gl.TRIANGLES, 0, fVertices.length / 2);
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
