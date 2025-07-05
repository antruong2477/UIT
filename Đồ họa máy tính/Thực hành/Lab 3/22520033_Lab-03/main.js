"use strict";

// Initialize WebGL
const canvas = document.getElementById("canvas");
// Initialize the GL context
const gl = canvas.getContext("webgl");

if (!gl) {
  console.error("WebGL not supported");
}

// Setup canvas and viewport
function resizeCanvasToDisplaySize(canvas) {
  const displayWidth = canvas.clientWidth;
  const displayHeight = canvas.clientHeight;

  if (canvas.width !== displayWidth || canvas.height !== displayHeight) {
    canvas.width = displayWidth;
    canvas.height = displayHeight;
    gl.viewport(0, 0, canvas.width, canvas.height);
  }
}

// Simple vertex shader for 2D drawing
const vsSource = `
attribute vec4 a_position;
uniform mat4 u_matrix;

void main() {
  gl_Position = u_matrix * a_position;
  gl_PointSize = 5.0;
}
`;

// Simple fragment shader for 2D drawing
const fsSource = `
precision mediump float;
uniform vec4 u_color;

void main() {
  gl_FragColor = u_color;
}
`;

// Initialize shaders
const shaderProgram = initShaderProgram(gl, vsSource, fsSource);

// Collect all shader program info
const programInfo = {
  program: shaderProgram,
  attribLocations: {
    vertexPosition: gl.getAttribLocation(shaderProgram, 'a_position'),
  },
  uniformLocations: {
    matrix: gl.getUniformLocation(shaderProgram, 'u_matrix'),
    color: gl.getUniformLocation(shaderProgram, 'u_color'),
  },
};

// Create a buffer for positions
const positionBuffer = gl.createBuffer();

// Set up event listeners
document.getElementById('draw-function').addEventListener('click', drawFunction);
document.getElementById('draw-bezier').addEventListener('click', drawBezier);
document.getElementById('draw-hermit').addEventListener('click', drawHermit);
document.getElementById('draw-flower').addEventListener('click', drawFlower);

document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    tab.classList.add('active');
    const activeTab = document.getElementById(tab.dataset.tab);
    activeTab.classList.add('active');
    
    console.log(activeTab.id);

    if (activeTab.id === 'function') {
      drawFunction();
    } else if (activeTab.id === 'bezier') {
        drawBezier();
    } else if (activeTab.id === 'hermit') {
      drawHermit();
    } else if (activeTab.id === 'flower') {
      drawFlower();
    }
  });
});

// Function to initialize shader program
function initShaderProgram(gl, vsSource, fsSource) {
  const vertexShader = loadShader(gl, gl.VERTEX_SHADER, vsSource);
  const fragmentShader = loadShader(gl, gl.FRAGMENT_SHADER, fsSource);

  // Create the shader program
  const shaderProgram = gl.createProgram();
  gl.attachShader(shaderProgram, vertexShader);
  gl.attachShader(shaderProgram, fragmentShader);
  gl.linkProgram(shaderProgram);

  // If creating the shader program failed, alert
  if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
    console.error(`Unable to initialize the shader program: ${gl.getProgramInfoLog(shaderProgram)}`);
    return null;
  }

  return shaderProgram;
}

// Function to load a shader
function loadShader(gl, type, source) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);

  // Check if compilation was successful
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    console.error(`An error occurred compiling the shaders: ${gl.getShaderInfoLog(shader)}`);
    gl.deleteShader(shader);
    return null;
  }

  return shader;
}

// Create projection matrix for 2D drawing
function createProjectionMatrix(width, height, minX, maxX, minY, maxY) {
  // Map from pixels to clip space
  const scaleX = 2 / (maxX - minX);
  const scaleY = 2 / (maxY - minY);
  const translateX = -minX * scaleX - 1;
  const translateY = -minY * scaleY - 1;

  return [
    scaleX, 0, 0, 0,
    0, scaleY, 0, 0,
    0, 0, 1, 0,
    translateX, translateY, 0, 1
  ];
}

// Clear the canvas with a white background
function clearCanvas() {
  resizeCanvasToDisplaySize(canvas);
  gl.clearColor(1.0, 1.0, 1.0, 1.0);
  gl.clear(gl.COLOR_BUFFER_BIT);
}

