import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function webglAvailable() {
  try {
    const canvas = document.createElement("canvas");
    return !!(window.WebGLRenderingContext && (canvas.getContext("webgl2") || canvas.getContext("webgl")));
  } catch (err) {
    return false;
  }
}

function initViewer(block) {
  if (block.dataset.viewerReady) return;
  block.dataset.viewerReady = "1";

  const stage = block.querySelector(".viewer-stage");
  const poster = block.querySelector(".viewer-poster");
  const loaderEl = block.querySelector("[data-viewer-loader]");
  const errorEl = block.querySelector("[data-viewer-error]");
  const bar = block.querySelector(".viewer-bar i");
  const rotateBtn = block.querySelector("[data-viewer-rotate]");
  const resetBtn = block.querySelector("[data-viewer-reset]");
  const fsBtn = block.querySelector("[data-viewer-fullscreen]");
  const modelUrl = block.dataset.model;
  const modelName = block.dataset.name || "this room";

  const fail = (message) => {
    block.dataset.state = "error";
    if (loaderEl) loaderEl.classList.add("is-hidden");
    if (errorEl) {
      const span = errorEl.querySelector("span");
      if (span) span.textContent = message;
      errorEl.hidden = false;
    }
    if (poster) poster.style.opacity = "";
  };

  if (!modelUrl) {
    fail("No model was specified for this room.");
    return;
  }
  if (!webglAvailable()) {
    fail("This browser cannot show WebGL 3D. The render above still shows the room.");
    return;
  }

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
  } catch (err) {
    fail("The 3D preview could not start on this device. The render above still shows the room.");
    return;
  }

  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.02;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  stage.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  scene.background = new THREE.Color("#e8dece");

  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  pmrem.dispose();

  scene.add(new THREE.HemisphereLight(0xfff3e0, 0x6f5c45, 1.15));

  const key = new THREE.DirectionalLight(0xffe3bd, 2.5);
  key.position.set(5, 6, 6);
  key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024);
  key.shadow.camera.left = -6;
  key.shadow.camera.right = 6;
  key.shadow.camera.top = 6;
  key.shadow.camera.bottom = -6;
  key.shadow.camera.near = 0.5;
  key.shadow.camera.far = 24;
  key.shadow.bias = -0.0004;
  key.shadow.normalBias = 0.02;
  key.target.position.set(0, 1, 0);
  scene.add(key, key.target);

  const fill = new THREE.DirectionalLight(0xfff6ea, 0.55);
  fill.position.set(-5, 4, 3);
  scene.add(fill);

  const camera = new THREE.PerspectiveCamera(40, 1, 0.1, 100);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.06;
  controls.enablePan = false;
  controls.rotateSpeed = 0.7;
  controls.zoomSpeed = 0.8;
  controls.autoRotate = false;
  controls.autoRotateSpeed = 0.5;
  controls.minPolarAngle = 0.15;
  controls.maxPolarAngle = Math.PI / 2 - 0.08;

  let startPosition = new THREE.Vector3(4, 4.2, 4.6);
  let startTarget = new THREE.Vector3(0, 1, 0);
  camera.position.copy(startPosition);
  controls.target.copy(startTarget);
  controls.update();

  const setAutoRotate = (on) => {
    controls.autoRotate = on;
    if (rotateBtn) {
      rotateBtn.setAttribute("aria-pressed", String(on));
      rotateBtn.textContent = on ? "Auto-rotate: on" : "Auto-rotate: off";
    }
  };
  setAutoRotate(!reduceMotion);

  const reset = () => {
    camera.position.copy(startPosition);
    controls.target.copy(startTarget);
    controls.update();
    setAutoRotate(!reduceMotion);
  };

  const resize = () => {
    const rect = stage.getBoundingClientRect();
    const width = Math.max(1, Math.round(rect.width));
    const height = Math.max(1, Math.round(rect.height));
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
  };
  resize();
  const resizeObserver = new ResizeObserver(resize);
  resizeObserver.observe(stage);

  let onScreen = false;
  let pageVisible = !document.hidden;
  let rafId = null;
  const tick = () => {
    rafId = null;
    if (!onScreen || !pageVisible) return;
    controls.update();
    renderer.render(scene, camera);
    rafId = requestAnimationFrame(tick);
  };
  const start = () => {
    if (rafId === null) rafId = requestAnimationFrame(tick);
  };
  const applyRunning = () => {
    if (onScreen && pageVisible) start();
  };
  const screenObserver = new IntersectionObserver(
    (entries) => {
      onScreen = entries.some((entry) => entry.isIntersecting);
      applyRunning();
    },
    { threshold: 0.01 }
  );
  screenObserver.observe(stage);
  document.addEventListener("visibilitychange", () => {
    pageVisible = !document.hidden;
    applyRunning();
  });

  controls.addEventListener("start", () => {
    if (controls.autoRotate) setAutoRotate(false);
  });

  stage.addEventListener("pointerdown", () => stage.focus({ preventScroll: true }));

  stage.addEventListener("keydown", (event) => {
    const keys = ["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "+", "=", "-", "0"];
    if (!keys.includes(event.key)) return;
    event.preventDefault();
    if (event.key === "0") {
      reset();
      return;
    }
    const offset = camera.position.clone().sub(controls.target);
    const spherical = new THREE.Spherical().setFromVector3(offset);
    if (event.key === "ArrowLeft") spherical.theta += 0.14;
    if (event.key === "ArrowRight") spherical.theta -= 0.14;
    if (event.key === "ArrowUp") spherical.phi = Math.max(controls.minPolarAngle, spherical.phi - 0.09);
    if (event.key === "ArrowDown") spherical.phi = Math.min(controls.maxPolarAngle, spherical.phi + 0.09);
    if (event.key === "+" || event.key === "=") spherical.radius = Math.max(controls.minDistance, spherical.radius * 0.92);
    if (event.key === "-") spherical.radius = Math.min(controls.maxDistance, spherical.radius * 1.08);
    camera.position.copy(controls.target).add(new THREE.Vector3().setFromSpherical(spherical));
    setAutoRotate(false);
    controls.update();
  });

  rotateBtn?.addEventListener("click", () => setAutoRotate(!controls.autoRotate));
  resetBtn?.addEventListener("click", reset);
  fsBtn?.addEventListener("click", async () => {
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else await block.requestFullscreen();
    } catch (err) {
      /* ignore fullscreen refusal */
    }
  });
  document.addEventListener("fullscreenchange", () => {
    const active = document.fullscreenElement === block;
    fsBtn.textContent = active ? "Exit fullscreen" : "Fullscreen";
    fsBtn.setAttribute("aria-pressed", String(active));
    setTimeout(resize, 80);
  });

  if (!block.requestFullscreen && fsBtn) fsBtn.hidden = true;

  const loader = new GLTFLoader();
  loader.load(
    modelUrl,
    (gltf) => {
      const root = gltf.scene;
      let meshes = 0;
      root.traverse((obj) => {
        if (!obj.isMesh) return;
        meshes += 1;
        obj.castShadow = true;
        obj.receiveShadow = true;
        const materials = Array.isArray(obj.material) ? obj.material : [obj.material];
        materials.forEach((material) => {
          if (!material) return;
          if ("envMapIntensity" in material) material.envMapIntensity = 0.5;
          if (material.emissiveIntensity > 2) material.emissiveIntensity = 2;
          material.needsUpdate = true;
        });
      });
      scene.add(root);

      const box = new THREE.Box3().setFromObject(root);
      const size = box.getSize(new THREE.Vector3());
      const center = box.getCenter(new THREE.Vector3());

      const plinth = new THREE.Mesh(
        new THREE.BoxGeometry(size.x + 0.16, 0.12, size.z + 0.16),
        new THREE.MeshStandardMaterial({ color: "#d8c9b4", roughness: 0.95 })
      );
      plinth.position.set(center.x, -0.065, center.z);
      plinth.castShadow = true;
      plinth.receiveShadow = true;
      scene.add(plinth);

      startTarget = new THREE.Vector3(center.x, 1.0, center.z);
      const radius = Math.max(size.x, size.z, 3.4) * 1.25;
      startPosition = startTarget.clone().add(new THREE.Vector3(radius * 0.62, radius * 0.52, radius * 0.72));

      camera.position.copy(startPosition);
      controls.target.copy(startTarget);
      controls.minDistance = Math.max(2, radius * 0.4);
      controls.maxDistance = radius * 2.4;
      controls.update();

      block.dataset.state = "ready";
      block.dataset.meshes = String(meshes);
      block.__viewer = { camera, controls, reset, setAutoRotate };
      stage.classList.add("is-ready");
      if (loaderEl) loaderEl.classList.add("is-hidden");
      if (poster) poster.setAttribute("aria-hidden", "true");
      [rotateBtn, resetBtn, fsBtn].forEach((button) => {
        if (button) button.disabled = false;
      });
      resize();
    },
    (event) => {
      if (!bar || !event.total) return;
      bar.style.width = `${Math.min(100, Math.round((event.loaded / event.total) * 100))}%`;
    },
    (err) => {
      console.error("3D model failed to load:", err);
      fail("The 3D model could not load. The render above still shows the room.");
    }
  );
}

const blocks = [...document.querySelectorAll("[data-3d]")];
if (blocks.length) {
  if (!("IntersectionObserver" in window)) {
    blocks.forEach(initViewer);
  } else {
    const initObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          observer.unobserve(entry.target);
          initViewer(entry.target);
        });
      },
      { rootMargin: "600px 0px" }
    );
    blocks.forEach((block) => initObserver.observe(block));
  }
}
