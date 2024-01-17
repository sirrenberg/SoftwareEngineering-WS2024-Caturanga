import "../styles/AddInput.css";
import { useNavigate, useParams } from "react-router-dom";
import { useForm } from "../hooks/useForm";
import { useEffect, useState } from "react";
import { CheckboxInputField, NumberInputField, SelectInputField} from "../components/SimsettingField";
import { movementRulesText, moveSpeedText, walkSpeedText, conflictWeightText,
  campWeightText, foreignWeightText, usePopForLocWeightText,
  popPowerForLocWeightText, conflictMovechanceText, idpcampMovechanceText,
  defaultMovechanceText, awarenessLevelText, startOnFootText, hastenText,
  optimisationsText, defaultValues, awarenessLevelOptions, spawnRulesText,
  displacedPerConflictDayText, maxValues} from "../helper/constants/SimsettingConstants";

function AddSetting() {
  const [submitted, setSubmitted] = useState<boolean>(false);
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const isNewSetting = id === "new";

  const initialValues = defaultValues;

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
                  <NumberInputField 
                    label="Max Move Speed"
                    infoText={moveSpeedText}
                    min={0}
                    max={maxValues.move_rules.max_move_speed}
                    name="max_move_speed"
                    value={values.move_rules.max_move_speed}
                    disabled={false}
                    onChange={handleInputChange}/>
                </div>
                <div className="input-field-container">
                  <NumberInputField 
                    label="Max Walk Speed"
                    infoText={walkSpeedText}
                    min={0}
                    max={maxValues.move_rules.max_walk_speed}
                    name="max_walk_speed"
                    value={values.move_rules.max_walk_speed}
                    disabled={false}
                    onChange={handleInputChange}/>
                </div>
              </div>
              
              <h3 className="page-subsubtitle">Location Weight</h3>
              <div className="fields-container">
               <div className="input-field-container">
                    <NumberInputField 
                      label="Conflict Weight"
                      infoText={conflictWeightText}
                      min={0}
                      max={maxValues.move_rules.conflict_weight}
                      name="conflict_weight"
                      value={values.move_rules.conflict_weight}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
                <div className="input-field-container">
                    <NumberInputField 
                      label="Camp Weight"
                      infoText={campWeightText}
                      min={0}
                      max={maxValues.move_rules.camp_weight}
                      name="camp_weight"
                      value={values.move_rules.camp_weight}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
                <div className="input-field-container">
                    <NumberInputField 
                      label="Foreign Weight"
                      infoText={foreignWeightText}
                      min={0}
                      max={maxValues.move_rules.foreign_weight}
                      name="foreign_weight"
                      value={values.move_rules.foreign_weight}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
              </div>

              <div className="fields-container">
                <div className="input-field-container">
                    <CheckboxInputField 
                      label="Use Population For Location Weight"
                      infoText={usePopForLocWeightText}
                      name="use_pop_for_loc_weight"
                      checked={values.move_rules.use_pop_for_loc_weight}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
                <div className="input-field-container">
                    <NumberInputField 
                      label="Population Power For Location Weight"
                      infoText={popPowerForLocWeightText}
                      min={0}
                      max={maxValues.move_rules.pop_power_for_loc_weight}
                      name="pop_power_for_loc_weight"
                      value={values.move_rules.pop_power_for_loc_weight}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
              </div>
              
              <h3 className="page-subsubtitle">Movement Chance</h3>
              <div className="fields-container">
                <div className="input-field-container">
                    <NumberInputField 
                      label="Conflict Movechance"
                      infoText={conflictMovechanceText}
                      min={0}
                      max={maxValues.move_rules.conflict_movechance}
                      name="conflict_movechance"
                      value={values.move_rules.conflict_movechance}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
                <div className="input-field-container">
                    <NumberInputField 
                      label="Camp Movechance"
                      infoText={idpcampMovechanceText}
                      min={0}
                      max={maxValues.move_rules.idpcamp_movechance}
                      name="idpcamp_movechance"
                      value={values.move_rules.idpcamp_movechance}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
                <div className="input-field-container">
                    <NumberInputField 
                      label="Default Movechance"
                      infoText={defaultMovechanceText}
                      min={0}
                      max={maxValues.move_rules.default_movechance}
                      name="default_movechance"
                      value={values.move_rules.default_movechance}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
              </div>
              
              <h3 className="page-subsubtitle">Advanced</h3>
              <div className="fields-container">
               <div className="input-field-container">
                    <SelectInputField 
                      label="Awareness Level"
                      infoText={awarenessLevelText}
                      name="awareness_level"
                      value={values.move_rules.awareness_level}
                      options={awarenessLevelOptions}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
                <div className="input-field-container">
                    <CheckboxInputField 
                      label="Start On Foot"
                      infoText={startOnFootText}
                      name="start_on_foot"
                      checked={values.move_rules.start_on_foot}
                      disabled={false}
                      onChange={handleInputChange}/>
                </div>
              </div>
            </div>

            <div className="spawn-rules-container settings-input-section">
            <h2 className="page-subtitle">Spawn Rules</h2>
              <p className="section-subtext">{spawnRulesText}</p>
              <h3 className="page-subsubtitle">Conflict Driven Spawning</h3>
              <div className="fields-container">
                <div className="input-field-container">
                  <NumberInputField 
                    label="Displaced Percentage of IDPs Per Conflict Day"
                    infoText={displacedPerConflictDayText}
                    min={0}
                    max={maxValues.spawn_rules.conflict_driven_spawning.displaced_per_conflict_day}
                    name="displaced_per_conflict_day"
                    value={values.spawn_rules.conflict_driven_spawning.displaced_per_conflict_day}
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
                    <NumberInputField 
                      label="Hasten"
                      infoText={hastenText}
                      min={1}
                      max={maxValues.optimisations.hasten}
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
          disabled={submitted}
          onClick={(e) => {
            setSubmitted(true);
            handleSubmit(e, "/simsettings", "POST", () => {navigate("/settings");});
          }}
        >
          Save
        </button>
      </div>
    </div>
  );
}

export default AddSetting;