// Draw coordinate axes
function drawAxes(minX, maxX, minY, maxY) {
  // Create the axes vertices
  const axesVertices = [
    minX, 0.0, 0.0,  // X-axis start
    maxX, 0.0, 0.0,  // X-axis end
    0.0, minY, 0.0,  // Y-axis start
    0.0, maxY, 0.0,  // Y-axis end
  ];

  // Bind the axes buffer
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(axesVertices), gl.STATIC_DRAW);

  // Set up attributes
  gl.vertexAttribPointer(programInfo.attribLocations.vertexPosition, 3, gl.FLOAT, false, 0, 0);
  gl.enableVertexAttribArray(programInfo.attribLocations.vertexPosition);

  // Set color to black for axes
  gl.uniform4fv(programInfo.uniformLocations.color, [0.0, 0.0, 0.0, 1.0]);

  // Draw the X and Y axes
  gl.drawArrays(gl.LINES, 0, 4);
}

// Draw grid lines
function drawGrid(minX, maxX, minY, maxY) {
  const gridVertices = [];
  const gridSpacing = 1.0; // 1 unit spacing

  // Vertical grid lines
  for (let x = Math.ceil(minX / gridSpacing) * gridSpacing; x <= maxX; x += gridSpacing) {
    if (Math.abs(x) < 0.1) continue; // Skip near the main axis
    gridVertices.push(x, minY, 0.0);
    gridVertices.push(x, maxY, 0.0);
  }

  // Horizontal grid lines
  for (let y = Math.ceil(minY / gridSpacing) * gridSpacing; y <= maxY; y += gridSpacing) {
    if (Math.abs(y) < 0.1) continue; // Skip near the main axis
    gridVertices.push(minX, y, 0.0);
    gridVertices.push(maxX, y, 0.0);
  }

  if (gridVertices.length === 0) return; // No grid lines to draw

  // Bind the grid buffer
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(gridVertices), gl.STATIC_DRAW);

  // Set up attributes
  gl.vertexAttribPointer(programInfo.attribLocations.vertexPosition, 3, gl.FLOAT, false, 0, 0);
  gl.enableVertexAttribArray(programInfo.attribLocations.vertexPosition);

  // Set color to light gray for grid
  gl.uniform4fv(programInfo.uniformLocations.color, [0.8, 0.8, 0.8, 1.0]);

  // Draw the grid lines
  gl.drawArrays(gl.LINES, 0, gridVertices.length / 3);
}

// 1. Function to draw a mathematical function curve
function drawFunction() {
  clearCanvas();

  // Get the function and range from inputs
  let functionExpr = document.getElementById('func-expression').value;
  functionExpr = functionExpr.replace(/cos/g, "Math.cos").replace(/sin/g, "Math.sin").replace(/tan/g, "Math.tan");
  const minX = parseFloat(document.getElementById('range-min').value);
  const maxX = parseFloat(document.getElementById('range-max').value);

  // Calculate a reasonable range for Y based on the function values
  let minY = Number.MAX_VALUE;
  let maxY = Number.MIN_VALUE;
  
  // Sample the function to determine the Y range
  const points = [];
  const numSamples = 100;
  
  for (let i = 0; i <= numSamples; i++) {
    const x = minX + (maxX - minX) * (i / numSamples);
    
    // Evaluate the function
    let y;
    try {
      // Create a safe function evaluation
      const f = new Function('x', `return ${functionExpr};`);
      y = f(x);
      
      if (isNaN(y) || !isFinite(y)) continue;
      
      minY = Math.min(minY, y);
      maxY = Math.max(maxY, y);
      
      points.push(x, y, 0);
    } catch (e) {
      console.error("Error evaluating function:", e);
      return;
    }
  }
  
  // Ensure the Y range is reasonable and not too flat
  if (minY === maxY) {
    minY -= 1;
    maxY += 1;
  } else {
    // Add some padding to the Y range
    const padding = (maxY - minY) * 0.1;
    minY -= padding;
    maxY += padding;
  }
  
  // Create a projection matrix for the coordinate system
  const projectionMatrix = createProjectionMatrix(canvas.width, canvas.height, minX, maxX, minY, maxY);
  
  // Use the shader program
  gl.useProgram(programInfo.program);
  
  // Set the projection matrix
  gl.uniformMatrix4fv(programInfo.uniformLocations.matrix, false, projectionMatrix);
  
  // Draw the coordinate axes and grid
  drawGrid(minX, maxX, minY, maxY);
  drawAxes(minX, maxX, minY, maxY);
  
  // Bind the buffer with the function points
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(points), gl.STATIC_DRAW);
  
  // Set up attributes
  gl.vertexAttribPointer(programInfo.attribLocations.vertexPosition, 3, gl.FLOAT, false, 0, 0);
  gl.enableVertexAttribArray(programInfo.attribLocations.vertexPosition);
  
  gl.uniform4fv(programInfo.uniformLocations.color, [1.0, 0.7, 0.8, 1.0]);
  
  // Draw the function curve
  gl.drawArrays(gl.LINE_STRIP, 0, points.length / 3);
}

