import "./App.css";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";

import LandingPage from "./pages/LandingPage";
import Configurations from "./pages/Configurations";

function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/configurations" element={<Configurations />} />
      </Routes>
    </div>
  );
}

export default App;
