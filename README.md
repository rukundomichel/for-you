# For You ❤️

A tiny, cute web app for your favourite person.

## How to run

1. Install the one dependency (once):

   ```
   pip install streamlit
   ```

2. Run the app from this folder:

   ```
   streamlit run app.py
   ```

3. Open the link it prints (http://localhost:8501). Send that link to her
   phone on the same Wi-Fi and let her open it there for the full effect.

## What she sees

1. Big text **"Hi my love"** with a beating heart
2. A big **"Press OK"** button
3. A surprise love message
4. A cute photo frame with **floating hearts**
5. Soft **music** starts when she presses OK, with a toggle button
   (top-right corner)

## How to customize

| What                          | How to change it                                          |
| ----------------------------- | --------------------------------------------------------- |
| The love message              | Edit `LOVE_MESSAGE` at the top of `app.py`                |
| Her photo                     | Drop `my_love.jpg` (or `.png`) next to `app.py`           |
| The soft music                | Drop `music.mp3` next to `app.py`                         |
| Colors / sizes / animations   | The CSS block inside `build_html()` in `app.py`           |

Every change is clearly marked in the code with comments.

## How to share it online (Streamlit Cloud, free)

Works even when your PC is off — it runs in the cloud 24/7.

1. **Add her photo & music first** (so the cloud has them):
   drop `my_love.jpg` and `music.mp3` in this folder.

2. **Put this folder on GitHub** (public repo — she gets the link later):
   ```
   git init
   git add .
   git commit -m "For You <3"
   gh repo create for-you --public --source . --push
   ```

3. **Deploy:** go to https://share.streamlit.io, sign in with GitHub,
   click **Create app**, pick the repo, set Main file to `app.py`,
   and click **Deploy**.

4. Streamlit gives you a public link like
   `https://for-you-username.streamlit.app` — send that to her.

Small note: free Streamlit Cloud apps fall asleep after inactivity, but
wake up automatically when she opens the link, so no one will notice.
