import { FormEvent, useState } from "react";
import { useAPI } from "../hooks/useAPI";

export function useForm(initialFValues: any) {
  const [values, setValues] = useState(initialFValues);

  const handleInputChange = (
    e:
      | React.ChangeEvent<HTMLInputElement>
      | React.ChangeEvent<HTMLSelectElement>
  ) => {
    const { name, value } = e.target;

    // if name is date or length, then we need to update the sim_period object
    if (name === "date" || name === "length") {
      setValues({
        ...values,
        sim_period: [
          {
            ...values.sim_period[0],
            [name]: value,
          },
        ],
      });
      return;
    }

    // else, update the values object
    setValues({
      ...values,
      [name]: value,
    });
  };

  const resetForm = () => {
    setValues(initialFValues);
  };

  function handleSubmit(e: FormEvent, url: string, method: string) {}

  function handlePrefillData(url: string) {
    const { sendRequest } = useAPI();
    sendRequest(url, "GET").then((data) => {
      setValues(data);
    });
  }

  return {
    values,
    setValues,
    handleInputChange,
    handleSubmit,
    resetForm,
    handlePrefillData,
  };
}
