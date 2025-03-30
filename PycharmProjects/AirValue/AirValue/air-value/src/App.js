import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Discover from './Discover';
import PropertyForm from './PropertyForm';
import Home from './Home';
import PropertySearch from './PropertySearch';
import PropertyInfo from './PropertyInfo';
import AreaHealth from './AreaHealth'; // ✅ Import the new page

function AppContent() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/Discover" element={<Discover />} />
        <Route path="/PropertyForm" element={<PropertyForm />} />
        <Route path="/PropertySearch" element={<PropertySearch />} />
        <Route path="/property/:id" element={<PropertyInfo />} />
        <Route path="/AreaHealth" element={<AreaHealth />} /> {/* ✅ Added new route */}
      </Routes>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;

