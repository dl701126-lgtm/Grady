import streamlit as st
import streamlit.components.v1 as components

st.title(🏎️ Racing games)
st.write("電腦：方向鍵或滑鼠移動 🚗｜手機：左右滑動 🚘")

game_html = """
<!DOCTYPE html>
<html>
<head>
  <style>
    body { background: #111; }
    #game {
      width: 300px;
      height: 500px;
      background: #222;
      margin: auto;
      position: relative;
      overflow: hidden;
      border: 3px solid white;
    }
    /* 護欄 */
    .barrier {
      width: 20px;
      height: 500px;
      background: gray;
      position: absolute;
      top: 0;
    }
    #leftBarrier { left: 0; }
    #rightBarrier { right: 0; }

    /* 賽道線條 */
    .lane-line {
      width: 5px;
      height: 40px;
      background: white;
      position: absolute;
      left: 150px;
      animation: moveLine 1s linear infinite;
    }
    @keyframes moveLine {
      0% { top: -40px; }
      100% { top: 500px; }
    }

    /* 車輛樣式 */
    .car {
      width: 40px;
      height: 70px;
      position: absolute;
      bottom: 20px;
      border-radius: 5px;
    }
    .car-body {
      width: 100%;
      height: 100%;
      border-radius: 8px;
      position: relative;
    }
    .window {
      width: 26px;
      height: 20px;
      background: white;
      border-radius: 3px;
      position: absolute;
      top: 8px;
      left: 7px;
    }
    .wheel {
      width: 12px;
      height: 12px;
      background: black;
      border-radius: 50%;
      position: absolute;
    }
    .wheel.left { left: -6px; }
    .wheel.right { right: -6px; }
    .wheel.top { top: 10px; }
    .wheel.bottom { bottom: 10px; }

    /* 玩家車（紅色） */
    #car .car-body { background: red; }

    /* 障礙車（藍色） */
    .obstacle .car-body { background: blue; }

    #score {
      color: white;
      font-size: 20px;
      text-align: center;
      margin-top: 10px;
    }
  </style>
</head>
<body>
  <div id="score">Score: 0</div>
  <div id="game">
    <div id="leftBarrier" class="barrier"></div>
    <div id="rightBarrier" class="barrier"></div>

    <!-- 玩家車 -->
    <div id="car" class="car" style="left:130px;">
      <div class="car-body">
        <div class="window"></div>
        <div class="wheel left top"></div>
        <div class="wheel right top"></div>
        <div class="wheel left bottom"></div>
        <div class="wheel right bottom"></div>
      </div>
    </div>
  </div>

  <script>
    const game = document.getElementById("game");
    const car = document.getElementById("car");
    const scoreDisplay = document.getElementById("score");
    const leftBarrier = document.getElementById("leftBarrier");
    const rightBarrier = document.getElementById("rightBarrier");

    let carX = 130;
    let score = 0;
    let gameOver = false;

    function moveCar(dx) {
      carX += dx;
      if (carX < 0) carX = 0;
      if (carX > 260) carX = 260;
      car.style.left = carX + "px";
      checkBarrierCollision();
    }

    function setCarX(x) {
      if (x < 0) x = 0;
      if (x > 260) x = 260;
      carX = x;
      car.style.left = carX + "px";
      checkBarrierCollision();
    }

    // 碰到護欄檢查
    function checkBarrierCollision() {
      let carRect = car.getBoundingClientRect();
      let leftRect = leftBarrier.getBoundingClientRect();
      let rightRect = rightBarrier.getBoundingClientRect();

      if (
        carRect.left <= leftRect.right ||
        carRect.right >= rightRect.left
      ) {
        gameOver = true;
        alert("🚧 撞到護欄！遊戲結束！得分：" + score);
        location.reload();
      }
    }

    // 鍵盤控制 (電腦)
    document.addEventListener("keydown", function(e) {
      if (e.key === "ArrowLeft") moveCar(-20);
      if (e.key === "ArrowRight") moveCar(20);
    });

    // 滑鼠控制 (電腦)
    game.addEventListener("mousemove", e => {
      let rect = game.getBoundingClientRect();
      let mouseX = e.clientX - rect.left;
      setCarX(mouseX - 20);
    });

    // 觸控控制 (手機)
    game.addEventListener("touchmove", e => {
      let rect = game.getBoundingClientRect();
      let touchX = e.touches[0].clientX - rect.left;
      setCarX(touchX - 20);
    });

    // 建立障礙車
    function createObstacle() {
      if (gameOver) return;
      const obs = document.createElement("div");
      obs.classList.add("car", "obstacle");
      obs.style.left = Math.floor(Math.random() * 5) * 60 + "px";
      obs.style.top = "-100px";

      // 內部藍色小車
      obs.innerHTML = `
        <div class="car-body">
          <div class="window"></div>
          <div class="wheel left top"></div>
          <div class="wheel right top"></div>
          <div class="wheel left bottom"></div>
          <div class="wheel right bottom"></div>
        </div>
      `;
      game.appendChild(obs);

      let obsInterval = setInterval(() => {
        if (gameOver) {
          clearInterval(obsInterval);
          return;
        }
        let obsTop = parseInt(obs.style.top);
        obsTop += 5;
        obs.style.top = obsTop + "px";

        // 碰撞檢測
        let carRect = car.getBoundingClientRect();
        let obsRect = obs.getBoundingClientRect();
        if (
          carRect.left < obsRect.right &&
          carRect.right > obsRect.left &&
          carRect.top < obsRect.bottom &&
          carRect.bottom > obsRect.top
        ) {
          gameOver = true;
          alert("💥 撞車啦！遊戲結束！得分：" + score);
          location.reload();
        }

        // 通過障礙物加分
        if (obsTop > 500) {
          clearInterval(obsInterval);
          obs.remove();
          score++;
          scoreDisplay.innerText = "Score: " + score;
        }
      }, 30);
    }

    setInterval(createObstacle, 1500);

    // 建立不斷移動的白線
    setInterval(() => {
      if (gameOver) return;
      const line = document.createElement("div");
      line.classList.add("lane-line");
      game.appendChild(line);
      setTimeout(() => line.remove(), 1000);
    }, 300);
  </script>
</body>
</html>
"""

components.html(game_html, height=600)
