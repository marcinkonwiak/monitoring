document.querySelectorAll('.card').forEach(card => {
    const randomDegree = Math.floor(Math.random() * 360);
    const randomColor1 = 'rgba(0, 0, 0, 0.5)';

    let randomColor2;
    do {
        const red = Math.floor(Math.random() * 256);
        const green = Math.floor(Math.random() * 256);
        const blue = Math.floor(Math.random() * 256);
        const brightness = (red * 0.299 + green * 0.587 + blue * 0.114);
        if (brightness > 100) { // Threshold for brightness
            randomColor2 = `rgba(${red}, ${green}, ${blue}, 0.3)`;
        }
    } while (!randomColor2);

    const randomSpacing = Math.floor(Math.random() * 20) + 5;

    card.addEventListener('mouseenter', () => {
        card.style.background = `repeating-linear-gradient(
            ${randomDegree}deg,
            ${randomColor1},
            ${randomColor2} ${randomSpacing}px,
            transparent ${randomSpacing}px,
            transparent ${randomSpacing * 2}px
        )`;
    });

    card.addEventListener('mouseleave', () => {
        card.style.background = 'none';
    });
});
