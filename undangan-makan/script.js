/* =========================================================
   Undangan Makan Romantis untuk Oktalina - Script
   ========================================================= */

const NAMA = 'Olin';
const PANGGILAN = 'Olin';

/* ---------- 1. HATI BERTABURAN ---------- */
const heartsLayer = document.getElementById('hearts');
const heartChars = ['', '', '', '', '', '', ''];

function spawnHeart() {
  const h = document.createElement('span');
  h.className = 'heart';
  h.textContent = heartChars[Math.floor(Math.random() * heartChars.length)];
  h.style.left = Math.random() * 100 + 'vw';
  h.style.fontSize = (16 + Math.random() * 22) + 'px';
  const dur = 6 + Math.random() * 6;
  h.style.animationDuration = dur + 's';
  heartsLayer.appendChild(h);
  setTimeout(() => h.remove(), dur * 1000);
}
setInterval(spawnHeart, 350);

/* ---------- 1b. NAMA "OKTALINA" MELAYANG DI BACKGROUND ---------- */
const nameLayer = document.getElementById('nameFloats');
function spawnName() {
  const n = document.createElement('span');
  n.className = 'name-float';
  n.textContent = NAMA;
  n.style.top = (5 + Math.random() * 90) + 'vh';
  const dur = 12 + Math.random() * 10;
  n.style.animationDuration = dur + 's';
  nameLayer.appendChild(n);
  setTimeout(() => n.remove(), dur * 1000);
}
for (let i = 0; i < 3; i++) setTimeout(spawnName, i * 1500);
setInterval(spawnName, 4500);

/* ---------- 2. AMPLOP COVER ---------- */
const envelope = document.getElementById('envelope');
const cover    = document.getElementById('cover');
const invite   = document.getElementById('invite');

function openEnvelope() {
  envelope.classList.add('open');
  setTimeout(() => {
    cover.classList.add('hidden');
    invite.classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, 1300);
}
envelope.addEventListener('click', openEnvelope);
envelope.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') openEnvelope();
});

/* ---------- 3. TOMBOL "GAK MAU" YANG KABUR ---------- */
const btnNo  = document.getElementById('btnNo');
const tinyHint = document.getElementById('tinyHint');
let dodgeCount = 0;
const noTexts = [
  ' Gak mau ah',
  ' Eits, jangan dong Olin~',
  ' Coba tangkap dulu!',
  ' Kabuuur~',
  ' Hayo Olin mau kemana',
  ' Yakin nih, Olin?',
  ' Pilih yang pink aja~',
  ' Aku malu Olin~',
  ' Sini sayang sini~',
  ' Olin jangan tinggalin aku',
  ' Aku gak bisa hidup tanpa Olin',
  ' Sayaaang, mauu yaa?'
];

function dodge() {
  dodgeCount++;
  const parent = btnNo.parentElement;
  const pRect  = parent.getBoundingClientRect();
  const bRect  = btnNo.getBoundingClientRect();

  const maxX = Math.max(0, pRect.width  - bRect.width);
  const maxY = 220;

  const x = Math.random() * maxX;
  const y = (Math.random() - 0.5) * maxY;

  btnNo.classList.add('run');
  btnNo.style.left = x + 'px';
  btnNo.style.top  = y + 'px';

  const span = btnNo.querySelector('span');
  span.textContent = noTexts[dodgeCount % noTexts.length];

  if (dodgeCount === 3 && tinyHint) {
    tinyHint.textContent = '(Hihi, susah ya nangkepnya, Olin~)';
  }
  if (dodgeCount > 6) {
    btnNo.style.opacity = '.4';
    btnNo.style.filter  = 'blur(.5px)';
  }
  if (dodgeCount > 10 && tinyHint) {
    tinyHint.textContent = '(Udah Olin, klik yang pink aja yuk )';
  }
}
btnNo.addEventListener('mouseenter', dodge);
btnNo.addEventListener('focus', dodge);
btnNo.addEventListener('touchstart', dodge);
btnNo.addEventListener('click', (e) => {
  e.preventDefault();
  dodge();
});

/* ---------- 4. TOMBOL "MAU" -> CONFETTI + MODAL SURAT CINTA ---------- */
const btnYes   = document.getElementById('btnYes');
const yesModal = document.getElementById('yesModal');
const waBtn    = document.getElementById('waBtn');

// ====== NOMOR WA OLIN ======
// Format: 62xxxxxxxxxxx (tanpa + dan tanpa 0 di depan)
const WA_NUMBER = '6282178316261';

const waMessage =
  `Halo sayang Olin~ \n\n` +
  `Aku udah liat undangannya, dan… aku tau kamu bilang "MAU"! \n\n` +
  `Besok jam 10.30 aku jemput kamu ya. ` +
  `Pakai baju yang Olin nyaman aja, gak perlu ribet — ` +
  `kamu udah cantik banget di mata aku.\n\n` +
  `Sampai ketemu besok, Olin. Aku gak sabar~ `;

if (WA_NUMBER) {
  waBtn.href = `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(waMessage)}`;
} else {
  waBtn.href = '#';
  waBtn.addEventListener('click', async (e) => {
    e.preventDefault();
    try {
      await navigator.clipboard.writeText(waMessage);
      waBtn.innerHTML = ' Pesan disalin! Tinggal paste ke WA';
      setTimeout(() => { waBtn.innerHTML = ' Chat aku di WA'; }, 2500);
    } catch {
      waBtn.innerHTML = ' (Atur nomor WA dulu di script.js)';
    }
  });
}

