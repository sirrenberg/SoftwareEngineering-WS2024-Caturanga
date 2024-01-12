import "../styles/Menu.css";
import { useEffect, useState, useContext } from "react";
import { StartSimContext } from "../contexts/StartSimContext";
import { SimSettings } from "../types";
import { Link } from "react-router-dom";
import { useAPI } from "../hooks/useAPI";
import { NavLink } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPenToSquare, faTrash } from "@fortawesome/free-solid-svg-icons";

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

          {settings.length === 0 && 
          <h3>Loading...</h3>
          }

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
                      value={settings[selectedSettingIndex].log_levels.agent}
                      disabled={true}
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
                      value={settings[selectedSettingIndex].log_levels.link}
                      disabled={true}
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
                      value={settings[selectedSettingIndex].log_levels.camp}
                      disabled={true}
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
                      value={settings[selectedSettingIndex].log_levels.conflict}
                      disabled={true}
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
                      value={settings[selectedSettingIndex].log_levels.init}
                      disabled={true}
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
                      value={
                        settings[selectedSettingIndex].log_levels.idp_totals
                      }
                      disabled={true}
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
                      value={
                        settings[selectedSettingIndex].log_levels.granularity
                      }
                      disabled={true}
                    />
                  </label>
                </div>
              </div>
            </div>

            <div className="spawn-rules-container settings-input-section">
              <h2 className="page-subtitle">Spawn Rules</h2>
              <div className="fields-container">
                <div className="input-field-container">
                  <label htmlFor="" className="checkbox-label">
                    Take From Population: <br />
                    <input
                      className="input-field"
                      type="checkbox"
                      placeholder="0"
                      name="take_from_population"
                      checked={
                        settings[selectedSettingIndex].spawn_rules
                          .take_from_population
                      }
                      disabled={true}
                    />
                  </label>
                </div>
                <div className="input-field-container">
                  <label htmlFor="" className="checkbox-label">
                    Insert Day0: <br />
                    <input
                      className="input-field"
                      type="checkbox"
                      placeholder="0"
                      name="take_from_population"
                      checked={
                        settings[selectedSettingIndex].spawn_rules.insert_day0
                      }
                      disabled={true}
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
                      value={
                        settings[selectedSettingIndex].move_rules.max_move_speed
                      }
                      disabled={true}
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
                      value={
                        settings[selectedSettingIndex].move_rules.max_walk_speed
                      }
                      disabled={true}
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
                      value={
                        settings[selectedSettingIndex].move_rules.foreign_weight
                      }
                      disabled={true}
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
                      value={
                        settings[selectedSettingIndex].move_rules
                          .conflict_weight
                      }
                      disabled={true}
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
                      value={
                        settings[selectedSettingIndex].move_rules.camp_weight
                      }
                      disabled={true}
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
                      value={
                        settings[selectedSettingIndex].move_rules
                          .conflict_movechance
                      }
                      disabled={true}
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
                      value={
                        settings[selectedSettingIndex].move_rules
                          .camp_movechance
                      }
                      disabled={true}
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
                      value={
                        settings[selectedSettingIndex].move_rules
                          .default_movechance
                      }
                      disabled={true}
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
                      value={
                        settings[selectedSettingIndex].move_rules
                          .awareness_level
                      }
                      disabled={true}
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
                      value={
                        settings[selectedSettingIndex].move_rules
                          .capacity_scaling
                      }
                      disabled={true}
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
                      value={
                        settings[selectedSettingIndex].move_rules.weight_power
                      }
                      disabled={true}
                    />
                  </label>
                </div>
              </div>

              <div className="fields-container">
                <div className="input-field-container">
                  <label htmlFor="" className="checkbox-label">
                    Avoid Short Stints: <br />
                    <input
                      className="input-field"
                      type="checkbox"
                      placeholder="0"
                      name="avoid_short_stints"
                      checked={
                        settings[selectedSettingIndex].move_rules
                          .avoid_short_stints
                      }
                      disabled={true}
                    />
                  </label>
                </div>
                <div className="input-field-container">
                  <label htmlFor="" className="checkbox-label">
                    Start On Foot: <br />
                    <input
                      className="input-field"
                      type="checkbox"
                      placeholder="0"
                      name="start_on_foot"
                      checked={
                        settings[selectedSettingIndex].move_rules.start_on_foot
                      }
                      disabled={true}
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
                      value={
                        settings[selectedSettingIndex].optimisations.hasten
                      }
                      disabled={true}
                    />
                  </label>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <span></span>
        )}

        <div className="buttons-container">
          <Link
            to={selectedSettingIndex === -1 ? "/settings/" : "/results"}
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
