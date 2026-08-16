# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════
  FOR YOU ❤️  —  a tiny, cute Streamlit web app
═══════════════════════════════════════════════════════════════════
  HOW TO RUN:
      pip install streamlit
      streamlit run app.py
      (then open the localhost link it prints, best on her phone)

  ┌─────────────────────────────────────────────────────────────────┐
  │  WHAT YOU CAN CUSTOMIZE  (everything is commented below)       │
  ├─────────────────────────────────────────────────────────────────┤
  │ 1. The love message  → look for "LOVE_MESSAGE" below           │
  │ 2. Her photo         → drop a file named  my_love.jpg          │
  │                        in THIS folder (png works too)          │
  │ 3. Soft music        → drop a file named  music.mp3            │
  │                        in THIS folder (any soft mp3)           │
  │ 4. Colors / sizes    → look for the CSS inside build_html(),   │
  │                        all the pinks live in the :root{} block │
  └─────────────────────────────────────────────────────────────────┘
"""

# ──────────────────────────────────────────────────────────────────────
# imports
# ──────────────────────────────────────────────────────────────────────
import base64                # turns her photo / the music into text the
                             # browser can display without needing a server
import html                  # keeps your message safe inside the HTML
import mimetypes             # figures out the type of your photo/music
import os                    # checks whether the photo/music files exist

import streamlit as st                       # the web app framework
import streamlit.components.v1 as components # lets us inject our own
                                             # HTML + CSS + JavaScript

# ══════════════════════════════════════════════════════════════════════
# ✏️  EDIT ME #1  —  THE LOVE MESSAGE
#    Change the text inside the quotes. It can be as long as you like.
# ══════════════════════════════════════════════════════════════════════
LOVE_MESSAGE = (
    "I made this just for you. I love you so much. "
    "You make my days better. - Michel"
)

# ══════════════════════════════════════════════════════════════════════
# ✏️  EDIT ME #2  —  HER PHOTO + THE MUSIC
#    Just drop the files with these exact names into the same folder
#    as app.py. If a file is missing, the app still works and shows
#    a cute placeholder instead.
# ══════════════════════════════════════════════════════════════════════
PHOTO_FILE = "my_love.jpg"   # ← her picture (jpg or png)
MUSIC_FILE = "music.mp3"     # ← soft background music (any mp3)

# ──────────────────────────────────────────────────────────────────────
# nice tab title + small heart icon shown in the browser tab
# ──────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="For You ❤️",
    page_icon="💗",
    layout="centered",
)


# ══════════════════════════════════════════════════════════════════════
#  HELPER 1 — turn her photo into a "data URI"
#    A data URI is just the picture written as one long text string.
#    We do this so the photo can live inside our custom HTML below
#    (Streamlit's custom HTML runs in a little sandboxed box, and a
#    data URI is the simplest way to get the image into that box).
#    The @st.cache_data means we only re-encode it once, not on every
#    click of the button.
# ══════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def image_to_data_uri(file_path: str) -> str | None:
    """Returns the photo as a data URI, or None if the file is missing."""
    if not os.path.exists(file_path):
        return None
    mime = mimetypes.guess_type(file_path)[0] or "image/jpeg"  # type of file
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


# ══════════════════════════════════════════════════════════════════════
#  HELPER 2 — turn the music file into a data URI (same trick as above)
# ══════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def audio_to_data_uri(file_path: str) -> str | None:
    """Returns the music as a data URI, or None if the file is missing."""
    if not os.path.exists(file_path):
        return None
    mime = mimetypes.guess_type(file_path)[0] or "audio/mpeg"
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


# ══════════════════════════════════════════════════════════════════════
#  HELPER 3 — a cute placeholder picture (used only while she hasn't
#    dropped a my_love.jpg next to app.py yet)
# ══════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def placeholder_photo_uri() -> str:
    """A soft pink SVG with a heart, shown until a real photo is added."""
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="500" '
        'viewBox="0 0 400 500">'
        '<rect width="400" height="500" fill="#ffeef4"/>'
        '<rect x="20" y="20" width="360" height="460" rx="24" fill="none" '
        'stroke="#ffb3d1" stroke-width="4" stroke-dasharray="12 10"/>'
        '<text x="200" y="235" font-size="95" text-anchor="middle">💗</text>'
        '<text x="200" y="330" font-size="30" fill="#d81b60" '
        'font-family="sans-serif" text-anchor="middle" font-weight="bold">'
        'your photo goes here</text>'
        "</svg>"
    )
    encoded = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"


# ══════════════════════════════════════════════════════════════════════
#  THE MAGIC — one big block of HTML + CSS + JavaScript
#
#  This is the entire "page" the app shows. It has two screens:
#    • "landing"   → the big "Hi my love" + the big "Press OK" button
#    • "surprise"  → hidden until she presses OK; shows the message,
#                    the photo frame and the floating hearts
#
#  The placeholders like __MESSAGE__ are swapped for real content at the
#  bottom of this file, so we never have to fight with curly braces in
#  the CSS/JavaScript.
# ══════════════════════════════════════════════════════════════════════
def build_html(message: str, photo_uri: str, music_uri: str | None) -> str:
    """Puts together the full page HTML. Nothing inside here is secret —
       it is all plain HTML you can read like a recipe."""

    # does music exist? we tell the JavaScript so it can show/hide the
    # little music button and only try to play when there is a file
    has_music = music_uri is not None
    # the JavaScript needs the word "true"/"false", not a Python value
    has_music_str = "true" if has_music else "false"

    # if music exists we build an <audio> tag that points at it
    audio_tag = f'<source src="{music_uri}">' if has_music else ""

    page = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- ─────────────────────────────────────────────────────────────
     ✏️  EDIT ME #3  —  COLORS, SIZES, EVERYTHING LOOKS-RELATED
     All the pink shades live in the CSS ":root" block below. Change
     any colour there and the whole page updates everywhere at once.
     ───────────────────────────────────────────────────────────── -->
<style>
  :root {{
    --pink:        #ff6fb5;   /* main pink (the button)      */
    --deep-pink:   #e11d74;   /* the big title text          */
    --soft-pink:   #ffc2dc;   /* card borders + frame edge   */
    --blush:       #fff0f6;   /* lightest background pink    */
    --rose:        #ffd9e8;   /* middle background pink      */
    --blossom:     #ffc2dc;   /* deepest background pink     */
    --ink:         #831843;   /* dark plum colour for text   */
  }}

  /* reset the default spacing so we control everything */
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    font-family: 'Segoe UI', -apple-system, 'Helvetica Neue', Arial, sans-serif;
    color: var(--ink);
    /* soft pink gradient from top-left to bottom-right */
    background: linear-gradient(160deg, var(--blush) 0%, var(--rose) 50%, var(--blossom) 100%);
    min-height: 100vh;      /* old phones need this */
    min-height: 100dvh;     /* modern phones use this */
    overflow-x: hidden;
  }}

  /* the canvas that draws the floating hearts — it is fixed to the
     whole screen and lets every tap "fall through" to the content */
  #hearts {{
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: none;
  }}

  /* everything sits on top of the hearts, centred on screen */
  .page {{
    position: relative;
    z-index: 1;
    min-height: 100vh;
    min-height: 100dvh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
    text-align: center;
  }}

  /* ───────────── LANDING SCREEN (before she presses OK) ───────────── */

  .big-heart {{
    font-size: clamp(4rem, 20vw, 7rem);   /* huge, but shrinks on phones */
    display: inline-block;
    animation: beat 1.2s infinite ease-in-out;   /* heart "heartbeat" */
  }}

  @keyframes beat {{
    0%, 100% {{ transform: scale(1); }}
    20%      {{ transform: scale(1.15); }}
    40%      {{ transform: scale(1); }}
    60%      {{ transform: scale(1.12); }}
  }}

  h1 {{
    font-size: clamp(2.6rem, 10vw, 5rem);
    font-weight: 800;
    color: var(--deep-pink);
    margin: 12px 0 30px;
    letter-spacing: 1px;
    text-shadow: 0 2px 12px rgba(225, 29, 116, 0.15);
  }}

  /* the big "Press OK" pill button */
  #okBtn {{
    font-size: clamp(1.4rem, 5vw, 2rem);
    font-weight: 700;
    color: #ffffff;
    background: linear-gradient(135deg, var(--pink), #f43f8e);
    border: none;
    border-radius: 999px;
    padding: 18px 56px;
    cursor: pointer;
    box-shadow: 0 10px 30px rgba(244, 63, 142, 0.45);
    transition: transform .15s ease, box-shadow .15s ease;
    touch-action: manipulation;   /* no double-tap zoom on phones */
  }}
  #okBtn:hover   {{ transform: translateY(-2px) scale(1.03);
                   box-shadow: 0 14px 34px rgba(244,63,142,.55); }}
  #okBtn:active  {{ transform: scale(.96); }}

  .hint {{ margin-top: 18px; color: var(--deep-pink); opacity: .7; }}

  /* ───────────── SURPRISE SCREEN (after she presses OK) ───────────── */

  .hidden {{ display: none !important; }}   /* flips the screen off/on */

  #surprise {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 22px;
    animation: pop .6s ease;   /* cute little pop-in effect */
  }}

  @keyframes pop {{
    from {{ opacity: 0; transform: scale(.8); }}
    to   {{ opacity: 1; transform: scale(1); }}
  }}

  /* the white card that holds your message */
  .message-card {{
    background: rgba(255, 255, 255, .85);
    border: 2px solid var(--soft-pink);
    border-radius: 24px;
    padding: 26px 28px;
    max-width: 460px;
    box-shadow: 0 12px 30px rgba(225, 29, 116, .18);
  }}

  .message-card p {{
    font-size: clamp(1.15rem, 4.5vw, 1.55rem);
    line-height: 1.6;
    font-weight: 600;
  }}

  /* the cute photo frame — white border, pink edge, slightly tilted */
  .photo-frame {{
    width: min(78vw, 300px);      /* biggest on a phone, capped on desktop */
    aspect-ratio: 4 / 5;          /* nice portrait rectangle */
    background: #ffffff;
    border: 8px solid #ffffff;
    outline: 2px solid var(--soft-pink);
    border-radius: 22px;
    transform: rotate(-3deg);     /* that playful tilted look */
    box-shadow: 0 16px 36px rgba(225, 29, 116, .28);
    overflow: hidden;
  }}
  .photo-frame img {{
    width: 100%;
    height: 100%;
    object-fit: cover;   /* her photo fills the frame without stretching */
    display: block;
  }}

  .signature {{ color: var(--deep-pink); opacity: .8; }}

  /* ───────────── THE MUSIC BUTTON (top-right corner) ───────────── */

  #musicBtn {{
    position: fixed;
    top: 16px;
    right: 16px;
    z-index: 5;
    width: 52px;
    height: 52px;
    border-radius: 50%;
    border: none;
    font-size: 1.4rem;
    background: rgba(255, 255, 255, .9);
    box-shadow: 0 6px 16px rgba(225, 29, 116, .25);
    cursor: pointer;
    touch-action: manipulation;
    transition: transform .15s ease;
  }}
  #musicBtn:active {{ transform: scale(.9); }}
</style>
</head>

<body>

  <!-- the floating-hearts canvas lives behind everything -->
  <canvas id="hearts"></canvas>

  <div class="page">

    <!-- ═══════════ SCREEN 1 · LANDING ═══════════ -->
    <div id="landing">
      <span class="big-heart">💗</span>
      <h1>Hi my love</h1>
      <!-- pressing this button calls reveal() in the JavaScript below -->
      <button id="okBtn" onclick="reveal()">Press OK</button>
      <p class="hint">go on… press it 💌</p>
    </div>

    <!-- ═══════════ SCREEN 2 · SURPRISE (hidden until OK is pressed) ═══════════ -->
    <div id="surprise" class="hidden">

      <!-- the message card — your text appears here -->
      <div class="message-card">
        <p>{message}</p>
      </div>

      <!-- the photo frame — her picture appears here -->
      <div class="photo-frame">
        <img src="{photo_uri}" alt="my love">
      </div>

      <p class="signature">made with ❤️ for you</p>
    </div>

  </div>

  <!-- the music button (hidden automatically if no music.mp3 exists) -->
  <button id="musicBtn">🎵</button>
  <!-- the audio player itself — loop makes it repeat softly forever -->
  <audio id="music" loop preload="auto">{audio_tag}</audio>

<script>
  // ────────────────────────────────────────────────────────────────────
  //  JAVASCRIPT — the tiny bit of "interactivity magic"
  //   1. reveal()  → swaps to the surprise screen + starts the hearts
  //   2. the hearts animation (drawn on a canvas with emoji 💗)
  //   3. toggleMusic() → plays / pauses the soft music
  // ────────────────────────────────────────────────────────────────────

  // is there a music file? ("true" / "false" is filled in by Python)
  const HAS_MUSIC = {has_music_str};

  // grab the two screens so we can swap between them
  const landing  = document.getElementById('landing');
  const surprise = document.getElementById('surprise');

  // what she sees when she presses the big button
  function reveal() {{
    landing.classList.add('hidden');      // hide the "Hi my love" screen
    surprise.classList.remove('hidden');  // show the surprise screen
    if (!running) {{                      // start the hearts only once
      running = true;
      requestAnimationFrame(drawHearts);
    }}
    // browsers only allow music to start after a tap/click, so this is
    // the perfect moment to start the soft music automatically
    if (HAS_MUSIC && audio.paused) {{
      audio.play().catch(() => {{}});     // .catch in case the browser says no
      setMusicIcon(true);
    }}
  }}

  // ── floating hearts ────────────────────────────────────────────────
  const canvas  = document.getElementById('hearts');
  const ctx     = canvas.getContext('2d');
  const hearts  = [];
  let running   = false;

  function sizeCanvas() {{
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
  }}
  window.addEventListener('resize', sizeCanvas);
  sizeCanvas();   // set the size once on load

  // create one heart at a random spot below the bottom of the screen
  function spawnHeart() {{
    hearts.push({{
      x:   Math.random() * canvas.width,          // random left/right
      y:   canvas.height + 30,                    // start just off-screen
      s:   14 + Math.random() * 22,               // random size
      v:   0.7 + Math.random() * 1.4,             // random float speed
      o:   0.6 + Math.random() * 0.4,             // random see-through-ness
      wob: Math.random() * Math.PI * 2            // random sway start point
    }});
  }}

  // draw every heart, move them up, repeat forever
  function drawHearts() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (Math.random() < 0.25) spawnHeart();       // occasionally add a new one
    for (let i = 0; i < hearts.length; i++) {{
      const h = hearts[i];
      h.y   -= h.v;                               // float upwards
      h.wob += 0.05;
      h.x   += Math.sin(h.wob) * 0.6;             // gentle left/right sway
      ctx.font = h.s + 'px serif';
      ctx.textAlign    = 'center';
      ctx.textBaseline = 'middle';
      ctx.globalAlpha  = h.o;
      ctx.fillText('💗', h.x, h.y);               // draw the heart emoji
    }}
    ctx.globalAlpha = 1;
    // forget hearts that have floated off the top
    hearts.splice(0, hearts.length, ...hearts.filter(h => h.y > -50));
    requestAnimationFrame(drawHearts);            // do it again next frame
  }}

  // ── music toggle ───────────────────────────────────────────────────
  const audio    = document.getElementById('music');
  const musicBtn = document.getElementById('musicBtn');

  function setMusicIcon(playing) {{
    musicBtn.textContent = playing ? '🔇' : '🎵';  // 🎵 on, 🔇 off
  }}

  function toggleMusic() {{
    if (!HAS_MUSIC) return;
    if (audio.paused) {{
      audio.play().catch(() => {{}});
      setMusicIcon(true);
    }} else {{
      audio.pause();
      setMusicIcon(false);
    }}
  }}

  // only wire up the button if there is actually a music file
  if (HAS_MUSIC) {{
    musicBtn.addEventListener('click', toggleMusic);
  }} else {{
    musicBtn.style.display = 'none';   // no music → hide the button
  }}
</script>

</body>
</html>
"""

    # ── the "fill in the blanks" step ──────────────────────────────────
    # swap the placeholders for the real content. We use an f-string so
    # the message / photo / music get inserted directly into the page.
    return page


# ══════════════════════════════════════════════════════════════════════
#  PUTTING IT ALL TOGETHER — the actual page that runs
# ══════════════════════════════════════════════════════════════════════

# 1) get her photo as a data URI (or the cute placeholder if missing)
photo_uri = image_to_data_uri(PHOTO_FILE)
if photo_uri is None:
    photo_uri = placeholder_photo_uri()

# 2) get the music as a data URI (or None if missing)
music_uri = audio_to_data_uri(MUSIC_FILE)

# 3) build the whole page with the real message + photo + music inside
page_html = build_html(
    message=html.escape(LOVE_MESSAGE),   # keeps your message text safe
    photo_uri=photo_uri,
    music_uri=music_uri,
)

# 4) show it! scrolling=False keeps it looking like a clean full page
components.html(page_html, height=1000, scrolling=False)

# 5) small helper hints — only appear while a file is still missing
if not os.path.exists(PHOTO_FILE):
    st.caption("💡 Tip: drop a file named `my_love.jpg` next to app.py to show her photo.")
if not os.path.exists(MUSIC_FILE):
    st.caption("💡 Tip: drop a file named `music.mp3` next to app.py to add soft music.")
