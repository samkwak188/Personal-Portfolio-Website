/* GPU-rendered signal field and exploded mechanical compute core.
   Static geometry lives in GPU buffers; pointer and scroll motion are shader uniforms. */
(function () {
  "use strict";

  function clamp(value, low, high) {
    return Math.max(low, Math.min(high, value));
  }

  function init(canvas) {
    if (canvas.dataset.spatialFieldReady === "true") return;
    canvas.dataset.spatialFieldReady = "true";

    var hero = canvas.closest(".hero");
    var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    var finePointer = window.matchMedia("(pointer: fine)").matches;
    var gl = canvas.getContext("webgl", {
      alpha: true,
      antialias: true,
      depth: true,
      stencil: false,
      desynchronized: true,
      powerPreference: "high-performance",
      preserveDrawingBuffer: false,
    }) || canvas.getContext("experimental-webgl");

    if (!gl) {
      if (hero) hero.classList.add("no-webgl");
      return;
    }

    function compile(type, source) {
      var shader = gl.createShader(type);
      gl.shaderSource(shader, source);
      gl.compileShader(shader);
      if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        var message = gl.getShaderInfoLog(shader);
        gl.deleteShader(shader);
        throw new Error(message || "Unable to compile WebGL shader");
      }
      return shader;
    }

    function createProgram(vertexSource, fragmentSource) {
      var program = gl.createProgram();
      gl.attachShader(program, compile(gl.VERTEX_SHADER, vertexSource));
      gl.attachShader(program, compile(gl.FRAGMENT_SHADER, fragmentSource));
      gl.linkProgram(program);
      if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        var message = gl.getProgramInfoLog(program);
        gl.deleteProgram(program);
        throw new Error(message || "Unable to link WebGL program");
      }
      return program;
    }

    var lineProgram;
    var coreProgram;
    try {
      lineProgram = createProgram(
        [
          "attribute vec2 a_position;",
          "attribute float a_phase;",
          "uniform float u_time;",
          "uniform vec2 u_pointer;",
          "varying float v_alpha;",
          "void main() {",
          "  vec2 p = a_position;",
          "  float core = 1.0 - smoothstep(0.16, 1.28, distance(p, vec2(0.48, -0.02)));",
          "  p.y += sin(p.x * 5.0 + a_phase * 6.283 + u_time * 0.3) * 0.004 * core;",
          "  p += u_pointer * 0.014 * core;",
          "  float edge = (1.0 - smoothstep(0.78, 1.18, abs(p.x))) * (1.0 - smoothstep(0.76, 1.08, abs(p.y)));",
          "  float copyFade = smoothstep(-0.58, 0.14, p.x);",
          "  v_alpha = (0.035 + core * 0.2) * edge * mix(0.3, 1.0, copyFade);",
          "  gl_Position = vec4(p, 0.0, 1.0);",
          "}",
        ].join("\n"),
        [
          "precision mediump float;",
          "varying float v_alpha;",
          "void main() {",
          "  gl_FragColor = vec4(0.82, 0.81, 0.76, v_alpha);",
          "}",
        ].join("\n")
      );

      coreProgram = createProgram(
        [
          "precision mediump float;",
          "attribute vec3 a_position;",
          "attribute vec3 a_normal;",
          "attribute vec3 a_explode;",
          "attribute float a_material;",
          "uniform float u_aspect;",
          "uniform float u_time;",
          "uniform float u_disassembly;",
          "uniform vec2 u_pointer;",
          "uniform vec2 u_rotation;",
          "uniform float u_hover;",
          "uniform float u_interaction;",
          "varying vec3 v_normal;",
          "varying vec3 v_world;",
          "varying vec3 v_local;",
          "varying vec3 v_view_direction;",
          "varying float v_depth;",
          "varying float v_material;",
          "vec3 rotateX(vec3 point, float angle) {",
          "  float sine = sin(angle);",
          "  float cosine = cos(angle);",
          "  return vec3(point.x, point.y * cosine - point.z * sine, point.y * sine + point.z * cosine);",
          "}",
          "vec3 rotateY(vec3 point, float angle) {",
          "  float sine = sin(angle);",
          "  float cosine = cos(angle);",
          "  return vec3(point.x * cosine + point.z * sine, point.y, -point.x * sine + point.z * cosine);",
          "}",
          "void main() {",
          "  float eased = u_disassembly * u_disassembly * (3.0 - 2.0 * u_disassembly);",
          "  vec3 localPosition = a_position + a_explode * eased;",
          "  vec2 orbit = u_rotation + vec2(-u_pointer.y * 0.075, u_pointer.x * 0.12);",
          "  vec3 assembled = rotateY(rotateX(localPosition, orbit.x), orbit.y);",
          "  vec3 objectNormal = rotateY(rotateX(a_normal, orbit.x), orbit.y);",
          "  assembled.y += u_hover * 0.025;",
          "  assembled *= 1.0 + u_interaction * 0.006;",
          "  vec3 cameraPosition = vec3(",
          "    2.45 + u_pointer.x * 0.34 + sin(u_time * 0.12) * 0.045,",
          "    1.72 - u_pointer.y * 0.23,",
          "    4.65 - u_hover * 0.055",
          "  );",
          "  vec3 cameraTarget = vec3(0.0, 0.04, 0.0);",
          "  vec3 forward = normalize(cameraTarget - cameraPosition);",
          "  vec3 right = normalize(cross(forward, vec3(0.0, 1.0, 0.0)));",
          "  vec3 cameraUp = normalize(cross(right, forward));",
          "  vec3 relative = assembled - cameraPosition;",
          "  vec3 viewPosition = vec3(",
          "    dot(relative, right),",
          "    dot(relative, cameraUp),",
          "    dot(relative, forward)",
          "  );",
          "  float focalLength = 2.55;",
          "  vec2 clipPosition = vec2(",
          "    viewPosition.x * focalLength / max(u_aspect, 1.0),",
          "    viewPosition.y * focalLength",
          "  );",
          "  clipPosition += vec2(0.48, -0.015) * viewPosition.z;",
          "  float nearPlane = 2.6;",
          "  float farPlane = 8.2;",
          "  float clipDepth = ((farPlane + nearPlane) / (farPlane - nearPlane)) * viewPosition.z",
          "    - (2.0 * farPlane * nearPlane) / (farPlane - nearPlane);",
          "  v_normal = normalize(objectNormal);",
          "  v_world = assembled;",
          "  v_local = localPosition;",
          "  v_view_direction = normalize(cameraPosition - assembled);",
          "  v_depth = 5.4 - viewPosition.z;",
          "  v_material = a_material;",
          "  gl_Position = vec4(clipPosition, clipDepth, viewPosition.z);",
          "}",
        ].join("\n"),
        [
          "precision mediump float;",
          "uniform float u_time;",
          "uniform vec2 u_pointer;",
          "uniform float u_hover;",
          "uniform float u_interaction;",
          "varying vec3 v_normal;",
          "varying vec3 v_world;",
          "varying vec3 v_local;",
          "varying vec3 v_view_direction;",
          "varying float v_depth;",
          "varying float v_material;",
          "void main() {",
          "  vec3 n = normalize(v_normal);",
          "  vec3 viewDirection = normalize(v_view_direction);",
          "  float nDotV = max(dot(n, viewDirection), 0.0);",
          "  float fresnel = pow(1.0 - nDotV, 5.0);",
          "  vec3 keyLight = normalize(vec3(-0.46 + u_pointer.x * 0.24, 0.9 + u_pointer.y * 0.1, 0.58));",
          "  vec3 movingLight = normalize(vec3(sin(u_time * 0.34) * 0.72 + u_pointer.x * 0.42, 0.62 + u_pointer.y * 0.2, cos(u_time * 0.27) * 0.72));",
          "  vec3 fillLight = normalize(vec3(0.72, 0.24, -0.58));",
          "  float keyDiffuse = max(dot(n, keyLight), 0.0);",
          "  float fillDiffuse = max(dot(n, fillLight), 0.0);",
          "  vec3 reflection = reflect(-viewDirection, n);",
          "  float horizon = pow(max(1.0 - abs(reflection.y), 0.0), 3.0);",
          "  vec3 environment = mix(vec3(0.012, 0.017, 0.025), vec3(0.78, 0.82, 0.86), smoothstep(-0.34, 0.94, reflection.y));",
          "  environment += horizon * vec3(0.055, 0.11, 0.48);",
          "  float brushed = 0.5 + 0.5 * sin((v_local.x + v_local.z * 0.31) * 145.0);",
          "  float grain = fract(sin(dot(v_local.xz * 71.0 + v_local.y, vec2(12.9898, 78.233))) * 43758.5453);",
          "  vec3 graphite = vec3(0.035, 0.043, 0.052);",
          "  vec3 steel = vec3(0.39, 0.45, 0.50);",
          "  vec3 cobalt = vec3(0.025, 0.13, 0.95);",
          "  vec3 ceramic = vec3(0.76, 0.74, 0.67);",
          "  vec3 base = graphite;",
          "  float roughness = 0.34;",
          "  float metalness = 0.56;",
          "  if (v_material > 2.5) base = ceramic;",
          "  if (v_material > 2.5) { roughness = 0.23; metalness = 0.08; }",
          "  else if (v_material > 1.5) { base = cobalt; roughness = 0.18; metalness = 0.82; }",
          "  else if (v_material > 0.5) { base = steel; roughness = 0.14; metalness = 0.96; }",
          "  float specularPower = mix(20.0, 92.0, 1.0 - roughness);",
          "  float keySpecular = pow(max(dot(n, normalize(keyLight + viewDirection)), 0.0), specularPower);",
          "  float movingSpecular = pow(max(dot(n, normalize(movingLight + viewDirection)), 0.0), specularPower * 1.18);",
          "  float fillSpecular = pow(max(dot(n, normalize(fillLight + viewDirection)), 0.0), 34.0);",
          "  float clearCoat = pow(max(dot(n, normalize(movingLight + viewDirection)), 0.0), 112.0);",
          "  float edgeGlow = pow(1.0 - nDotV, 2.4);",
          "  float diffuseLevel = 0.22 + keyDiffuse * 0.46 + fillDiffuse * 0.13 + v_depth * 0.025;",
          "  vec3 dielectric = base * diffuseLevel + environment * base * 0.14;",
          "  vec3 metallic = base * (0.16 + diffuseLevel * 0.5) + environment * (0.45 + fresnel * 0.5);",
          "  vec3 color = mix(dielectric, metallic, metalness);",
          "  vec3 specularColor = mix(vec3(0.96), base * 0.55 + vec3(0.38), metalness);",
          "  float shineBoost = 1.0 + u_hover * 0.2 + u_interaction * 0.48;",
          "  color += specularColor * (keySpecular * 1.34 + movingSpecular * 0.92 + fillSpecular * 0.24 + clearCoat * 1.35) * shineBoost;",
          "  color += environment * fresnel * (0.25 + metalness * 0.52);",
          "  color += vec3(0.035, 0.085, 0.44) * edgeGlow * (0.18 + u_hover * 0.2);",
          "  color *= 0.972 + brushed * 0.024 + grain * 0.018;",
          "  color = pow(color, vec3(0.92));",
          "  gl_FragColor = vec4(color, 0.99);",
          "}",
        ].join("\n")
      );
    } catch (error) {
      if (hero) hero.classList.add("no-webgl");
      window.__portfolioWebGLError = String(error);
      return;
    }

    var lineLocations = {
      position: gl.getAttribLocation(lineProgram, "a_position"),
      phase: gl.getAttribLocation(lineProgram, "a_phase"),
      time: gl.getUniformLocation(lineProgram, "u_time"),
      pointer: gl.getUniformLocation(lineProgram, "u_pointer"),
    };
    var coreLocations = {
      position: gl.getAttribLocation(coreProgram, "a_position"),
      normal: gl.getAttribLocation(coreProgram, "a_normal"),
      explode: gl.getAttribLocation(coreProgram, "a_explode"),
      material: gl.getAttribLocation(coreProgram, "a_material"),
      aspect: gl.getUniformLocation(coreProgram, "u_aspect"),
      time: gl.getUniformLocation(coreProgram, "u_time"),
      disassembly: gl.getUniformLocation(coreProgram, "u_disassembly"),
      pointer: gl.getUniformLocation(coreProgram, "u_pointer"),
      rotation: gl.getUniformLocation(coreProgram, "u_rotation"),
      hover: gl.getUniformLocation(coreProgram, "u_hover"),
      interaction: gl.getUniformLocation(coreProgram, "u_interaction"),
    };

    function linePoint(x, lane) {
      var cx = 0.47;
      var cy = -0.03;
      var dx = x - cx;
      var dy = lane - cy;
      var absY = Math.abs(dy);
      var influence = Math.exp(-dx * dx * 2.05) * Math.exp(-absY * 0.52);
      var direction = dy < 0 ? -1 : 1;
      var gather = -direction * 0.16 * influence * (1 - Math.exp(-absY * 4.2));
      var curl = Math.sin(dx * 2.75 - direction * 0.85) * influence * 0.12 / (0.48 + absY);
      return [x + influence * Math.sin(lane * 4.1) * 0.025, lane + gather + curl];
    }

    function buildLineGeometry(compact) {
      var vertices = [];
      var lanes = compact ? 54 : 96;
      var steps = compact ? 68 : 96;
      var xMin = -1.24;
      var xMax = 1.24;
      var i;
      var j;

      for (i = 0; i < lanes; i++) {
        var lane = -1.04 + (2.08 * i) / (lanes - 1);
        var phase = i / lanes;
        for (j = 0; j < steps - 1; j++) {
          var x0 = xMin + ((xMax - xMin) * j) / (steps - 1);
          var x1 = xMin + ((xMax - xMin) * (j + 1)) / (steps - 1);
          var p0 = linePoint(x0, lane);
          var p1 = linePoint(x1, lane);
          vertices.push(p0[0], p0[1], phase, p1[0], p1[1], phase);
        }
      }

      var rings = compact ? 8 : 18;
      var ringSteps = compact ? 46 : 68;
      for (i = 0; i < rings; i++) {
        var rx = 0.11 + i * 0.02;
        var ry = 0.07 + i * 0.013;
        var ringPhase = 0.2 + i / rings;
        for (j = 0; j < ringSteps; j++) {
          var a0 = (Math.PI * 2 * j) / ringSteps;
          var a1 = (Math.PI * 2 * (j + 1)) / ringSteps;
          vertices.push(
            0.48 + Math.cos(a0) * rx,
            -0.02 + Math.sin(a0) * ry,
            ringPhase,
            0.48 + Math.cos(a1) * rx,
            -0.02 + Math.sin(a1) * ry,
            ringPhase
          );
        }
      }
      return new Float32Array(vertices);
    }

    function pushMechanicalVertex(target, point, normal, explode, material) {
      target.push(
        point[0], point[1], point[2],
        normal[0], normal[1], normal[2],
        explode[0], explode[1], explode[2],
        material
      );
    }

    function pushQuad(target, a, b, c, d, normal, explode, material) {
      pushMechanicalVertex(target, a, normal, explode, material);
      pushMechanicalVertex(target, b, normal, explode, material);
      pushMechanicalVertex(target, c, normal, explode, material);
      pushMechanicalVertex(target, a, normal, explode, material);
      pushMechanicalVertex(target, c, normal, explode, material);
      pushMechanicalVertex(target, d, normal, explode, material);
    }

    function addBox(target, center, size, explode, material) {
      var x0 = center[0] - size[0] / 2;
      var x1 = center[0] + size[0] / 2;
      var y0 = center[1] - size[1] / 2;
      var y1 = center[1] + size[1] / 2;
      var z0 = center[2] - size[2] / 2;
      var z1 = center[2] + size[2] / 2;
      pushQuad(target, [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1], [0, 0, 1], explode, material);
      pushQuad(target, [x1, y0, z0], [x0, y0, z0], [x0, y1, z0], [x1, y1, z0], [0, 0, -1], explode, material);
      pushQuad(target, [x0, y0, z0], [x0, y0, z1], [x0, y1, z1], [x0, y1, z0], [-1, 0, 0], explode, material);
      pushQuad(target, [x1, y0, z1], [x1, y0, z0], [x1, y1, z0], [x1, y1, z1], [1, 0, 0], explode, material);
      pushQuad(target, [x0, y1, z1], [x1, y1, z1], [x1, y1, z0], [x0, y1, z0], [0, 1, 0], explode, material);
      pushQuad(target, [x0, y0, z0], [x1, y0, z0], [x1, y0, z1], [x0, y0, z1], [0, -1, 0], explode, material);
    }

    function addCylinder(target, center, radius, height, segments, explode, material) {
      var y0 = center[1] - height / 2;
      var y1 = center[1] + height / 2;
      for (var i = 0; i < segments; i++) {
        var a0 = (Math.PI * 2 * i) / segments;
        var a1 = (Math.PI * 2 * (i + 1)) / segments;
        var n0 = [Math.cos(a0), 0, Math.sin(a0)];
        var n1 = [Math.cos(a1), 0, Math.sin(a1)];
        var b0 = [center[0] + n0[0] * radius, y0, center[2] + n0[2] * radius];
        var b1 = [center[0] + n1[0] * radius, y0, center[2] + n1[2] * radius];
        var t0 = [b0[0], y1, b0[2]];
        var t1 = [b1[0], y1, b1[2]];
        pushMechanicalVertex(target, b0, n0, explode, material);
        pushMechanicalVertex(target, b1, n1, explode, material);
        pushMechanicalVertex(target, t1, n1, explode, material);
        pushMechanicalVertex(target, b0, n0, explode, material);
        pushMechanicalVertex(target, t1, n1, explode, material);
        pushMechanicalVertex(target, t0, n0, explode, material);
        pushMechanicalVertex(target, [center[0], y1, center[2]], [0, 1, 0], explode, material);
        pushMechanicalVertex(target, t0, [0, 1, 0], explode, material);
        pushMechanicalVertex(target, t1, [0, 1, 0], explode, material);
      }
    }

    function buildMechanicalGeometry() {
      var vertices = [];

      /* Separated structural layers communicate a processor, enclosure, and heat sink. */
      addBox(vertices, [0, -0.54, 0], [1.5, 0.08, 1.08], [0, -0.56, 0], 1);
      addBox(vertices, [0, -0.35, 0], [1.26, 0.07, 0.9], [0, -0.34, 0], 3);
      addBox(vertices, [0, -0.16, 0], [1.42, 0.11, 1.05], [0, -0.12, 0], 0);

      /* Circuit traces and side connectors. */
      [-0.66, -0.52, 0.52, 0.66].forEach(function (x, index) {
        addBox(vertices, [x, -0.075, 0], [0.055, 0.024, 0.72], [x * 0.34, 0.02, index % 2 ? 0.12 : -0.12], 2);
      });
      [-0.34, 0.34].forEach(function (z) {
        addBox(vertices, [0, -0.07, z], [1.04, 0.025, 0.055], [0, 0.02, z * 0.34], 2);
      });
      [-1, 1].forEach(function (side) {
        addBox(vertices, [side * 0.86, -0.1, -0.28], [0.26, 0.18, 0.25], [side * 0.56, 0.02, -0.12], 1);
        addBox(vertices, [side * 0.86, -0.1, 0.28], [0.26, 0.18, 0.25], [side * 0.56, 0.02, 0.12], 1);
      });

      /* Central compute package and ceramic die. */
      addBox(vertices, [0, 0.02, 0], [0.78, 0.2, 0.68], [0, 0, 0], 2);
      addBox(vertices, [0, 0.16, 0], [0.46, 0.07, 0.4], [0, 0.16, 0], 3);

      /* Open retention frame. */
      addBox(vertices, [-0.62, 0.27, 0], [0.1, 0.08, 0.94], [-0.32, 0.26, 0], 1);
      addBox(vertices, [0.62, 0.27, 0], [0.1, 0.08, 0.94], [0.32, 0.26, 0], 1);
      addBox(vertices, [0, 0.27, -0.42], [1.14, 0.08, 0.1], [0, 0.26, -0.26], 1);
      addBox(vertices, [0, 0.27, 0.42], [1.14, 0.08, 0.1], [0, 0.26, 0.26], 1);

      /* Heat-spreader and individually separated fins. */
      addBox(vertices, [0, 0.43, 0], [1.08, 0.09, 0.76], [0, 0.48, 0], 1);
      for (var fin = -5; fin <= 5; fin++) {
        var fx = fin * 0.095;
        addBox(
          vertices,
          [fx, 0.68, 0],
          [0.045, 0.44, 0.72],
          [fx * 0.92, 0.72 + Math.abs(fin) * 0.018, fin % 2 === 0 ? 0.12 : -0.12],
          fin === 0 ? 2 : 1
        );
      }

      /* Four mounting screws make the exploded assembly read mechanically. */
      [-0.58, 0.58].forEach(function (x) {
        [-0.4, 0.4].forEach(function (z) {
          addCylinder(vertices, [x, -0.3, z], 0.055, 0.33, 18, [x * 0.34, -0.38, z * 0.3], 3);
        });
      });

      return new Float32Array(vertices);
    }

    var lineData = buildLineGeometry(canvas.clientWidth < 760);
    var mechanicalData = buildMechanicalGeometry();
    var lineBuffer = gl.createBuffer();
    var mechanicalBuffer = gl.createBuffer();

    gl.bindBuffer(gl.ARRAY_BUFFER, lineBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, lineData, gl.STATIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, mechanicalBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, mechanicalData, gl.STATIC_DRAW);

    var pointerTarget = [0, 0];
    var pointer = [0, 0];
    var rotationTarget = [0, 0];
    var rotation = [0, 0];
    var angularVelocity = [0, 0];
    var hoverTarget = 0;
    var hover = 0;
    var interactionTarget = 0;
    var interaction = 0;
    var dragging = false;
    var dragPointerId = null;
    var dragLast = [0, 0];
    var lastPointerSample = [0, 0];
    var scrollTarget = 0;
    var disassembly = 0;
    var heroRect = null;
    var inView = true;
    var frame = null;
    var startedAt = performance.now();
    var frameTotal = 0;
    var frameCount = 0;
    var lastFrameAt = startedAt;
    var lastCompact = canvas.clientWidth < 760;

    var metrics = {
      renderer: "WebGL",
      powerPreference: "high-performance",
      shader: "brushed-metal-clearcoat",
      lineVertices: lineData.length / 3,
      mechanicalVertices: mechanicalData.length / 10,
      averageFrameMs: 0,
      running: false,
      reducedMotion: reducedMotion.matches,
      mechanicalActive: canvas.clientWidth >= 700,
      disassembly: 0,
      rotation: [0, 0],
      interaction: 0,
      dragging: false,
      drawCalls: 2,
    };
    window.__portfolioPerformance = metrics;

    function rebuildLinesIfNeeded() {
      var compact = canvas.clientWidth < 760;
      if (compact === lastCompact) return;
      lastCompact = compact;
      lineData = buildLineGeometry(compact);
      gl.bindBuffer(gl.ARRAY_BUFFER, lineBuffer);
      gl.bufferData(gl.ARRAY_BUFFER, lineData, gl.STATIC_DRAW);
      metrics.lineVertices = lineData.length / 3;
    }

    function updateScrollTarget() {
      if (!hero) return;
      var rect = hero.getBoundingClientRect();
      var progress = clamp((-rect.top + 24) / Math.max(rect.height * 0.74, 1), 0, 1);
      scrollTarget = reducedMotion.matches ? 0.18 : progress;
      if (reducedMotion.matches) {
        disassembly = scrollTarget;
        render(performance.now());
      } else {
        start();
      }
    }

    function resize() {
      var rect = canvas.getBoundingClientRect();
      heroRect = hero ? hero.getBoundingClientRect() : rect;
      var dprCap = rect.width < 760 ? 1.15 : 1.5;
      var dpr = Math.min(window.devicePixelRatio || 1, dprCap);
      var width = Math.max(1, Math.round(rect.width * dpr));
      var height = Math.max(1, Math.round(rect.height * dpr));
      if (canvas.width !== width || canvas.height !== height) {
        canvas.width = width;
        canvas.height = height;
        gl.viewport(0, 0, width, height);
      }
      metrics.mechanicalActive = rect.width >= 700;
      rebuildLinesIfNeeded();
      updateScrollTarget();
    }

    function drawLines(time) {
      gl.useProgram(lineProgram);
      gl.disable(gl.DEPTH_TEST);
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
      gl.bindBuffer(gl.ARRAY_BUFFER, lineBuffer);
      gl.enableVertexAttribArray(lineLocations.position);
      gl.enableVertexAttribArray(lineLocations.phase);
      gl.vertexAttribPointer(lineLocations.position, 2, gl.FLOAT, false, 12, 0);
      gl.vertexAttribPointer(lineLocations.phase, 1, gl.FLOAT, false, 12, 8);
      gl.uniform1f(lineLocations.time, time);
      gl.uniform2f(lineLocations.pointer, pointer[0], pointer[1]);
      gl.drawArrays(gl.LINES, 0, lineData.length / 3);
    }

    function drawMechanicalCore(time) {
      if (!metrics.mechanicalActive) return;
      gl.useProgram(coreProgram);
      gl.enable(gl.DEPTH_TEST);
      gl.depthFunc(gl.LEQUAL);
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
      gl.bindBuffer(gl.ARRAY_BUFFER, mechanicalBuffer);

      gl.enableVertexAttribArray(coreLocations.position);
      gl.enableVertexAttribArray(coreLocations.normal);
      gl.enableVertexAttribArray(coreLocations.explode);
      gl.enableVertexAttribArray(coreLocations.material);
      gl.vertexAttribPointer(coreLocations.position, 3, gl.FLOAT, false, 40, 0);
      gl.vertexAttribPointer(coreLocations.normal, 3, gl.FLOAT, false, 40, 12);
      gl.vertexAttribPointer(coreLocations.explode, 3, gl.FLOAT, false, 40, 24);
      gl.vertexAttribPointer(coreLocations.material, 1, gl.FLOAT, false, 40, 36);
      gl.uniform1f(coreLocations.aspect, canvas.width / canvas.height);
      gl.uniform1f(coreLocations.time, time);
      gl.uniform1f(coreLocations.disassembly, disassembly);
      gl.uniform2f(coreLocations.pointer, pointer[0], pointer[1]);
      gl.uniform2f(coreLocations.rotation, rotation[0], rotation[1]);
      gl.uniform1f(coreLocations.hover, hover);
      gl.uniform1f(coreLocations.interaction, interaction);
      gl.drawArrays(gl.TRIANGLES, 0, mechanicalData.length / 10);
    }

    function render(now) {
      pointer[0] += (pointerTarget[0] - pointer[0]) * 0.07;
      pointer[1] += (pointerTarget[1] - pointer[1]) * 0.07;
      if (!dragging) {
        rotationTarget[0] += angularVelocity[0];
        rotationTarget[1] += angularVelocity[1];
        angularVelocity[0] *= 0.91;
        angularVelocity[1] *= 0.91;
      }
      rotation[0] += (rotationTarget[0] - rotation[0]) * 0.11;
      rotation[1] += (rotationTarget[1] - rotation[1]) * 0.11;
      hover += (hoverTarget - hover) * 0.085;
      interaction += (interactionTarget - interaction) * 0.16;
      interactionTarget *= 0.925;
      rotationTarget[0] = clamp(rotationTarget[0], -0.32, 0.32);
      rotationTarget[1] = clamp(rotationTarget[1], -0.68, 0.68);
      disassembly += (scrollTarget - disassembly) * 0.075;
      var elapsed = (now - startedAt) / 1000;

      gl.clearColor(0.043, 0.047, 0.047, 1);
      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      drawLines(elapsed);
      drawMechanicalCore(elapsed);
      metrics.disassembly = Number(disassembly.toFixed(3));
      metrics.rotation = [Number(rotation[0].toFixed(3)), Number(rotation[1].toFixed(3))];
      metrics.hover = Number(hover.toFixed(3));
      metrics.interaction = Number(interaction.toFixed(3));
      metrics.dragging = dragging;

      var frameDuration = now - lastFrameAt;
      lastFrameAt = now;
      if (frameDuration < 100) {
        frameTotal += frameDuration;
        frameCount += 1;
        if (frameCount >= 60) {
          metrics.averageFrameMs = Number((frameTotal / frameCount).toFixed(2));
          frameTotal = 0;
          frameCount = 0;
        }
      }
    }

    function loop(now) {
      frame = null;
      if (!inView || document.hidden || reducedMotion.matches) {
        metrics.running = false;
        return;
      }
      render(now);
      metrics.running = true;
      frame = requestAnimationFrame(loop);
    }

    function start() {
      if (reducedMotion.matches) {
        render(performance.now());
        metrics.running = false;
        return;
      }
      if (frame === null && inView && !document.hidden) {
        lastFrameAt = performance.now();
        frame = requestAnimationFrame(loop);
      }
    }

    function stop() {
      if (frame !== null) cancelAnimationFrame(frame);
      frame = null;
      metrics.running = false;
    }

    if (finePointer && hero) {
      hero.addEventListener("pointerenter", function (event) {
        heroRect = hero.getBoundingClientRect();
        lastPointerSample[0] = event.clientX;
        lastPointerSample[1] = event.clientY;
      }, { passive: true });
      hero.addEventListener("pointermove", function (event) {
        var rect = heroRect || hero.getBoundingClientRect();
        pointerTarget[0] = ((event.clientX - rect.left) / rect.width - 0.5) * 2;
        pointerTarget[1] = -((event.clientY - rect.top) / rect.height - 0.5) * 2;
        var pointerDeltaX = event.clientX - lastPointerSample[0];
        var pointerDeltaY = event.clientY - lastPointerSample[1];
        var pointerSpeed = Math.sqrt(pointerDeltaX * pointerDeltaX + pointerDeltaY * pointerDeltaY);
        interactionTarget = Math.max(interactionTarget, clamp(pointerSpeed / 36, 0, 0.76));
        hoverTarget = pointerTarget[0] > 0.12 && Math.abs(pointerTarget[1]) < 0.82 ? 1 : 0;
        lastPointerSample[0] = event.clientX;
        lastPointerSample[1] = event.clientY;
      }, { passive: true });
      hero.addEventListener("pointerleave", function () {
        if (dragging) return;
        pointerTarget[0] = 0;
        pointerTarget[1] = 0;
        hoverTarget = 0;
      }, { passive: true });
    }

    function beginCoreDrag(event) {
      if (!finePointer || reducedMotion.matches || !metrics.mechanicalActive || event.button !== 0) return;
      var rect = canvas.getBoundingClientRect();
      if (event.clientX < rect.left + rect.width * 0.5) return;
      event.preventDefault();
      dragging = true;
      dragPointerId = event.pointerId;
      dragLast[0] = event.clientX;
      dragLast[1] = event.clientY;
      angularVelocity[0] = 0;
      angularVelocity[1] = 0;
      interactionTarget = 1;
      hoverTarget = 1;
      canvas.setPointerCapture(event.pointerId);
      if (hero) hero.classList.add("is-core-interacting");
    }

    function moveCoreDrag(event) {
      if (!dragging || event.pointerId !== dragPointerId) return;
      var dragX = event.clientX - dragLast[0];
      var dragY = event.clientY - dragLast[1];
      rotationTarget[0] = clamp(rotationTarget[0] + dragY * 0.003, -0.32, 0.32);
      rotationTarget[1] = clamp(rotationTarget[1] + dragX * 0.0035, -0.68, 0.68);
      angularVelocity[0] = dragY * 0.00004;
      angularVelocity[1] = dragX * 0.000055;
      dragLast[0] = event.clientX;
      dragLast[1] = event.clientY;
      interactionTarget = 1;
    }

    function endCoreDrag(event) {
      if (!dragging || (event && event.pointerId !== dragPointerId)) return;
      if (event && canvas.hasPointerCapture(event.pointerId)) canvas.releasePointerCapture(event.pointerId);
      dragging = false;
      dragPointerId = null;
      interactionTarget = Math.max(interactionTarget, 0.58);
      if (hero) hero.classList.remove("is-core-interacting");
    }

    if (finePointer) {
      canvas.addEventListener("pointerdown", beginCoreDrag);
      canvas.addEventListener("pointermove", moveCoreDrag, { passive: true });
      canvas.addEventListener("pointerup", endCoreDrag);
      canvas.addEventListener("pointercancel", endCoreDrag);
      canvas.addEventListener("dblclick", function (event) {
        var rect = canvas.getBoundingClientRect();
        if (event.clientX < rect.left + rect.width * 0.5 || reducedMotion.matches) return;
        rotationTarget[0] = 0;
        rotationTarget[1] = 0;
        angularVelocity[0] = 0;
        angularVelocity[1] = 0;
        interactionTarget = 1;
      });
    }

    window.addEventListener("scroll", updateScrollTarget, { passive: true });

    if ("IntersectionObserver" in window && hero) {
      new IntersectionObserver(function (entries) {
        inView = entries[0].isIntersecting;
        if (inView) start(); else stop();
      }, { rootMargin: "160px 0px" }).observe(hero);
    }

    document.addEventListener("visibilitychange", function () {
      if (document.hidden) stop(); else start();
    });

    if (reducedMotion.addEventListener) {
      reducedMotion.addEventListener("change", function () {
        metrics.reducedMotion = reducedMotion.matches;
        stop();
        updateScrollTarget();
        start();
      });
    }

    if ("ResizeObserver" in window) {
      new ResizeObserver(function () {
        resize();
        if (reducedMotion.matches) render(performance.now());
      }).observe(canvas);
    } else {
      window.addEventListener("resize", resize, { passive: true });
    }

    canvas.addEventListener("webglcontextlost", function (event) {
      event.preventDefault();
      stop();
      metrics.running = false;
    });

    resize();
    updateScrollTarget();
    render(performance.now());
    start();
  }

  function boot() {
    var canvas = document.getElementById("spatial-field");
    if (!canvas) return false;
    init(canvas);
    return true;
  }

  function waitForCanvas() {
    if (boot()) return;
    var observer = new MutationObserver(function () {
      if (boot()) observer.disconnect();
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", waitForCanvas);
  else waitForCanvas();
})();
