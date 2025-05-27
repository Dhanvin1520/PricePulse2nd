import { useState } from 'react';
import axios from 'axios';
import PriceChart from './PriceChart';

function PriceTracker() {
  const backendUrl = 'https://pricepulse-backend-odjv.onrender.com';

  const [url, setUrl] = useState('');
  const [targetPrice, setTargetPrice] = useState('');
  const [email, setEmail] = useState('');
  const [product, setProduct] = useState(null);
  const [error, setError] = useState('');
  const [prices, setPrices] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await axios.post(`${backendUrl}/api/track`, {
        url,
        target_price: targetPrice,
        email,
      });
      setProduct(response.data);
      const pricesResponse = await axios.get(`${backendUrl}/api/prices/${encodeURIComponent(url)}`);
      setPrices(pricesResponse.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Something went wrong');
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-lg">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Amazon Product URL</label>
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter Amazon product URL"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Target Price (₹)</label>
          <input
            type="number"
            value={targetPrice}
            onChange={(e) => setTargetPrice(e.target.value)}
            className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Notify me when price drops below"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Your Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your email for alerts"
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700 transition"
        >
          Start Tracking
        </button>
      </form>
      {error && <p className="mt-4 text-red-500">{error}</p>}
      {product && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold">{product.name}</h2>
          <p className="text-lg">Current Price: ₹{product.price}</p>
          <img src={product.image} alt={product.name} className="w-full h-48 object-contain mt-4" />
          <a href={product.url} className="text-blue-600 hover:underline">View Product</a>
          {targetPrice && email && (
            <p className="mt-2 text-green-600">Alert scheduled for price below ₹{targetPrice}</p>
          )}
          <PriceChart prices={prices} />
        </div>
      )}
    </div>
  );
}

export default PriceTracker;
