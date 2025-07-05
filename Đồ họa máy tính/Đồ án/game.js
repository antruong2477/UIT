import * as THREE from "three";
import { PointerLockControls } from "three/examples/jsm/controls/PointerLockControls.js";

let scene, camera, renderer, controls;
let bullets = [];
let enemies = [];
let clock = new THREE.Clock();

init();
animate();

function init() {
    // Renderer
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // Scene & Camera
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    
    // Controls
    controls = new PointerLockControls(camera, document.body);
    document.getElementById("startButton").addEventListener("click", () => {
        controls.lock();
    });

    // Ánh sáng
    let light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(10, 10, 10);
    scene.add(light);

    // Mặt đất
    let floor = new THREE.Mesh(
        new THREE.PlaneGeometry(50, 50),
        new THREE.MeshStandardMaterial({ color: 0x228B22 })
    );
    floor.rotation.x = -Math.PI / 2;
    scene.add(floor);

    // Kẻ địch
    for (let i = 0; i < 5; i++) {
        let enemy = new THREE.Mesh(
            new THREE.SphereGeometry(1),
            new THREE.MeshStandardMaterial({ color: 0xff0000 })
        );
        enemy.position.set(Math.random() * 30 - 15, 1, Math.random() * 30 - 15);
        scene.add(enemy);
        enemies.push(enemy);
    }

    // Lắng nghe sự kiện bàn phím và chuột
    document.addEventListener("keydown", onKeyDown);
    document.addEventListener("click", shoot);
}

// Xử lý di chuyển
const speed = 0.1;
function onKeyDown(event) {
    if (event.code === "KeyW") controls.moveForward(speed);
    if (event.code === "KeyS") controls.moveForward(-speed);
    if (event.code === "KeyA") controls.moveRight(-speed);
    if (event.code === "KeyD") controls.moveRight(speed);
}

// Bắn đạn
function shoot() {
    let bullet = new THREE.Mesh(
        new THREE.SphereGeometry(0.1),
        new THREE.MeshBasicMaterial({ color: 0xffff00 })
    );
    bullet.position.copy(camera.position);
    bullet.velocity = new THREE.Vector3();
    bullet.velocity.set(0, 0, -1).applyQuaternion(camera.quaternion);
    scene.add(bullet);
    bullets.push(bullet);
}

// Cập nhật đạn và kiểm tra va chạm
function updateBullets() {
    bullets.forEach((bullet, index) => {
        bullet.position.add(bullet.velocity.clone().multiplyScalar(0.5));
        
        enemies.forEach((enemy, eIndex) => {
            if (bullet.position.distanceTo(enemy.position) < 1) {
                scene.remove(enemy);
                enemies.splice(eIndex, 1);
                scene.remove(bullet);
                bullets.splice(index, 1);
            }
        });

        if (bullet.position.length() > 50) {
            scene.remove(bullet);
            bullets.splice(index, 1);
        }
    });
}

// Cập nhật kẻ địch di chuyển ngẫu nhiên
function updateEnemies() {
    enemies.forEach(enemy => {
        enemy.position.x += (Math.random() - 0.5) * 0.1;
        enemy.position.z += (Math.random() - 0.5) * 0.1;
    });
}

// Vòng lặp render
function animate() {
    requestAnimationFrame(animate);
    updateBullets();
    updateEnemies();
    renderer.render(scene, camera);
}

