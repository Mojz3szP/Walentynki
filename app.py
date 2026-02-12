import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Walentynka", layout="wide")

# --- TŁO STREAMLIT: różowe + serduszka + bez dziwnych marginesów ---
st.markdown(
    """
    <style>
      /* tło całej aplikacji */
      .stApp {
        background-color: #ffb6c1;
        /* serduszka jako pattern (SVG data-uri) */
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Ctext x='14' y='44' font-size='34'%3E%E2%9D%A4%EF%B8%8F%3C/text%3E%3Ctext x='86' y='108' font-size='26'%3E%E2%9D%A4%EF%B8%8F%3C/text%3E%3Ctext x='118' y='36' font-size='18'%3E%E2%9D%A4%EF%B8%8F%3C/text%3E%3C/svg%3E");
        background-repeat: repeat;
        background-size: 160px 160px;
      }

      /* usuń domyślne “ramki/odstępy” streamlit */
      header, footer, #MainMenu { visibility: hidden; }
      .block-container { padding-top: 0.5rem; padding-bottom: 0.5rem; }

      /* iframe od components.html bez obramowania i bez tła */
      iframe {
        border: 0 !important;
        background: transparent !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- HTML+JS (w iframe) ---
html = r"""
<style>
  html, body {
    margin: 0; padding: 0;
    background: transparent;
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial;
  }

  .wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 92vh;
    padding: 18px;
    box-sizing: border-box;
    background: transparent;
  }

  .card {
    width: min(760px, 92vw);
    background: rgba(255,255,255,0.90);
    border-radius: 22px;
    padding: 42px 26px 62px 26px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
    position: relative;
    overflow: hidden;
  }

  .title {
    font-size: clamp(26px, 3.2vw, 42px);
    font-weight: 900;
    text-align: center;
    color: #b1005a;
    margin: 0 0 26px 0;
  }

  /* ARENA */
  .arena {
    position: relative;
    height: 220px;
    margin-top: 8px;
  }

  /* WSPÓLNA wielkość przycisków */
  .btn {
    height: 56px;                 /* stała wysokość (symetria) */
    min-width: 180px;             /* stała szerokość (symetria) */
    padding: 0 28px;              /* bez zmiany wysokości */
    border-radius: 14px;
    border: none;
    font-size: 20px;
    font-weight: 900;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    user-select: none;
    line-height: 1;               /* nie rozjeżdża baseline */
  }

  /* Start: symetrycznie (lewy/prawy), ten sam TOP */
  .yes-btn, .no-btn {
    position: absolute;
    top: 90px;                    /* identyczna wysokość */
    transform: translate(-50%, -50%);
  }
  .yes-btn { left: 35%; }
  .no-btn  { left: 65%; }

  .yes-btn {
    background: #ff2e88;
    color: white;
    box-shadow: 0 8px 18px rgba(255,46,136,0.35);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
  }
  .yes-btn:hover {
    transform: translate(-50%, -50%) scale(1.10);
    box-shadow: 0 12px 26px rgba(255,46,136,0.45);
  }

  .no-btn {
    background: #ffffff;
    color: #b1005a;
    box-shadow: 0 8px 18px rgba(0,0,0,0.15);
    will-change: left, top;
  }

  /* MODAL: "Kocham Cię <3" */
  .modal-backdrop {
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,0.25);
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 10;
    padding: 18px;
    box-sizing: border-box;
  }
  .modal {
    width: min(520px, 92vw);
    background: rgba(255,255,255,0.95);
    border-radius: 18px;
    padding: 26px 18px;
    box-shadow: 0 18px 40px rgba(0,0,0,0.18);
    text-align: center;
  }
  .modal h2 {
    margin: 0 0 14px 0;
    font-size: 34px;
    color: #b1005a;
    font-weight: 1000;
  }
  .modal p {
    margin: 0 0 18px 0;
    font-size: 18px;
    color: #7a003e;
    font-weight: 700;
  }
  .close-btn {
    background: #ff2e88;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 18px;
    font-weight: 900;
    cursor: pointer;
  }

  /* serduszka animowane */
  .heart {
    position: absolute;
    bottom: -40px;
    font-size: 22px;
    opacity: 0.9;
    animation: floatUp linear forwards;
    pointer-events: none;
    filter: drop-shadow(0 6px 10px rgba(0,0,0,0.15));
    z-index: 5;
  }
  @keyframes floatUp {
    from { transform: translateY(0) translateX(0) rotate(0deg); opacity: 0.95; }
    to   { transform: translateY(-520px) translateX(var(--drift)) rotate(18deg); opacity: 0; }
  }

  /* canvas konfetti */
  #confettiCanvas {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 4;
  }
