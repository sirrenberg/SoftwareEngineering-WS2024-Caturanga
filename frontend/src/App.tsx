import "./App.css";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";

import LandingPage from "./pages/LandingPage";
import Inputs from "./pages/Inputs";
import AddInput from "./pages/AddInput";

function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/inputs" element={<Inputs />} />
        <Route path="/inputs/:id" element={<AddInput />} />
      </Routes>
    </div>
  );
}

export default App;
