import "../styles/Menu.css";
import { useEffect, useState, useContext } from "react";
import { StartSimContext } from "../contexts/StartSimContext";
import { SimSettings } from "../types";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { useAPI } from "../hooks/useAPI";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPenToSquare, faTrash } from "@fortawesome/free-solid-svg-icons";
import { movementRulesText, moveSpeedText, walkSpeedText, conflictWeightText,
        campWeightText, foreignWeightText, usePopForLocWeightText,
        popPowerForLocWeightText, conflictMovechanceText, idpcampMovechanceText,
        defaultMovechanceText, awarenessLevelText, startOnFootText, hastenText,
        optimisationsText, awarenessLevelOptions, spawnRulesText, displacedPerConflictDayText } 
        from "../helper/constants/SimsettingConstants";
import { CheckboxInputField, NumberInputField, SelectInputField } from "../components/SimsettingField";

function Settings() {
  const { sendRequest } = useAPI();
  const navigate = useNavigate();

  const [settings, setSettings] = useState<SimSettings[] | undefined>(
    undefined
  );
  const [selectedSettingIndex, setSelectedSettingIndex] = useState<number>(-1);
  const [protectedSimSettingIDs, setProtectedSimSettingIDs] = useState<string[]>([]);

  const context = useContext(StartSimContext);
  if (!context) {
    throw new Error("StartSimContext is null");
  }
  const { setSettingsId, setSettingsName } = context;

  useEffect(() => {
    sendRequest("/simsettings", "GET").then((response) => {
      const { data, protectedIDs } = response;
      console.log("Response: ", response);
      console.log("Protected IDs: ", protectedIDs);
      setProtectedSimSettingIDs(protectedIDs);
      console.log("Data: ", data);
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
          {!settings && <h3>Loading...</h3>}

          {settings && settings.length === 0 && <h3>Empty</h3>}

          {settings &&
            settings.map((setting, index) => {
              return (
                <button
                  key={setting._id}
                  className={
                    "simple-button" +
                    (index === selectedSettingIndex ? " selected-item" : "")
                  }
                  onClick={() => {
                    setSelectedSettingIndex(index);
                    setSettingsId(settings[index]._id);
                    setSettingsName(settings[index].name);
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
                    {!protectedSimSettingIDs.includes(setting._id) && (
                      <FontAwesomeIcon
                        icon={faTrash}
                        className="item-icon"
                        //style={{ border: "none" , backgroundColor: "transparent" , padding : 0, color: "inherit"}}
                        onClick={(event) => {
                          event.stopPropagation();
                          // if the setting to be deleted is the one that is currently selected, deselect it
                          if (selectedSettingIndex === index) {
                            setSelectedSettingIndex(-1);
                          }
                          sendRequest("/simsettings/" + setting._id, "DELETE")
                            .then((_) => {
                              // if the setting to be deleted is before the currently selected one, decrement the selected index
                              const indexOfDeleted = settings.findIndex(
                                (s) => s._id === setting._id
                              );
                              if (indexOfDeleted < selectedSettingIndex) {
                                setSelectedSettingIndex(
                                  selectedSettingIndex - 1
                                );
                              }
                              setSettings(
                                settings.filter(
                                  (simsetting) => simsetting._id !== setting._id
                                )
                              );
                            })
                            .catch((err) => {
                              console.error(err);
                            });
                        }}
                      />
                    )}
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
          {settings
            ? selectedSettingIndex === -1
              ? "Choose a Setting"
              : settings[selectedSettingIndex].name
            : ""}
        </h2>

        {settings && selectedSettingIndex !== -1 ? (
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
                    value={
                      settings[selectedSettingIndex].move_rules.max_move_speed
                    }
                    disabled={true}
                  />
                </div>
                <div className="input-field-container">
                  <NumberInputField
                    label="Max Walk Speed"
                    infoText={walkSpeedText}
                    name="max_walk_speed"
                    value={
                      settings[selectedSettingIndex].move_rules.max_walk_speed
                    }
                    disabled={true}
                  />
                </div>
              </div>

              <h3 className="page-subsubtitle">Location Weight</h3>
              <div className="fields-container">
                <div className="input-field-container">
                  <NumberInputField
                    label="Conflict Weight"
                    infoText={conflictWeightText}
                    name="conflict_weight"
                    value={
                      settings[selectedSettingIndex].move_rules.conflict_weight
                    }
                    disabled={true}
                  />
                </div>
                <div className="input-field-container">
                  <NumberInputField
                    label="Camp Weight"
                    infoText={campWeightText}
                    name="camp_weight"
                    value={
                      settings[selectedSettingIndex].move_rules.camp_weight
                    }
                    disabled={true}
                  />
                </div>
                <div className="input-field-container">
                  <NumberInputField
                    label="Foreign Weight"
                    infoText={foreignWeightText}
                    name="foreign_weight"
                    value={
                      settings[selectedSettingIndex].move_rules.foreign_weight
                    }
                    disabled={true}
                  />
                </div>
              </div>

              <div className="fields-container">
                <div className="input-field-container">
                  <CheckboxInputField
                    label="Utilize the Population For Location Weight"
                    infoText={usePopForLocWeightText}
                    name="use_pop_for_loc_weight"
                    checked={
                      settings[selectedSettingIndex].move_rules
                        .use_pop_for_loc_weight
                    }
                    disabled={true}
                  />
                </div>
                <div className="input-field-container">
                  <NumberInputField
                    label="Population Power For Location Weight"
                    infoText={popPowerForLocWeightText}
                    name="pop_power_for_loc_weight"
                    value={
                      settings[selectedSettingIndex].move_rules
                        .pop_power_for_loc_weight
                    }
                    disabled={true}
                  />
                </div>
              </div>

              <h3 className="page-subsubtitle">Movement Chance</h3>
              <div className="fields-container">
                <div className="input-field-container">
                  <NumberInputField
                    label="Conflict Movechance"
                    infoText={conflictMovechanceText}
                    name="conflict_movechance"
                    value={
                      settings[selectedSettingIndex].move_rules
                        .conflict_movechance
                    }
                    disabled={true}
                  />
                </div>
                <div className="input-field-container">
                    <NumberInputField 
                      label="Camp Movechance"
                      infoText={idpcampMovechanceText}
                      name="idpcamp_movechance"
                      value={settings[selectedSettingIndex].move_rules.idpcamp_movechance}
                      disabled={true}/>
                </div>
                <div className="input-field-container">
                  <NumberInputField
                    label="Default Movechance"
                    infoText={defaultMovechanceText}
                    name="default_movechance"
                    value={
                      settings[selectedSettingIndex].move_rules
                        .default_movechance
                    }
                    disabled={true}
                  />
                </div>
              </div>

              <h3 className="page-subsubtitle">Advanced</h3>
              <div className="fields-container">
                <div className="input-field-container">
                  <SelectInputField
                    label="Awareness Level"
                    infoText={awarenessLevelText}
                    name="awareness_level"
                    value={
                      settings[selectedSettingIndex].move_rules.awareness_level
                    }
                    options={awarenessLevelOptions}
                    disabled={true}
                  />
                </div>
                <div className="input-field-container">
                  <CheckboxInputField
                    label="Start On Foot"
                    infoText={startOnFootText}
                    name="start_on_foot"
                    checked={
                      settings[selectedSettingIndex].move_rules.start_on_foot
                    }
                    disabled={true}
                  />
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
                    name="displaced_per_conflict_day"
                    value={
                      settings[selectedSettingIndex].spawn_rules
                        .conflict_driven_spawning.displaced_per_conflict_day
                    }
                    disabled={true}
                  />
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
                    name="hasten"
                    value={settings[selectedSettingIndex].optimisations.hasten}
                    disabled={true}
                  />
                </div>
              </div>
            </div>
          </div>
        ) : (
          <span></span>
        )}

        <div className="buttons-container">
          <Link to={selectedSettingIndex === -1 ? "/settings/" : "/results"}>
            <button
              className="simple-button"
              disabled={
                selectedSettingIndex === -1 ||
                context.settingsId === "" ||
                context.inputId === ""
              }
              onClick={() => {
                sendRequest("/run_simulation/config", "POST", {
                  input: {
                    input_id: context.inputId,
                    input_name: context.inputName,
                  },
                  settings: {
                    simsettings_id: context.settingsId,
                    simsettings_name: context.settingsName,
                  },
                });

                navigate("/results");
              }}
            >
              Start Simulation
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Settings;
