const hours = document.getElementById('hours');
const hoursValue = document.getElementById('hoursValue');
const score = document.getElementById('score');
const meterFill = document.getElementById('meterFill');
const resultMessage = document.getElementById('resultMessage');
const predictBtn = document.getElementById('predictBtn');

// Aturan ilustratif: nilai = 45 + (jam belajar x 7), dibatasi maksimum 100.
function predict() {
  const studyHours = Number(hours.value);
  const predictedScore = Math.min(100, 45 + (studyHours * 7));

  hoursValue.textContent = `${studyHours} jam`;
  score.textContent = predictedScore;
  meterFill.style.width = `${predictedScore}%`;
  resultMessage.textContent =
    `Dengan ${studyHours} jam belajar per hari, model simulasi memperkirakan nilai ${predictedScore} dari 100.`;
}

hours.addEventListener('input', predict);
predictBtn.addEventListener('click', predict);
predict();
