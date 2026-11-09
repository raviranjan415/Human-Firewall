/**
 * Human Firewall — 2D Interactive Cybersecurity Adventure Game Engine
 * 
 * Supports:
 * - 2D Top-down open-world movement (WASD, Arrow keys, Shift to run, Touch D-Pad)
 * - Dynamic environments: Digital City, Corporate Office, Computer Lab, SOC Operations, Escape Room
 * - Animated characters with 4-way direction, walk cycles, dust particles, and shadows
 * - Autonomous NPCs with floating quest indicators (!), proximity interaction ([E] Talk)
 * - In-game interactive devices (Smartphone, Terminal, SIEM Workstation, Door Ciphers)
 * - Real-time cybersecurity investigation (inspect sender, link hover, attachment scan, threat triage)
 * - Server-side XP awarding, progress sync, and educational debriefs
 * - Built-in sound synthesis via Web Audio API
 */

(function (window, document) {
  "use strict";

  // =========================================================================
  // 1. Audio Synthesizer (Web Audio API)
  // =========================================================================
  class AudioSynth {
    constructor() {
      this.ctx = null;
      this.enabled = true;
    }

    _init() {
      if (!this.ctx && (window.AudioContext || window.webkitAudioContext)) {
        this.ctx = new (window.AudioContext || window.webkitAudioContext)();
      }
      if (this.ctx && this.ctx.state === "suspended") {
        this.ctx.resume();
      }
    }

    play(type) {
      if (!this.enabled) return;
      try {
        this._init();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.connect(gain);
        gain.connect(this.ctx.destination);

        if (type === "step") {
          osc.type = "sine";
          osc.frequency.setValueAtTime(140, now);
          osc.frequency.exponentialRampToValueAtTime(80, now + 0.04);
          gain.gain.setValueAtTime(0.04, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
          osc.start(now);
          osc.stop(now + 0.04);
        } else if (type === "chirp" || type === "talk") {
          osc.type = "triangle";
          osc.frequency.setValueAtTime(580, now);
          osc.frequency.setValueAtTime(740, now + 0.05);
          gain.gain.setValueAtTime(0.08, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
          osc.start(now);
          osc.stop(now + 0.1);
        } else if (type === "notify") {
          osc.type = "sine";
          osc.frequency.setValueAtTime(523.25, now); // C5
          osc.frequency.setValueAtTime(659.25, now + 0.08); // E5
          gain.gain.setValueAtTime(0.12, now);
          gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);
          osc.start(now);
          osc.stop(now + 0.25);
        } else if (type === "success") {
          // Upbeat fanfare C5 -> E5 -> G5 -> C6
          const notes = [523.25, 659.25, 783.99, 1046.5];
          notes.forEach((freq, idx) => {
            const o = this.ctx.createOscillator();
            const g = this.ctx.createGain();
            o.connect(g);
            g.connect(this.ctx.destination);
            o.type = "sine";
            o.frequency.setValueAtTime(freq, now + idx * 0.07);
            g.gain.setValueAtTime(0.15, now + idx * 0.07);
            g.gain.exponentialRampToValueAtTime(0.01, now + idx * 0.07 + 0.25);
            o.start(now + idx * 0.07);
            o.stop(now + idx * 0.07 + 0.25);
          });
        } else if (type === "fail" || type === "error") {
          osc.type = "sawtooth";
          osc.frequency.setValueAtTime(220, now);
          osc.frequency.exponentialRampToValueAtTime(110, now + 0.3);
          gain.gain.setValueAtTime(0.18, now);
          gain.gain.exponentialRampToValueAtTime(0.01, now + 0.35);
          osc.start(now);
          osc.stop(now + 0.35);
        }
      } catch (err) {
        // audio muted or restricted by user interaction policy
      }
    }
  }

  // =========================================================================
  // 2. TileMap & World Environments
  // =========================================================================
  class TileMap {
    constructor(genre = "city", width = 1600, height = 1100) {
      this.genre = genre;
      this.width = width;
      this.height = height;
      this.solidBoxes = [];
      this.decorations = [];
      this.buildings = [];
      this.initEnvironment();
    }

    initEnvironment() {
      this.solidBoxes = [];
      this.decorations = [];
      this.buildings = [];

      // World Boundary Collisions
      this.solidBoxes.push({ x: 0, y: 0, w: this.width, h: 20 });
      this.solidBoxes.push({ x: 0, y: this.height - 20, w: this.width, h: 20 });
      this.solidBoxes.push({ x: 0, y: 0, w: 20, h: this.height });
      this.solidBoxes.push({ x: this.width - 20, y: 0, w: 20, h: this.height });

      if (this.genre === "office") {
        // Corporate Office Layout: Lobby, Workspaces, Server Room, Break Room
        this.buildings.push({
          name: "Server Room (Restricted)",
          x: 950,
          y: 80,
          w: 480,
          h: 300,
          color: "#1e293b",
          roof: "#0f172a",
          door: { x: 1150, y: 380, label: "Server Vault [Keycard]" },
        });
        this.buildings.push({
          name: "Executive Suite",
          x: 100,
          y: 80,
          w: 420,
          h: 280,
          color: "#334155",
          roof: "#1e293b",
          door: { x: 280, y: 360, label: "Executive Office" },
        });
        this.buildings.push({
          name: "Employee Break Room",
          x: 100,
          y: 650,
          w: 420,
          h: 320,
          color: "#334155",
          roof: "#1e293b",
          door: { x: 280, y: 650, label: "Break Room & Café" },
        });

        // Add Solid Desks & Turnstiles
        this.solidBoxes.push({ x: 620, y: 480, w: 320, h: 40 }); // Security Turnstiles
        this.solidBoxes.push({ x: 700, y: 680, w: 240, h: 80 }); // Open Desk Pod A
        this.solidBoxes.push({ x: 1050, y: 680, w: 240, h: 80 }); // Open Desk Pod B
      } else if (this.genre === "soc" || this.genre === "lab") {
        // SOC & Computer Lab Environment
        this.buildings.push({
          name: "SIEM Threat Wall & SOC Pods",
          x: 200,
          y: 80,
          w: 1200,
          h: 220,
          color: "#0f172a",
          roof: "#0284c7",
          door: { x: 760, y: 300, label: "SOC Mainframe" },
        });
        this.solidBoxes.push({ x: 300, y: 480, w: 280, h: 90 }); // Analyst Pod Alpha
        this.solidBoxes.push({ x: 920, y: 480, w: 280, h: 90 }); // Analyst Pod Bravo
        this.solidBoxes.push({ x: 300, y: 720, w: 900, h: 70 }); // Server Quarantine Rack
      } else if (this.genre === "escaperoom") {
        // Multi-Room Puzzle Dungeon
        // Room A: Authentication Chamber
        this.buildings.push({
          name: "Chamber 1: Password Vault",
          x: 80,
          y: 80,
          w: 420,
          h: 400,
          color: "#1e293b",
          roof: "#3b82f6",
          door: { x: 500, y: 260, label: "Cipher Gate 1" },
        });
        // Room B: Encryption Core
        this.buildings.push({
          name: "Chamber 2: Firewall Core",
          x: 580,
          y: 80,
          w: 440,
          h: 400,
          color: "#1e293b",
          roof: "#10b981",
          door: { x: 1020, y: 260, label: "Cipher Gate 2" },
        });
        // Room C: Exit Portal
        this.buildings.push({
          name: "Chamber 3: Emergency Exit",
          x: 1100,
          y: 80,
          w: 420,
          h: 400,
          color: "#1e293b",
          roof: "#f59e0b",
          door: { x: 1280, y: 480, label: "Extraction Airlock" },
        });
      } else {
        // Default: Digital City (Phishing City, URL Inspector, Wi-Fi Warrior)
        // 1. Central National Bank
        this.buildings.push({
          name: "First National Cyber Bank",
          x: 100,
          y: 80,
          w: 420,
          h: 280,
          color: "#1e293b",
          roof: "#2563eb",
          door: { x: 280, y: 360, label: "Bank Main Entrance" },
        });
        // 2. Cyber Coffee Shop
        this.buildings.push({
          name: "Byte & Brew Coffee",
          x: 620,
          y: 80,
          w: 380,
          h: 280,
          color: "#334155",
          roof: "#d97706",
          door: { x: 780, y: 360, label: "Coffee Shop [Free Wi-Fi]" },
        });
        // 3. Cyber Internet Café & Tech Hub
        this.buildings.push({
          name: "Matrix Internet Café",
          x: 1100,
          y: 80,
          w: 400,
          h: 280,
          color: "#1e293b",
          roof: "#059669",
          door: { x: 1280, y: 360, label: "Internet Café Terminal" },
        });
        // 4. City Hall & Police Station
        this.buildings.push({
          name: "Cyber Crime Police Bureau",
          x: 100,
          y: 680,
          w: 460,
          h: 300,
          color: "#1e293b",
          roof: "#4f46e5",
          door: { x: 300, y: 680, label: "Police Reporting Desk" },
        });
        // 5. Corporate Tech Tower
        this.buildings.push({
          name: "Apex Global Technology",
          x: 950,
          y: 680,
          w: 550,
          h: 300,
          color: "#0f172a",
          roof: "#0284c7",
          door: { x: 1200, y: 680, label: "Corporate HQ Lobby" },
        });
      }

      // Add building structures to solid collision boxes
      this.buildings.forEach((b) => {
        this.solidBoxes.push({ x: b.x, y: b.y, w: b.w, h: b.h });
      });
    }

    collides(x, y, radius = 18) {
      for (let i = 0; i < this.solidBoxes.length; i++) {
        const box = this.solidBoxes[i];
        if (
          x + radius > box.x &&
          x - radius < box.x + box.w &&
          y + radius > box.y &&
          y - radius < box.y + box.h
        ) {
          return true;
        }
      }
      return false;
    }

    render(ctx, camera) {
      // 1. Draw World Ground (Roads & Sidewalks / Indoor Tiles)
      if (this.genre === "office" || this.genre === "soc" || this.genre === "lab") {
        ctx.fillStyle = "#0b1329";
        ctx.fillRect(0, 0, this.width, this.height);

        // Office Grid / Floor Mats
        ctx.strokeStyle = "rgba(255, 255, 255, 0.04)";
        ctx.lineWidth = 1;
        for (let x = 0; x < this.width; x += 64) {
          ctx.beginPath();
          ctx.moveTo(x, 0);
          ctx.lineTo(x, this.height);
          ctx.stroke();
        }
        for (let y = 0; y < this.height; y += 64) {
          ctx.beginPath();
          ctx.moveTo(0, y);
          ctx.lineTo(this.width, y);
          ctx.stroke();
        }
      } else {
        // Digital City: Grass base + Roads + Sidewalks
        ctx.fillStyle = "#0d1b2a";
        ctx.fillRect(0, 0, this.width, this.height);

        // Main Cross Streets (Asphalt Road)
        ctx.fillStyle = "#162238";
        // Horizontal Main Ave
        ctx.fillRect(0, 440, this.width, 160);
        // Vertical Central Blvd
        ctx.fillRect(680, 0, 180, this.height);

        // Road Markings (Dashed Yellow Lines)
        ctx.strokeStyle = "#eab308";
        ctx.lineWidth = 4;
        ctx.setLineDash([24, 20]);

        // Horizontal Road divider
        ctx.beginPath();
        ctx.moveTo(0, 520);
        ctx.lineTo(this.width, 520);
        ctx.stroke();

        // Vertical Road divider
        ctx.beginPath();
        ctx.moveTo(770, 0);
        ctx.lineTo(770, this.height);
        ctx.stroke();
        ctx.setLineDash([]); // Reset dash

        // Pedestrian Crosswalks
        ctx.fillStyle = "#ffffff";
        for (let i = 0; i < 6; i++) {
          ctx.fillRect(640, 450 + i * 24, 30, 14);
          ctx.fillRect(870, 450 + i * 24, 30, 14);
        }
      }

      // 2. Draw Buildings & Structures
      this.buildings.forEach((b) => {
        // Building Shadow
        ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
        ctx.fillRect(b.x + 10, b.y + 10, b.w, b.h);

        // Building Body
        ctx.fillStyle = b.color;
        ctx.fillRect(b.x, b.y, b.w, b.h);

        // Building Roof Trim
        ctx.fillStyle = b.roof;
        ctx.fillRect(b.x, b.y, b.w, 36);

        // Building Title Header
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 15px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
        ctx.textAlign = "center";
        ctx.fillText(b.name, b.x + b.w / 2, b.y + 24);

        // Building Windows Grid
        ctx.fillStyle = "rgba(147, 197, 253, 0.25)";
        const cols = Math.floor(b.w / 70);
        const rows = Math.floor((b.h - 80) / 60);
        for (let c = 0; c < cols; c++) {
          for (let r = 0; r < rows; r++) {
            ctx.fillRect(b.x + 25 + c * 70, b.y + 60 + r * 60, 40, 32);
          }
        }

        // Building Door Entrance
        if (b.door) {
          ctx.fillStyle = "#f59e0b";
          ctx.fillRect(b.door.x - 30, b.door.y - 12, 60, 24);
          ctx.fillStyle = "#000000";
          ctx.font = "bold 11px sans-serif";
          ctx.fillText("DOOR", b.door.x, b.door.y + 4);
        }
      });

      // 3. Draw Solid Furniture / Turnstiles
      this.solidBoxes.forEach((box) => {
        // Only draw non-building interior obstacles
        if (!this.buildings.some((b) => b.x === box.x && b.y === box.y)) {
          ctx.fillStyle = "#334155";
          ctx.fillRect(box.x, box.y, box.w, box.h);
          ctx.strokeStyle = "#475569";
          ctx.lineWidth = 2;
          ctx.strokeRect(box.x, box.y, box.w, box.h);
        }
      });
    }
  }

  // =========================================================================
  // 3. Player Character Controller
  // =========================================================================
  class Player {
    constructor(x, y) {
      this.x = x;
      this.y = y;
      this.radius = 18;
      this.speed = 3.2;
      this.runSpeed = 5.5;
      this.direction = 0; // 0: down, 1: left, 2: right, 3: up
      this.animStep = 0;
      this.isMoving = false;
      this.isRunning = false;
      this.particles = [];
    }

    update(keys, tileMap, audioSynth) {
      let dx = 0;
      let dy = 0;

      if (keys["ArrowUp"] || keys["KeyW"]) dy -= 1;
      if (keys["ArrowDown"] || keys["KeyS"]) dy += 1;
      if (keys["ArrowLeft"] || keys["KeyA"]) dx -= 1;
      if (keys["ArrowRight"] || keys["KeyD"]) dx += 1;

      this.isRunning = Boolean(keys["ShiftLeft"] || keys["ShiftRight"] || keys["RunBtn"]);
      const currentSpeed = this.isRunning ? this.runSpeed : this.speed;

      this.isMoving = dx !== 0 || dy !== 0;

      if (this.isMoving) {
        // Determine Direction
        if (dy > 0) this.direction = 0;
        else if (dy < 0) this.direction = 3;
        else if (dx < 0) this.direction = 1;
        else if (dx > 0) this.direction = 2;

        // Normalize Diagonal Speed
        if (dx !== 0 && dy !== 0) {
          dx *= 0.7071;
          dy *= 0.7071;
        }

        const nextX = this.x + dx * currentSpeed;
        const nextY = this.y + dy * currentSpeed;

        // Collision Check with sliding
        if (!tileMap.collides(nextX, this.y, this.radius)) {
          this.x = nextX;
        }
        if (!tileMap.collides(this.x, nextY, this.radius)) {
          this.y = nextY;
        }

        this.animStep += this.isRunning ? 0.35 : 0.2;
        if (Math.sin(this.animStep) > 0.95) {
          audioSynth.play("step");
        }

        // Running Dust Particles
        if (this.isRunning && Math.random() < 0.4) {
          this.particles.push({
            x: this.x + (Math.random() * 12 - 6),
            y: this.y + 14,
            r: Math.random() * 4 + 2,
            alpha: 0.6,
          });
        }
      }

      // Update Particles
      for (let i = this.particles.length - 1; i >= 0; i--) {
        const p = this.particles[i];
        p.alpha -= 0.05;
        p.r *= 0.95;
        if (p.alpha <= 0) this.particles.splice(i, 1);
      }
    }

    render(ctx) {
      // 1. Draw Dust Particles
      this.particles.forEach((p) => {
        ctx.fillStyle = `rgba(203, 213, 225, ${p.alpha})`;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fill();
      });

      // 2. Drop Shadow
      ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
      ctx.beginPath();
      ctx.ellipse(this.x, this.y + 16, 16, 7, 0, 0, Math.PI * 2);
      ctx.fill();

      // 3. Animated Legs (Walk cycle)
      const walkOffset = this.isMoving ? Math.sin(this.animStep) * 6 : 0;
      ctx.fillStyle = "#1e293b";
      // Left leg
      ctx.fillRect(this.x - 7, this.y + 6 - walkOffset, 5, 12 + walkOffset);
      // Right leg
      ctx.fillRect(this.x + 2, this.y + 6 + walkOffset, 5, 12 - walkOffset);

      // 4. Torso / Cyber Defender Jacket
      ctx.fillStyle = "#2563eb";
      ctx.beginPath();
      ctx.roundRect(this.x - 11, this.y - 12, 22, 20, 4);
      ctx.fill();

      // Defender Badge / Collar
      ctx.fillStyle = "#38bdf8";
      ctx.fillRect(this.x - 3, this.y - 10, 6, 6);

      // 5. Head & Cyber Visor
      ctx.fillStyle = "#fcd34d"; // Skin
      ctx.beginPath();
      ctx.arc(this.x, this.y - 20, 11, 0, Math.PI * 2);
      ctx.fill();

      // Hair
      ctx.fillStyle = "#0f172a";
      ctx.beginPath();
      ctx.arc(this.x, this.y - 24, 11, Math.PI, Math.PI * 2);
      ctx.fill();

      // Visor / Eyes based on direction
      ctx.fillStyle = "#0284c7";
      if (this.direction === 0) {
        // Facing down
        ctx.fillRect(this.x - 6, this.y - 21, 12, 4);
      } else if (this.direction === 1) {
        // Facing left
        ctx.fillRect(this.x - 9, this.y - 21, 6, 4);
      } else if (this.direction === 2) {
        // Facing right
        ctx.fillRect(this.x + 3, this.y - 21, 6, 4);
      }

      // Overhead Player Tag
      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 12px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("Human Defender", this.x, this.y - 38);
    }
  }

  // =========================================================================
  // 4. Non-Player Characters (NPCs) & Mission Givers
  // =========================================================================
  class NPC {
    constructor(spec) {
      this.id = spec.id;
      this.name = spec.name;
      this.role = spec.role;
      this.x = spec.x;
      this.y = spec.y;
      this.scenarioIndex = spec.scenarioIndex;
      this.color = spec.color || "#10b981";
      this.hair = spec.hair || "#78350f";
      this.status = "quest"; // 'quest', 'done'
      this.animOffset = Math.random() * Math.PI;
    }

    render(ctx, playerX, playerY) {
      const dist = Math.hypot(this.x - playerX, this.y - playerY);
      const isNearby = dist < 75;

      // Drop shadow
      ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
      ctx.beginPath();
      ctx.ellipse(this.x, this.y + 16, 14, 6, 0, 0, Math.PI * 2);
      ctx.fill();

      // Subtle Idle Bobbing
      const bob = Math.sin(Date.now() / 350 + this.animOffset) * 2;

      // Torso
      ctx.fillStyle = this.color;
      ctx.beginPath();
      ctx.roundRect(this.x - 10, this.y - 12 + bob, 20, 20, 4);
      ctx.fill();

      // Head
      ctx.fillStyle = "#fde68a";
      ctx.beginPath();
      ctx.arc(this.x, this.y - 20 + bob, 10, 0, Math.PI * 2);
      ctx.fill();

      // Hair
      ctx.fillStyle = this.hair;
      ctx.beginPath();
      ctx.arc(this.x, this.y - 24 + bob, 10, Math.PI, Math.PI * 2);
      ctx.fill();

      // Overhead Name & Role Tag
      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 11px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(this.name, this.x, this.y - 36 + bob);

      ctx.fillStyle = "#94a3b8";
      ctx.font = "10px sans-serif";
      ctx.fillText(this.role, this.x, this.y - 25 + bob);

      // Quest / Status Icon
      if (this.status === "quest") {
        // Bobbing Exclamation Mark (!)
        const exBob = Math.sin(Date.now() / 200) * 4;
        ctx.fillStyle = "#f59e0b";
        ctx.beginPath();
        ctx.arc(this.x, this.y - 54 + exBob, 11, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#000000";
        ctx.font = "bold 14px sans-serif";
        ctx.fillText("!", this.x, this.y - 49 + exBob);
      } else {
        // Protected Checkmark (✓)
        ctx.fillStyle = "#10b981";
        ctx.beginPath();
        ctx.arc(this.x, this.y - 52, 9, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 11px sans-serif";
        ctx.fillText("✓", this.x, this.y - 48);
      }

      // Proximity Interaction Prompt [E]
      if (isNearby && this.status === "quest") {
        ctx.fillStyle = "rgba(15, 23, 42, 0.9)";
        ctx.beginPath();
        ctx.roundRect(this.x - 48, this.y + 24, 96, 26, 6);
        ctx.fill();
        ctx.strokeStyle = "#38bdf8";
        ctx.lineWidth = 1.5;
        ctx.stroke();

        ctx.fillStyle = "#38bdf8";
        ctx.font = "bold 11px sans-serif";
        ctx.fillText("Press [E] to Talk", this.x, this.y + 41);
      }
    }
  }

  // =========================================================================
  // 5. In-Game Device / Smartphone / Terminal Overlay Interface
  // =========================================================================
  class InGameDeviceUI {
    constructor(overlayElement, audioSynth, onAnswerSubmit) {
      this.overlay = overlayElement;
      this.audioSynth = audioSynth;
      this.onAnswerSubmit = onAnswerSubmit;
      this.activeScenario = null;
      this.activeNPC = null;
      this.isOpen = false;
    }

    open(npc, scenario) {
      this.activeNPC = npc;
      this.activeScenario = scenario;
      this.isOpen = true;
      this.audioSynth.play("notify");

      this.overlay.innerHTML = "";
      this.overlay.style.display = "flex";

      const deviceWrap = document.createElement("div");
      deviceWrap.className = "cq-game2d-phone-mockup cq-fade-in";

      // Device Top Header / Notch
      const phoneHeader = document.createElement("div");
      phoneHeader.className = "cq-phone-notch d-flex justify-content-between align-items-center px-3 py-1";
      phoneHeader.innerHTML = `
        <span class="small text-light fw-bold">9:41 AM</span>
        <div class="cq-phone-sensor"></div>
        <span class="small text-light">100% 🔋</span>
      `;
      deviceWrap.appendChild(phoneHeader);

      // App Title Bar
      const appTitle = document.createElement("div");
      appTitle.className = "bg-primary text-white p-2 d-flex justify-content-between align-items-center";
      appTitle.innerHTML = `
        <div>
          <span class="badge bg-dark me-1">🛡️ CYBER-ALERT</span>
          <strong>${npc.name} (${npc.role})</strong>
        </div>
        <button type="button" class="btn btn-sm btn-outline-light py-0 px-2" id="closePhoneBtn">&times;</button>
      `;
      deviceWrap.appendChild(appTitle);

      // Message Body Content
      const contentBox = document.createElement("div");
      contentBox.className = "p-3 bg-dark text-light overflow-auto";
      contentBox.style.maxHeight = "360px";

      const bubble = document.createElement("div");
      bubble.className = "p-3 rounded-3 bg-secondary bg-opacity-25 border border-secondary mb-3";
      bubble.innerHTML = `
        <div class="small text-warning fw-bold mb-1">Incoming Communication Received by Citizen:</div>
        <div class="d-flex justify-content-between small text-secondary border-bottom border-secondary pb-1 mb-2">
          <span>From: <strong class="text-info">${scenario.sender || "External Contact"}</strong></span>
          <span>${scenario.type ? scenario.type.toUpperCase() : "MESSAGE"}</span>
        </div>
        ${scenario.subject ? `<div class="fw-bold text-light mb-2">${scenario.subject}</div>` : ""}
        <div class="font-monospace small p-2 rounded bg-black bg-opacity-50 text-light" style="white-space: pre-wrap;">${scenario.body || "No text payload"}</div>
      `;
      contentBox.appendChild(bubble);

      // Clue Radar / Tooltips
      const clueBar = document.createElement("div");
      clueBar.className = "d-flex gap-2 mb-3";
      clueBar.innerHTML = `
        <button type="button" class="btn btn-outline-info btn-sm flex-fill" id="inspectDomainBtn">🔍 Inspect Domain</button>
        <button type="button" class="btn btn-outline-warning btn-sm flex-fill" id="inspectUrgencyBtn">⏰ Clue Radar</button>
      `;
      contentBox.appendChild(clueBar);

      const clueFeedback = document.createElement("div");
      clueFeedback.id = "clueFeedbackBox";
      clueFeedback.className = "alert alert-secondary small p-2 mb-3"
      clueFeedback.style.display = "none";
      contentBox.appendChild(clueFeedback);

      // Decision Actions
      const actionsWrap = document.createElement("div");
      actionsWrap.className = "d-grid gap-2";

      if (scenario.choices && scenario.choices.length > 0) {
        scenario.choices.forEach((choice) => {
          const btn = document.createElement("button");
          btn.type = "button";
          btn.className = "btn btn-outline-light text-start small py-2 px-3";
          btn.innerHTML = `<strong>&rarr;</strong> ${choice.text}`;
          btn.addEventListener("click", () => {
            this._submitChoice(choice.id, btn, contentBox);
          });
          actionsWrap.appendChild(btn);
        });
      } else {
        // Binary choice: Threat vs Safe
        const btnThreat = document.createElement("button");
        btnThreat.type = "button";
        btnThreat.className = "btn btn-danger py-2 fw-bold";
        btnThreat.innerHTML = "🚨 Block & Report as Security Threat";
        btnThreat.addEventListener("click", () => {
          this._submitThreatChoice(true, btnThreat, contentBox);
        });

        const btnSafe = document.createElement("button");
        btnSafe.type = "button";
        btnSafe.className = "btn btn-success py-2 fw-bold";
        btnSafe.innerHTML = "✅ Mark as Verified Safe & Allow";
        btnSafe.addEventListener("click", () => {
          this._submitThreatChoice(false, btnSafe, contentBox);
        });

        actionsWrap.appendChild(btnThreat);
        actionsWrap.appendChild(btnSafe);
      }

      contentBox.appendChild(actionsWrap);
      deviceWrap.appendChild(contentBox);
      this.overlay.appendChild(deviceWrap);

      // Event Listeners
      document.getElementById("closePhoneBtn").addEventListener("click", () => this.close());
      document.getElementById("inspectDomainBtn").addEventListener("click", () => {
        const box = document.getElementById("clueFeedbackBox");
        box.style.display = "block";
        box.className = "alert alert-info small p-2 mb-3";
        box.innerHTML = `<strong>Domain Analysis:</strong> Check sender <code>${scenario.sender}</code> against authentic corporate domains. Look for subtle spelling mutations or odd top-level domains.`;
      });
      document.getElementById("inspectUrgencyBtn").addEventListener("click", () => {
        const box = document.getElementById("clueFeedbackBox");
        box.style.display = "block";
        box.className = "alert alert-warning small p-2 mb-3";
        box.innerHTML = `<strong>Psychological Trigger:</strong> Threat actors use artificial panic (e.g. <em>"Account blocked in 15 mins!"</em>) to bypass your analytical thinking.`;
      });
    }

    _submitChoice(choiceId, btn, container) {
      this.onAnswerSubmit(this.activeScenario.id, { choice_id: choiceId }, (res) => {
        this._displayResult(res, btn, container);
      });
    }

    _submitThreatChoice(isThreat, btn, container) {
      this.onAnswerSubmit(this.activeScenario.id, { is_threat: isThreat }, (res) => {
        this._displayResult(res, btn, container);
      });
    }

    _displayResult(res, btn, container) {
      const isCorrect = res.correct;
      if (isCorrect) {
        btn.className = "btn btn-success text-start small py-2 px-3 fw-bold";
        this.audioSynth.play("success");
        this.activeNPC.status = "done";
      } else {
        btn.className = "btn btn-danger text-start small py-2 px-3 fw-bold";
        this.audioSynth.play("fail");
      }

      const resultBox = document.createElement("div");
      resultBox.className = `alert ${isCorrect ? "alert-success" : "alert-danger"} mt-3 small`;
      resultBox.innerHTML = `
        <div class="fw-bold fs-6 mb-1">${isCorrect ? "🛡️ Threat Prevented!" : "⚠️ Defense Bypassed!"}</div>
        <p class="mb-2">${res.feedback || ""}</p>
        <div class="border-top border-secondary pt-2">
          <strong>Key Cybersecurity Principle:</strong> ${res.explanation || "Always verify through independent channels."}
        </div>
        ${res.warning_signs ? `<div class="mt-1 text-warning"><strong>Caught Clue:</strong> ${res.warning_signs}</div>` : ""}
        <div class="text-end mt-2">
          <button type="button" class="btn btn-primary btn-sm px-3 fw-bold" id="continueMissionBtn">Continue Patrol &rarr;</button>
        </div>
      `;
      container.appendChild(resultBox);
      resultBox.scrollIntoView({ behavior: "smooth" });

      document.getElementById("continueMissionBtn").addEventListener("click", () => {
        this.close();
      });
    }

    close() {
      this.isOpen = false;
      this.overlay.style.display = "none";
      this.overlay.innerHTML = "";
    }
  }

  // =========================================================================
  // 6. Master 2D Adventure Game Coordinator
  // =========================================================================
  class Game2DEngine {
    constructor(config) {
      this.canvas = document.getElementById(config.canvasId);
      this.ctx = this.canvas.getContext("2d");
      this.slug = config.slug;
      this.scenarios = config.scenarios || [];
      this.genre = config.genre || "city";
      this.overlay = document.getElementById(config.overlayId);

      this.score = 0;
      this.completedMissions = 0;
      this.totalMissions = this.scenarios.length;
      this.startTime = Date.now();

      this.audio = new AudioSynth();
      this.tileMap = new TileMap(this.genre, 1600, 1100);
      this.player = new Player(400, 520);
      this.camera = { x: 0, y: 0, w: 960, h: 540 };

      this.keys = {};
      this.npcs = [];
      this.initNPCs();

      this.deviceUI = new InGameDeviceUI(this.overlay, this.audio, this.handleAnswer.bind(this));

      this._bindInputs();
      this._resizeCanvas();
      window.addEventListener("resize", () => this._resizeCanvas());

      this.running = true;
      requestAnimationFrame(this.gameLoop.bind(this));
    }

    initNPCs() {
      this.npcs = [];
      // Setup NPCs according to scenarios available
      const npcConfigs = [
        { name: "Maya Patel", role: "Coffee Shop Guest", x: 740, y: 390, color: "#ec4899", hair: "#1f2937" },
        { name: "Mr. Sharma", role: "Bank Branch Manager", x: 260, y: 380, color: "#3b82f6", hair: "#64748b" },
        { name: "Rahul Verma", role: "Student / Gamer", x: 1240, y: 380, color: "#10b981", hair: "#9a3412" },
        { name: "Officer Neha", role: "Police Cyber Desk", x: 320, y: 690, color: "#6366f1", hair: "#0f172a" },
        { name: "Dev Vikram", role: "Corporate Employee", x: 1180, y: 690, color: "#eab308", hair: "#374151" },
      ];

      this.scenarios.forEach((sc, idx) => {
        const spec = npcConfigs[idx % npcConfigs.length];
        this.npcs.push(
          new NPC({
            id: sc.id,
            name: spec.name,
            role: spec.role,
            x: spec.x,
            y: spec.y,
            color: spec.color,
            hair: spec.hair,
            scenarioIndex: idx,
          })
        );
      });
    }

    _bindInputs() {
      window.addEventListener("keydown", (e) => {
        this.keys[e.code] = true;
        if (e.code === "KeyE" || e.code === "Space") {
          this.interactNearestNPC();
        }
      });

      window.addEventListener("keyup", (e) => {
        this.keys[e.code] = false;
      });

      // Virtual D-Pad for Mobile Touch
      const dpadKeys = ["Up", "Down", "Left", "Right"];
      dpadKeys.forEach((dir) => {
        const btn = document.getElementById(`dpad${dir}`);
        if (btn) {
          const code = `Arrow${dir}`;
          btn.addEventListener("touchstart", (e) => {
            e.preventDefault();
            this.keys[code] = true;
          });
          btn.addEventListener("touchend", (e) => {
            e.preventDefault();
            this.keys[code] = false;
          });
        }
      });

      const touchInteract = document.getElementById("touchInteractBtn");
      if (touchInteract) {
        touchInteract.addEventListener("touchstart", (e) => {
          e.preventDefault();
          this.interactNearestNPC();
        });
      }
    }

    _resizeCanvas() {
      // Internal virtual resolution is 960x540 for crisp rendering
      this.canvas.width = 960;
      this.canvas.height = 540;
      this.camera.w = 960;
      this.camera.h = 540;
    }

    interactNearestNPC() {
      if (this.deviceUI.isOpen) return;

      for (let i = 0; i < this.npcs.length; i++) {
        const npc = this.npcs[i];
        const dist = Math.hypot(npc.x - this.player.x, npc.y - this.player.y);
        if (dist < 75 && npc.status === "quest") {
          const scenario = this.scenarios[npc.scenarioIndex];
          this.deviceUI.open(npc, scenario);
          break;
        }
      }
    }

    handleAnswer(scenarioId, payload, callback) {
      const url = `/api/games/${encodeURIComponent(this.slug)}/answer`;
      payload.scenario_id = scenarioId;

      window.CQ.post(url, payload)
        .then((res) => {
          if (!res.ok) {
            window.CQ.toast("Network verification error. Please retry.", "error");
            return;
          }
          const body = res.body || {};
          if (body.correct) {
            this.score += body.xp_value || 25;
            this.completedMissions += 1;
            const hudScore = document.getElementById("hud2DScore");
            if (hudScore) hudScore.textContent = `${this.score} XP`;

            const hudProg = document.getElementById("hud2DProgress");
            if (hudProg) hudProg.textContent = `${this.completedMissions}/${this.totalMissions} Protected`;

            if (this.completedMissions >= this.totalMissions) {
              setTimeout(() => this.completeGame(), 1500);
            }
          }
          callback(body);
        })
        .catch(() => {
          window.CQ.toast("Server connection failed.", "error");
        });
    }

    completeGame() {
      const completeUrl = `/api/games/${encodeURIComponent(this.slug)}/complete`;
      const elapsed = Math.round((Date.now() - this.startTime) / 1000);

      window.CQ.post(completeUrl, { score: this.score, elapsed_seconds: elapsed }).then((res) => {
        const resultScreen = document.getElementById("game2DResultModal");
        if (resultScreen) {
          resultScreen.style.display = "flex";
          document.getElementById("res2DScore").textContent = `${this.score} XP`;
          document.getElementById("res2DAccuracy").textContent = `${this.completedMissions} of ${this.totalMissions} Threats Handled`;
          this.audio.play("success");
        }
      });
    }

    updateCamera() {
      // Center camera smoothly on player
      this.camera.x = this.player.x - this.camera.w / 2;
      this.camera.y = this.player.y - this.camera.h / 2;

      // Clamp camera to map boundaries
      this.camera.x = Math.max(0, Math.min(this.tileMap.width - this.camera.w, this.camera.x));
      this.camera.y = Math.max(0, Math.min(this.tileMap.height - this.camera.h, this.camera.y));
    }

    renderHUD() {
      // 1. Mission Objective HUD (Top-Left)
      this.ctx.fillStyle = "rgba(15, 23, 42, 0.85)";
      this.ctx.beginPath();
      this.ctx.roundRect(16, 16, 260, 68, 8);
      this.ctx.fill();
      this.ctx.strokeStyle = "#38bdf8";
      this.ctx.lineWidth = 1.5;
      this.ctx.stroke();

      this.ctx.fillStyle = "#38bdf8";
      this.ctx.font = "bold 12px sans-serif";
      this.ctx.textAlign = "left";
      this.ctx.fillText("ACTIVE DEFENSE PATROL", 28, 34);

      this.ctx.fillStyle = "#ffffff";
      this.ctx.font = "12px sans-serif";
      this.ctx.fillText(`Protected Citizens: ${this.completedMissions} / ${this.totalMissions}`, 28, 52);

      // Objective Progress Bar
      this.ctx.fillStyle = "#1e293b";
      this.ctx.fillRect(28, 62, 236, 8);
      this.ctx.fillStyle = "#10b981";
      const pct = this.totalMissions ? this.completedMissions / this.totalMissions : 0;
      this.ctx.fillRect(28, 62, 236 * pct, 8);

      // 2. Radar Minimap (Top-Right)
      const mapX = this.camera.w - 110;
      const mapY = 16;
      const mapW = 94;
      const mapH = 68;

      this.ctx.fillStyle = "rgba(15, 23, 42, 0.85)";
      this.ctx.beginPath();
      this.ctx.roundRect(mapX, mapY, mapW, mapH, 6);
      this.ctx.fill();
      this.ctx.strokeStyle = "#475569";
      this.ctx.lineWidth = 1;
      this.ctx.stroke();

      const scaleX = mapW / this.tileMap.width;
      const scaleY = mapH / this.tileMap.height;

      // Player blip
      this.ctx.fillStyle = "#38bdf8";
      this.ctx.beginPath();
      this.ctx.arc(mapX + this.player.x * scaleX, mapY + this.player.y * scaleY, 3, 0, Math.PI * 2);
      this.ctx.fill();

      // NPC blips
      this.npcs.forEach((npc) => {
        this.ctx.fillStyle = npc.status === "quest" ? "#f59e0b" : "#10b981";
        this.ctx.beginPath();
        this.ctx.arc(mapX + npc.x * scaleX, mapY + npc.y * scaleY, 2.5, 0, Math.PI * 2);
        this.ctx.fill();
      });
    }

    gameLoop() {
      if (!this.running) return;

      // Update Phase
      if (!this.deviceUI.isOpen) {
        this.player.update(this.keys, this.tileMap, this.audio);
      }
      this.updateCamera();

      // Render Phase
      this.ctx.save();
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

      // Translate context by camera offset
      this.ctx.translate(-this.camera.x, -this.camera.y);

      // 1. Draw Map & Buildings
      this.tileMap.render(this.ctx, this.camera);

      // 2. Draw NPCs
      this.npcs.forEach((npc) => {
        npc.render(this.ctx, this.player.x, this.player.y);
      });

      // 3. Draw Player
      this.player.render(this.ctx);

      this.ctx.restore();

      // 4. Draw HUD (Screen space, outside camera transform)
      this.renderHUD();

      requestAnimationFrame(this.gameLoop.bind(this));
    }
  }

  window.Game2DEngine = Game2DEngine;
})(window, document);