// 2. Function to draw a Bezier curve
function drawBezier() {
  clearCanvas();
  
  // Get control points from the textarea
  const pointsText = document.getElementById('bezier-points').value;
  const controlPoints = [];
  
  // Parse the control points
  pointsText.split('\n').forEach(line => {
    const [x, y] = line.split(',').map(val => parseFloat(val.trim()));
    if (!isNaN(x) && !isNaN(y)) {
      controlPoints.push(x, y);
    }
  });
  
  if (controlPoints.length < 4 || controlPoints.length % 2 !== 0) {
    console.error("Need at least 2 valid control points");
    return;
  }
  
  // Calculate the bounds for the viewport
  let minX = Number.MAX_VALUE;
  let maxX = Number.MIN_VALUE;
  let minY = Number.MAX_VALUE;
  let maxY = Number.MIN_VALUE;
  
  for (let i = 0; i < controlPoints.length; i += 2) {
    minX = Math.min(minX, controlPoints[i]);
    maxX = Math.max(maxX, controlPoints[i]);
    minY = Math.min(minY, controlPoints[i + 1]);
    maxY = Math.max(maxY, controlPoints[i + 1]);
  }
  
  // Add some padding
  const paddingX = (maxX - minX) * 0.1;
  const paddingY = (maxY - minY) * 0.1;
  minX -= paddingX;
  maxX += paddingX;
  minY -= paddingY;
  maxY += paddingY;
  
  // Ensure minimum size
  if (maxX - minX < 2) {
    const center = (minX + maxX) / 2;
    minX = center - 1;
    maxX = center + 1;
  }
  if (maxY - minY < 2) {
    const center = (minY + maxY) / 2;
    minY = center - 1;
    maxY = center + 1;
  }
  
  // Create a projection matrix for the coordinate system
  const projectionMatrix = createProjectionMatrix(canvas.width, canvas.height, minX, maxX, minY, maxY);
  
  // Use the shader program
  gl.useProgram(programInfo.program);
  
  // Set the projection matrix
  gl.uniformMatrix4fv(programInfo.uniformLocations.matrix, false, projectionMatrix);
  
  // Draw the coordinate axes and grid
  drawGrid(minX, maxX, minY, maxY);
  drawAxes(minX, maxX, minY, maxY);
  
  // Draw control points
  const controlPointsWithZ = [];
  for (let i = 0; i < controlPoints.length; i += 2) {
    controlPointsWithZ.push(controlPoints[i], controlPoints[i + 1], 0);
  }
  
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(controlPointsWithZ), gl.STATIC_DRAW);
  gl.vertexAttribPointer(programInfo.attribLocations.vertexPosition, 3, gl.FLOAT, false, 0, 0);
  gl.enableVertexAttribArray(programInfo.attribLocations.vertexPosition);
  
  // Set color to red for control points
  gl.uniform4fv(programInfo.uniformLocations.color, [1.0, 0.0, 0.0, 1.0]);
  
  // Draw the control points
  gl.drawArrays(gl.POINTS, 0, controlPointsWithZ.length / 3);
  
  // Draw lines connecting control points
  gl.uniform4fv(programInfo.uniformLocations.color, [0.6, 1.0, 0.6, 1.0]);
  gl.drawArrays(gl.LINE_STRIP, 0, controlPointsWithZ.length / 3);
  
  // Generate Bezier curve points
  const numPoints = 100;
  const curvePoints = [];
  
  for (let i = 0; i <= numPoints; i++) {
    const t = i / numPoints;
    const point = bezierPoint(controlPoints, t);
    curvePoints.push(point.x, point.y, 0);
  }
  
  // Draw Bezier curve
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(curvePoints), gl.STATIC_DRAW);
  gl.vertexAttribPointer(programInfo.attribLocations.vertexPosition, 3, gl.FLOAT, false, 0, 0);
  gl.enableVertexAttribArray(programInfo.attribLocations.vertexPosition);
  
  gl.uniform4fv(programInfo.uniformLocations.color, [1.0, 0.7, 0.8, 1.0]);
  
  // Draw the Bezier curve
  gl.drawArrays(gl.LINE_STRIP, 0, curvePoints.length / 3);
}

