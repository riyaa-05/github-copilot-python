// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const SCORES_STORAGE_KEY = 'sudokuTopScores';
const THEME_STORAGE_KEY = 'sudokuTheme';
const MAX_SCORES = 10;
const DIFFICULTY_SETTINGS = {
  easy: { clues: 45, rank: 1 },
  medium: { clues: 35, rank: 2 },
  hard: { clues: 25, rank: 3 }
};
let puzzle = [];
let gameStartedAt = null;
let gameDifficulty = 'medium';
let hintsUsed = 0;
let gameCompleted = false;
let timerId = null;
let elapsedSeconds = 0;

function loadScores() {
  try {
    const scores = JSON.parse(localStorage.getItem(SCORES_STORAGE_KEY) || '[]');
    return Array.isArray(scores) ? scores : [];
  } catch (error) {
    console.error('Unable to load Sudoku scores.', error);
    return [];
  }
}

function scoreSort(a, b) {
  return a.completionTime - b.completionTime
    || a.hintsUsed - b.hintsUsed
    || b.difficultyRank - a.difficultyRank;
}

function saveScore(score) {
  const scores = loadScores();
  scores.push(score);
  scores.sort(scoreSort);
  const topScores = scores.slice(0, MAX_SCORES);
  try {
    localStorage.setItem(SCORES_STORAGE_KEY, JSON.stringify(topScores));
  } catch (error) {
    console.error('Unable to save Sudoku score.', error);
  }
  renderScores(topScores);
}

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = (seconds % 60).toFixed(1).padStart(4, '0');
  return `${minutes}:${remainingSeconds}`;
}

function updateTimer() {
  const timer = document.getElementById('timer');
  if (timer) timer.textContent = formatTime(elapsedSeconds);
}

function stopTimer() {
  if (timerId !== null) {
    window.clearInterval(timerId);
    timerId = null;
  }
}

function startTimer() {
  stopTimer();
  elapsedSeconds = 0;
  updateTimer();
  const startedAt = performance.now();
  timerId = window.setInterval(() => {
    elapsedSeconds = (performance.now() - startedAt) / 1000;
    updateTimer();
  }, 100);
}

function setTheme(theme) {
  const isDark = theme === 'dark';
  document.body.classList.toggle('dark-mode', isDark);
  const toggle = document.getElementById('theme-toggle');
  if (toggle) {
    toggle.setAttribute('aria-pressed', String(isDark));
    toggle.textContent = isDark ? 'Light mode' : 'Dark mode';
  }
  try {
    localStorage.setItem(THEME_STORAGE_KEY, isDark ? 'dark' : 'light');
  } catch (error) {
    console.error('Unable to save Sudoku theme.', error);
  }
}

function initializeTheme() {
  let theme = 'light';
  try {
    theme = localStorage.getItem(THEME_STORAGE_KEY) || 'light';
  } catch (error) {
    console.error('Unable to load Sudoku theme.', error);
  }
  setTheme(theme);
}

