import { useState, createContext, ReactNode } from "react";

interface StartSimContextType {
  input_id: string;
  setInput_id: (input_id: string) => void;
  inputName: string;
  setInputName: (inputName: string) => void;
  settings_id: string;
  setSettings_id: (settings_id: string) => void;
  settingsName: string;
  setSettingsName: (settingsName: string) => void;
}

const Context = createContext<StartSimContextType | undefined>(undefined);

function ContextProvider({ children }: { children: ReactNode }) {
  const [input_id, setInput_id] = useState("");
  const [inputName, setInputName] = useState("");
  const [settings_id, setSettings_id] = useState("");
  const [settingsName, setSettingsName] = useState("");

  return (
    <Context.Provider
      value={{
        input_id,
        setInput_id,
        inputName,
        setInputName,
        settings_id,
        setSettings_id,
        settingsName,
        setSettingsName,
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
