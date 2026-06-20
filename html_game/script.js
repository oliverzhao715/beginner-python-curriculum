const startBtn = document.getElementById('startBtn');
const scoreEl = document.getElementById('score');
const timeEl = document.getElementById('time');
const gameArea = document.getElementById('gameArea');
const message = document.getElementById('message');

let score = 0;
let timeLeft = 30;
let spawnInterval = 1000; // ms
let timerId = null;
let spawnId = null;

function randomPosition(size) {
  const rect = gameArea.getBoundingClientRect();
  const x = Math.random() * (rect.width - size);
  const y = Math.random() * (rect.height - size);
  return { x, y };
}

function spawnTarget() {
  gameArea.innerHTML = '';
  const target = document.createElement('div');
  target.className = 'target';
  const size = Math.max(40, 60 - Math.floor(score/5));
  target.style.width = size + 'px';
  target.style.height = size + 'px';
  target.textContent = '';
  const pos = randomPosition(size);
  target.style.left = pos.x + 'px';
  target.style.top = pos.y + 'px';
  target.addEventListener('click', () => {
    score += 1;
    scoreEl.textContent = score;
    // speed up slightly
    clearInterval(spawnId);
    spawnInterval = Math.max(350, spawnInterval - 30);
    spawnId = setInterval(spawnTarget, spawnInterval);
    spawnTarget();
  });
  gameArea.appendChild(target);
}

function startGame(){
  score = 0;
  timeLeft = 30;
  spawnInterval = 1000;
  scoreEl.textContent = score;
  timeEl.textContent = timeLeft;
  message.textContent = '';
  startBtn.disabled = true;

  spawnTarget();
  spawnId = setInterval(spawnTarget, spawnInterval);

  timerId = setInterval(()=>{
    timeLeft -= 1;
    timeEl.textContent = timeLeft;
    if(timeLeft <= 0){
      endGame();
    }
  }, 1000);
}

function endGame(){
  clearInterval(timerId);
  clearInterval(spawnId);
  startBtn.disabled = false;
  gameArea.innerHTML = '';
  message.textContent = `Game over! Your score: ${score}. Click Start to play again.`;
}

startBtn.addEventListener('click', startGame);
