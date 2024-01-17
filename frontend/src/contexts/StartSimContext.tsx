import { useState, createContext, ReactNode } from "react";

interface StartSimContextType {
  inputId: string;
  setInputId: (input_id: string) => void;
  inputName: string;
  setInputName: (inputName: string) => void;
  settingsId: string;
  setSettingsId: (settings_id: string) => void;
  settingsName: string;
  setSettingsName: (settingsName: string) => void;
}

const Context = createContext<StartSimContextType | undefined>(undefined);

function ContextProvider({ children }: { children: ReactNode }) {
  const [inputId, setInputId] = useState("");
  const [inputName, setInputName] = useState("");
  const [settingsId, setSettingsId] = useState("");
  const [settingsName, setSettingsName] = useState("");

  return (
    <Context.Provider
      value={{
        inputId,
        setInputId,
        inputName,
        setInputName,
        settingsId,
        setSettingsId,
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