btnYes.addEventListener('click', () => {
  burstConfetti();
  setTimeout(burstConfetti, 600);
  setTimeout(burstConfetti, 1200);
  setTimeout(() => yesModal.classList.remove('hidden'), 500);
});

function closeYes() {
  yesModal.classList.add('hidden');
}
window.closeYes = closeYes;

/* ---------- 5. CONFETTI CANVAS ---------- */
const canvas = document.getElementById('confetti');
const ctx = canvas.getContext('2d');
let confettiPieces = [];
let confettiRunning = false;

function resizeCanvas() {
  canvas.width  = window.innerWidth;
  canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

const colors = ['#ff4d8d', '#ffd166', '#ff79a8', '#ff9ec1', '#ffb3cb', '#ffffff', '#e63b78'];
const shapes = ['rect', 'circle', 'heart', 'heart'];

function makePiece() {
  return {
    x: Math.random() * canvas.width,
    y: -20 - Math.random() * canvas.height * 0.4,
    w: 8 + Math.random() * 10,
    h: 8 + Math.random() * 14,
    vx: (Math.random() - 0.5) * 6,
    vy: 3 + Math.random() * 4,
    rot: Math.random() * Math.PI * 2,
    vr: (Math.random() - 0.5) * 0.2,
    color: colors[Math.floor(Math.random() * colors.length)],
    shape: shapes[Math.floor(Math.random() * shapes.length)],
    life: 0,
    maxLife: 250 + Math.random() * 150
  };
}

function burstConfetti() {
  for (let i = 0; i < 200; i++) confettiPieces.push(makePiece());
  if (!confettiRunning) {
    confettiRunning = true;
    requestAnimationFrame(loopConfetti);
  }
}

function drawHeart(ctx, size) {
  ctx.beginPath();
  const s = size / 10;
  ctx.moveTo(0, -3 * s);
  ctx.bezierCurveTo(-5*s, -8*s, -10*s, -2*s, 0, 5*s);
  ctx.bezierCurveTo(10*s, -2*s, 5*s, -8*s, 0, -3*s);
  ctx.fill();
}

function loopConfetti() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  confettiPieces.forEach(p => {
    p.x   += p.vx;
    p.y   += p.vy;
    p.rot += p.vr;
    p.vy  += 0.05;
    p.life++;

    ctx.save();
    ctx.translate(p.x, p.y);
    ctx.rotate(p.rot);
    ctx.fillStyle = p.color;
    if (p.shape === 'rect') {
      ctx.fillRect(-p.w/2, -p.h/2, p.w, p.h);
    } else if (p.shape === 'circle') {
      ctx.beginPath();
      ctx.arc(0, 0, p.w/2, 0, Math.PI * 2);
      ctx.fill();
    } else {
      drawHeart(ctx, p.w * 1.5);
    }
    ctx.restore();
  });

  confettiPieces = confettiPieces.filter(p =>
    p.life < p.maxLife && p.y < canvas.height + 30
  );

  if (confettiPieces.length > 0) {
    requestAnimationFrame(loopConfetti);
  } else {
    confettiRunning = false;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }
}

/* ---------- 6. MUSIK ROMANTIS (Web Audio API) ---------- */
const musicBtn  = document.getElementById('musicBtn');
const musicIcon = document.getElementById('musicIcon');
let audioCtx, masterGain, melodyTimer;
let musicOn = false;

const melody = [
  [523.25, .35], [659.25, .35], [783.99, .35], [880.00, .55],
  [783.99, .35], [659.25, .35], [587.33, .55], [523.25, .55],
  [659.25, .35], [698.46, .35], [783.99, .55], [659.25, .55],
];

function playNote(freq, dur, when) {
  const osc  = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = 'sine';
  osc.frequency.value = freq;
  gain.gain.setValueAtTime(0, when);
  gain.gain.linearRampToValueAtTime(0.18, when + 0.02);
  gain.gain.exponentialRampToValueAtTime(0.001, when + dur);
  osc.connect(gain).connect(masterGain);
  osc.start(when);
  osc.stop(when + dur + 0.05);
}

function startMusic() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    masterGain = audioCtx.createGain();
    masterGain.gain.value = 0.5;
    masterGain.connect(audioCtx.destination);
  }
  if (audioCtx.state === 'suspended') audioCtx.resume();

  function scheduleLoop() {
    let t = audioCtx.currentTime + 0.05;
    melody.forEach(([f, d]) => {
      playNote(f, d, t);
      t += d;
    });
    melodyTimer = setTimeout(scheduleLoop, (t - audioCtx.currentTime) * 1000);
  }
  scheduleLoop();
  musicOn = true;
  musicBtn.classList.add('playing');
  musicIcon.textContent = '';
}

function stopMusic() {
  if (melodyTimer) clearTimeout(melodyTimer);
  if (audioCtx) audioCtx.suspend();
  musicOn = false;
  musicBtn.classList.remove('playing');
  musicIcon.textContent = '';
}

musicIcon.textContent = '';
musicBtn.addEventListener('click', () => {
  if (musicOn) stopMusic();
  else startMusic();
});
