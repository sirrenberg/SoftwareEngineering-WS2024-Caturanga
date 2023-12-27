import "../styles/Modal.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faX } from "@fortawesome/free-solid-svg-icons";
import { useForm } from "../hooks/useForm";
import { SimLocation, Input } from "../types";

function LocationModal({
  isLocationModalOpen,
  setLocationModalOpen,
  location,
  setSimValues,
  simValues,
}: {
  isLocationModalOpen: boolean;
  setLocationModalOpen: any;
  location: SimLocation | null;
  setSimValues: any;
  simValues: Input;
}) {
  const {
    values,
    setValues,
    handleInputChange,
    handlePrefillData,
    handleSubmit,
  } = useForm(location);

  console.log("values in Modal", values);
  console.log("simValues in Modal", simValues);

  if (!location) {
    return null;
  }

  return (
    <div className="modal-overlay">
      <div className="modal-container">
        <h2 className="modal-title">Location Details</h2>
        <FontAwesomeIcon
          className="modal-close-icon"
          icon={faX}
          onClick={() => {
            setLocationModalOpen(false);
          }}
        />

        <div className="modal-form">
          <div className="fields-container">
            <div className="input-field-container">
              <label htmlFor="name">Name</label>
              <input
                className="input-field"
                type="text"
                id="name"
                name="name"
                value={values.name}
                onChange={handleInputChange}
              />
            </div>

            {/* INput for region */}
            <div className="input-field-container">
              <label htmlFor="region">Region</label>
              <input
                className="input-field"
                type="text"
                id="region"
                name="region"
                value={values.region}
                onChange={handleInputChange}
              />
            </div>
            {/* INput for country */}
            <div className="input-field-container">
              <label htmlFor="country">Country</label>
              <input
                className="input-field"
                type="text"
                id="country"
                name="country"
                value={values.country}
                onChange={handleInputChange}
              />
            </div>
          </div>

          <div className="fields-container">
            <div className="input-field-container">
              <label htmlFor="latitude">Latitude</label>
              <input
                className="input-field"
                type="number"
                id="latitude"
                name="laltitude"
                value={values.latitude}
                onChange={handleInputChange}
              />
            </div>
            <div className="input-field-container">
              <label htmlFor="longitude">Longitude</label>
              <input
                className="input-field"
                type="number"
                id="longitude"
                name="longitude"
                value={values.longitude}
                onChange={handleInputChange}
              />
            </div>
          </div>

          <div className="fields-container">
            <div className="input-field-container">
              <label htmlFor="location_type">Location Type</label>
              <select
                className="input-field"
                id="location_type"
                name="location_type"
                value={values.location_type}
                onChange={handleInputChange}
              >
                <option value="conflict_zone">Conflict Zone</option>
                <option value="town">Town</option>
                <option value="forwarding_hub">Forwarding Hub</option>
                <option value="camp">Camp</option>
              </select>
            </div>
            <div className="input-field-container">
              <label htmlFor="population">Population</label>
              <input
                className="input-field"
                type="number"
                id="population"
                name="population"
                value={values.population}
                onChange={handleInputChange}
              />
            </div>
          </div>
        </div>

        <button
          className="simple-button"
          onClick={() => {
            setSimValues({
              ...simValues,
              locations: [
                ...simValues.locations.filter(
                  (loc: SimLocation) => loc.name !== location.name
                ),
                values,
              ],
            });
            setLocationModalOpen(false);
          }}
        >
          Save
        </button>
      </div>
    </div>
  );
}

export default LocationModal;