// Function to calculate a point on a Bezier curve
function bezierPoint(controlPoints, t) {
  const n = controlPoints.length / 2 - 1; // Degree of the Bezier curve
  let x = 0;
  let y = 0;
  
  for (let i = 0; i <= n; i++) {
    const coefficient = binomialCoefficient(n, i) * Math.pow(1 - t, n - i) * Math.pow(t, i);
    x += coefficient * controlPoints[i * 2];
    y += coefficient * controlPoints[i * 2 + 1];
  }
  
  return { x, y };
}

// Function to calculate binomial coefficient (n choose k)
function binomialCoefficient(n, k) {
  if (k < 0 || k > n) return 0;
  if (k === 0 || k === n) return 1;
  
  let result = 1;
  for (let i = 1; i <= k; i++) {
    result *= (n - (k - i));
    result /= i;
  }
  
  return result;
}

// 3. Function to draw a Hermit curve
function drawHermit() {
  clearCanvas();
  
  // Get the input points and vectors
  const p1 = {
    x: parseFloat(document.getElementById('p1-x').value),
    y: parseFloat(document.getElementById('p1-y').value)
  };
  
  const p2 = {
    x: parseFloat(document.getElementById('p2-x').value),
    y: parseFloat(document.getElementById('p2-y').value)
  };
  
  const v1 = {
    x: parseFloat(document.getElementById('v1-x').value),
    y: parseFloat(document.getElementById('v1-y').value)
  };
  
  const v2 = {
    x: parseFloat(document.getElementById('v2-x').value),
    y: parseFloat(document.getElementById('v2-y').value)
  };
  
  // Calculate bounds for viewport
  let minX = Math.min(p1.x, p2.x);
  let maxX = Math.max(p1.x, p2.x);
  let minY = Math.min(p1.y, p2.y);
  let maxY = Math.max(p1.y, p2.y);
  
  // Extend bounds considering tangent vectors
  minX = Math.min(minX, p1.x + v1.x, p2.x + v2.x);
  maxX = Math.max(maxX, p1.x + v1.x, p2.x + v2.x);
  minY = Math.min(minY, p1.y + v1.y, p2.y + v2.y);
  maxY = Math.max(maxY, p1.y + v1.y, p2.y + v2.y);
  
  // Add padding
  const paddingX = (maxX - minX) * 0.2;
  const paddingY = (maxY - minY) * 0.2;
  minX -= paddingX;
  maxX += paddingX;
  minY -= paddingY;
  maxY += paddingY;
  
  // Ensure minimum size
  if (maxX - minX < 2) {
    const center = (minX + maxX) / 2;
    minX = center - 1;
    maxX = center + 1;
  }
  if (maxY - minY < 2) {
    const center = (minY + maxY) / 2;
    minY = center - 1;
    maxY = center + 1;
  }
  
  // Create a projection matrix for the coordinate system
  const projectionMatrix = createProjectionMatrix(canvas.width, canvas.height, minX, maxX, minY, maxY);
  
  // Use the shader program
  gl.useProgram(programInfo.program);
  
  // Set the projection matrix
  gl.uniformMatrix4fv(programInfo.uniformLocations.matrix, false, projectionMatrix);
  
  // Draw the coordinate axes and grid
  drawGrid(minX, maxX, minY, maxY);
  drawAxes(minX, maxX, minY, maxY);
  
  // Draw points
  const pointsWithZ = [
    p1.x, p1.y, 0,
    p2.x, p2.y, 0
  ];
  
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(pointsWithZ), gl.STATIC_DRAW);
  gl.vertexAttribPointer(programInfo.attribLocations.vertexPosition, 3, gl.FLOAT, false, 0, 0);
  gl.enableVertexAttribArray(programInfo.attribLocations.vertexPosition);
  
  // Set color to red for points
  gl.uniform4fv(programInfo.uniformLocations.color, [1.0, 0.0, 0.0, 1.0]);
  
  // Draw the points
  gl.drawArrays(gl.POINTS, 0, 2);
  
  // Draw vectors
  const vectorsWithZ = [
    p1.x, p1.y, 0,
    p1.x + v1.x, p1.y + v1.y, 0,
    p2.x, p2.y, 0,
    p2.x + v2.x, p2.y + v2.y, 0
  ];
  
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vectorsWithZ), gl.STATIC_DRAW);
  gl.vertexAttribPointer(programInfo.attribLocations.vertexPosition, 3, gl.FLOAT, false, 0, 0);
  gl.enableVertexAttribArray(programInfo.attribLocations.vertexPosition);
  
  // Set color to orange for vectors
  gl.uniform4fv(programInfo.uniformLocations.color, [0.6, 1.0, 0.6, 1.0]);
  
  // Draw the vectors as lines
  gl.drawArrays(gl.LINES, 0, 4);
  
  // Generate Hermit curve points
  const numPoints = 100;
  const curvePoints = [];
  
  for (let i = 0; i <= numPoints; i++) {
    const t = i / numPoints;
    const point = hermitPoint(p1, p2, v1, v2, t);
    curvePoints.push(point.x, point.y, 0);
  }
  
  // Draw Hermit curve
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(curvePoints), gl.STATIC_DRAW);
  gl.vertexAttribPointer(programInfo.attribLocations.vertexPosition, 3, gl.FLOAT, false, 0, 0);
  gl.enableVertexAttribArray(programInfo.attribLocations.vertexPosition);
  
  gl.uniform4fv(programInfo.uniformLocations.color,  [1.0, 0.7, 0.8, 1.0]);
  
  // Draw the Hermit curve
  gl.drawArrays(gl.LINE_STRIP, 0, curvePoints.length / 3);
}