function renderScores(scores = loadScores()) {
  const body = document.getElementById('scores-body');
  const emptyMessage = document.getElementById('no-scores');
  if (!body || !emptyMessage) return;

  body.innerHTML = '';
  emptyMessage.hidden = scores.length > 0;
  scores.forEach((score, index) => {
    const row = document.createElement('tr');
    [index + 1, score.playerName, formatTime(score.completionTime),
      score.difficulty, score.hintsUsed].forEach((value) => {
      const cell = document.createElement('td');
      cell.textContent = value;
      row.appendChild(cell);
    });
    body.appendChild(row);
  });
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    rowDiv.setAttribute('role', 'row');
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.inputMode = 'numeric';
      input.autocomplete = 'off';
      input.setAttribute('aria-label', `Row ${i + 1}, column ${j + 1}`);
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
      });
      input.addEventListener('keydown', (event) => {
        const direction = {
          ArrowUp: [-1, 0],
          ArrowDown: [1, 0],
          ArrowLeft: [0, -1],
          ArrowRight: [0, 1]
        }[event.key];
        if (!direction) return;

        const nextRow = i + direction[0];
        const nextCol = j + direction[1];
        if (nextRow < 0 || nextRow >= SIZE || nextCol < 0 || nextCol >= SIZE) return;
        event.preventDefault();
        boardDiv.querySelector(
          `.sudoku-cell[data-row="${nextRow}"][data-col="${nextCol}"]`
        ).focus();
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

function updateGameStatus() {
  const indicator = document.getElementById('difficulty-indicator');
  const count = document.getElementById('hint-count');
  if (indicator) {
    indicator.textContent = `${gameDifficulty[0].toUpperCase()}${gameDifficulty.slice(1)} puzzle`;
  }
  if (count) count.textContent = hintsUsed;
}

async function newGame() {
  const difficulty = document.getElementById('difficulty').value;
  const settings = DIFFICULTY_SETTINGS[difficulty];
  const msg = document.getElementById('message');
  try {
    const res = await fetch(`/new?clues=${settings.clues}`);
    const data = await res.json();
    if (!res.ok || !data.puzzle) throw new Error(data.error || 'Unable to start a new game.');
    renderPuzzle(data.puzzle);
    gameDifficulty = difficulty;
    gameStartedAt = performance.now();
    hintsUsed = 0;
    gameCompleted = false;
    startTimer();
    updateGameStatus();
    document.getElementById('hint').disabled = false;
    msg.textContent = '';
  } catch (error) {
    console.error('Unable to start Sudoku game.', error);
    msg.textContent = error.message;
  }
}

async function requestHint() {
  if (gameCompleted) return;
  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  const board = Array.from({length: SIZE}, (_, row) =>
    Array.from({length: SIZE}, (_, col) => {
      const value = inputs[row * SIZE + col].value;
      return value ? parseInt(value, 10) : 0;
    })
  );
  const msg = document.getElementById('message');
  try {
    const res = await fetch('/hint', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({board})
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Unable to provide a hint.');
    const input = inputs[data.row * SIZE + data.col];
    input.value = data.value;
    input.disabled = true;
    input.className = 'sudoku-cell hinted';
    hintsUsed += 1;
    updateGameStatus();
    msg.style.color = '';
    msg.textContent = 'One correct cell was filled in for you.';
    if (!Array.from(inputs).some((cell) => !cell.value)) {
      await checkSolution();
    }
  } catch (error) {
    console.error('Unable to get Sudoku hint.', error);
    msg.style.color = '#d32f2f';
    msg.textContent = error.message;
  }
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const msg = document.getElementById('message');
  let data;
  try {
    const res = await fetch('/check', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({board})
    });
    data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Unable to check the puzzle.');
  } catch (error) {
    console.error('Unable to check Sudoku solution.', error);
    msg.style.color = '#d32f2f';
    msg.textContent = error.message;
    return;
  }
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.textContent = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled && !inp.classList.contains('hinted')) continue;
    inp.classList.remove('incorrect');
    if (incorrect.has(idx)) {
      inp.classList.add('incorrect');
    }
  }
  if (incorrect.size === 0) {
    const hasEmptyCells = Array.from(inputs).some((input) => !input.value);
    if (hasEmptyCells) {
      msg.style.color = '';
      msg.textContent = 'No incorrect entries. Keep going!';
    } else {
      msg.style.color = '#388e3c';
      msg.textContent = `Congratulations! You solved it in ${formatTime(elapsedSeconds)}.`;
    }
    if (!hasEmptyCells && !gameCompleted && gameStartedAt !== null) {
      stopTimer();
      const settings = DIFFICULTY_SETTINGS[gameDifficulty];
      saveScore({
        playerName: document.getElementById('player-name').value.trim() || 'Anonymous',
        completionTime: elapsedSeconds,
        difficulty: gameDifficulty,
        difficultyRank: settings.rank,
        hintsUsed
      });
      gameCompleted = true;
      document.getElementById('hint').disabled = true;
    }
  } else {
    msg.style.color = '#d32f2f';
    msg.textContent = 'Some cells are incorrect.';
  }
}

// Wire buttons
window.addEventListener('load', () => {
  initializeTheme();
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('hint').addEventListener('click', requestHint);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('theme-toggle').addEventListener('click', () => {
    setTheme(document.body.classList.contains('dark-mode') ? 'light' : 'dark');
  });
  document.getElementById('difficulty').addEventListener('change', updateGameStatus);
  renderScores();
  // initialize
  newGame();
});