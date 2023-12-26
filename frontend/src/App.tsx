import "./App.css";
import { Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import Inputs from "./pages/Inputs";
import AddInput from "./pages/AddInput";
import Settings from "./pages/Settings";
import Simulations from "./pages/Simulations";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/inputs" element={<Inputs />} />
        <Route path="/inputs/:id" element={<AddInput />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/simulations" element={<Simulations />} />
      </Routes>
    </div>
  );
}

export default App;
