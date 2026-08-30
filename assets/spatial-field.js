/* GPU-rendered signal field and exploded mechanical compute core.
   Static geometry lives in GPU buffers; interaction, picking, and material motion stay on the GPU. */
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

    function createProgramWithSharedVertex(sourceProgram, fragmentSource) {
      var attached = gl.getAttachedShaders(sourceProgram) || [];
      var vertexShader = attached.filter(function (shader) {
        return gl.getShaderParameter(shader, gl.SHADER_TYPE) === gl.VERTEX_SHADER;
      })[0];
      if (!vertexShader) throw new Error("Unable to reuse mechanical vertex shader");

      var program = gl.createProgram();
      gl.attachShader(program, vertexShader);
      gl.attachShader(program, compile(gl.FRAGMENT_SHADER, fragmentSource));
      gl.linkProgram(program);
      if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        var message = gl.getProgramInfoLog(program);
        gl.deleteProgram(program);
        throw new Error(message || "Unable to link WebGL picking program");
      }
      return program;
    }

    var lineProgram;
    var coreProgram;
    var pickProgram;
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
          "attribute float a_part;",
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
          "varying float v_part;",
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
          "  vec3 localPosition = a_position + a_explode * eased * 0.72;",
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
          "  v_part = a_part;",
          "  gl_Position = vec4(clipPosition, clipDepth, viewPosition.z);",
          "}",
        ].join("\n"),
        [
          "precision mediump float;",
          "uniform float u_time;",
          "uniform vec2 u_pointer;",
          "uniform float u_hover;",
          "uniform float u_interaction;",
          "uniform float u_hovered_part;",
          "uniform float u_part_highlight;",
          "varying vec3 v_normal;",
          "varying vec3 v_world;",
          "varying vec3 v_local;",
          "varying vec3 v_view_direction;",
          "varying float v_depth;",
          "varying float v_material;",
          "varying float v_part;",
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
          "  float partMatch = 1.0 - step(0.45, abs(v_part - u_hovered_part));",
          "  float scan = 0.5 + 0.5 * sin(v_local.y * 19.0 - u_time * 8.0 + v_part * 0.61);",
          "  float highlightWave = 0.68 + 0.2 * sin(u_time * 5.4 + v_part * 0.47) + scan * 0.12;",
          "  float selected = partMatch * u_part_highlight;",
          "  color = mix(color, color * 1.16 + vec3(0.12, 0.2, 0.82), selected * 0.34 * highlightWave);",
          "  color += selected * (vec3(0.16, 0.28, 1.0) * (0.16 + scan * 0.22) + specularColor * 0.28);",
          "  color *= 0.972 + brushed * 0.024 + grain * 0.018;",
          "  color = pow(color, vec3(0.92));",
          "  gl_FragColor = vec4(color, 0.99);",
          "}",
        ].join("\n")
      );

      pickProgram = createProgramWithSharedVertex(
        coreProgram,
        [
          "precision mediump float;",
          "varying float v_part;",
          "void main() {",
          "  gl_FragColor = vec4(v_part / 255.0, 0.0, 0.0, 1.0);",
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
      part: gl.getAttribLocation(coreProgram, "a_part"),
      aspect: gl.getUniformLocation(coreProgram, "u_aspect"),
      time: gl.getUniformLocation(coreProgram, "u_time"),
      disassembly: gl.getUniformLocation(coreProgram, "u_disassembly"),
      pointer: gl.getUniformLocation(coreProgram, "u_pointer"),
      rotation: gl.getUniformLocation(coreProgram, "u_rotation"),
      hover: gl.getUniformLocation(coreProgram, "u_hover"),
      interaction: gl.getUniformLocation(coreProgram, "u_interaction"),
      hoveredPart: gl.getUniformLocation(coreProgram, "u_hovered_part"),
      partHighlight: gl.getUniformLocation(coreProgram, "u_part_highlight"),
    };
    var pickLocations = {
      position: gl.getAttribLocation(pickProgram, "a_position"),
      normal: gl.getAttribLocation(pickProgram, "a_normal"),
      explode: gl.getAttribLocation(pickProgram, "a_explode"),
      material: gl.getAttribLocation(pickProgram, "a_material"),
      part: gl.getAttribLocation(pickProgram, "a_part"),
      aspect: gl.getUniformLocation(pickProgram, "u_aspect"),
      time: gl.getUniformLocation(pickProgram, "u_time"),
      disassembly: gl.getUniformLocation(pickProgram, "u_disassembly"),
      pointer: gl.getUniformLocation(pickProgram, "u_pointer"),
      rotation: gl.getUniformLocation(pickProgram, "u_rotation"),
      hover: gl.getUniformLocation(pickProgram, "u_hover"),
      interaction: gl.getUniformLocation(pickProgram, "u_interaction"),
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

    function pushMechanicalVertex(target, point, normal, explode, material, part) {
      target.push(
        point[0], point[1], point[2],
        normal[0], normal[1], normal[2],
        explode[0], explode[1], explode[2],
        material,
        part
      );
    }

    function pushQuad(target, a, b, c, d, normal, explode, material, part) {
      pushMechanicalVertex(target, a, normal, explode, material, part);
      pushMechanicalVertex(target, b, normal, explode, material, part);
      pushMechanicalVertex(target, c, normal, explode, material, part);
      pushMechanicalVertex(target, a, normal, explode, material, part);
      pushMechanicalVertex(target, c, normal, explode, material, part);
      pushMechanicalVertex(target, d, normal, explode, material, part);
    }

    function addBox(target, center, size, explode, material, part) {
      var x0 = center[0] - size[0] / 2;
      var x1 = center[0] + size[0] / 2;
      var y0 = center[1] - size[1] / 2;
      var y1 = center[1] + size[1] / 2;
      var z0 = center[2] - size[2] / 2;
      var z1 = center[2] + size[2] / 2;
      pushQuad(target, [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1], [0, 0, 1], explode, material, part);
      pushQuad(target, [x1, y0, z0], [x0, y0, z0], [x0, y1, z0], [x1, y1, z0], [0, 0, -1], explode, material, part);
      pushQuad(target, [x0, y0, z0], [x0, y0, z1], [x0, y1, z1], [x0, y1, z0], [-1, 0, 0], explode, material, part);
      pushQuad(target, [x1, y0, z1], [x1, y0, z0], [x1, y1, z0], [x1, y1, z1], [1, 0, 0], explode, material, part);
      pushQuad(target, [x0, y1, z1], [x1, y1, z1], [x1, y1, z0], [x0, y1, z0], [0, 1, 0], explode, material, part);
      pushQuad(target, [x0, y0, z0], [x1, y0, z0], [x1, y0, z1], [x0, y0, z1], [0, -1, 0], explode, material, part);
    }

    function addCylinder(target, center, radius, height, segments, explode, material, part) {
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
        pushMechanicalVertex(target, b0, n0, explode, material, part);
        pushMechanicalVertex(target, b1, n1, explode, material, part);
        pushMechanicalVertex(target, t1, n1, explode, material, part);
        pushMechanicalVertex(target, b0, n0, explode, material, part);
        pushMechanicalVertex(target, t1, n1, explode, material, part);
        pushMechanicalVertex(target, t0, n0, explode, material, part);
        pushMechanicalVertex(target, [center[0], y1, center[2]], [0, 1, 0], explode, material, part);
        pushMechanicalVertex(target, t0, [0, 1, 0], explode, material, part);
        pushMechanicalVertex(target, t1, [0, 1, 0], explode, material, part);
      }
    }

    var mechanicalPartCount = 0;

    function buildMechanicalGeometry() {
      var vertices = [];
      var partId = 0;

      function box(center, size, explode, material) {
        partId += 1;
        addBox(vertices, center, size, explode, material, partId);
      }

      function cylinder(center, radius, height, segments, explode, material) {
        partId += 1;
        addCylinder(vertices, center, radius, height, segments, explode, material, partId);
      }

      /* Every physical primitive receives a stable ID for exact GPU hover picking. */
      box([0, -0.54, 0], [1.5, 0.08, 1.08], [0, -0.56, 0], 1);
      box([0, -0.35, 0], [1.26, 0.07, 0.9], [0, -0.34, 0], 3);
      box([0, -0.16, 0], [1.42, 0.11, 1.05], [0, -0.12, 0], 0);

      /* Circuit traces and side connectors. */
      [-0.66, -0.52, 0.52, 0.66].forEach(function (x, index) {
        box([x, -0.075, 0], [0.055, 0.024, 0.72], [x * 0.34, 0.02, index % 2 ? 0.12 : -0.12], 2);
      });
      [-0.34, 0.34].forEach(function (z) {
        box([0, -0.07, z], [1.04, 0.025, 0.055], [0, 0.02, z * 0.34], 2);
      });
      [-1, 1].forEach(function (side) {
        box([side * 0.86, -0.1, -0.28], [0.26, 0.18, 0.25], [side * 0.56, 0.02, -0.12], 1);
        box([side * 0.86, -0.1, 0.28], [0.26, 0.18, 0.25], [side * 0.56, 0.02, 0.12], 1);
      });

      /* Central compute package and ceramic die. */
      box([0, 0.02, 0], [0.78, 0.2, 0.68], [0, 0, 0], 2);
      box([0, 0.16, 0], [0.46, 0.07, 0.4], [0, 0.16, 0], 3);

      /* Open retention frame. */
      box([-0.62, 0.27, 0], [0.1, 0.08, 0.94], [-0.32, 0.26, 0], 1);
      box([0.62, 0.27, 0], [0.1, 0.08, 0.94], [0.32, 0.26, 0], 1);
      box([0, 0.27, -0.42], [1.14, 0.08, 0.1], [0, 0.26, -0.26], 1);
      box([0, 0.27, 0.42], [1.14, 0.08, 0.1], [0, 0.26, 0.26], 1);

      /* Heat-spreader and individually selectable fins. */
      box([0, 0.43, 0], [1.08, 0.09, 0.76], [0, 0.48, 0], 1);
      for (var fin = -5; fin <= 5; fin++) {
        var fx = fin * 0.095;
        box(
          [fx, 0.68, 0],
          [0.045, 0.44, 0.72],
          [fx * 0.92, 0.72 + Math.abs(fin) * 0.018, fin % 2 === 0 ? 0.12 : -0.12],
          fin === 0 ? 2 : 1
        );
      }

      /* Four mounting screws remain individually selectable. */
      [-0.58, 0.58].forEach(function (x) {
        [-0.4, 0.4].forEach(function (z) {
          cylinder([x, -0.3, z], 0.055, 0.33, 18, [x * 0.34, -0.38, z * 0.3], 3);
        });
      });

      mechanicalPartCount = partId;
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

    var pickFramebuffer = gl.createFramebuffer();
    var pickTexture = gl.createTexture();
    var pickDepthBuffer = gl.createRenderbuffer();
    gl.bindTexture(gl.TEXTURE_2D, pickTexture);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.bindTexture(gl.TEXTURE_2D, null);

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
    var disassemblyTarget = 0;
    var disassembly = 0;
    var coreEngaged = false;
    var coreHoverCandidate = false;
    var pickPosition = [0, 0];
    var pickRequested = false;
    var lastPickAt = 0;
    var lastPickDisassembly = -1;
    var partMissStartedAt = 0;
    var partMissGraceMs = 85;
    var disassemblyTimeConstant = 0.44;
    var pickPixel = new Uint8Array(4);
    var hoveredPart = 0;
    var partHighlightTarget = 0;
    var partHighlight = 0;
    var pickPasses = 0;
    var pickingAvailable = true;
    var heroRect = null;
    var inView = true;
    var frame = null;
    var reducedFrame = null;
    var startedAt = performance.now();
    var frameTotal = 0;
    var frameCount = 0;
    var lastFrameAt = startedAt;
    var lastCompact = canvas.clientWidth < 760;

    var metrics = {
      renderer: "WebGL",
      powerPreference: "high-performance",
      shader: "brushed-metal-clearcoat-part-picking",
      lineVertices: lineData.length / 3,
      mechanicalVertices: mechanicalData.length / 11,
      mechanicalParts: mechanicalPartCount,
      averageFrameMs: 0,
      running: false,
      reducedMotion: reducedMotion.matches,
      mechanicalActive: canvas.clientWidth >= 700,
      disassembly: 0,
      disassemblyTrigger: "mesh-hover",
      hoveredPart: 0,
      partHighlight: 0,
      pickPasses: 0,
      partMissGraceMs: partMissGraceMs,
      disassemblyTimeConstantMs: disassemblyTimeConstant * 1000,
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

    function resizePickBuffer(width, height) {
      gl.bindTexture(gl.TEXTURE_2D, pickTexture);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, width, height, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
      gl.bindFramebuffer(gl.FRAMEBUFFER, pickFramebuffer);
      gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, pickTexture, 0);
      gl.bindRenderbuffer(gl.RENDERBUFFER, pickDepthBuffer);
      gl.renderbufferStorage(gl.RENDERBUFFER, gl.DEPTH_COMPONENT16, width, height);
      gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.RENDERBUFFER, pickDepthBuffer);
      pickingAvailable = gl.checkFramebufferStatus(gl.FRAMEBUFFER) === gl.FRAMEBUFFER_COMPLETE;
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
      gl.bindRenderbuffer(gl.RENDERBUFFER, null);
      gl.bindTexture(gl.TEXTURE_2D, null);
      metrics.pickingAvailable = pickingAvailable;
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
        resizePickBuffer(width, height);
      }
      metrics.mechanicalActive = rect.width >= 700;
      rebuildLinesIfNeeded();
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

    function bindMechanicalAttribute(location, size, offset) {
      if (location < 0) return;
      gl.enableVertexAttribArray(location);
      gl.vertexAttribPointer(location, size, gl.FLOAT, false, 44, offset);
    }

    function bindMechanicalAttributes(locations) {
      gl.bindBuffer(gl.ARRAY_BUFFER, mechanicalBuffer);
      bindMechanicalAttribute(locations.position, 3, 0);
      bindMechanicalAttribute(locations.normal, 3, 12);
      bindMechanicalAttribute(locations.explode, 3, 24);
      bindMechanicalAttribute(locations.material, 1, 36);
      bindMechanicalAttribute(locations.part, 1, 40);
    }

    function setMechanicalTransformUniforms(locations, time) {
      gl.uniform1f(locations.aspect, canvas.width / canvas.height);
      gl.uniform1f(locations.time, time);
      gl.uniform1f(locations.disassembly, disassembly);
      gl.uniform2f(locations.pointer, pointer[0], pointer[1]);
      gl.uniform2f(locations.rotation, rotation[0], rotation[1]);
      gl.uniform1f(locations.hover, hover);
      gl.uniform1f(locations.interaction, interaction);
    }

    function setHoveredPart(nextPart) {
      var validPart = nextPart >= 1 && nextPart <= mechanicalPartCount ? nextPart : 0;
      if (validPart === hoveredPart) return;
      hoveredPart = validPart;
      partHighlight = 0;
      partHighlightTarget = validPart > 0 ? 1 : 0;
      if (hero) hero.classList.toggle("is-core-part-hovered", validPart > 0);
      if (reducedMotion.matches) {
        partHighlight = partHighlightTarget;
        requestReducedFrame();
      }
    }

    function engageCore() {
      if (coreEngaged) return;
      coreEngaged = true;
      partMissStartedAt = 0;
      disassemblyTarget = 1;
      hoverTarget = 1;
      interactionTarget = 1;
      if (hero) hero.classList.add("is-core-hovered");
      if (reducedMotion.matches) {
        disassembly = 1;
        hover = 1;
        requestReducedFrame();
      } else {
        start();
      }
    }

    function disengageCore() {
      coreEngaged = false;
      partMissStartedAt = 0;
      disassemblyTarget = 0;
      hoverTarget = 0;
      pickRequested = false;
      setHoveredPart(0);
      if (hero) {
        hero.classList.remove("is-core-hovered");
        hero.classList.remove("is-core-interacting");
      }
      if (reducedMotion.matches) {
        disassembly = 0;
        hover = 0;
        requestReducedFrame();
      }
    }

    function drawPickPass(time, now) {
      if (!pickRequested || !pickingAvailable || !metrics.mechanicalActive) return;
      if (!reducedMotion.matches && now - lastPickAt < 34) return;

      pickRequested = false;
      lastPickAt = now;
      lastPickDisassembly = disassembly;
      var pixelX = clamp(Math.floor(pickPosition[0] * canvas.width), 0, canvas.width - 1);
      var pixelY = clamp(Math.floor((1 - pickPosition[1]) * canvas.height), 0, canvas.height - 1);

      gl.bindFramebuffer(gl.FRAMEBUFFER, pickFramebuffer);
      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.enable(gl.SCISSOR_TEST);
      gl.scissor(pixelX, pixelY, 1, 1);
      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      gl.useProgram(pickProgram);
      gl.enable(gl.DEPTH_TEST);
      gl.depthFunc(gl.LEQUAL);
      gl.disable(gl.BLEND);
      bindMechanicalAttributes(pickLocations);
      setMechanicalTransformUniforms(pickLocations, time);
      gl.drawArrays(gl.TRIANGLES, 0, mechanicalData.length / 11);
      gl.readPixels(pixelX, pixelY, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, pickPixel);
      gl.disable(gl.SCISSOR_TEST);
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
      gl.viewport(0, 0, canvas.width, canvas.height);
      pickPasses += 1;

      var pickedPart = pickPixel[0];
      if (!coreEngaged && coreHoverCandidate && pickedPart > 0) engageCore();
      if (coreEngaged && disassembly > 0.38) {
        if (pickedPart > 0) {
          partMissStartedAt = 0;
          setHoveredPart(pickedPart);
        } else {
          setHoveredPart(0);
          if (dragging) {
            partMissStartedAt = 0;
          } else if (reducedMotion.matches) {
            disengageCore();
          } else {
            if (!partMissStartedAt) partMissStartedAt = now;
            if (now - partMissStartedAt >= partMissGraceMs) disengageCore();
            else pickRequested = true;
          }
        }
      } else {
        setHoveredPart(0);
      }
    }

    function drawMechanicalCore(time) {
      if (!metrics.mechanicalActive) return;
      gl.useProgram(coreProgram);
      gl.enable(gl.DEPTH_TEST);
      gl.depthFunc(gl.LEQUAL);
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
      bindMechanicalAttributes(coreLocations);
      setMechanicalTransformUniforms(coreLocations, time);
      gl.uniform1f(coreLocations.hoveredPart, hoveredPart);
      gl.uniform1f(coreLocations.partHighlight, partHighlight);
      gl.drawArrays(gl.TRIANGLES, 0, mechanicalData.length / 11);
    }

    function render(now) {
      var frameSeconds = clamp((now - lastFrameAt) / 1000, 1 / 240, 0.05);
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
      partHighlight += (partHighlightTarget - partHighlight) * 0.17;
      rotationTarget[0] = clamp(rotationTarget[0], -0.32, 0.32);
      rotationTarget[1] = clamp(rotationTarget[1], -0.68, 0.68);
      var disassemblyStep = 1 - Math.exp(-frameSeconds / disassemblyTimeConstant);
      disassembly += (disassemblyTarget - disassembly) * disassemblyStep;
      var elapsed = (now - startedAt) / 1000;

      if (
        coreEngaged &&
        coreHoverCandidate &&
        (Math.abs(disassembly - lastPickDisassembly) > 0.018 || dragging)
      ) {
        pickRequested = true;
      }

      gl.clearColor(0.043, 0.047, 0.047, 1);
      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      drawLines(elapsed);
      drawMechanicalCore(elapsed);
      drawPickPass(elapsed, now);
      metrics.disassembly = Number(disassembly.toFixed(3));
      metrics.disassemblyTarget = disassemblyTarget;
      metrics.coreEngaged = coreEngaged;
      metrics.hoveredPart = hoveredPart;
      metrics.partHighlight = Number(partHighlight.toFixed(3));
      metrics.pickPasses = pickPasses;
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

    function requestReducedFrame() {
      if (!reducedMotion.matches || reducedFrame !== null || !inView || document.hidden) return;
      reducedFrame = requestAnimationFrame(function (now) {
        reducedFrame = null;
        render(now);
        metrics.running = false;
      });
    }

    function start() {
      if (reducedMotion.matches) {
        requestReducedFrame();
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
      if (reducedFrame !== null) cancelAnimationFrame(reducedFrame);
      frame = null;
      reducedFrame = null;
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
        var normalizedX = (event.clientX - rect.left) / rect.width;
        var normalizedY = (event.clientY - rect.top) / rect.height;
        pointerTarget[0] = (normalizedX - 0.5) * 2;
        pointerTarget[1] = -(normalizedY - 0.5) * 2;
        pickPosition[0] = normalizedX;
        pickPosition[1] = normalizedY;
        var pointerDeltaX = event.clientX - lastPointerSample[0];
        var pointerDeltaY = event.clientY - lastPointerSample[1];
        var pointerSpeed = Math.sqrt(pointerDeltaX * pointerDeltaX + pointerDeltaY * pointerDeltaY);
        interactionTarget = Math.max(interactionTarget, clamp(pointerSpeed / 36, 0, 0.76));
        coreHoverCandidate = normalizedX > 0.46 && normalizedX < 0.99 && normalizedY > 0.035 && normalizedY < 0.92;
        if (coreHoverCandidate) {
          pickRequested = true;
          if (coreEngaged) {
            disassemblyTarget = 1;
            hoverTarget = 1;
          }
        } else if (!dragging) {
          disengageCore();
        }
        lastPointerSample[0] = event.clientX;
        lastPointerSample[1] = event.clientY;
        if (reducedMotion.matches) {
          pointer[0] = pointerTarget[0];
          pointer[1] = pointerTarget[1];
          requestReducedFrame();
        }
      }, { passive: true });
      hero.addEventListener("pointerleave", function () {
        if (dragging) return;
        coreHoverCandidate = false;
        pointerTarget[0] = 0;
        pointerTarget[1] = 0;
        disengageCore();
      }, { passive: true });
    }

    function beginCoreDrag(event) {
      if (!finePointer || reducedMotion.matches || !metrics.mechanicalActive || !coreEngaged || event.button !== 0) return;
      event.preventDefault();
      dragging = true;
      dragPointerId = event.pointerId;
      dragLast[0] = event.clientX;
      dragLast[1] = event.clientY;
      angularVelocity[0] = 0;
      angularVelocity[1] = 0;
      interactionTarget = 1;
      hoverTarget = 1;
      disassemblyTarget = 1;
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
      if (!coreHoverCandidate) disengageCore();
    }

    if (finePointer) {
      canvas.addEventListener("pointerdown", beginCoreDrag);
      canvas.addEventListener("pointermove", moveCoreDrag, { passive: true });
      canvas.addEventListener("pointerup", endCoreDrag);
      canvas.addEventListener("pointercancel", endCoreDrag);
      canvas.addEventListener("dblclick", function (event) {
        if (!coreEngaged || reducedMotion.matches) return;
        rotationTarget[0] = 0;
        rotationTarget[1] = 0;
        angularVelocity[0] = 0;
        angularVelocity[1] = 0;
        interactionTarget = 1;
      });
    }

    if ("IntersectionObserver" in window && hero) {
      new IntersectionObserver(function (entries) {
        inView = entries[0].isIntersecting;
        if (inView) start();
        else {
          disengageCore();
          stop();
        }
      }, { rootMargin: "160px 0px" }).observe(hero);
    }

    document.addEventListener("visibilitychange", function () {
      if (document.hidden) stop(); else start();
    });

    if (reducedMotion.addEventListener) {
      reducedMotion.addEventListener("change", function () {
        metrics.reducedMotion = reducedMotion.matches;
        stop();
        if (reducedMotion.matches) {
          disassembly = disassemblyTarget;
          hover = hoverTarget;
        }
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
