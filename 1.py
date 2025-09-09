import streamlit as st
import streamlit.components.v1 as components

st.title("⚽ 手機觸控足球遊戲 + 障礙物 + 血量系統")

game_html = """
<!DOCTYPE html>
<html>
<head>
  <style>
    body { background: #87CEEB; display: flex; justify-content: center; }
    #game {
      width: 400px;
      height: 500px;
      background: #e0f7fa;
      border: 4px solid #000;
      position: relative;
      overflow: hidden;
      touch-action: none;
    }
    #ball {
      width: 40px;
      height: 40px;
      background: black;
      border-radius: 50%;
      position: absolute;
      bottom: 20px;
      left: 180px;
    }
    #goal {
      width: 100px;
      height: 60px;
      border: 4px solid red;
      position: absolute;
      top: 50px;
      left: 150px;
      border-bottom: none;
    }
    #obstacle {
      width: 80px;
      height: 20px;
      background: brown;
      position: absolute;
      top: 200px;
      left: 0px;
    }
    .falling {
      width: 30px;
      height: 30px;
      background: gray;
      border-radius: 50%;
      position: absolute;
      top: -30px;
    }
    #scoreBoard, #timeBoard, #hpBoard {
      position: absolute;
      font-size: 18px;
      font-weight: bold;
      color: black;
    }
    #scoreBoard { top: 10px; left: 10px; }
    #timeBoard { top: 10px; right: 10px; }
    #hpBoard { bottom: 10px; left: 10px; }
  </style>
</head>
<body>
  <div id="game">
    <div id="scoreBoard">分數: 0</div>
    <div id="timeBoard">時間: 60</div>
    <div id="hpBoard">HP: ❤️❤️❤️</div>
    <div id="ball"></div>
    <div id="goal"></div>
    <div id="obstacle"></div>
  </div>

  <script>
    const game = document.getElementById("game");
    const ball = document.getElementById("ball");
    const goal = document.getElementById("goal");
    const obstacle = document.getElementById("obstacle");
    const scoreBoard = document.getElementById("scoreBoard");
    const timeBoard = document.getElementById("timeBoard");
    const hpBoard = document.getElementById("hpBoard");

    let ballX = 180, ballY = 20, velocityY = 0, gravity = -0.4;
    let score = 0, timeLeft = 60, gameActive = true;
    let hp = 3;

    let goalX = 150, goalY = 50, goalWidth = 100, goalHeight = 60;
    let dx = 3, dy = 2;

    let obsX = 0, obsY = 200, obsWidth = 80, obsHeight = 20;
    let obsDx = 4;

    let fallingObstacles = [];

    // 點擊跳躍
    document.body.addEventListener("click", () => {
      if(gameActive) velocityY = 8;
    });

    // 滑動移動
    let startX = null;
    document.body.addEventListener("touchstart", (e) => { startX = e.touches[0].clientX; });
    document.body.addEventListener("touchmove", (e) => {
      if (startX !== null) {
        let deltaX = e.touches[0].clientX - startX;
        ballX += deltaX;
        if(ballX < 0) ballX = 0;
        if(ballX > 360) ballX = 360;
        ball.style.left = ballX + "px";
        startX = e.touches[0].clientX;
      }
    });
    document.body.addEventListener("touchend", () => { startX = null; });

    function resetBall() {
      ballX = 180;
      ballY = 20;
      velocityY = 0;
      ball.style.left = ballX + "px";
      ball.style.bottom = ballY + "px";
    }

    function loseHP() {
      hp--;
      let hearts = "❤️".repeat(hp);
      hpBoard.innerText = "HP: " + (hearts || "💀");
      if (hp <= 0) {
        gameActive = false;
        alert("💀 遊戲結束！\\n你的分數是: " + score);
        location.reload();
      } else {
        resetBall();
      }
    }

    function spawnFallingObstacle() {
      if(!gameActive) return;
      let obs = document.createElement("div");
      obs.classList.add("falling");
      obs.style.left = Math.floor(Math.random() * 370) + "px";
      obs.style.top = "-30px";
      game.appendChild(obs);
      fallingObstacles.push(obs);
    }

    function gameLoop() {
      if(!gameActive) return;

      // 球移動
      ballY += velocityY;
      velocityY += gravity;
      if(ballY < 0){ ballY = 0; velocityY = 0; }
      ball.style.bottom = ballY + "px";
      ball.style.left = ballX + "px";

      // 球門移動
      goalX += dx; goalY += dy;
      if(goalX <= 0 || goalX + goalWidth >= 400) dx *= -1;
      if(goalY <= 30 || goalY + goalHeight >= 250) dy *= -1;
      goal.style.left = goalX + "px";
      goal.style.top = goalY + "px";

      // 障礙物移動
      obsX += obsDx;
      if(obsX <= 0 || obsX + obsWidth >= 400) obsDx *= -1;
      obstacle.style.left = obsX + "px";
      obstacle.style.top = obsY + "px";

      let ballRect = ball.getBoundingClientRect();
      let goalRect = goal.getBoundingClientRect();
      let obsRect = obstacle.getBoundingClientRect();

      // 撞到橫向障礙物
      if (
        ballRect.bottom >= obsRect.top &&
        ballRect.top <= obsRect.bottom &&
        ballRect.left + 20 >= obsRect.left &&
        ballRect.right - 20 <= obsRect.right
      ) {
        loseHP();
      }

      // 更新掉落障礙物
      for (let i = 0; i < fallingObstacles.length; i++) {
        let fo = fallingObstacles[i];
        let top = parseInt(fo.style.top);
        fo.style.top = (top + 5) + "px";

        let foRect = fo.getBoundingClientRect();
        if (
          ballRect.bottom >= foRect.top &&
          ballRect.top <= foRect.bottom &&
          ballRect.left + 20 >= foRect.left &&
          ballRect.right - 20 <= foRect.right
        ) {
          loseHP();
          fo.remove();
          fallingObstacles.splice(i, 1);
          i--;
        }

        if (top > 500) {
          fo.remove();
          fallingObstacles.splice(i, 1);
          i--;
        }
      }

      // 進球判斷
      if (
        ballRect.bottom >= goalRect.top &&
        ballRect.top <= goalRect.bottom &&
        ballRect.left + 20 >= goalRect.left &&
        ballRect.right - 20 <= goalRect.right
      ) {
        score++;
        scoreBoard.innerText = "分數: " + score;
        resetBall();
        if(score % 3 === 0){ dx *= 1.2; dy *= 1.2; obsDx *= 1.2; }
      }
    }

    function startTimer() {
      const timer = setInterval(() => {
        if(!gameActive) { clearInterval(timer); return; }
        timeLeft--;
        timeBoard.innerText = "時間: " + timeLeft;
        if(timeLeft <= 0){
          gameActive = false;
          alert("⏱️ 遊戲結束！\\n你的分數是: " + score);
          location.reload();
        }
      }, 1000);

      // 每 2 秒掉一個石頭
      setInterval(spawnFallingObstacle, 2000);
    }

    setInterval(gameLoop, 30);
    startTimer();
  </script>
</body>
</html>
"""

components.html(game_html, height=550)
