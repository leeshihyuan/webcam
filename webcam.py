# app.py
from flask import Flask, Response

app = Flask(__name__)

HTML = """<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Webcam 即時預覽</title>
  <style>
    body { margin: 0; font-family: system-ui, -apple-system, "Segoe UI", Roboto; background:#0b0f14; color:#e6e6e6; }
    header { padding: 16px 24px; font-weight: 600; }
    main { display:flex; justify-content:center; align-items:center; padding:24px; }
    .panel { width:min(960px, 95vw); }
    video { width:100%; max-height:80vh; border-radius:16px; background:#000; }
    .controls { margin-top:12px; display:flex; gap:8px; flex-wrap:wrap; }
    button, select { padding:8px 12px; border-radius:10px; border:1px solid #2a3441; background:#121822; color:#e6e6e6; }
    .note { opacity:.8; font-size:14px; margin-top:8px; }
  </style>
</head>
<body>
  <header>YOLO Cat Webcam 即時預覽（本機 getUserMedia）</header>
  <main>
    <div class="panel">
      <video id="video" autoplay playsinline muted></video>
      <div class="controls">
        <select id="deviceSelect" title="選擇攝影機"></select>
        <button id="startBtn">開始</button>
        <button id="stopBtn">停止</button>
      </div>
      <div class="note">
        提示：首次使用 Yolo Cat Webcam 會跳出權限詢問。需在 <b>localhost</b> 或 <b>HTTPS</b> 網域才能開啟鏡頭。
      </div>
    </div>
  </main>
  <script>
    const video = document.getElementById('video');
    const deviceSelect = document.getElementById('deviceSelect');
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    let currentStream = null;

    async function listCameras() {
      const devices = await navigator.mediaDevices.enumerateDevices();
      const cams = devices.filter(d => d.kind === 'videoinput');
      deviceSelect.innerHTML = '';
      cams.forEach((cam, idx) => {
        const opt = document.createElement('option');
        opt.value = cam.deviceId;
        opt.textContent = cam.label || `攝影機 ${idx+1}`;
        deviceSelect.appendChild(opt);
      });
    }

    async function start() {
      try {
        if (currentStream) stop();
        const constraints = {
          video: deviceSelect.value ? { deviceId: { exact: deviceSelect.value } } : { width: { ideal: 1280 }, height: { ideal: 720 } },
          audio: false
        };
        currentStream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = currentStream;
      } catch (err) {
        alert('開啟攝影機失敗：' + err);
        console.error(err);
      }
    }

    function stop() {
      if (currentStream) {
        currentStream.getTracks().forEach(t => t.stop());
        currentStream = null;
        video.srcObject = null;
      }
    }

    startBtn.addEventListener('click', start);
    stopBtn.addEventListener('click', stop);

    // 部分瀏覽器需要先取得一次權限，才能列出有名稱的裝置
    (async () => {
      try {
        await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      } catch(_) {}
      await listCameras();
    })();

    navigator.mediaDevices.addEventListener('devicechange', listCameras);
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return Response(HTML, mimetype="text/html")

if __name__ == "__main__":
    # 直接跑：python app.py  -> 然後打開 http://localhost:5000
    app.run(host="127.0.0.1", port=5000, debug=True)
