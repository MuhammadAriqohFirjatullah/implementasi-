const form = document.getElementById('feedbackForm');
const resultIcon = document.getElementById('resultIcon');
const resultTitle = document.getElementById('resultTitle');
const resultText = document.getElementById('resultText');
const resultDetails = document.getElementById('resultDetails');
const themeToggle = document.getElementById('themeToggle');

// Memberi umpan balik setelah pengguna mengirim formulir.
form.addEventListener('submit', function (event) {
  event.preventDefault();

  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }

  const formData = new FormData(form);
  const name = formData.get('name').trim();
  const rating = formData.get('rating');
  const comment = formData.get('comment').trim();

  resultIcon.textContent = '✓';
  resultTitle.textContent = `Terima kasih, ${name}!`;
  resultText.textContent = 'Umpan balik Anda berhasil diproses dalam demo ini.';
  resultDetails.hidden = false;
  resultDetails.replaceChildren();

  const ratingLine = document.createElement('p');
  ratingLine.textContent = `Penilaian: ${rating}`;
  resultDetails.appendChild(ratingLine);

  if (comment) {
    const commentLine = document.createElement('p');
    commentLine.textContent = `Saran: ${comment}`;
    resultDetails.appendChild(commentLine);
  }

  resultDetails.setAttribute('role', 'status');
});

// Memberi pengguna kontrol untuk memilih tampilan terang atau gelap.
themeToggle.addEventListener('click', function () {
  const isDark = document.body.classList.toggle('dark');
  themeToggle.textContent = isDark ? '☀️ Mode terang' : '🌙 Mode gelap';
  themeToggle.setAttribute('aria-pressed', String(isDark));
});
