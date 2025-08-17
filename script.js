let board = Array(9).fill('');
let currentPlayer = 'X';
let gameActive = false;
let aiMode = false;
let score = { X: 0, O: 0, Tie: 0 };

const boardDiv = document.getElementById('board');
const statusDiv = document.getElementById('status');
const scoreDiv = document.getElementById('score');
const container = document.getElementById('game-container');

// Sound Effects
const winSound = new Audio('assets/click.mp3');
const winSound = new Audio('assets/win.mp3');
const drawSound = new Audio('assets/draw.mp3');
const lossSound = new Audio('assets/loss.mp3');
const aiWinMusic = new Audio('assets/aiwin.mp3');

// Rotating background music
const musicTracks = [
  new Audio('assets/bg1.mp3'),
  new Audio('assets/bg2.mp3'),
  new Audio('assets/bg3.mp3'),
  new Audio('assets/bg4.mp3'),
  new Audio('assets/bg5.mp3')
];
let currentMusicIndex = 0;
musicTracks.forEach(track => track.loop = true);

function startMusic() {
  musicTracks[currentMusicIndex].play();
  document.getElementById('start-btn').style.display = 'none';
}

function startGame(isAI) {
  aiMode = isAI;
  container.style.display = 'block';
  document.querySelector('.mode-select').style.display = 'none';
  disableModeButtons();
  resetGame();
}

function disableModeButtons() {
  document.querySelectorAll('.mode-select button').forEach(btn => {
    btn.disabled = true;
    btn.style.opacity = '0.6';
    btn.style.cursor = 'not-allowed';
  });
}

function createBoard() {
  boardDiv.innerHTML = '';
  board.forEach((val, i) => {
    const cell = document.createElement('div');
    cell.className = 'cell';
    cell.dataset.index = i;
    cell.innerText = val === 'X' ? '❌' : val === 'O' ? '🟢' : '';
    cell.onclick = () => handleMove(i);
    boardDiv.appendChild(cell);
  });
}

function handleMove(i) {
  if (board[i] || !gameActive) return;

  board[i] = currentPlayer;
  clickSound.play();
  updateUI();

  const winCombo = checkWin(currentPlayer);
  if (winCombo) {
    statusDiv.innerText = `🎉 Player ${currentPlayer === 'X' ? '❌' : '🟢'} wins!`;
    score[currentPlayer]++;
    gameActive = false;
    updateScore();
    disableBoard();
    highlightWinningCells(winCombo);

    if (aiMode && currentPlayer === 'O') {
      lossSound.play();
      aiWinMusic.play();
    } else {
      winSound.play();
    }

    stopMusic();
    document.getElementById('restart-container').style.display = 'block';
    return;
  }

  if (!board.includes('')) {
    statusDiv.innerText = `🤝 It's a Tie!`;
    score.Tie++;
    gameActive = false;
    updateScore();
    disableBoard();
    drawSound.play();
    stopMusic();
    document.getElementById('restart-container').style.display = 'block';
    return;
  }

  currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
  statusDiv.innerText = `Player ${currentPlayer === 'X' ? '❌' : '🟢'}'s turn`;

  if (aiMode && currentPlayer === 'O') {
    setTimeout(() => {
      const aiMove = getBestMove('O');
      handleMove(aiMove);
    }, 300);
  }
}

function updateUI() {
  createBoard();
}

function disableBoard() {
  document.querySelectorAll('.cell').forEach(cell => {
    cell.style.pointerEvents = 'none';
    cell.style.opacity = '0.5';
  });
}

function enableBoard() {
  document.querySelectorAll('.cell').forEach(cell => {
    cell.style.pointerEvents = 'auto';
    cell.style.opacity = '1';
  });
}

function updateScore() {
  scoreDiv.innerText = `❌ X: ${score.X}    🟢 O: ${score.O}    🤝 Ties: ${score.Tie}`;
}

function resetGame() {
  board = Array(9).fill('');
  currentPlayer = 'X';
  gameActive = true;
  statusDiv.innerText = `Player ❌'s turn`;
  updateUI();
  enableBoard();
  document.getElementById('restart-container').style.display = 'none';

  // Stop current track
  musicTracks[currentMusicIndex].pause();
  musicTracks[currentMusicIndex].currentTime = 0;

  // Switch to next music
  currentMusicIndex = (currentMusicIndex + 1) % musicTracks.length;
  musicTracks[currentMusicIndex].play();
}

function stopMusic() {
  musicTracks[currentMusicIndex].pause();
  musicTracks[currentMusicIndex].currentTime = 0;
}

function checkWin(player) {
  const wins = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
  ];
  return wins.find(combo => combo.every(i => board[i] === player));
}

function getBestMove(player) {
  const opponent = player === 'X' ? 'O' : 'X';

  const minimax = (newBoard, current) => {
    const avail = newBoard.map((val, i) => val === '' ? i : null).filter(v => v !== null);

    if (checkStaticWin(newBoard, opponent)) return { score: -1 };
    if (checkStaticWin(newBoard, player)) return { score: 1 };
    if (avail.length === 0) return { score: 0 };

    const moves = [];

    for (let i of avail) {
      let move = {};
      move.index = i;
      newBoard[i] = current;

      let result = minimax(newBoard, current === player ? opponent : player);
      move.score = result.score;

      newBoard[i] = '';
      moves.push(move);
    }

    let bestMove;
    if (current === player) {
      let bestScore = -Infinity;
      for (let m of moves) {
        if (m.score > bestScore) {
          bestScore = m.score;
          bestMove = m;
        }
      }
    } else {
      let bestScore = Infinity;
      for (let m of moves) {
        if (m.score < bestScore) {
          bestScore = m.score;
          bestMove = m;
        }
      }
    }

    return bestMove;
  };

  return minimax([...board], player).index;
}

function checkStaticWin(b, player) {
  const wins = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
  ];
  return wins.some(combo => combo.every(i => b[i] === player));
}

function highlightWinningCells(combo) {
  combo.forEach(i => {
    const cell = document.querySelector(`.cell[data-index='${i}']`);
    cell.style.backgroundColor = currentPlayer === 'X' ? '#ffcccc' : '#ccffcc';
  });
}

