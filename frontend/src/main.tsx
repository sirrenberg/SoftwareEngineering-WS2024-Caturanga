import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import { BrowserRouter as Router } from "react-router-dom";
// import mainTheme from "./themes/MainTheme";
// import { ThemeProvider } from "@mui/material/styles";
import { StyledEngineProvider } from "@mui/material/styles";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Router>
      <StyledEngineProvider injectFirst>
        <App />
      </StyledEngineProvider>
    </Router>
  </React.StrictMode>
);
