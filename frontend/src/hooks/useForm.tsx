import { FormEvent, useState } from "react";
import { useAPI } from "../hooks/useAPI";
import { maxValues } from "../helper/constants/SimsettingConstants";
import { maxValues as inputMaxValues, minValues as inputMinValues } from "../helper/constants/InputConstants";

export function useForm(initialFValues: any) {
  const [values, setValues] = useState(initialFValues);

  function str2bool(value: any) {
    if (value && typeof value === "string") {
      if (value.toLowerCase() === "true") return true;
      if (value.toLowerCase() === "false") return false;
    }
    return value;
  }

  const handleInputChange =
  (
    e:
      | React.ChangeEvent<HTMLInputElement>
      | React.ChangeEvent<HTMLSelectElement>,
  ) => {
    let { name, value, type } = e.target;

    // sanitise name input
    if(name === "name") {
      if (value.length > 30) {
        value = value.slice(0, 30);
      } else if (value.length === 0) {
        value = "untitled";
      }
    }

    // handle type = checkbox
    if (type === "checkbox") {
      if (type === "checkbox") {
        value = (e.target as HTMLInputElement).checked.toString();
      }
    }

    // convert string to boolean
    value = str2bool(value);

    // Input
    if (name === "length") {
      value = sanitiseInput(value,
                            inputMaxValues.sim_period.length,
                            inputMinValues.sim_period.length);
      setValues({
        ...values,
        sim_period: {
          ...values.sim_period,
          [name]: value,
        },
      });
      return;
    }

    // Simsettings
    // Move rules
    if (
      [
        "max_move_speed",
        "max_walk_speed",
        "foreign_weight",
        "conflict_weight",
        "camp_weight",
        "pop_power_for_loc_weight",
        "conflict_movechance",
        "camp_movechance",
        "default_movechance",
        "awareness_level",
        "capacity_scaling",
        "weight_power",
      ].includes(name)
    ) {
      value = sanitiseInput(value, 
                            maxValues.
                            move_rules[name as keyof typeof maxValues.move_rules]);
      setValues({
        ...values,
        move_rules: {
          ...values.move_rules,
          [name]: Number(value),
        },
      });
      return;
    }

    if (
      [
        "use_pop_for_loc_weight",
        "avoid_short_stints",
        "start_on_foot",
      ].includes(name)
    ) {
      setValues({
        ...values,
        move_rules: {
          ...values.move_rules,
          [name]: Boolean(value),
        },
      });
      return;
    }

    // Spawn rules
    if (name === "displaced_per_conflict_day") {
      value = sanitiseInput(value, 
                            maxValues.
                            spawn_rules.
                            conflict_driven_spawning[name as keyof typeof maxValues.spawn_rules.conflict_driven_spawning]);
      setValues({
        ...values,
        spawn_rules: {
          ...values.spawn_rules,
          conflict_driven_spawning: {
            ...values.spawn_rules.conflict_driven_spawning,
            [name]: Number(value),
        }
      }});
      return;
    }

    // Optimisations are nested in the sim_settings object
    if (name === "hasten") {
      value = sanitiseInput(value, 
                            maxValues.
                            optimisations[name as keyof typeof maxValues.optimisations]);
      setValues({
        ...values,
        optimisations: {
          ...values.optimisations,
          [name]: Number(value),
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

  function sanitiseInput(value: string, max?: number, min?: number) {
    if (max && Number(value) > max) {
      value = max.toString();
    } else if (value.length > 10) {
      value = value.slice(0, 10);
    } else if (min && Number(value) < min) {
      value = min.toString();
    }
    return value;
  }

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
