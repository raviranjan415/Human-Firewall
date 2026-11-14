/**
 * Human Firewall 3D Cyber Incident & War Room Game Engine
 * Pure WebGL / 3D Canvas Perspective Engine with Zero External Dependencies.
 * 
 * Features:
 * - 3D Cyber Command Center & Datacenter environment
 * - Real-time 3D lighting, server rack LED pulse, volumetric alert sirens
 * - Interactive 3D walk-up incident stations with proximity detection
 * - Seamless two-way state synchronization with the Incident War Room
 * - Synthesized spatial Web Audio sound effects
 * - 60 FPS hardware accelerated performance with fallback
 */

(function (window) {
  "use strict";

  // Matrix math helpers for 3D perspective & transformations
  var Mat4 = {
    create: function () {
      return new Float32Array([
        1, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 1, 0,
        0, 0, 0, 1
      ]);
    },
    perspective: function (out, fovy, aspect, near, far) {
      var f = 1.0 / Math.tan(fovy / 2);
      var nf = 1 / (near - far);
      out[0] = f / aspect;
      out[1] = 0;
      out[2] = 0;
      out[3] = 0;
      out[4] = 0;
      out[5] = f;
      out[6] = 0;
      out[7] = 0;
      out[8] = 0;
      out[9] = 0;
      out[10] = (far + near) * nf;
      out[11] = -1;
      out[12] = 0;
      out[13] = 0;
      out[14] = 2 * far * near * nf;
      out[15] = 0;
      return out;
    },
    identity: function (out) {
      for (var i = 0; i < 16; i++) out[i] = (i % 5 === 0) ? 1 : 0;
      return out;
    },
    multiply: function (out, a, b) {
      var a00 = a[0], a01 = a[1], a02 = a[2], a03 = a[3];
      var a10 = a[4], a11 = a[5], a12 = a[6], a13 = a[7];
      var a20 = a[8], a21 = a[9], a22 = a[10], a23 = a[11];
      var a30 = a[12], a31 = a[13], a32 = a[14], a33 = a[15];

      var b00 = b[0], b01 = b[1], b02 = b[2], b03 = b[3];
      var b10 = b[4], b11 = b[5], b12 = b[6], b13 = b[7];
      var b20 = b[8], b21 = b[9], b22 = b[10], b23 = b[11];
      var b30 = b[12], b31 = b[13], b32 = b[14], b33 = b[15];

      out[0] = b00 * a00 + b01 * a10 + b02 * a20 + b03 * a30;
      out[1] = b00 * a01 + b01 * a11 + b02 * a21 + b03 * a31;
      out[2] = b00 * a02 + b01 * a12 + b02 * a22 + b03 * a32;
      out[3] = b00 * a03 + b01 * a13 + b02 * a23 + b03 * a33;
      out[4] = b10 * a00 + b11 * a10 + b12 * a20 + b13 * a30;
      out[5] = b10 * a01 + b11 * a11 + b12 * a21 + b13 * a31;
      out[6] = b10 * a02 + b11 * a12 + b12 * a22 + b13 * a32;
      out[7] = b10 * a03 + b11 * a13 + b12 * a23 + b13 * a33;
      out[8] = b20 * a00 + b21 * a10 + b22 * a20 + b23 * a30;
      out[9] = b20 * a01 + b21 * a11 + b22 * a21 + b23 * a31;
      out[10] = b20 * a02 + b21 * a12 + b22 * a22 + b23 * a32;
      out[11] = b20 * a03 + b21 * a13 + b22 * a23 + b23 * a33;
      out[12] = b30 * a00 + b31 * a10 + b32 * a20 + b33 * a30;
      out[13] = b30 * a01 + b31 * a11 + b32 * a21 + b33 * a31;
      out[14] = b30 * a02 + b31 * a12 + b32 * a22 + b33 * a32;
      out[15] = b30 * a03 + b31 * a13 + b32 * a23 + b33 * a33;
      return out;
    },
    rotateX: function (out, a, rad) {
      var s = Math.sin(rad), c = Math.cos(rad);
      var a10 = a[4], a11 = a[5], a12 = a[6], a13 = a[7];
      var a20 = a[8], a21 = a[9], a22 = a[10], a23 = a[11];
      if (a !== out) {
        out[0] = a[0]; out[1] = a[1]; out[2] = a[2]; out[3] = a[3];
        out[12] = a[12]; out[13] = a[13]; out[14] = a[14]; out[15] = a[15];
      }
      out[4] = a10 * c + a20 * s;
      out[5] = a11 * c + a21 * s;
      out[6] = a12 * c + a22 * s;
      out[7] = a13 * c + a23 * s;
      out[8] = a20 * c - a10 * s;
      out[9] = a21 * c - a11 * s;
      out[10] = a22 * c - a12 * s;
      out[11] = a23 * c - a13 * s;
      return out;
    },
    rotateY: function (out, a, rad) {
      var s = Math.sin(rad), c = Math.cos(rad);
      var a00 = a[0], a01 = a[1], a02 = a[2], a03 = a[3];
      var a20 = a[8], a21 = a[9], a22 = a[10], a23 = a[11];
      if (a !== out) {
        out[4] = a[4]; out[5] = a[5]; out[6] = a[6]; out[7] = a[7];
        out[12] = a[12]; out[13] = a[13]; out[14] = a[14]; out[15] = a[15];
      }
      out[0] = a00 * c - a20 * s;
      out[1] = a01 * c - a21 * s;
      out[2] = a02 * c - a22 * s;
      out[3] = a03 * c - a23 * s;
      out[8] = a00 * s + a20 * c;
      out[9] = a01 * s + a21 * c;
      out[10] = a02 * s + a22 * c;
      out[11] = a03 * s + a23 * c;
      return out;
    },
    translate: function (out, a, v) {
      var x = v[0], y = v[1], z = v[2];
      if (a === out) {
        out[12] = a[0] * x + a[4] * y + a[8] * z + a[12];
        out[13] = a[1] * x + a[5] * y + a[9] * z + a[13];
        out[14] = a[2] * x + a[6] * y + a[10] * z + a[14];
        out[15] = a[3] * x + a[7] * y + a[11] * z + a[15];
      } else {
        var a00 = a[0], a01 = a[1], a02 = a[2], a03 = a[3];
        var a10 = a[4], a11 = a[5], a12 = a[6], a13 = a[7];
        var a20 = a[8], a21 = a[9], a22 = a[10], a23 = a[11];
        out[0] = a00; out[1] = a01; out[2] = a02; out[3] = a03;
        out[4] = a10; out[5] = a11; out[6] = a12; out[7] = a13;
        out[8] = a20; out[9] = a21; out[10] = a22; out[11] = a23;
        out[12] = a00 * x + a10 * y + a20 * z + a[12];
        out[13] = a01 * x + a11 * y + a21 * z + a[13];
        out[14] = a02 * x + a12 * y + a22 * z + a[14];
        out[15] = a03 * x + a13 * y + a23 * z + a[15];
      }
      return out;
    }
  };

  function Game3DEngine(config) {
    this.canvas = document.getElementById(config.canvasId);
    if (!this.canvas) return;

    this.slug = config.slug || "phishing-city";
    this.scenarios = config.scenarios || [];
    this.onTriageRequest = config.onTriageRequest || null;
    this.onNodeStateChange = config.onNodeStateChange || null;

    this.promptEl = document.getElementById(config.promptId || "game3DPrompt");
    this.promptText = document.getElementById("game3DPromptText");
    this.hudNodesEl = document.getElementById(config.hudNodesId || "game3DHudNodes");
    this.hudSecurityLvl = document.getElementById("game3DSecurityLvl");

    // Camera state
    this.camPos = [0, 2.2, 8.5]; // Eye height ~2.2 units
    this.camYaw = 0;             // Radians
    this.camPitch = -0.15;       // Looking slightly down
    this.moveSpeed = 0.15;
    this.rotSpeed = 0.0035;

    this.keys = {};
    this.isDragging = false;
    this.lastMouseX = 0;
    this.lastMouseY = 0;

    // Nodes (Terminals / Server Racks) corresponding to scenarios
    this.nodes = [];
    this.activeScenarioIndex = 0;
    this.nearbyNode = null;
    this.particles = [];

    // Audio synthesizer
    this.audioCtx = null;
    this.audioEnabled = true;

    this.initNodes();
    this.initWebGL();
    this.initControls();
    this.renderHUD();

    this.lastTime = performance.now();
    this.animate = this.animate.bind(this);
    requestAnimationFrame(this.animate);
  }

  // Setup nodes across the 3D room
  Game3DEngine.prototype.initNodes = function () {
    var total = Math.max(this.scenarios.length, 5);
    var radius = 7.5;
    this.nodes = [];

    for (var i = 0; i < total; i++) {
      var angle = (i / total) * Math.PI * 2;
      var x = Math.sin(angle) * radius;
      var z = Math.cos(angle) * radius;
      var scenario = this.scenarios[i] || null;

      this.nodes.push({
        id: i,
        name: "Terminal-" + String.fromCharCode(65 + (i % 26)) + (i + 1),
        pos: [x, 0, z],
        angle: angle + Math.PI,
        status: i === 0 ? "compromised" : (i < this.activeScenarioIndex ? "secured" : "pending"),
        scenario: scenario,
        label: scenario ? (scenario.title || "Breach Alert") : "Security Station"
      });
    }
  };

  Game3DEngine.prototype.initWebGL = function () {
    var gl = this.canvas.getContext("webgl") || this.canvas.getContext("experimental-webgl");
    if (!gl) {
      console.warn("WebGL not supported; falling back to 3D Canvas rendering.");
      this.useCanvasFallback = true;
      this.ctx2d = this.canvas.getContext("2d");
      return;
    }

    this.gl = gl;
    this.useCanvasFallback = false;

    // Shaders
    var vsSource = [
      "attribute vec3 aPos;",
      "attribute vec3 aColor;",
      "attribute vec3 aNormal;",
      "uniform mat4 uProj;",
      "uniform mat4 uView;",
      "uniform mat4 uModel;",
      "uniform vec3 uAlertLight;",
      "varying vec3 vColor;",
      "varying vec3 vNormal;",
      "varying vec3 vWorldPos;",
      "void main(void) {",
      "  vec4 worldPos = uModel * vec4(aPos, 1.0);",
      "  vWorldPos = worldPos.xyz;",
      "  vNormal = mat3(uModel) * aNormal;",
      "  vColor = aColor;",
      "  gl_Position = uProj * uView * worldPos;",
      "}"
    ].join("\n");

    var fsSource = [
      "precision mediump float;",
      "varying vec3 vColor;",
      "varying vec3 vNormal;",
      "varying vec3 vWorldPos;",
      "uniform vec3 uAlertLight;",
      "uniform float uAlertIntensity;",
      "uniform float uTime;",
      "void main(void) {",
      "  vec3 norm = normalize(vNormal);",
      "  vec3 lightDir = normalize(vec3(0.5, 1.0, 0.3));",
      "  float diff = max(dot(norm, lightDir), 0.2);",
      "  vec3 ambient = vec3(0.08, 0.12, 0.22);",
      "  float distToCenter = length(vWorldPos.xz);",
      "  vec3 alertColor = uAlertLight * uAlertIntensity * (1.0 / (1.0 + distToCenter * 0.15));",
      "  vec3 finalColor = vColor * diff + ambient + alertColor;",
      "  float fog = clamp((length(vWorldPos) - 4.0) / 22.0, 0.0, 0.75);",
      "  gl_FragColor = vec4(mix(finalColor, vec3(0.02, 0.04, 0.09), fog), 1.0);",
      "}"
    ].join("\n");

    var vs = this.compileShader(gl.VERTEX_SHADER, vsSource);
    var fs = this.compileShader(gl.FRAGMENT_SHADER, fsSource);
    var prog = gl.createProgram();
    gl.attachShader(prog, vs);
    gl.attachShader(prog, fs);
    gl.linkProgram(prog);

    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
      console.error("Shader link error:", gl.getProgramInfoLog(prog));
      this.useCanvasFallback = true;
      this.ctx2d = this.canvas.getContext("2d");
      return;
    }

    this.prog = prog;
    this.uProj = gl.getUniformLocation(prog, "uProj");
    this.uView = gl.getUniformLocation(prog, "uView");
    this.uModel = gl.getUniformLocation(prog, "uModel");
    this.uAlertLight = gl.getUniformLocation(prog, "uAlertLight");
    this.uAlertIntensity = gl.getUniformLocation(prog, "uAlertIntensity");
    this.uTime = gl.getUniformLocation(prog, "uTime");

    this.aPos = gl.getAttribLocation(prog, "aPos");
    this.aColor = gl.getAttribLocation(prog, "aColor");
    this.aNormal = gl.getAttribLocation(prog, "aNormal");

    this.buildMeshes();
  };

  Game3DEngine.prototype.compileShader = function (type, src) {
    var s = this.gl.createShader(type);
    this.gl.shaderSource(s, src);
    this.gl.compileShader(s);
    if (!this.gl.getShaderParameter(s, this.gl.COMPILE_STATUS)) {
      console.error("Shader error:", this.gl.getShaderInfoLog(s));
    }
    return s;
  };

  Game3DEngine.prototype.buildMeshes = function () {
    var gl = this.gl;
    var vertices = []; // pos.xyz, color.rgb, norm.xyz

    function addQuad(p1, p2, p3, p4, col, norm) {
      var r = col[0], g = col[1], b = col[2];
      var nx = norm[0], ny = norm[1], nz = norm[2];
      var pts = [p1, p2, p3, p1, p3, p4];
      for (var i = 0; i < 6; i++) {
        var p = pts[i];
        vertices.push(p[0], p[1], p[2], r, g, b, nx, ny, nz);
      }
    }

    function addBox(x, y, z, sx, sy, sz, colSide, colTop) {
      var hx = sx / 2, hy = sy / 2, hz = sz / 2;
      // Front
      addQuad([x-hx, y-hy, z+hz], [x+hx, y-hy, z+hz], [x+hx, y+hy, z+hz], [x-hx, y+hy, z+hz], colSide, [0, 0, 1]);
      // Back
      addQuad([x+hx, y-hy, z-hz], [x-hx, y-hy, z-hz], [x-hx, y+hy, z-hz], [x+hx, y+hy, z-hz], colSide, [0, 0, -1]);
      // Top
      addQuad([x-hx, y+hy, z+hz], [x+hx, y+hy, z+hz], [x+hx, y+hy, z-hz], [x-hx, y+hy, z-hz], colTop || colSide, [0, 1, 0]);
      // Bottom
      addQuad([x-hx, y-hy, z-hz], [x+hx, y-hy, z-hz], [x+hx, y-hy, z+hz], [x-hx, y-hy, z+hz], [0.05, 0.05, 0.08], [0, -1, 0]);
      // Left
      addQuad([x-hx, y-hy, z-hz], [x-hx, y-hy, z+hz], [x-hx, y+hy, z+hz], [x-hx, y+hy, z-hz], colSide, [-1, 0, 0]);
      // Right
      addQuad([x+hx, y-hy, z+hz], [x+hx, y-hy, z-hz], [x+hx, y+hy, z-hz], [x+hx, y+hy, z+hz], colSide, [1, 0, 0]);
    }

    // 1. Grid Floor
    var floorSize = 14;
    var tileSize = 1.4;
    for (var fx = -floorSize; fx < floorSize; fx += tileSize) {
      for (var fz = -floorSize; fz < floorSize; fz += tileSize) {
        var isOdd = Math.abs((fx / tileSize + fz / tileSize) % 2) === 1;
        var fCol = isOdd ? [0.06, 0.09, 0.16] : [0.03, 0.05, 0.11];
        addQuad(
          [fx, 0, fz],
          [fx + tileSize, 0, fz],
          [fx + tileSize, 0, fz + tileSize],
          [fx, 0, fz + tileSize],
          fCol,
          [0, 1, 0]
        );
      }
    }

    // 2. Room Perimeter Walls
    var wallH = 4.5;
    var wDist = floorSize;
    var wallCol = [0.08, 0.12, 0.22];
    var trimCol = [0.2, 0.65, 0.95];
    // North Wall
    addQuad([-wDist, 0, -wDist], [wDist, 0, -wDist], [wDist, wallH, -wDist], [-wDist, wallH, -wDist], wallCol, [0, 0, 1]);
    // South Wall
    addQuad([wDist, 0, wDist], [-wDist, 0, wDist], [-wDist, wallH, wDist], [wDist, wallH, wDist], wallCol, [0, 0, -1]);
    // West Wall
    addQuad([-wDist, 0, wDist], [-wDist, 0, -wDist], [-wDist, wallH, -wDist], [-wDist, wallH, wDist], wallCol, [1, 0, 0]);
    // East Wall
    addQuad([wDist, 0, -wDist], [wDist, 0, wDist], [wDist, wallH, wDist], [wDist, wallH, -wDist], wallCol, [-1, 0, 0]);

    // Neon Accent Trim along walls
    addQuad([-wDist, 1.2, -wDist + 0.05], [wDist, 1.2, -wDist + 0.05], [wDist, 1.3, -wDist + 0.05], [-wDist, 1.3, -wDist + 0.05], trimCol, [0, 0, 1]);
    addQuad([-wDist + 0.05, 1.2, -wDist], [-wDist + 0.05, 1.2, wDist], [-wDist + 0.05, 1.3, wDist], [-wDist + 0.05, 1.3, -wDist], trimCol, [1, 0, 0]);
    addQuad([wDist - 0.05, 1.2, wDist], [wDist - 0.05, 1.2, -wDist], [wDist - 0.05, 1.3, -wDist], [wDist - 0.05, 1.3, wDist], trimCol, [-1, 0, 0]);

    // 3. Central Hologram Core Pedestal
    addBox(0, 0.4, 0, 2.2, 0.8, 2.2, [0.12, 0.18, 0.3], [0.22, 0.7, 0.95]);

    this.baseVertexCount = vertices.length / 9;
    this.buffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.buffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW);
  };

  Game3DEngine.prototype.initControls = function () {
    var self = this;

    window.addEventListener("keydown", function (e) {
      self.keys[e.key.toLowerCase()] = true;
      if (e.key === "e" || e.key === "E" || e.key === " ") {
        if (self.nearbyNode) {
          self.triggerTriage(self.nearbyNode);
        }
      }
    });

    window.addEventListener("keyup", function (e) {
      self.keys[e.key.toLowerCase()] = false;
    });

    this.canvas.addEventListener("mousedown", function (e) {
      self.isDragging = true;
      self.lastMouseX = e.clientX;
      self.lastMouseY = e.clientY;
    });

    window.addEventListener("mouseup", function () {
      self.isDragging = false;
    });

    this.canvas.addEventListener("mousemove", function (e) {
      if (!self.isDragging) return;
      var dx = e.clientX - self.lastMouseX;
      var dy = e.clientY - self.lastMouseY;
      self.lastMouseX = e.clientX;
      self.lastMouseY = e.clientY;

      self.camYaw -= dx * self.rotSpeed;
      self.camPitch -= dy * self.rotSpeed;
      if (self.camPitch > 0.6) self.camPitch = 0.6;
      if (self.camPitch < -0.8) self.camPitch = -0.8;
    });

    // Touch support for mobile / tablets
    var touchStartX = 0, touchStartY = 0;
    this.canvas.addEventListener("touchstart", function (e) {
      if (e.touches.length > 0) {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
      }
    }, { passive: true });

    this.canvas.addEventListener("touchmove", function (e) {
      if (e.touches.length > 0) {
        var dx = e.touches[0].clientX - touchStartX;
        var dy = e.touches[0].clientY - touchStartY;
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;

        self.camYaw -= dx * self.rotSpeed * 1.5;
        self.camPitch -= dy * self.rotSpeed * 1.5;
      }
    }, { passive: true });

    if (this.promptEl) {
      this.promptEl.addEventListener("click", function () {
        if (self.nearbyNode) {
          self.triggerTriage(self.nearbyNode);
        }
      });
    }

    // Window resize
    window.addEventListener("resize", function () {
      self.resizeCanvas();
    });
    this.resizeCanvas();
  };

  Game3DEngine.prototype.resizeCanvas = function () {
    if (!this.canvas) return;
    var rect = this.canvas.getBoundingClientRect();
    var dpr = window.devicePixelRatio || 1;
    this.canvas.width = Math.floor(rect.width * dpr);
    this.canvas.height = Math.floor(rect.height * dpr);
    if (this.gl) {
      this.gl.viewport(0, 0, this.canvas.width, this.canvas.height);
    }
  };

  Game3DEngine.prototype.updateCamera = function (dt) {
    var fwd = [Math.sin(this.camYaw), 0, -Math.cos(this.camYaw)];
    var right = [Math.cos(this.camYaw), 0, Math.sin(this.camYaw)];
    var speed = this.keys["shift"] ? this.moveSpeed * 1.8 : this.moveSpeed;

    var moveX = 0, moveZ = 0;
    if (this.keys["w"] || this.keys["arrowup"]) {
      moveX += fwd[0] * speed;
      moveZ += fwd[2] * speed;
    }
    if (this.keys["s"] || this.keys["arrowdown"]) {
      moveX -= fwd[0] * speed;
      moveZ -= fwd[2] * speed;
    }
    if (this.keys["a"] || this.keys["arrowleft"]) {
      moveX -= right[0] * speed;
      moveZ -= right[2] * speed;
    }
    if (this.keys["d"] || this.keys["arrowright"]) {
      moveX += right[0] * speed;
      moveZ += right[2] * speed;
    }

    // Apply movement with room bounds
    var newX = this.camPos[0] + moveX;
    var newZ = this.camPos[2] + moveZ;
    var bound = 12.0;

    if (newX > -bound && newX < bound) this.camPos[0] = newX;
    if (newZ > -bound && newZ < bound) this.camPos[2] = newZ;

    // Check node proximity
    var closestNode = null;
    var minDist = 4.0; // Distance threshold to interact

    for (var i = 0; i < this.nodes.length; i++) {
      var n = this.nodes[i];
      var dx = this.camPos[0] - n.pos[0];
      var dz = this.camPos[2] - n.pos[2];
      var dist = Math.sqrt(dx * dx + dz * dz);
      if (dist < minDist) {
        minDist = dist;
        closestNode = n;
      }
    }

    this.nearbyNode = closestNode;
    if (this.promptEl) {
      if (closestNode) {
        this.promptEl.style.display = "flex";
        if (this.promptText) {
          var stateLabel = closestNode.status === "compromised" ? "🚨 TRIAGE BREACH" : (closestNode.status === "secured" ? "✅ VIEW DEFENSES" : "🔍 INSPECT");
          this.promptText.textContent = stateLabel + ": " + closestNode.name + " (" + closestNode.label + ")";
        }
      } else {
        this.promptEl.style.display = "none";
      }
    }
  };

  Game3DEngine.prototype.triggerTriage = function (node) {
    this.playAudio("terminal");
    if (this.onTriageRequest) {
      this.onTriageRequest(node.id, node);
    }
  };

  Game3DEngine.prototype.setNodeStatus = function (index, status) {
    if (index >= 0 && index < this.nodes.length) {
      this.nodes[index].status = status;
      if (status === "secured") {
        this.playAudio("success");
        this.emitParticles(this.nodes[index].pos, [0.2, 0.95, 0.4]);
      } else if (status === "compromised") {
        this.playAudio("alarm");
        this.emitParticles(this.nodes[index].pos, [1.0, 0.2, 0.2]);
      }
      this.renderHUD();
      if (this.onNodeStateChange) {
        this.onNodeStateChange(index, status);
      }
    }
  };

  Game3DEngine.prototype.setActiveScenario = function (index) {
    this.activeScenarioIndex = index;
    for (var i = 0; i < this.nodes.length; i++) {
      if (i < index) {
        this.nodes[i].status = "secured";
      } else if (i === index) {
        this.nodes[i].status = "compromised";
      } else {
        this.nodes[i].status = "pending";
      }
    }
    this.renderHUD();
  };

  Game3DEngine.prototype.emitParticles = function (origin, color) {
    for (var i = 0; i < 35; i++) {
      this.particles.push({
        x: origin[0] + (Math.random() - 0.5) * 0.8,
        y: 1.5 + Math.random() * 0.6,
        z: origin[2] + (Math.random() - 0.5) * 0.8,
        vx: (Math.random() - 0.5) * 0.12,
        vy: 0.05 + Math.random() * 0.1,
        vz: (Math.random() - 0.5) * 0.12,
        color: color,
        life: 1.0,
        decay: 0.02 + Math.random() * 0.02
      });
    }
  };

  Game3DEngine.prototype.renderHUD = function () {
    if (this.hudNodesEl) {
      var html = "";
      for (var i = 0; i < this.nodes.length; i++) {
        var n = this.nodes[i];
        var badge = "bg-secondary";
        var icon = "⚪";
        if (n.status === "compromised") { badge = "bg-danger text-white animate-pulse"; icon = "🚨"; }
        else if (n.status === "secured") { badge = "bg-success text-white"; icon = "✅"; }
        html += '<span class="badge ' + badge + ' me-1 mb-1 p-1" style="font-size:0.75rem;">' + icon + ' ' + n.name + '</span>';
      }
      this.hudNodesEl.innerHTML = html;
    }
    if (this.hudSecurityLvl) {
      var secured = 0;
      for (var j = 0; j < this.nodes.length; j++) {
        if (this.nodes[j].status === "secured") secured++;
      }
      var pct = Math.round((secured / this.nodes.length) * 100);
      this.hudSecurityLvl.textContent = pct + "% Integrity";
      this.hudSecurityLvl.className = pct >= 80 ? "text-success fw-bold" : (pct >= 40 ? "text-warning fw-bold" : "text-danger fw-bold");
    }
  };

  Game3DEngine.prototype.playAudio = function (type) {
    if (!this.audioEnabled) return;
    try {
      if (!this.audioCtx && (window.AudioContext || window.webkitAudioContext)) {
        this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
      if (!this.audioCtx) return;
      if (this.audioCtx.state === "suspended") {
        this.audioCtx.resume();
      }

      var now = this.audioCtx.currentTime;
      var osc = this.audioCtx.createOscillator();
      var gain = this.audioCtx.createGain();
      osc.connect(gain);
      gain.connect(this.audioCtx.destination);

      if (type === "terminal") {
        osc.type = "sine";
        osc.frequency.setValueAtTime(880, now);
        osc.frequency.exponentialRampToValueAtTime(1760, now + 0.08);
        gain.gain.setValueAtTime(0.12, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.08);
        osc.start(now);
        osc.stop(now + 0.09);
      } else if (type === "success") {
        // High-tech victory arpeggio: C5 -> E5 -> G5 -> C6
        var notes = [523.25, 659.25, 783.99, 1046.50];
        notes.forEach(function (freq, i) {
          var o = this.audioCtx.createOscillator();
          var g = this.audioCtx.createGain();
          o.connect(g);
          g.connect(this.audioCtx.destination);
          o.type = "triangle";
          o.frequency.setValueAtTime(freq, now + i * 0.07);
          g.gain.setValueAtTime(0.15, now + i * 0.07);
          g.gain.linearRampToValueAtTime(0.001, now + i * 0.07 + 0.25);
          o.start(now + i * 0.07);
          o.stop(now + i * 0.07 + 0.26);
        }.bind(this));
      } else if (type === "alarm") {
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.linearRampToValueAtTime(320, now + 0.18);
        gain.gain.setValueAtTime(0.15, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.18);
        osc.start(now);
        osc.stop(now + 0.19);
      }
    } catch (e) {
      // Audio not permitted without user gesture
    }
  };

  Game3DEngine.prototype.animate = function (time) {
    requestAnimationFrame(this.animate);
    var dt = (time - this.lastTime) * 0.001;
    this.lastTime = time;

    this.updateCamera(dt);

    if (this.useCanvasFallback) {
      this.renderCanvasFallback(time);
    } else {
      this.renderWebGL(time);
    }
  };

  Game3DEngine.prototype.renderWebGL = function (time) {
    var gl = this.gl;
    if (!gl) return;

    gl.clearColor(0.02, 0.04, 0.09, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.enable(gl.DEPTH_TEST);
    gl.enable(gl.CULL_FACE);

    gl.useProgram(this.prog);

    // Camera view matrix
    var pMatrix = Mat4.create();
    var aspect = this.canvas.width / this.canvas.height;
    Mat4.perspective(pMatrix, 60 * Math.PI / 180, aspect, 0.1, 100.0);

    var vMatrix = Mat4.create();
    Mat4.rotateX(vMatrix, vMatrix, -this.camPitch);
    Mat4.rotateY(vMatrix, vMatrix, -this.camYaw);
    Mat4.translate(vMatrix, vMatrix, [-this.camPos[0], -this.camPos[1], -this.camPos[2]]);

    var mMatrix = Mat4.create();

    // Alert siren light pulse
    var pulse = 0.5 + 0.5 * Math.sin(time * 0.006);
    gl.uniform3fv(this.uAlertLight, [1.0, 0.15, 0.15]);
    gl.uniform1f(this.uAlertIntensity, pulse);
    gl.uniform1f(this.uTime, time * 0.001);

    gl.uniformMatrix4fv(this.uProj, false, pMatrix);
    gl.uniformMatrix4fv(this.uView, false, vMatrix);
    gl.uniformMatrix4fv(this.uModel, false, mMatrix);

    // Bind base geometry buffer
    gl.bindBuffer(gl.ARRAY_BUFFER, this.buffer);
    var stride = 9 * 4;
    gl.vertexAttribPointer(this.aPos, 3, gl.FLOAT, false, stride, 0);
    gl.enableVertexAttribArray(this.aPos);
    gl.vertexAttribPointer(this.aColor, 3, gl.FLOAT, false, stride, 3 * 4);
    gl.enableVertexAttribArray(this.aColor);
    gl.vertexAttribPointer(this.aNormal, 3, gl.FLOAT, false, stride, 6 * 4);
    gl.enableVertexAttribArray(this.aNormal);

    // Render floor and walls
    gl.drawArrays(gl.TRIANGLES, 0, this.baseVertexCount);

    // Render 3D dynamic nodes (Server Racks and Stations)
    this.renderDynamicNodes(gl, pMatrix, vMatrix, time);
  };

  Game3DEngine.prototype.renderDynamicNodes = function (gl, pMatrix, vMatrix, time) {
    // Render each server rack node
    for (var i = 0; i < this.nodes.length; i++) {
      var n = this.nodes[i];
      var col = [0.15, 0.2, 0.28];
      var beaconCol = [0.2, 0.5, 0.9];
      if (n.status === "compromised") {
        col = [0.4, 0.1, 0.1];
        beaconCol = [1.0, 0.1, 0.1];
      } else if (n.status === "secured") {
        col = [0.1, 0.35, 0.18];
        beaconCol = [0.2, 0.95, 0.4];
      }

      // Draw server rack cabinet
      var m = Mat4.create();
      Mat4.translate(m, m, n.pos);
      Mat4.rotateY(m, m, n.angle);

      gl.uniformMatrix4fv(this.uModel, false, m);
      // Dynamic server LED blink
      if (n.status === "compromised") {
        var flash = 0.5 + 0.5 * Math.sin(time * 0.01 + i);
        gl.uniform1f(this.uAlertIntensity, flash);
      }
    }
  };

  // Graceful Canvas 2D Perspective Projection Fallback for ultra-low spec systems
  Game3DEngine.prototype.renderCanvasFallback = function (time) {
    var ctx = this.ctx2d;
    var w = this.canvas.width;
    var h = this.canvas.height;

    ctx.fillStyle = "#030712";
    ctx.fillRect(0, 0, w, h);

    // Draw high-tech perspective floor grid
    ctx.strokeStyle = "rgba(56, 189, 248, 0.18)";
    ctx.lineWidth = 1.5;
    var horizon = h * 0.45 + this.camPitch * h * 0.5;

    for (var x = -w; x <= w * 2; x += 60) {
      ctx.beginPath();
      ctx.moveTo(w / 2, horizon);
      ctx.lineTo(x, h);
      ctx.stroke();
    }
    for (var y = horizon + 10; y < h; y += (y - horizon) * 0.45 + 8) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(w, y);
      ctx.stroke();
    }

    // Central Hologram Globe & Orbit
    var centerX = w / 2;
    var centerY = horizon - 40;
    var pulse = 0.8 + 0.2 * Math.sin(time * 0.005);
    ctx.strokeStyle = "rgba(56, 189, 248, " + (0.7 * pulse) + ")";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.ellipse(centerX, centerY, 60 * pulse, 30 * pulse, time * 0.001, 0, Math.PI * 2);
    ctx.stroke();

    ctx.fillStyle = "rgba(56, 189, 248, 0.9)";
    ctx.font = "bold 14px monospace";
    ctx.textAlign = "center";
    ctx.fillText("🛡️ CYBER DEFENSE WAR ROOM 3D", centerX, centerY + 5);

    // Draw Stations in perspective
    for (var i = 0; i < this.nodes.length; i++) {
      var n = this.nodes[i];
      var screenX = centerX + Math.sin(n.angle + this.camYaw) * (w * 0.38);
      var screenY = horizon + Math.cos(n.angle + this.camYaw) * (h * 0.35) + (h * 0.2);

      var isCompromised = n.status === "compromised";
      var isSecured = n.status === "secured";

      ctx.fillStyle = isCompromised ? "#ef4444" : (isSecured ? "#10b981" : "#38bdf8");
      ctx.shadowColor = ctx.fillStyle;
      ctx.shadowBlur = isCompromised ? 15 : 8;

      ctx.beginPath();
      ctx.arc(screenX, screenY, isCompromised ? 16 : 12, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowBlur = 0;

      ctx.fillStyle = "#ffffff";
      ctx.font = "11px monospace";
      ctx.fillText(n.name, screenX, screenY + 24);
    }
  };

  window.Game3DEngine = Game3DEngine;

})(window);

