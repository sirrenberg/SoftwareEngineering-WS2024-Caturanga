import { useState, createContext, ReactNode } from "react";

interface StartSimContextType {
  input_id: string;
  setInput_id: (input_id: string) => void;
  settings_id: string;
  setSettings_id: (settings_id: string) => void;
}

const Context = createContext<StartSimContextType | undefined>(undefined);

function ContextProvider({ children }: { children: ReactNode }) {
  const [input_id, setInput_id] = useState("");
  const [settings_id, setSettings_id] = useState("");

  return (
    <Context.Provider
      value={{
        input_id,
        setInput_id,
        settings_id,
        setSettings_id,
      }}
    >
      {children}
    </Context.Provider>
  );
}

export {
  ContextProvider as StartSimContextProvider,
  Context as StartSimContext,
};
