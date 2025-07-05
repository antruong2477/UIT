function init() {
    var scene = new THREE.Scene();

    var box = getBox(1, 1, 1);
    var sphere = getSphere(0.5);
    var torus = getTorus(0.4, 0.15);
    var plane = getPlane(4);

    box.position.set(-1, box.geometry.parameters.height / 2, 0);
    sphere.position.set(1, 0.5, 0);
    torus.position.set(0, 0.5, 1);
    plane.rotation.x = Math.PI / 2;

    scene.add(box);
    scene.add(sphere);
    scene.add(torus);
    scene.add(plane);

    var camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 1000);
    camera.position.set(1, 2, 5);
    camera.lookAt(new THREE.Vector3(0, 0, 0));

    var renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.getElementById("webgl").appendChild(renderer.domElement);
    renderer.render(scene, camera);
}

function getBox(w, h, d) {
    var geometry = new THREE.BoxGeometry(w, d, h);
    var material = new THREE.MeshBasicMaterial({ color: 0xff0000 });
    return new THREE.Mesh(geometry, material);
}

function getSphere(radius) {
    var geometry = new THREE.SphereGeometry(radius, 32, 32);
    var material = new THREE.MeshBasicMaterial({ color: 0x0000ff });
    return new THREE.Mesh(geometry, material);
}

function getTorus(radius, tube) {
    var geometry = new THREE.TorusGeometry(radius, tube, 16, 100);
    var material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    return new THREE.Mesh(geometry, material);
}

function getPlane(size) {
    var geometry = new THREE.PlaneGeometry(size, size);
    var material = new THREE.MeshBasicMaterial({ color: 0x888888, side: THREE.DoubleSide });
    return new THREE.Mesh(geometry, material);
}

init();