import "../styles/Menu.css";
import { useEffect, useState, useContext } from "react";
import { StartSimContext } from "../contexts/StartSimContext";
import { SimSettings } from "../types";
import { Link, NavLink } from "react-router-dom";
import { useAPI } from "../hooks/useAPI";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPenToSquare, faTrash } from "@fortawesome/free-solid-svg-icons";
import { movementRulesText, moveSpeedText, walkSpeedText, conflictWeightText,
        campWeightText, foreignWeightText, usePopForLocWeightText,
        popPowerForLocWeightText, conflictMovechanceText, campMovechanceText,
        defaultMovechanceText, awarenessLevelText, startOnFootText, hastenText,
        optimisationsText, awarenessLevelOptions } from "../helper/constants";
import { CheckboxInputField, NumberInputField, SelectInputField } from "../components/SimsettingField";

function Settings() {
  const { sendRequest } = useAPI();

  const [settings, setSettings] = useState<SimSettings[]>([]);
  const [selectedSettingIndex, setSelectedSettingIndex] = useState<number>(-1);

  const context = useContext(StartSimContext);
  if (!context) {
    throw new Error("StartSimContext is null");
  }
  const { setSettings_id } = context;

  useEffect(() => {
    sendRequest("/simsettings", "GET").then((data) => {
      setSettings(data);
    });
  }, []);

  return (
    <div
      className="menu-items-container content-page"
      id="settings-menu-container"
    >
      <div className="items-list-container" id="settings-list-container">
        <h2 className="items-list-title">Saved Settings</h2>

        <div className="items-list" id="settings-items-list">
          {settings.map((setting, index) => {
            return (
              <button
                key={setting._id}
                className={
                  "simple-button" +
                  (index === selectedSettingIndex ? " selected-item" : "")
                }
                onClick={() => {
                  setSelectedSettingIndex(index);
                  setSettings_id(settings[index]._id);
                }}
              >
                <p>{setting.name}</p>
                <span className="items-list-item-icons">
                  <NavLink to={"/settings/" + setting._id}>
                    <FontAwesomeIcon
                      icon={faPenToSquare}
                      className="item-icon"
                    />
                  </NavLink>
                  <FontAwesomeIcon icon={faTrash} className="item-icon" />
                </span>
              </button>
            );
          })}
        </div>

        <NavLink to="/settings/new">
          <button className="simple-button">Add New Settings</button>
        </NavLink>
      </div>

      <div className="content-section">
        <h2 className="selected-item-title page-title">
          {selectedSettingIndex === -1
            ? "Choose a Setting"
            : settings[selectedSettingIndex].name}
        </h2>

        {selectedSettingIndex !== -1 ? (
          <div className="settings-preview-container">
            <div className="name-container settings-input-section">
              <h2 className="page-subtitle">Name</h2>
              <div className="name-fields-container fields-container">
                <div className="input-field-container">
                  <label htmlFor="">
                    Name: <br />
                    <input
                      className="input-field"
                      type="text"
                      placeholder="Setting Name"
                      name="name"
                      value={settings[selectedSettingIndex].name}
                      disabled={true}
                    />
                  </label>
                </div>
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
                    name="max_move_speed"
                    min={0}
                    max={1000}
                    value={settings[selectedSettingIndex].move_rules.max_move_speed}
                    disabled={true}/>
                </div>
                <div className="input-field-container">
                  <NumberInputField 
                    label="Max Walk Speed"
                    infoText={walkSpeedText}
                    min={0}
                    max={1000}
                    name="max_walk_speed"
                    value={settings[selectedSettingIndex].move_rules.max_walk_speed}
                    disabled={true}/>
                </div>
              </div>
              
              <h3 className="page-subsubtitle">Location Weight</h3>
              <div className="fields-container">
               <div className="input-field-container">
                    <NumberInputField 
                      label="Conflict Weight"
                      infoText={conflictWeightText}
                      min={0}
                      max={100}
                      name="conflict_weight"
                      value={settings[selectedSettingIndex].move_rules.conflict_weight}
                      disabled={true}/>
                </div>
                <div className="input-field-container">
                    <NumberInputField 
                      label="Camp Weight"
                      infoText={campWeightText}
                      min={0}
                      max={100}
                      name="camp_weight"
                      value={settings[selectedSettingIndex].move_rules.camp_weight}
                      disabled={true}/>
                </div>
                <div className="input-field-container">
                    <NumberInputField 
                      label="Foreign Weight"
                      infoText={foreignWeightText}
                      min={0}
                      max={100}
                      name="foreign_weight"
                      value={settings[selectedSettingIndex].move_rules.foreign_weight}
                      disabled={true}/>
                </div>
              </div>

              <div className="fields-container">
                <div className="input-field-container">
                    <CheckboxInputField 
                      label="Utilize the Population For Location Weight"
                      infoText={usePopForLocWeightText}
                      name="use_pop_for_loc_weight"
                      checked={settings[selectedSettingIndex].move_rules.use_pop_for_loc_weight}
                      disabled={true}/>
                </div>
                <div className="input-field-container">
                    <NumberInputField 
                      label="Population Power For Location Weight"
                      infoText={popPowerForLocWeightText}
                      min={0}
                      max={100}
                      name="pop_power_for_loc_weight"
                      value={settings[selectedSettingIndex].move_rules.pop_power_for_loc_weight}
                      disabled={true}/>
                </div>
              </div>
              
              <h3 className="page-subsubtitle">Movement Chance</h3>
              <div className="fields-container">
                <div className="input-field-container">
                    <NumberInputField 
                      label="Conflict Movechance"
                      infoText={conflictMovechanceText}
                      min={0}
                      max={1}
                      name="conflict_movechance"
                      value={settings[selectedSettingIndex].move_rules.conflict_movechance}
                      disabled={true}/>
                </div>
                <div className="input-field-container">
                    <NumberInputField 
                      label="Camp Movechance"
                      infoText={campMovechanceText}
                      min={0}
                      max={1}
                      name="camp_movechance"
                      value={settings[selectedSettingIndex].move_rules.camp_movechance}
                      disabled={true}/>
                </div>
                <div className="input-field-container">
                    <NumberInputField 
                      label="Default Movechance"
                      infoText={defaultMovechanceText}
                      min={0}
                      max={1}
                      name="default_movechance"
                      value={settings[selectedSettingIndex].move_rules.default_movechance}
                      disabled={true}/>
                </div>
              </div>
              
              <h3 className="page-subsubtitle">Advanced</h3>
              <div className="fields-container">
               <div className="input-field-container">
                    <SelectInputField
                      label="Awareness Level"
                      infoText={awarenessLevelText}
                      name="awareness_level"
                      value={settings[selectedSettingIndex].move_rules.awareness_level}
                      options={awarenessLevelOptions}
                      disabled={true}/>
                </div>
                <div className="input-field-container">
                    <CheckboxInputField 
                      label="Start On Foot"
                      infoText={startOnFootText}
                      name="start_on_foot"
                      checked={settings[selectedSettingIndex].move_rules.start_on_foot}
                      disabled={true}/>
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
                      min={0}
                      max={1000}
                      name="hasten"
                      value={settings[selectedSettingIndex].optimisations.hasten}
                      disabled={true}/>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <span></span>
        )}

        <div className="buttons-container">
          <Link
            to={selectedSettingIndex === -1 ? "/settings/" : "/simulations"}
          >
            <button
              className="simple-button"
              disabled={selectedSettingIndex === -1}
            >
              Continue
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Settings;
