import { useEffect, useRef } from 'react';
import './Charts.css';

function EnergyChart({ results }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current || !results) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    ctx.clearRect(0, 0, width, height);

    const data = [
      { label: 'Input', value: -results.energyRequired, color: '#f44336' },
      { label: 'Output', value: results.totalEnergyOutput, color: '#4caf50' },
      { label: 'Net', value: results.netEnergyBalance, color: results.netEnergyBalance >= 0 ? '#4caf50' : '#f44336' }
    ];

    const margin = 60;
    const chartWidth = width - 2 * margin;
    const chartHeight = height - 2 * margin;
    const barWidth = chartWidth / (data.length * 2);
    const maxValue = Math.max(...data.map(d => Math.abs(d.value)));

    data.forEach((item, i) => {
      const barHeight = (Math.abs(item.value) / maxValue) * (chartHeight - 40);
      const x = margin + (i * 2 + 0.5) * barWidth;
      const y = item.value >= 0 ? height - margin - barHeight : height - margin;

      ctx.fillStyle = item.color;
      ctx.fillRect(x, y, barWidth, barHeight);

      ctx.fillStyle = '#333';
      ctx.font = '14px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(item.label, x + barWidth / 2, height - margin + 25);

      ctx.fillText(
        item.value.toFixed(1),
        x + barWidth / 2,
        item.value >= 0 ? y - 10 : y + barHeight + 20
      );
    });

    ctx.strokeStyle = '#ddd';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(margin, height - margin);
    ctx.lineTo(width - margin, height - margin);
    ctx.stroke();
  }, [results]);

  return (
    <div className="chart-container">
      <canvas ref={canvasRef} width={500} height={300} />
    </div>
  );
}

export default EnergyChart;
