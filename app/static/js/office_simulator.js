/**
 * Human Firewall — Corporate Office & Cybersecurity Career Simulator Engine
 * 
 * Supports both standalone flagship mode and dynamic scenario execution across all 35 games:
 * - 3D Corporate Office Environment (Reception, Open Floor, Manager's Office, Server Room, SOC)
 * - Spatial Audio Synthesizer (Zero external audio files required)
 * - Proximity detection and interactive workstations
 * - In-Game CyberWork OS Desktop:
 *   - CyberMail (Email Client with dynamic MIME headers, link inspector, quarantine)
 *   - DeskFlow (IT Helpdesk with Identity Verification & Pretexting checks)
 *   - CyberSIEM (Real-time telemetry, host network isolation, IP blocking)
 *   - Incident Desk (Report builder & investigation dossier)
 *   - ChatLink (Live manager communicator & task board)
 * - End-of-Day Performance Review & Idempotent XP Integration
 */

(function (window) {
  "use strict";

  // Matrix math helpers for 3D perspective
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
    }
  };

  function CorporateOfficeSimulator(config) {
    this.canvas = document.getElementById(config.canvasId || "officeCanvas3D");
    this.gameSlug = config.gameSlug || "corporate-office-simulator";
    this.csrfToken = config.csrfToken || "";
    this.onShiftComplete = config.onShiftComplete || null;

    // Simulation state
    this.playerX = 0;
    this.playerZ = 4;
    this.playerYaw = 0;
    this.playerSpeed = 0.12;

    this.keys = {};
    this.isDesktopOpen = false;
    this.activeApp = "mail"; // 'mail' | 'helpdesk' | 'siem' | 'report' | 'chat'

    // Scenarios from game or default fallback
    this.scenarios = config.scenarios || [];
    this.gameTitle = config.gameTitle || "Corporate Cybersecurity Mission";
    this.debriefText = config.debriefText || "Rigorous verification and multi-factor defense protect the human firewall.";

    // Build tasks from scenarios or default 4 tasks
    this.tasks = [];
    if (this.scenarios && this.scenarios.length > 0) {
      var pts = Math.max(10, Math.floor(100 / this.scenarios.length));
      for (var sIdx = 0; sIdx < this.scenarios.length; sIdx++) {
        var sc = this.scenarios[sIdx];
        this.tasks.push({
          id: "task" + (sIdx + 1),
          scenarioId: sc.id,
          title: sc.subject || (sc.sender ? "Investigate: " + sc.sender : "Incident Inspection #" + (sIdx + 1)),
          completed: false,
          score: 0,
          points: pts,
          scenario: sc
        });
      }
    } else {
      this.tasks = [
        { id: "task1", title: "Investigate Suspicious HR Payroll Email", completed: false, score: 0, points: 25 },
        { id: "task2", title: "Triage Urgent Executive Password Reset Request", completed: false, score: 0, points: 25 },
        { id: "task3", title: "Contain EDR Beaconing Alert in SIEM", completed: false, score: 0, points: 25 },
        { id: "task4", title: "Compile & Submit Investigation Report", completed: false, score: 0, points: 25 }
      ];
    }

    this.timeRemaining = 600; // 10 minutes
    this.shiftStartTime = Date.now();
    this.mistakesCount = 0;
    this.soundEnabled = true;

    // Web Audio Synthesizer
    this.audioCtx = null;

    // Zones and interactive hotspots
    this.hotspots = [
      { id: "workstation", name: "Player Workstation #1", x: 0, z: 2.2, radius: 2.0, actionText: "Sit at Workstation [E]" },
      { id: "manager", name: "Marcus Vance (CISO)", x: 4.5, z: -3.5, radius: 2.2, actionText: "Talk to Marcus Vance [E]" },
      { id: "server", name: "Datacenter Rack A1", x: -4.5, z: -3.5, radius: 2.2, actionText: "Inspect Server Telemetry [E]" },
      { id: "soc", name: "SOC Video Wall", x: 0, z: -5.0, radius: 2.5, actionText: "View SOC Threat Display [E]" }
    ];

    this.currentNearbyHotspot = null;

    this.initWebGL();
    this.initControls();
    this.initDOM();
    this.startShiftTimer();

    this.animate = this.animate.bind(this);
    requestAnimationFrame(this.animate);
  }

  // Synthesize realistic soundscapes via Web Audio API
  CorporateOfficeSimulator.prototype.playSound = function (type) {
    if (!this.soundEnabled) return;
    try {
      var AudioContext = window.AudioContext || window.webkitAudioContext;
      if (!AudioContext) return;
      if (!this.audioCtx) this.audioCtx = new AudioContext();
      if (this.audioCtx.state === "suspended") this.audioCtx.resume();

      var ctx = this.audioCtx;
      var now = ctx.currentTime;
      var osc = ctx.createOscillator();
      var gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);

      if (type === "click") {
        osc.type = "sine";
        osc.frequency.setValueAtTime(650, now);
        osc.frequency.exponentialRampToValueAtTime(300, now + 0.04);
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.linearRampToValueAtTime(0.001, now + 0.04);
        osc.start(now);
        osc.stop(now + 0.04);
      } else if (type === "alert") {
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(880, now);
        osc.frequency.linearRampToValueAtTime(440, now + 0.18);
        gain.gain.setValueAtTime(0.12, now);
        gain.gain.linearRampToValueAtTime(0.001, now + 0.2);
        osc.start(now);
        osc.stop(now + 0.2);
      } else if (type === "success") {
        osc.type = "triangle";
        osc.frequency.setValueAtTime(523.25, now);
        osc.frequency.setValueAtTime(659.25, now + 0.08);
        osc.frequency.setValueAtTime(783.99, now + 0.16);
        gain.gain.setValueAtTime(0.12, now);
        gain.gain.linearRampToValueAtTime(0.001, now + 0.28);
        osc.start(now);
        osc.stop(now + 0.28);
      }
    } catch (e) {
      // Audio fallback silent
    }
  };

  CorporateOfficeSimulator.prototype.initWebGL = function () {
    if (!this.canvas) return;
    var gl = this.canvas.getContext("webgl") || this.canvas.getContext("experimental-webgl");
    this.gl = gl;

    if (!gl) {
      this.ctx2d = this.canvas.getContext("2d");
      return;
    }

    var rect = this.canvas.getBoundingClientRect();
    this.canvas.width = rect.width * (window.devicePixelRatio || 1);
    this.canvas.height = rect.height * (window.devicePixelRatio || 1);
    gl.viewport(0, 0, this.canvas.width, this.canvas.height);

    var vsSource = [
      "attribute vec3 aPosition;",
      "attribute vec3 aColor;",
      "uniform mat4 uProjection;",
      "uniform mat4 uView;",
      "uniform mat4 uModel;",
      "varying vec3 vColor;",
      "void main(void) {",
      "  gl_Position = uProjection * uView * uModel * vec4(aPosition, 1.0);",
      "  vColor = aColor;",
      "}"
    ].join("\n");

    var fsSource = [
      "precision mediump float;",
      "varying vec3 vColor;",
      "void main(void) {",
      "  gl_FragColor = vec4(vColor, 1.0);",
      "}"
    ].join("\n");

    var vs = gl.createShader(gl.VERTEX_SHADER);
    gl.shaderSource(vs, vsSource);
    gl.compileShader(vs);

    var fs = gl.createShader(gl.FRAGMENT_SHADER);
    gl.shaderSource(fs, fsSource);
    gl.compileShader(fs);

    var program = gl.createProgram();
    gl.attachShader(program, vs);
    gl.attachShader(program, fs);
    gl.linkProgram(program);
    gl.useProgram(program);
    this.program = program;

    this.aPosition = gl.getAttribLocation(program, "aPosition");
    this.aColor = gl.getAttribLocation(program, "aColor");
    this.uProjection = gl.getUniformLocation(program, "uProjection");
    this.uView = gl.getUniformLocation(program, "uView");
    this.uModel = gl.getUniformLocation(program, "uModel");

    this.buildOfficeGeometry(gl);
  };

  CorporateOfficeSimulator.prototype.buildOfficeGeometry = function (gl) {
    var vertices = [];

    function addQuad(x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, r, g, b) {
      vertices.push(
        x1, y1, z1, r, g, b,
        x2, y2, z2, r, g, b,
        x3, y3, z3, r, g, b,
        x1, y1, z1, r, g, b,
        x3, y3, z3, r, g, b,
        x4, y4, z4, r, g, b
      );
    }

    // 1. Corporate Office Floor
    addQuad(-9, 0, -9,  9, 0, -9,  9, 0, 9, -9, 0, 9, 0.12, 0.16, 0.22);
    // 2. Back Corporate Wall
    addQuad(-9, 0, -9,  9, 0, -9,  9, 4.5, -9, -9, 4.5, -9, 0.08, 0.11, 0.16);
    // 3. Side Walls
    addQuad(-9, 0, -9, -9, 0, 9, -9, 4.5, 9, -9, 4.5, -9, 0.10, 0.14, 0.20);
    addQuad( 9, 0, -9,  9, 0, 9,  9, 4.5, 9,  9, 4.5, -9, 0.10, 0.14, 0.20);
    // 4. Glass Partition for Manager's Office
    addQuad(2.5, 0, -8.5, 2.5, 0, -2, 2.5, 3.5, -2, 2.5, 3.5, -8.5, 0.15, 0.35, 0.50);
    // 5. Server Room Partition
    addQuad(-2.5, 0, -8.5, -2.5, 0, -2, -2.5, 3.5, -2, -2.5, 3.5, -8.5, 0.09, 0.10, 0.14);
    // 6. Player Workstation Desk #1
    addQuad(-1.5, 0.8, 1.5, 1.5, 0.8, 1.5, 1.5, 0.8, 3.0, -1.5, 0.8, 3.0, 0.25, 0.32, 0.42);
    addQuad(-1.0, 0.9, 1.8, -0.1, 0.9, 1.8, -0.1, 1.6, 1.8, -1.0, 1.6, 1.8, 0.05, 0.65, 0.95);
    addQuad( 0.1, 0.9, 1.8,  1.0, 0.9, 1.8,  1.0, 1.6, 1.8,  0.1, 1.6, 1.8, 0.10, 0.85, 0.45);
    // 7. Manager's Desk
    addQuad(3.5, 0.8, -4.5, 6.5, 0.8, -4.5, 6.5, 0.8, -3.0, 3.5, 0.8, -3.0, 0.35, 0.22, 0.18);
    // 8. Server Racks
    addQuad(-6.5, 0, -5.5, -4.5, 0, -5.5, -4.5, 3.2, -5.5, -6.5, 3.2, -5.5, 0.05, 0.08, 0.12);
    addQuad(-6.4, 0.5, -5.48, -4.6, 0.5, -5.48, -4.6, 0.6, -5.48, -6.4, 0.6, -5.48, 0.2, 0.9, 0.3);
    addQuad(-6.4, 1.5, -5.48, -4.6, 1.5, -5.48, -4.6, 1.6, -5.48, -6.4, 1.6, -5.48, 0.9, 0.2, 0.2);
    addQuad(-6.4, 2.5, -5.48, -4.6, 2.5, -5.48, -4.6, 2.6, -5.48, -6.4, 2.6, -5.48, 0.2, 0.7, 1.0);
    // 9. SOC Video Wall
    addQuad(-2.0, 1.5, -8.8, 2.0, 1.5, -8.8, 2.0, 3.8, -8.8, -2.0, 3.8, -8.8, 0.05, 0.45, 0.85);

    this.vertexCount = vertices.length / 6;
    this.buffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.buffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW);
  };

  CorporateOfficeSimulator.prototype.initControls = function () {
    var self = this;
    window.addEventListener("keydown", function (e) {
      if (self.isDesktopOpen && e.key !== "Escape") return;
      self.keys[e.key.toLowerCase()] = true;
      if (e.key === "e" || e.key === "E" || e.key === " ") {
        self.handleInteract();
      }
      if (e.key === "Escape" && self.isDesktopOpen) {
        self.toggleWorkstationDesktop(false);
      }
    });

    window.addEventListener("keyup", function (e) {
      self.keys[e.key.toLowerCase()] = false;
    });

    var btnSit = document.getElementById("btnVirtualSit");
    if (btnSit) {
      btnSit.addEventListener("click", function () {
        self.toggleWorkstationDesktop(true);
      });
    }
  };

  CorporateOfficeSimulator.prototype.handleInteract = function () {
    if (this.currentNearbyHotspot) {
      this.playSound("click");
      if (this.currentNearbyHotspot.id === "workstation") {
        this.toggleWorkstationDesktop(true);
      } else if (this.currentNearbyHotspot.id === "manager") {
        this.toggleWorkstationDesktop(true);
        this.switchApp("chat");
      } else if (this.currentNearbyHotspot.id === "server" || this.currentNearbyHotspot.id === "soc") {
        this.toggleWorkstationDesktop(true);
        this.switchApp("siem");
      }
    }
  };

  CorporateOfficeSimulator.prototype.toggleWorkstationDesktop = function (open) {
    this.isDesktopOpen = !!open;
    var deskEl = document.getElementById("cyberworkDesktopOverlay");
    var hudEl = document.getElementById("office3DHudOverlay");
    if (deskEl) {
      deskEl.style.display = this.isDesktopOpen ? "flex" : "none";
    }
    if (hudEl) {
      hudEl.style.display = this.isDesktopOpen ? "none" : "block";
    }
    this.playSound("click");
  };

  CorporateOfficeSimulator.prototype.startShiftTimer = function () {
    var self = this;
    var timerEl = document.getElementById("simShiftTimer");
    setInterval(function () {
      if (self.timeRemaining > 0) {
        self.timeRemaining--;
        var mins = Math.floor(self.timeRemaining / 60);
        var secs = self.timeRemaining % 60;
        if (timerEl) {
          timerEl.textContent = (mins < 10 ? "0" : "") + mins + ":" + (secs < 10 ? "0" : "") + secs;
        }
      }
    }, 1000);
  };

  CorporateOfficeSimulator.prototype.updatePlayer = function () {
    if (this.isDesktopOpen) return;

    var speed = this.playerSpeed;
    if (this.keys["shift"]) speed *= 1.6;

    if (this.keys["w"] || this.keys["arrowup"]) {
      this.playerZ -= speed;
    }
    if (this.keys["s"] || this.keys["arrowdown"]) {
      this.playerZ += speed;
    }
    if (this.keys["a"] || this.keys["arrowleft"]) {
      this.playerX -= speed;
    }
    if (this.keys["d"] || this.keys["arrowright"]) {
      this.playerX += speed;
    }

    this.playerX = Math.max(-7.5, Math.min(7.5, this.playerX));
    this.playerZ = Math.max(-7.5, Math.min(7.5, this.playerZ));

    var nearest = null;
    var minD = 999;
    for (var i = 0; i < this.hotspots.length; i++) {
      var h = this.hotspots[i];
      var dist = Math.sqrt(Math.pow(this.playerX - h.x, 2) + Math.pow(this.playerZ - h.z, 2));
      if (dist < h.radius && dist < minD) {
        minD = dist;
        nearest = h;
      }
    }

    this.currentNearbyHotspot = nearest;
    var promptEl = document.getElementById("simProximityPrompt");
    var promptText = document.getElementById("simProximityPromptText");
    if (promptEl && promptText) {
      if (nearest) {
        promptEl.style.display = "block";
        promptText.innerHTML = "<strong>" + nearest.name + "</strong>: " + nearest.actionText;
      } else {
        promptEl.style.display = "none";
      }
    }
  };

  CorporateOfficeSimulator.prototype.animate = function (now) {
    this.updatePlayer();

    if (this.gl) {
      this.renderWebGL(now);
    } else if (this.ctx2d) {
      this.render2DFallback(now);
    }

    requestAnimationFrame(this.animate);
  };

  CorporateOfficeSimulator.prototype.renderWebGL = function (now) {
    var gl = this.gl;
    gl.clearColor(0.04, 0.06, 0.10, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.enable(gl.DEPTH_TEST);

    var aspect = this.canvas.width / this.canvas.height;
    var pMatrix = Mat4.create();
    Mat4.perspective(pMatrix, 45 * Math.PI / 180, aspect, 0.1, 100.0);

    var vMatrix = Mat4.create();
    var camX = this.playerX * 0.4;
    var camY = 6.8;
    var camZ = this.playerZ + 6.2;
    Mat4.rotateX(vMatrix, vMatrix, 38 * Math.PI / 180);
    Mat4.translate(vMatrix, vMatrix, [-camX, -camY, -camZ]);

    var mMatrix = Mat4.create();

    gl.uniformMatrix4fv(this.uProjection, false, pMatrix);
    gl.uniformMatrix4fv(this.uView, false, vMatrix);
    gl.uniformMatrix4fv(this.uModel, false, mMatrix);

    gl.bindBuffer(gl.ARRAY_BUFFER, this.buffer);
    var stride = 6 * 4;
    gl.vertexAttribPointer(this.aPosition, 3, gl.FLOAT, false, stride, 0);
    gl.enableVertexAttribArray(this.aPosition);
    gl.vertexAttribPointer(this.aColor, 3, gl.FLOAT, false, stride, 3 * 4);
    gl.enableVertexAttribArray(this.aColor);

    gl.drawArrays(gl.TRIANGLES, 0, this.vertexCount);

    this.renderPlayerAvatar(gl, pMatrix, vMatrix);
  };

  CorporateOfficeSimulator.prototype.renderPlayerAvatar = function (gl, pMatrix, vMatrix) {
    var m = Mat4.create();
    Mat4.translate(m, m, [this.playerX, 0.45, this.playerZ]);
    gl.uniformMatrix4fv(this.uModel, false, m);
    gl.drawArrays(gl.TRIANGLES, 0, 6);
  };

  CorporateOfficeSimulator.prototype.render2DFallback = function (now) {
    var ctx = this.ctx2d;
    var w = this.canvas.width;
    var h = this.canvas.height;

    ctx.fillStyle = "#0a0f1d";
    ctx.fillRect(0, 0, w, h);

    ctx.strokeStyle = "rgba(56, 189, 248, 0.25)";
    ctx.lineWidth = 2;
    ctx.strokeRect(40, 40, w - 80, h - 80);

    ctx.fillStyle = "rgba(14, 165, 233, 0.15)";
    ctx.fillRect(w * 0.35, h * 0.5, w * 0.3, h * 0.3);
    ctx.fillStyle = "#38bdf8";
    ctx.font = "bold 12px monospace";
    ctx.fillText("💻 WORKSTATION POD #1", w * 0.38, h * 0.65);

    ctx.fillStyle = "rgba(239, 68, 68, 0.15)";
    ctx.fillRect(60, 60, w * 0.25, h * 0.35);
    ctx.fillStyle = "#ef4444";
    ctx.fillText("🚨 SERVER ROOM A1", 70, 90);

    ctx.fillStyle = "rgba(16, 185, 129, 0.15)";
    ctx.fillRect(w * 0.68, 60, w * 0.25, h * 0.35);
    ctx.fillStyle = "#10b981";
    ctx.fillText("👔 CISO MARCUS VANCE", w * 0.70, 90);

    var px = w * 0.5 + (this.playerX / 8) * (w * 0.4);
    var pz = h * 0.5 + (this.playerZ / 8) * (h * 0.4);

    ctx.fillStyle = "#fbbf24";
    ctx.beginPath();
    ctx.arc(px, pz, 12, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 11px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("YOU (Analyst)", px, pz - 16);
  };

  CorporateOfficeSimulator.prototype.initDOM = function () {
    var self = this;

    // Desktop App Switcher tabs
    var appButtons = document.querySelectorAll("[data-sim-app]");
    appButtons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var appName = this.getAttribute("data-sim-app");
        self.switchApp(appName);
      });
    });

    // Close desktop button
    var btnCloseDesk = document.getElementById("btnCloseDesktop");
    if (btnCloseDesk) {
      btnCloseDesk.addEventListener("click", function () {
        self.toggleWorkstationDesktop(false);
      });
    }

    // Render dynamic task board if container exists
    this.renderTaskBoard();

    // Initialize applications
    this.initMailClient();
    this.initHelpdeskClient();
    this.initSiemClient();
    this.initIncidentReport();
  };

  CorporateOfficeSimulator.prototype.renderTaskBoard = function () {
    var container = document.getElementById("simTaskListContainer");
    if (!container) return;

    container.innerHTML = "";
    for (var i = 0; i < this.tasks.length; i++) {
      var t = this.tasks[i];
      var div = document.createElement("div");
      div.className = "list-group-item bg-transparent text-light border-secondary p-2";
      div.id = "simTaskRow_" + t.id;
      div.innerHTML =
        '<div class="small fw-semibold">' + (i + 1) + '. ' + t.title + '</div>' +
        '<span class="badge bg-secondary mt-1">Pending (' + t.points + ' XP)</span>';
      container.appendChild(div);
    }
  };

  CorporateOfficeSimulator.prototype.switchApp = function (appName) {
    this.activeApp = appName;
    this.playSound("click");

    document.querySelectorAll(".sim-app-window").forEach(function (el) {
      el.style.display = "none";
    });
    var targetWindow = document.getElementById("simApp_" + appName);
    if (targetWindow) {
      targetWindow.style.display = "block";
    }

    document.querySelectorAll("[data-sim-app]").forEach(function (btn) {
      btn.classList.toggle("active", btn.getAttribute("data-sim-app") === appName);
    });
  };

  // APP 1: CyberMail Client
  CorporateOfficeSimulator.prototype.initMailClient = function () {
    var self = this;

    // Header inspection button
    var btnInspectHeaders = document.getElementById("btnInspectMimeHeaders");
    if (btnInspectHeaders) {
      btnInspectHeaders.addEventListener("click", function () {
        self.playSound("click");
        var modal = document.getElementById("simMimeHeadersModal");
        if (modal) modal.style.display = "flex";
      });
    }

    var btnCloseHeaders = document.getElementById("btnCloseMimeHeaders");
    if (btnCloseHeaders) {
      btnCloseHeaders.addEventListener("click", function () {
        var modal = document.getElementById("simMimeHeadersModal");
        if (modal) modal.style.display = "none";
      });
    }

    // Link inspection hover
    var linkInspectEl = document.getElementById("simPhishLink");
    var linkVerdict = document.getElementById("simLinkVerdictAlert");
    if (linkInspectEl && linkVerdict) {
      linkInspectEl.addEventListener("mouseenter", function () {
        linkVerdict.style.display = "block";
        self.playSound("alert");
      });
    }

    // Quarantine Email action
    var btnQuarantine = document.getElementById("btnQuarantinePhish");
    if (btnQuarantine) {
      btnQuarantine.addEventListener("click", function () {
        self.completeTask("task1", 25, "Threat Quarantined! Phishing communication isolated before credential exposure.");
        this.disabled = true;
        this.innerHTML = "✓ Quarantined & Blocked";
        this.className = "btn btn-sm btn-success";
        self.playSound("success");
      });
    }

    // Dynamic Scenario Choices (if current scenario has multiple choices)
    var choiceBtns = document.querySelectorAll(".sim-dynamic-choice-btn");
    choiceBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var isCorrect = this.getAttribute("data-correct") === "true";
        var feedback = this.getAttribute("data-feedback") || (isCorrect ? "Correct assessment!" : "Dangerous choice!");
        var taskId = this.getAttribute("data-task-id") || "task1";

        if (isCorrect) {
          self.completeTask(taskId, 25, "✓ " + feedback);
          self.playSound("success");
          this.classList.remove("btn-outline-info", "btn-outline-secondary");
          this.classList.add("btn-success");
        } else {
          self.mistakesCount++;
          self.playSound("alert");
          alert("SECURITY WARNING: " + feedback);
        }
      });
    });
  };

  // APP 2: DeskFlow IT Helpdesk
  CorporateOfficeSimulator.prototype.initHelpdeskClient = function () {
    var self = this;

    var btnRejectPretext = document.getElementById("btnRejectPretexting");
    if (btnRejectPretext) {
      btnRejectPretext.addEventListener("click", function () {
        self.completeTask("task2", 25, "Pretexting Trap Neutralized! Refused unauthorized password reset to unverified mobile.");
        this.disabled = true;
        this.innerHTML = "✓ Pretexting Defeated";
        this.className = "btn btn-sm btn-success";
        var btnBad = document.getElementById("btnApproveBadReset");
        if (btnBad) btnBad.disabled = true;
        self.playSound("success");
      });
    }

    var btnApproveBad = document.getElementById("btnApproveBadReset");
    if (btnApproveBad) {
      btnApproveBad.addEventListener("click", function () {
        self.mistakesCount++;
        self.playSound("alert");
        alert("SECURITY BREACH! You texted a temporary password to an unverified mobile number! The attacker compromised the executive account!");
      });
    }
  };

  // APP 3: CyberSIEM
  CorporateOfficeSimulator.prototype.initSiemClient = function () {
    var self = this;

    var btnIsolate = document.getElementById("btnIsolateHost");
    if (btnIsolate) {
      btnIsolate.addEventListener("click", function () {
        self.completeTask("task3", 25, "Host Isolated! Command-and-control beacon terminated at perimeter.");
        this.disabled = true;
        this.innerHTML = "🔒 Host ISOLATED from LAN";
        this.className = "btn btn-sm btn-success";
        self.playSound("success");
      });
    }
  };

  // APP 4: Incident Report & Shift Review
  CorporateOfficeSimulator.prototype.initIncidentReport = function () {
    var self = this;

    var reportForm = document.getElementById("simIncidentReportForm");
    if (reportForm) {
      reportForm.addEventListener("submit", function (e) {
        e.preventDefault();
        self.completeTask("task4", 25, "Formal Incident Report Submitted & Approved by CISO Marcus Vance.");
        self.playSound("success");
        self.showEndOfDayReview();
      });
    }
  };

  CorporateOfficeSimulator.prototype.completeTask = function (taskId, points, feedbackMsg) {
    for (var i = 0; i < this.tasks.length; i++) {
      if (this.tasks[i].id === taskId && !this.tasks[i].completed) {
        this.tasks[i].completed = true;
        this.tasks[i].score = points;

        var row = document.getElementById("simTaskRow_" + taskId);
        if (row) {
          row.classList.add("text-success", "fw-bold");
          var badge = row.querySelector(".badge");
          if (badge) {
            badge.className = "badge bg-success";
            badge.textContent = "✓ COMPLETED (+" + points + " XP)";
          }
        }

        var toast = document.getElementById("simNotificationToast");
        var toastBody = document.getElementById("simNotificationBody");
        if (toast && toastBody) {
          toastBody.textContent = feedbackMsg;
          toast.style.display = "block";
          setTimeout(function () { toast.style.display = "none"; }, 4500);
        }
        break;
      }
    }
    this.updateReadinessMeter();

    // Check if all tasks complete
    var allDone = this.tasks.every(function (t) { return t.completed; });
    if (allDone) {
      var self = this;
      setTimeout(function () {
        self.showEndOfDayReview();
      }, 1000);
    }
  };

  CorporateOfficeSimulator.prototype.updateReadinessMeter = function () {
    var completed = this.tasks.filter(function (t) { return t.completed; }).length;
    var pct = Math.round((completed / this.tasks.length) * 100);
    var meter = document.getElementById("simReadinessPct");
    var bar = document.getElementById("simReadinessBar");
    if (meter) meter.textContent = pct + "% Integrity";
    if (bar) bar.style.width = pct + "%";
  };

  CorporateOfficeSimulator.prototype.showEndOfDayReview = function () {
    var completed = this.tasks.filter(function (t) { return t.completed; }).length;
    var totalPoints = this.tasks.reduce(function (acc, t) { return acc + t.score; }, 0);
    var timeSpent = 600 - this.timeRemaining;
    var mins = Math.floor(timeSpent / 60);
    var secs = timeSpent % 60;
    var durationStr = mins + "m " + secs + "s";

    var modal = document.getElementById("simEndOfDayModal");
    if (modal) {
      var tasksEl = document.getElementById("simReviewTasks");
      var timeEl = document.getElementById("simReviewTime");
      var mistakesEl = document.getElementById("simReviewMistakes");
      var xpEl = document.getElementById("simReviewXP");

      if (tasksEl) tasksEl.textContent = completed + " / " + this.tasks.length;
      if (timeEl) timeEl.textContent = durationStr;
      if (mistakesEl) mistakesEl.textContent = this.mistakesCount;
      if (xpEl) xpEl.textContent = "+" + totalPoints + " XP";

      modal.style.display = "flex";
      this.playSound("success");
    }

    this.submitBackendCompletion(totalPoints, timeSpent);
  };

  CorporateOfficeSimulator.prototype.submitBackendCompletion = function (score, timeSpent) {
    var url = "/api/games/" + encodeURIComponent(this.gameSlug) + "/complete";
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": this.csrfToken
      },
      body: JSON.stringify({
        score: score,
        total: 100,
        time_spent: timeSpent
      })
    })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        var alertEl = document.getElementById("simReviewApiFeedback");
        if (alertEl && data.ok) {
          alertEl.style.display = "block";
          alertEl.innerHTML = "<strong>✓ Server Confirmed:</strong> Awarded <strong>+" + (data.xp_awarded || 100) + " XP</strong>! Total XP: <strong>" + (data.total_xp || "Updated") + "</strong>";
        }
      })
      .catch(function (err) {
        console.error("Shift completion submission error:", err);
      });
  };

  window.CorporateOfficeSimulator = CorporateOfficeSimulator;

})(window);
