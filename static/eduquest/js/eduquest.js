// Небольшие интерактивные эффекты EduQuest без тяжелых фронтенд-фреймворков.
(function () {
    function drawMiniChart(canvas) {
        const context = canvas.getContext('2d');
        const width = canvas.clientWidth;
        const height = canvas.clientHeight;
        canvas.width = width;
        canvas.height = height;

        const points = Number(canvas.dataset.points || 0);
        const solved = Number(canvas.dataset.solved || 0);
        const bars = [Math.max(points, 8), Math.max(solved * 30, 8), 80];
        const colors = ['#1f8a5b', '#2f80ed', '#d69b1f'];

        context.clearRect(0, 0, width, height);
        bars.forEach(function (value, index) {
            const barWidth = width / 5;
            const x = 30 + index * (barWidth + 28);
            const barHeight = Math.min(height - 42, value);
            context.fillStyle = colors[index];
            context.roundRect(x, height - barHeight - 24, barWidth, barHeight, 10);
            context.fill();
        });
    }

    function drawWorldChart(canvas) {
        const context = canvas.getContext('2d');
        const width = canvas.clientWidth;
        const height = canvas.clientHeight;
        canvas.width = width;
        canvas.height = height;

        const raw = canvas.dataset.worlds || '';
        const values = raw ? raw.split(',').map(function (item) {
            const parts = item.split(':');
            return { label: parts[0], value: Number(parts[1] || 0) };
        }) : [];

        context.clearRect(0, 0, width, height);
        context.strokeStyle = '#d8e4de';
        context.lineWidth = 2;
        context.beginPath();
        context.moveTo(24, height - 28);
        context.lineTo(width - 18, height - 28);
        context.stroke();

        values.forEach(function (item, index) {
            const x = 44 + index * 100;
            const barHeight = Math.max(10, Math.min(height - 62, item.value));
            context.fillStyle = ['#1f8a5b', '#7c4dff', '#2f80ed'][index % 3];
            context.roundRect(x, height - barHeight - 30, 54, barHeight, 8);
            context.fill();
            context.fillStyle = '#66736f';
            context.font = '12px Arial';
            context.fillText(item.label, x - 2, height - 8);
        });
    }

    document.querySelectorAll('.mini-chart').forEach(drawMiniChart);
    document.querySelectorAll('.world-chart').forEach(drawWorldChart);

    document.querySelectorAll('.quest-card, .world-card').forEach(function (card) {
        card.addEventListener('mousemove', function (event) {
            const rect = card.getBoundingClientRect();
            const x = (event.clientX - rect.left) / rect.width - 0.5;
            const y = (event.clientY - rect.top) / rect.height - 0.5;
            card.style.transform = 'translateY(-3px) rotateX(' + (-y * 2) + 'deg) rotateY(' + (x * 2) + 'deg)';
        });
        card.addEventListener('mouseleave', function () {
            card.style.transform = '';
        });
    });

    const resetForm = document.querySelector('[data-reset-form]');
    if (resetForm) {
        resetForm.addEventListener('submit', function (event) {
            const confirmed = window.confirm('Сбросить весь прогресс, баллы и историю решений? Это действие нельзя отменить.');
            if (!confirmed) {
                event.preventDefault();
            }
        });
    }
}());
