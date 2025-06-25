function createHeart() {
    const heart = document.createElement('div');
    heart.className = 'heart';
    heart.style.left = Math.random() * 100 + 'vw';
    heart.style.animationDuration = 4 + Math.random() * 4 + 's';
    document.body.appendChild(heart);
    setTimeout(() => heart.remove(), 8000);
}

setInterval(createHeart, 500);

// Typewriter effect for the love letter
document.addEventListener('DOMContentLoaded', () => {
    const wrapper = document.querySelector('.letter-wrapper');
    const textEl = document.querySelector('.letter-text');
    if (!wrapper || !textEl) return;
    const fullText = textEl.getAttribute('data-text') || '';
    let timer;

    wrapper.addEventListener('mouseenter', () => {
        clearInterval(timer);
        textEl.textContent = '';
        textEl.style.opacity = '1';
        let i = 0;
        timer = setInterval(() => {
            textEl.textContent += fullText.charAt(i);
            i++;
            if (i >= fullText.length) {
                clearInterval(timer);
            }
        }, 60);
    });

    wrapper.addEventListener('mouseleave', () => {
        clearInterval(timer);
        textEl.textContent = '';
        textEl.style.opacity = '0';
    });
});
