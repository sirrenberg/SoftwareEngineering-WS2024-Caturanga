import "../styles/AddInput.css";
import { useParams, useNavigate } from "react-router-dom";
import { SimSettings } from "../types";
import { useForm } from "../hooks/useForm";
import { useEffect } from "react";
import SimsettingInputField from "../components/SimsettingInputField";
import { movementRulesText, moveSpeedText, walkSpeedText, conflictWeightText,
  campWeightText, foreignWeightText, usePopForLocWeightText,
  popPowerForLocWeightText, conflictMovechanceText, campMovechanceText,
  defaultMovechanceText, awarenessLevelText, startOnFootText, hastenText,
  optimisationsText } from "../helper/constants";

function AddSetting() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const isNewSetting = id === "new";

  const initialValues: SimSettings = {
    _id: "",
    name: "untitled",
    move_rules: {
      max_move_speed: 360,
      max_walk_speed: 35,
      foreign_weight: 1,
      conflict_weight: 0.25,
      camp_weight: 1,
      use_pop_for_loc_weight: false,
      pop_power_for_loc_weight: 0.1,
      conflict_movechance: 1,
      camp_movechance: 0.001,
      default_movechance: 0.3,
      awareness_level: 1,
      capacity_scaling: 1,
      avoid_short_stints: false,
      start_on_foot: false,
      weight_power: 1,
    },
    optimisations: {
      hasten: 1,
    },
  };

  const { values, handleInputChange, handlePrefillData, handleSubmit } =
    useForm(initialValues);

  useEffect(() => {
    if (!isNewSetting) {
      handlePrefillData(`/simsettings/${id}`);
    }
  }, []);

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
              value={values.name === initialValues.name ? "" : values.name}
            />
          </label>
        </div>
      </div>

      <div className="move-rules-container settings-input-section">
              <h2 className="page-subtitle">Movement Rules</h2>
              <p className="section-subtext">{movementRulesText}</p>
              <h3 className="page-subsubtitle">Movement Speed</h3>
              <div className="fields-container">
                <div className="input-field-container">
                  <SimsettingInputField 
                    label="Max Move Speed"
                    infoText={moveSpeedText}
                    checkBox={false}
                    name="max_move_speed"
                    value={values.move_rules.max_move_speed}
                    disabled={false}
                    onChange={handleInputChange}/>
                </div>
                <div className="input-field-container">
                  <SimsettingInputField 
                    label="Max Walk Speed"
                    infoText={walkSpeedText}
                    checkBox={false}
                    name="max_walk_speed"
                    value={values.move_rules.max_walk_speed}
                    disabled={false}
                    onChange={handleInputChange}/>
                </div>
              </div>
              
              <h3 className="page-subsubtitle">Location Weight</h3>
              <div className="fields-container">
               <div className="input-field-container">
                    <SimsettingInputField 
                      label="Conflict Weight"
                      infoText={conflictWeightText}
                      checkBox={false}
                      name="conflict_weight"
                      value={values.move_rules.conflict_weight}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
                <div className="input-field-container">
                    <SimsettingInputField 
                      label="Camp Weight"
                      infoText={campWeightText}
                      checkBox={false}
                      name="camp_weight"
                      value={values.move_rules.camp_weight}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
                <div className="input-field-container">
                    <SimsettingInputField 
                      label="Foreign Weight"
                      infoText={foreignWeightText}
                      checkBox={false}
                      name="foreign_weight"
                      value={values.move_rules.foreign_weight}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
              </div>

              <div className="fields-container">
                <div className="input-field-container">
                    <SimsettingInputField 
                      label="Use Population For Location Weight"
                      infoText={usePopForLocWeightText}
                      checkBox={true}
                      name="use_pop_for_loc_weight"
                      checked={values.move_rules.use_pop_for_loc_weight}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
                <div className="input-field-container">
                    <SimsettingInputField 
                      label="Population Power For Location Weight"
                      infoText={popPowerForLocWeightText}
                      checkBox={false}
                      name="pop_power_for_loc_weight"
                      value={values.move_rules.pop_power_for_loc_weight}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
              </div>
              
              <h3 className="page-subsubtitle">Movement Chance</h3>
              <div className="fields-container">
                <div className="input-field-container">
                    <SimsettingInputField 
                      label="Conflict Movechance"
                      infoText={conflictMovechanceText}
                      checkBox={false}
                      name="conflict_movechance"
                      value={values.move_rules.conflict_movechance}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
                <div className="input-field-container">
                    <SimsettingInputField 
                      label="Camp Movechance"
                      infoText={campMovechanceText}
                      checkBox={false}
                      name="camp_movechance"
                      value={values.move_rules.camp_movechance}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
                <div className="input-field-container">
                    <SimsettingInputField 
                      label="Default Movechance"
                      infoText={defaultMovechanceText}
                      checkBox={false}
                      name="default_movechance"
                      value={values.move_rules.default_movechance}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
              </div>
              
              <h3 className="page-subsubtitle">Advanced</h3>
              <div className="fields-container">
               <div className="input-field-container">
                    <SimsettingInputField 
                      label="Awareness Level"
                      infoText={awarenessLevelText}
                      checkBox={false}
                      name="awareness_level"
                      value={values.move_rules.awareness_level}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
                <div className="input-field-container">
                    <SimsettingInputField 
                      label="Start On Foot"
                      infoText={startOnFootText}
                      checkBox={true}
                      name="start_on_foot"
                      checked={values.move_rules.start_on_foot}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
              </div>
            </div>

            <div className="optimisations-container settings-input-section">
              <h2 className="page-subtitle">Optimisations</h2>
              <p className="section-subtext">{optimisationsText}</p>
              <div className="fields-container">
              <div className="input-field-container">
                    <SimsettingInputField 
                      label="Hasten"
                      infoText={hastenText}
                      checkBox={false}
                      name="hasten"
                      value={values.optimisations.hasten}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
              </div>
            </div>

      <div className="submit-button-container add-input-section">
        <button
          id="submit-settings-button"
          className="simple-button"
          onClick={(e) => {
            /**
             * Handles the form submission and navigates to the "/settings" page.
             * @param {Event} e - The form submission event.
             */
            handleSubmit(e, "/simsettings", "POST");
            navigate("/settings");
          }}
        >
          Save
        </button>
      </div>
    </div>
  );
}

export default AddSetting;
