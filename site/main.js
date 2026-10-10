const switcher = document.querySelector('.client-switch');
const clients = [...document.querySelectorAll('[data-client]')];
const status = document.getElementById('copy-status');
function selectClient(name) {
  status.textContent = '';
  for (const button of clients) {
    const selected = button.dataset.client === name;
    button.setAttribute('aria-pressed', String(selected));
    document.getElementById(button.getAttribute('aria-controls')).hidden = !selected;
  }
}
if (switcher && clients.length) {
  switcher.hidden = false;
  selectClient('codex');
  for (const button of clients) button.addEventListener('click', () => selectClient(button.dataset.client));
}
for (const button of document.querySelectorAll('[data-copy]')) {
  const label = button.getAttribute('aria-label');
  let feedbackTimer;
  button.hidden = false;
  button.addEventListener('click', async () => {
    const code = document.getElementById(button.dataset.copy);
    const feedback = document.getElementById(button.dataset.status) || status;
    if (button.dataset.busy) return;
    button.dataset.busy = 'true';
    window.clearTimeout(feedbackTimer);
    button.textContent = 'Copy';
    button.setAttribute('aria-label', label);
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(code.textContent);
      feedback.textContent = 'Copied. Paste into ' + button.dataset.destination + '.';
      button.textContent = 'Copied';
      button.setAttribute('aria-label', label.replace(/^Copy /, 'Copied '));
      feedbackTimer = window.setTimeout(() => {
        button.textContent = 'Copy';
        button.setAttribute('aria-label', label);
      }, 1500);
    } catch {
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(code);
      selection.removeAllRanges();
      selection.addRange(range);
      feedback.textContent = 'Copy was unavailable. The text is selected; use your device’s copy command.';
    } finally {
      delete button.dataset.busy;
    }
  });
}
