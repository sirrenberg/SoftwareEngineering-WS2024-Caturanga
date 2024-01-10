import { FormEvent, useState } from "react";
import { useAPI } from "../hooks/useAPI";

export function useForm(initialFValues: any) {
  const [values, setValues] = useState(initialFValues);

  function str2bool(value: any) {
    if (value && typeof value === "string") {
      if (value.toLowerCase() === "true") return true;
      if (value.toLowerCase() === "false") return false;
    }
    return value;
  }

  const handleInputChange = (
    e:
      | React.ChangeEvent<HTMLInputElement>
      | React.ChangeEvent<HTMLSelectElement>
  ) => {
    let { name, value, type } = e.target;

    // handle type = checkbox
    if (type === "checkbox") {
      if (type === "checkbox") {
        value = (e.target as HTMLInputElement).checked.toString();
      }
    }

    // convert string to boolean
    value = str2bool(value);

    // if name is date or length, then we need to update the sim_period object
    if (name === "date" || name === "length") {
      setValues({
        ...values,
        sim_period: {
          ...values.sim_period,
          [name]: value,
        },
      });
      return;
    }

    // Move rules are nested in the sim_settings object
    if (
      [
        "max_move_speed",
        "max_walk_speed",
        "foreign_weight",
        "conflict_weight",
        "camp_weight",
        "use_pop_for_loc_weight",
        "pop_power_for_loc_weight",
        "conflict_movechance",
        "camp_movechance",
        "default_movechance",
        "awareness_level",
        "capacity_scaling",
        "avoid_short_stints",
        "start_on_foot",
        "weight_power",
      ].includes(name)
    ) {
      setValues({
        ...values,
        move_rules: {
          ...values.move_rules,
          [name]: value,
        },
      });
      return;
    }

    // Optimisations are nested in the sim_settings object
    if (["hasten"].includes(name)) {
      setValues({
        ...values,
        optimisations: {
          ...values.optimisations,
          [name]: value,
        },
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

  function handleSubmit(e: FormEvent, url: string, method: string) {
    e.preventDefault();
    const { sendRequest } = useAPI();
    sendRequest(url, method, values).then((data) => {
      console.log(data);
    });
  }

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
