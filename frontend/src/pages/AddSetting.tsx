import "../styles/AddInput.css";
import { useParams } from "react-router-dom";
import { SimSettings } from "../types";
import { useForm } from "../hooks/useForm";
import { useEffect } from "react";

function AddSetting() {
  const { id } = useParams<{ id: string }>();

  const isNewSetting = id === "new";

  const initialValues: SimSettings = {
    _id: "",
    name: "",
    log_levels: {
      agent: 0,
      link: 0,
      camp: 0,
      conflict: 0,
      init: 0,
      idp_totals: 0,
      granularity: "",
    },
    spawn_rules: {
      take_from_population: false,
      insert_day0: false,
    },
    move_rules: {
      max_move_speed: 0,
      max_walk_speed: 0,
      foreign_weight: 0,
      conflict_weight: 0,
      camp_weight: 0,
      conflict_movechance: 0,
      camp_movechance: 0,
      default_movechance: 0,
      awareness_level: 0,
      capacity_scaling: 0,
      avoid_short_stints: false,
      start_on_foot: false,
      weight_power: 0,
    },
    optimisations: {
      hasten: 0,
    },
  };

  const { values, handleInputChange, handlePrefillData, handleSubmit } =
    useForm(initialValues);

  useEffect(() => {
    if (!isNewSetting) {
      handlePrefillData(`/simsettings/${id}`);
    }
  }, []);

  console.log("values in AddSetting", values);

  return (
    <div className="add-input-container content-page">
      <h1 className="page-title">
        {isNewSetting ? "New Setting: " : "Edit Setting: "}
        {values.name}
      </h1>

      <div className="name-fields-container fields-container">
        <div className="input-field-container">
          <label htmlFor="">
            Name: <br />
            <input
              className="input-field"
              type="text"
              placeholder="Input Name"
              onChange={handleInputChange}
              name="name"
              value={values.name}
            />
          </label>
        </div>
      </div>

      <div className="log-levels-container settings-input-section">
        <h2 className="page-subtitle">Log Levels</h2>
        <div className="fields-container">
          <div className="input-field-container">
            <label htmlFor="">
              Agent: <br />
              <input
                className="input-field"
                type="number"
                placeholder="0"
                name="agent"
                value={values.log_levels.agent}
                onChange={handleInputChange}
              />
            </label>
          </div>
          <div className="input-field-container">
            <label htmlFor="">
              Link: <br />
              <input
                className="input-field"
                type="number"
                placeholder="0"
                name="link"
                value={values.log_levels.link}
                onChange={handleInputChange}
              />
            </label>
          </div>
          <div className="input-field-container">
            <label htmlFor="">
              Camp: <br />
              <input
                className="input-field"
                type="number"
                placeholder="0"
                name="camp"
                value={values.log_levels.camp}
                onChange={handleInputChange}
              />
            </label>
          </div>
          <div className="input-field-container">
            <label htmlFor="">
              Conflict: <br />
              <input
                className="input-field"
                type="number"
                placeholder="0"
                name="conflict"
                value={values.log_levels.conflict}
                onChange={handleInputChange}
              />
            </label>
          </div>
        </div>

        <div className="fields-container">
          <div className="input-field-container">
            <label htmlFor="">
              Init: <br />
              <input
                className="input-field"
                type="number"
                placeholder="0"
                name="init"
                value={values.log_levels.init}
                onChange={handleInputChange}
              />
            </label>
          </div>
          <div className="input-field-container">
            <label htmlFor="">
              IDP Totals: <br />
              <input
                className="input-field"
                type="number"
                placeholder="0"
                name="idp_totals"
                value={values.log_levels.idp_totals}
                onChange={handleInputChange}
              />
            </label>
          </div>
          <div className="input-field-container">
            <label htmlFor="">
              Granularity: <br />
              <input
                className="input-field"
                type="text"
                placeholder="0"
                name="granularity"
                value={values.log_levels.granularity}
                onChange={handleInputChange}
              />
            </label>
          </div>
        </div>
      </div>

      <div className="spawn-rules-container settings-input-section">
        <h2 className="page-subtitle">Spawn Rules</h2>
        <div className="fields-container">
          <div className="input-field-container">
            <label htmlFor="">
              Take From Population: <br />
              <input
                className="input-field"
                type="checkbox"
                placeholder="0"
                name="take_from_population"
                checked={values.spawn_rules.take_from_population}
                onChange={handleInputChange}
              />
            </label>
          </div>
          <div className="input-field-container">
            <label htmlFor="">
              Insert Day0: <br />
              <input
                className="input-field"
                type="checkbox"
                placeholder="0"
                name="insert_day0"
                checked={values.spawn_rules.insert_day0}
                onChange={handleInputChange}
              />
            </label>
          </div>
        </div>
      </div>

      <div className="move-rules-container settings-input-section">
        <h2 className="page-subtitle">Movement Rules</h2>
        <div className="fields-container">
          <div className="input-field-container">
            <label htmlFor="">
              Max Move Speed: <br />
              <input
                className="input-field"
                type="number"
                placeholder="0"
                name="max_move_speed"
                value={values.move_rules.max_move_speed}
                onChange={handleInputChange}
              />
            </label>
          </div>
          <div className="input-field-container">
            <label htmlFor="">
              Max Walk Speed: <br />
              <input
                className="input-field"
                type="number"
                placeholder="0"
                name="max_walk_speed"
                value={values.move_rules.max_walk_speed}
                onChange={handleInputChange}
              />
            </label>
          </div>
        </div>

        <div className="fields-container">
          <div className="input-field-container">
            <label htmlFor="">
              Foreign Weight: <br />
              <input
                className="input-field"
                type="number"
                placeholder="0"
                name="foreign_weight"
                value={values.move_rules.foreign_weight}
                onChange={handleInputChange}
              />
            </label>
          </div>
          <div className="input-field-container">
            <label htmlFor="">
              Conflict Weight: <br />
              <input
                className="input-field"
                type="number"
                placeholder="0"
                name="conflict_weight"
                value={values.move_rules.conflict_weight}
                onChange={handleInputChange}
              />
            </label>
          </div>
          <div className="input-field-container">
            <label htmlFor="">
              Camp Weight: <br />
              <input
                className="input-field"
                type="number"
                placeholder="0"
                name="camp_weight"
                value={values.move_rules.camp_weight}
                onChange={handleInputChange}
              />
            </label>
          </div>
        </div>

        <div className="fields-container">
          <div className="input-field-container">
            <label htmlFor="">
              Conflict Movechance: <br />
              <input
                className="input-field"
                type="number"
                placeholder="0"
                name="conflict_movechance"
                value={values.move_rules.conflict_movechance}
                onChange={handleInputChange}
              />
            </label>
          </div>

          <div className="input-field-container">
            <label htmlFor="">
              Camp Movechance: <br />
              <input
                className="input-field"
                type="number"
                placeholder="0"
                name="camp_movechance"
                value={values.move_rules.camp_movechance}
                onChange={handleInputChange}
              />
            </label>
          </div>
          <div className="input-field-container">
            <label htmlFor="">
              Default Movechance: <br />
              <input
                className="input-field"
                type="number"
                placeholder="0"
                name="default_movechance"
                value={values.move_rules.default_movechance}
                onChange={handleInputChange}
              />
            </label>
          </div>
        </div>

        <div className="fields-container">
          <div className="input-field-container">
            <label htmlFor="">
              Awareness Level: <br />
              <input
                className="input-field"
                type="number"
                placeholder="0"
                name="awareness_level"
                value={values.move_rules.awareness_level}
                onChange={handleInputChange}
              />
            </label>
          </div>
          <div className="input-field-container">
            <label htmlFor="">
              Capacity Scaling: <br />
              <input
                className="input-field"
                type="number"
                placeholder="0"
                name="capacity_scaling"
                value={values.move_rules.capacity_scaling}
                onChange={handleInputChange}
              />
            </label>
          </div>

          <div className="input-field-container">
            <label htmlFor="">
              Weight Power: <br />
              <input
                className="input-field"
                type="number"
                placeholder="0"
                name="weight_power"
                value={values.move_rules.weight_power}
                onChange={handleInputChange}
              />
            </label>
          </div>
        </div>

        <div className="fields-container">
          <div className="input-field-container">
            <label htmlFor="">
              Avoid Short Stints: <br />
              <input
                className="input-field"
                type="checkbox"
                placeholder="0"
                name="avoid_short_stints"
                checked={values.move_rules.avoid_short_stints}
                onChange={handleInputChange}
              />
            </label>
          </div>
          <div className="input-field-container">
            <label htmlFor="">
              Start On Foot: <br />
              <input
                className="input-field"
                type="checkbox"
                placeholder="0"
                name="start_on_foot"
                checked={values.move_rules.start_on_foot}
                onChange={handleInputChange}
              />
            </label>
          </div>
        </div>
      </div>

      <div className="optimisations-container settings-input-section">
        <h2 className="page-subtitle">Optimisations</h2>
        <div className="fields-container">
          <div className="input-field-container">
            <label htmlFor="">
              Hasten: <br />
              <input
                className="input-field"
                type="number"
                placeholder="0"
                name="hasten"
                value={values.optimisations.hasten}
                onChange={handleInputChange}
              />
            </label>
          </div>
        </div>
      </div>

      <div className="submit-button-container add-input-section">
        <button
          id="submit-settings-button"
          className="simple-button"
          onClick={(e) => {
            handleSubmit(e, "/simsettings", isNewSetting ? "POST" : "PUT");
          }}
        >
          Save
        </button>
      </div>
    </div>
  );
}

export default AddSetting;