// Function to calculate a point on a Hermit curve
function hermitPoint(p1, p2, v1, v2, t) {
  // Hermite basis functions
  const h1 = 2*t*t*t - 3*t*t + 1;
  const h2 = -2*t*t*t + 3*t*t;
  const h3 = t*t*t - 2*t*t + t;
  const h4 = t*t*t - t*t;
  
  // Calculate point coordinates
  const x = h1 * p1.x + h2 * p2.x + h3 * v1.x + h4 * v2.x;
  const y = h1 * p1.y + h2 * p2.y + h3 * v1.y + h4 * v2.y;
  
  return { x, y };
}

// 4. Function to draw a flower petal using parametric equations
function drawFlower() {
  clearCanvas();
  
  // Get the number of petals from input
  const petalCount = parseInt(document.getElementById('petal-count').value) || 5;
  
  // Define the bounds for the viewport
  const minX = -1.5;
  const maxX = 1.5;
  const minY = -1.5;
  const maxY = 1.5;
  
  // Create a projection matrix for the coordinate system
  const projectionMatrix = createProjectionMatrix(canvas.width, canvas.height, minX, maxX, minY, maxY);
  
  // Use the shader program
  gl.useProgram(programInfo.program);
  
  // Set the projection matrix
  gl.uniformMatrix4fv(programInfo.uniformLocations.matrix, false, projectionMatrix);
  
  // Draw the coordinate axes and grid
  drawGrid(minX, maxX, minY, maxY);
  drawAxes(minX, maxX, minY, maxY);
  
  // Generate parametric curve points for flower petal
  const numPoints = 500; // More points for smooth curve
  const curvePoints = [];
  
  for (let i = 0; i <= numPoints; i++) {
    const t = (2 * Math.PI) * (i / numPoints);
    
    let x, y;
 
        if (petalCount % 2 === 1) {
        // For odd numbers of petals (3, 5, 7, etc.)
        x = Math.cos(petalCount * t) * Math.cos(t);
        y = Math.cos(petalCount * t) * Math.sin(t);
        } else {
    
        if (petalCount % 4 === 0) {
    
            x = Math.cos(petalCount / 2 * t) * Math.cos(t);
            y = Math.cos(petalCount / 2 * t) * Math.sin(t);
        } else {
            // For petalsCount = 6, 10, 14, ...
            x = Math.sin(petalCount * t /2) * Math.cos(t/2);
            y = Math.sin(petalCount * t /2) * Math.sin(t/2);
          }
        }
        
        curvePoints.push(x, y, 0);
    }
  
  // Draw the parametric curve
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(curvePoints), gl.STATIC_DRAW);
  gl.vertexAttribPointer(programInfo.attribLocations.vertexPosition, 3, gl.FLOAT, false, 0, 0);
  gl.enableVertexAttribArray(programInfo.attribLocations.vertexPosition);
  
  // Set color to purple for the flower
  gl.uniform4fv(programInfo.uniformLocations.color,  [1.0, 0.7, 0.8, 1.0]);
  
  // Draw the flower curve
  gl.drawArrays(gl.LINE_STRIP, 0, curvePoints.length / 3);
}

// Initialize with the function curve
window.onload = function() {
  drawFunction();
};