</style>

<div class="wrap">
  <div class="card" id="card">
    <canvas id="confettiCanvas"></canvas>

    <div class="modal-backdrop" id="modalBg">
      <div class="modal">
        <h2>Kocham Cię &lt;3</h2>
        <p>Najpiękniejsza walentynka na świecie ❤️</p>
        <button class="close-btn" id="closeModal">OK</button>
      </div>
    </div>

    <div class="title">Misiu, czy zostaniesz moją walentynką?</div>

    <div class="arena" id="arena">
      <button class="btn yes-btn" id="yesBtn">Tak</button>

      <button class="btn no-btn" id="noBtn"
        onclick="return false;"
        onmousedown="return false;"
        ontouchstart="return false;"
      >Nie</button>
    </div>
  </div>
</div>

<script>
  function clamp(v, min, max){ return Math.max(min, Math.min(max, v)); }
  function rand(min, max){ return Math.random() * (max - min) + min; }

  // --- MODAL
  function openModal(){
    const bg = document.getElementById("modalBg");
    if (bg) bg.style.display = "flex";
  }
  function closeModal(){
    const bg = document.getElementById("modalBg");
    if (bg) bg.style.display = "none";
  }

  // --- DŹWIĘK (opcjonalny)
  function playDing(){
    try{
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      const ctx = new AudioCtx();
      const o1 = ctx.createOscillator();
      const o2 = ctx.createOscillator();
      const g  = ctx.createGain();

      o1.type = "sine"; o2.type = "triangle";
      o1.frequency.value = 880;
      o2.frequency.value = 1320;

      g.gain.setValueAtTime(0.0001, ctx.currentTime);
      g.gain.exponentialRampToValueAtTime(0.30, ctx.currentTime + 0.02);
      g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.55);

      o1.connect(g); o2.connect(g); g.connect(ctx.destination);
      o1.start(); o2.start();
      o1.stop(ctx.currentTime + 0.6);
      o2.stop(ctx.currentTime + 0.6);
    }catch(e){}
  }

  // --- SERDUSZKA
  function spawnHearts(durationMs=2200){
    const card = document.getElementById("card");
    if(!card) return;

    const start = performance.now();
    const timer = setInterval(() => {
      if(performance.now() - start > durationMs){
        clearInterval(timer);
        return;
      }
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
    }, 70);
  }

  // --- KONFETTI
  function runConfetti(durationMs=2200){
    const canvas = document.getElementById("confettiCanvas");
    const card = document.getElementById("card");
    if(!canvas || !card) return;

    const ctx = canvas.getContext("2d");

    function resize(){
      const r = card.getBoundingClientRect();
      canvas.width = Math.floor(r.width * devicePixelRatio);
      canvas.height = Math.floor(r.height * devicePixelRatio);
      canvas.style.width = r.width + "px";
      canvas.style.height = r.height + "px";
      ctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0);
    }
    resize();
    window.addEventListener("resize", resize);

    const pieces = [];
    const W = () => card.getBoundingClientRect().width;
    const H = () => card.getBoundingClientRect().height;
    const colors = ["#ff2e88","#b1005a","#ffffff","#ff6fb3","#ffd1e6"];

    for(let i=0;i<150;i++){
      pieces.push({
        x: rand(0, W()),
        y: rand(-H()*0.3, 0),
        vx: rand(-2.2, 2.2),
        vy: rand(2.0, 5.5),
        r: rand(3, 6),
        a: rand(0, Math.PI*2),
        va: rand(-0.2, 0.2),
        c: colors[Math.floor(rand(0, colors.length))]
      });
    }

    const t0 = performance.now();
    function draw(){
      const elapsed = performance.now() - t0;

      ctx.clearRect(0,0,W(),H());
      for(const p of pieces){
        p.x += p.vx; p.y += p.vy; p.a += p.va;
        p.vy += 0.02;

        if(p.y > H()+20){
          p.y = rand(-40, 0);
          p.x = rand(0, W());
          p.vy = rand(2.0, 5.5);
        }
        if(p.x < -20) p.x = W()+20;
        if(p.x > W()+20) p.x = -20;

        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.a);
        ctx.fillStyle = p.c;
        ctx.fillRect(-p.r, -p.r, p.r*2, p.r*2);
        ctx.restore();
      }

      if(elapsed < durationMs) requestAnimationFrame(draw);
      else {
        ctx.clearRect(0,0,W(),H());
        window.removeEventListener("resize", resize);
      }
    }
    requestAnimationFrame(draw);
  }

  // --- TAK: zawsze pokazuje wiadomość
  (function setupYes(){
    const yes = document.getElementById("yesBtn");
    const close = document.getElementById("closeModal");
    const bg = document.getElementById("modalBg");

    if(close) close.addEventListener("click", closeModal);
    if(bg) bg.addEventListener("click", (e) => { if(e.target === bg) closeModal(); });

    if(!yes) return;
    yes.addEventListener("click", () => {
      openModal();
      playDing();
      runConfetti(2200);
      spawnHearts(2200);
    });
  })();

  // --- NIE: rusza się dopiero gdy jesteś BARDZO blisko
  function setupRunaway(){
    const arena = document.getElementById("arena");
    const btn = document.getElementById("noBtn");
    if(!arena || !btn) return;

    const phrases = ["Nie","Na pewno?","Serio?","Ej no… 🥺","No weź… ❤️"];
    let idx = 0;

    function setTextNext(){
      idx = (idx + 1) % phrases.length;
      btn.textContent = phrases[idx];
    }

    function placeInside(centerLeftPx, centerTopPx){
      const ar = arena.getBoundingClientRect();
      const br = btn.getBoundingClientRect();
      const halfW = br.width / 2;
      const halfH = br.height / 2;

      const minLeft = halfW;
      const maxLeft = ar.width - halfW;
      const minTop  = halfH;
      const maxTop  = ar.height - halfH;

      btn.style.left = clamp(centerLeftPx, minLeft, maxLeft) + "px";
      btn.style.top  = clamp(centerTopPx, minTop, maxTop) + "px";
    }

    // ustaw start w px (zostaje symetrycznie z CSS: 65%)
    setTimeout(() => {
      const ar = arena.getBoundingClientRect();
      placeInside(ar.width * 0.65, 90);
    }, 0);

    const threshold = 45;   // <-- teraz rusza się dopiero “prawie na nim”
    const stepMin = 120;
    const stepMax = 220;

    function flee(mx, my){
      const ar = arena.getBoundingClientRect();
      const b = btn.getBoundingClientRect();

      const bx = b.left + b.width/2;
      const by = b.top + b.height/2;

      const dx = bx - mx;
      const dy = by - my;
      const dist = Math.sqrt(dx*dx + dy*dy);

      if(dist > threshold) return;

      const nx = dx / (dist || 1);
      const ny = dy / (dist || 1);
      const step = rand(stepMin, stepMax);

      const currentLeft = (b.left - ar.left) + b.width/2;
      const currentTop  = (b.top  - ar.top)  + b.height/2;

      const newLeft = currentLeft + nx * step + rand(-8, 8);
      const newTop  = currentTop  + ny * step + rand(-8, 8);

      placeInside(newLeft, newTop);
      setTextNext();
    }

    arena.addEventListener("mousemove", (e) => flee(e.clientX, e.clientY));
    btn.addEventListener("mouseenter", (e) => flee(e.clientX, e.clientY));
    btn.addEventListener("mousedown", (e) => {
      flee(e.clientX, e.clientY);
      e.preventDefault(); e.stopPropagation();
      return false;
    });
    btn.addEventListener("touchstart", (e) => {
      const t = e.touches?.[0];
      if(t) flee(t.clientX, t.clientY);
      e.preventDefault(); e.stopPropagation();
      return false;
    });
  }

  setupRunaway();
</script>
"""

components.html(html, height=720, scrolling=False)

