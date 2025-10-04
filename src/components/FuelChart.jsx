import { useEffect, useRef } from 'react';
import './Charts.css';

function FuelChart({ results }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current || !results) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    ctx.clearRect(0, 0, width, height);

    const fuelData = Object.entries(results.fuelProduced).map(([fuel, amount]) => ({
      label: fuel.charAt(0).toUpperCase() + fuel.slice(1),
      value: amount
    }));

    const total = fuelData.reduce((sum, item) => sum + item.value, 0);
    const colors = ['#4caf50', '#2196f3', '#ff9800', '#f44336', '#9c27b0'];

    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) / 3;

    let currentAngle = -Math.PI / 2;

    fuelData.forEach((item, i) => {
      const sliceAngle = (item.value / total) * 2 * Math.PI;

      ctx.fillStyle = colors[i % colors.length];
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
      ctx.closePath();
      ctx.fill();

      const labelAngle = currentAngle + sliceAngle / 2;
      const labelX = centerX + (radius * 0.65) * Math.cos(labelAngle);
      const labelY = centerY + (radius * 0.65) * Math.sin(labelAngle);

      ctx.fillStyle = 'white';
      ctx.font = 'bold 13px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      const percentage = ((item.value / total) * 100).toFixed(1);
      ctx.fillText(`${percentage}%`, labelX, labelY);

      currentAngle += sliceAngle;
    });

    let legendY = 20;
    fuelData.forEach((item, i) => {
      ctx.fillStyle = colors[i % colors.length];
      ctx.fillRect(width - 120, legendY, 15, 15);

      ctx.fillStyle = '#333';
      ctx.font = '13px sans-serif';
      ctx.textAlign = 'left';
      const percentage = ((item.value / total) * 100).toFixed(1);
      ctx.fillText(`${item.label}: ${percentage}%`, width - 100, legendY + 12);

      legendY += 25;
    });
  }, [results]);

  return (
    <div className="chart-container">
      <canvas ref={canvasRef} width={500} height={300} />
    </div>
  );
}

export default FuelChart;
