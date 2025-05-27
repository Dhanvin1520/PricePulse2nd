import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function PriceChart({ prices }) {
  const data = {
    labels: prices.map(p => new Date(p.timestamp).toLocaleString()),
    datasets: [
      {
        label: 'Price (₹)',
        data: prices.map(p => p.price),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Price Trend' }
    }
  };

  return <div className="mt-6">{prices.length > 0 && <Line data={data} options={options} />}</div>;
}

export default PriceChart;