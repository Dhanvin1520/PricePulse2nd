import PriceTracker from './components/PriceTracker';

function App() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      <h1 className="text-4xl font-bold text-gray-800 mb-6">PricePulse</h1>
      <PriceTracker />
    </div>
  );
}

export default App;