// import logo from './logo.svg';
import './App.css';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/pages/Home';
import Research from './components/pages/Research';
import Team from './components/pages/Team';
import HowItWorks from './components/pages/HowItWorks';
import Supporters from './components/pages/Supporters.js';
import Contact from './components/pages/Contact.js';

function App() {
  return (
    <>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/team-process-map" element={<Home />} />
          <Route path="/Research" element={<Research />} />
          <Route path="/Team" element={<Team />} />
          <Route path="/HowItWorks" element={<HowItWorks />} />
          <Route path = "/Supporters" element={<Supporters />} />
          <Route path = "/Contact" element={<Contact />} />
        </Routes>
        <Footer />
      </Router>
    </>
  );
}

export default App;
