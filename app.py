import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Walentynka", layout="centered")

if "yes_clicked" not in st.session_state:
    st.session_state.yes_clicked = False

if "fire_fx" not in st.session_state:
    st.session_state.fire_fx = False

# Obsługa kliknięcia TAK przez query param (?ans=yes)
params = st.query_params
if params.get("ans") == "yes":
    st.session_state.yes_clicked = True
    st.session_state.fire_fx = True
    st.query_params.clear()
else:
    st.session_state.fire_fx = False

html = f"""
<style>
  html, body {{
    margin: 0;
    padding: 0;
    background: transparent;
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial;
  }}

  .page {{
    background: #ffb6c1;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    box-sizing: border-box;
  }}

  .card {{
    width: min(760px, 92vw);
    background: rgba(255,255,255,0.88);
    border-radius: 22px;
    padding: 42px 26px 62px 26px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
    position: relative;
    overflow: hidden;
  }}

  .pulse {{
    animation: pulse 650ms ease-in-out 1;
  }}
  @keyframes pulse {{
    0%   {{ transform: scale(1); }}
    40%  {{ transform: scale(1.03); }}
    100% {{ transform: scale(1); }}
  }}

  .title {{
    font-size: clamp(26px, 3.2vw, 42px);
    font-weight: 900;
    text-align: center;
    color: #b1005a;
    margin: 0 0 26px 0;
  }}

  .btn-row {{
    display: flex;
    justify-content: center;
    gap: 26px;
    margin-top: 12px;
    position: relative;
    height: 190px;
  }}

  .yes-btn {{
    border: none;
    cursor: pointer;
    font-size: 20px;
    font-weight: 900;
    padding: 14px 34px;
    border-radius: 14px;
    background: #ff2e88;
    color: white;
    box-shadow: 0 8px 18px rgba(255,46,136,0.35);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
  }}
  .yes-btn:hover {{
    transform: scale(1.12);
    box-shadow: 0 12px 26px rgba(255,46,136,0.45);
  }}

  .no-btn {{
    position: absolute;
    top: 80px;
    left: 420px;
    border: none;
    cursor: pointer;
    font-size: 20px;
    font-weight: 900;
    padding: 14px 34px;
    border-radius: 14px;
    background: #ffffff;
    color: #b1005a;
    box-shadow: 0 8px 18px rgba(0,0,0,0.15);
    user-select: none;
    will-change: transform, top, left;
  }}

  .msg {{
    margin-top: 18px;
    text-align: center;
    font-size: 32px;
    font-weight: 1000;
    color: #b1005a;
  }}

  #confettiCanvas {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
  }}

  .heart {{
    position: absolute;
    bottom: -40px;
    font-size: 22px;
    opacity: 0.9;
    animation: floatUp linear forwards;
    pointer-events: none;
    filter: drop-shadow(0 6px 10px rgba(0,0,0,0.15));
  }}
  @keyframes floatUp {{
    from {{
      transform: translateY(0) translateX(0) rotate(0deg);
      opacity: 0.95;
    }}
    to {{
      transform: translateY(-520px) translateX(var(--drift)) rotate(18deg);
      opacity: 0;
    }}
  }}
</style>

<div class="page">
  <div class="card" id="card">
    <canvas id="confettiCanvas"></canvas>

    <div class="title">Misiu, czy zostaniesz moją walentynką?</div>

    <div class="btn-row" id="arena">
      <button class="yes-btn" onclick="window.top.location.search='?ans=yes'">Tak</button>

      <button id="noBtn" class="no-btn"
        onclick="return false;"
        onmousedown="return false;"
        ontouchstart="return false;"
      >Nie</button>
    </div>

    {"<div class='msg'>Kocham Cię ❤️</div>" if st.session_state.yes_clicked else ""}
  </div>
</div>

<script>
  function clamp(v, min, max) {{
    return Math.max(min, Math.min(max, v));
  }}
  function rand(min, max) {{
    return Math.random() * (max - min) + min;
  }}

  function setupRunaway() {{
    const arena = document.getElementById("arena");
    const btn = document.getElementById("noBtn");
    if (!arena || !btn) return;

    const phrases = ["Nie","Na pewno?","Serio?","Ej no… 🥺","Nie dasz rady 😏","Zastanów się 😳","No weź… ❤️"];
    let idx = 0;

    function setTextNext() {{
      idx = (idx + 1) % phrases.length;
      btn.textContent = phrases[idx];
    }}

    function placeInside(left, top) {{
      const ar = arena.getBoundingClientRect();
      const br = btn.getBoundingClientRect();
      const maxLeft = Math.max(0, ar.width - br.width);
      const maxTop  = Math.max(0, ar.height - br.height);
      btn.style.left = clamp(left, 0, maxLeft) + "px";
      btn.style.top  = clamp(top, 0, maxTop) + "px";
    }}

    placeInside(420, 80);

    const threshold = 150;
    const stepMin = 55;
    const stepMax = 150;

    function flee(mx, my) {{
      const b = btn.getBoundingClientRect();
      const bx = b.left + b.width/2;
      const by = b.top + b.height/2;

      const dx = bx - mx;
      const dy = by - my;
      const dist = Math.sqrt(dx*dx + dy*dy);

      if (dist > threshold) return;

      const nx = dx / (dist || 1);
      const ny = dy / (dist || 1);

      const step = rand(stepMin, stepMax) * (1 + (threshold - dist)/threshold);

      let newLeft = btn.offsetLeft + nx * step + rand(-22, 22);
      let newTop  = btn.offsetTop  + ny * step + rand(-22, 22);

      placeInside(newLeft, newTop);
      setTextNext();
    }}

    arena.addEventListener("mousemove", (e) => flee(e.clientX, e.clientY));
    btn.addEventListener("mouseenter", (e) => flee(e.clientX, e.clientY));
    btn.addEventListener("mousedown", (e) => {{
      flee(e.clientX, e.clientY);
      e.preventDefault(); e.stopPropagation();
      return false;
    }});
    btn.addEventListener("touchstart", (e) => {{
      const t = e.touches?.[0];
      if (t) flee(t.clientX, t.clientY);
      e.preventDefault(); e.stopPropagation();
      return false;
    }});
  }}

  function playDing() {{
    try {{
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      const ctx = new AudioCtx();
      const o1 = ctx.createOscillator();
      const o2 = ctx.createOscillator();
      const g  = ctx.createGain();

      o1.type = "sine"; o2.type = "triangle";
      o1.frequency.value = 880;
      o2.frequency.value = 1320;

      g.gain.setValueAtTime(0.0001, ctx.currentTime);
      g.gain.exponentialRampToValueAtTime(0.35, ctx.currentTime + 0.02);
      g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.55);

      o1.connect(g); o2.connect(g); g.connect(ctx.destination);
      o1.start(); o2.start();
      o1.stop(ctx.currentTime + 0.6);
      o2.stop(ctx.currentTime + 0.6);
    }} catch (e) {{}}
  }}

  function spawnHearts(durationMs=2200) {{
    const card = document.getElementById("card");
    if (!card) return;

    const start = performance.now();
    const timer = setInterval(() => {{
      const now = performance.now();
      if (now - start > durationMs) {{
        clearInterval(timer);
        return;
      }}

      const h = document.createElement("div");
      h.className = "heart";
      h.textContent = "❤️";

      const rect = card.getBoundingClientRect();
      const left = rand(20, rect.width - 40);
      const drift = rand(-120, 120);
      const size = rand(18, 34);
      const life = rand(1200, 2100);

      h.style.left = left + "px";
      h.style.fontSize = size + "px";
      h.style.setProperty("--drift", drift + "px");
      h.style.animationDuration = life + "ms";

      card.appendChild(h);
      setTimeout(() => h.remove(), life + 50);
    }}, 70);
  }}

  function runConfetti(durationMs=2200) {{
    const canvas = document.getElementById("confettiCanvas");
    const card = document.getElementById("card");
    if (!canvas || !card) return;

    const ctx = canvas.getContext("2d");

    function resize() {{
      const r = card.getBoundingClientRect();
      canvas.width = Math.floor(r.width * devicePixelRatio);
      canvas.height = Math.floor(r.height * devicePixelRatio);
      canvas.style.width = r.width + "px";
      canvas.style.height = r.height + "px";
      ctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0);
    }}
    resize();
    window.addEventListener("resize", resize);

    const pieces = [];
    const W = () => card.getBoundingClientRect().width;
    const H = () => card.getBoundingClientRect().height;
    const colors = ["#ff2e88", "#b1005a", "#ffffff", "#ff6fb3", "#ffd1e6"];

    for (let i=0; i<160; i++) {{
      pieces.push({{
        x: rand(0, W()),
        y: rand(-H()*0.3, 0),
        vx: rand(-2.2, 2.2),
        vy: rand(2.0, 5.5),
        r: rand(3, 6),
        a: rand(0, Math.PI*2),
        va: rand(-0.2, 0.2),
        c: colors[Math.floor(rand(0, colors.length))]
      }});
    }}

    const t0 = performance.now();
    function draw() {{
      const t = performance.now();
      const elapsed = t - t0;

      ctx.clearRect(0, 0, W(), H());

      for (const p of pieces) {{
        p.x += p.vx;
        p.y += p.vy;
        p.a += p.va;
        p.vy += 0.02;

        if (p.y > H() + 20) {{
          p.y = rand(-40, 0);
          p.x = rand(0, W());
          p.vy = rand(2.0, 5.5);
        }}
        if (p.x < -20) p.x = W()+20;
        if (p.x > W()+20) p.x = -20;

        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.a);
        ctx.fillStyle = p.c;
        ctx.fillRect(-p.r, -p.r, p.r*2, p.r*2);
        ctx.restore();
      }}

      if (elapsed < durationMs) requestAnimationFrame(draw);
      else {{
        ctx.clearRect(0, 0, W(), H());
        window.removeEventListener("resize", resize);
      }}
    }}
    requestAnimationFrame(draw);
  }}

  function fireYesFx() {{
    const card = document.getElementById("card");
    if (card) {{
      card.classList.remove("pulse");
      void card.offsetWidth;
      card.classList.add("pulse");
    }}
    playDing();
    runConfetti(2400);
    spawnHearts(2400);
  }}

  setupRunaway();

  const shouldFire = {str(st.session_state.fire_fx).lower()};
  if (shouldFire) fireYesFx();
</script>
"""

# To renderuje HTML+JS poprawnie (w iframe), bez pokazywania tagów jako tekst
components.html(html, height=640, scrolling=False)
