import "../styles/Modal.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faX } from "@fortawesome/free-solid-svg-icons";
import { useForm } from "../hooks/useForm";
import { SimLocation, Input } from "../types";

function RouteModal({
  setRouteModalOpen,
  route,
  setSimValues,
  simValues,
}: {
  setRouteModalOpen: any;
  route: SimLocation | null;
  setSimValues: any;
  simValues: Input;
}) {
  const { values, handleInputChange } = useForm(route);

  console.log("values in Modal", values);
  console.log("simValues in Modal", simValues);

  if (!route) {
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
            setRouteModalOpen(false);
          }}
        />

        <div className="modal-form">
          <div className="fields-container">
            <div className="input-field-container">
              <label htmlFor="from">From</label>
              <input
                className="input-field"
                type="text"
                id="from"
                name="from"
                value={values.from}
                onChange={handleInputChange}
              />
            </div>

            {/* INput for to */}
            <div className="input-field-container">
              <label htmlFor="to">To</label>
              <input
                className="input-field"
                type="text"
                id="to"
                name="to"
                value={values.to}
                onChange={handleInputChange}
              />
            </div>
          </div>

          <div className="fields-container">
            <div className="input-field-container">
              <label htmlFor="distance">Distance (km)</label>
              <input
                className="input-field"
                type="number"
                id="distance"
                name="distance"
                value={values.distance}
                onChange={handleInputChange}
              />
            </div>
            <div className="input-field-container">
              <label htmlFor="forced_redirection">Forced Redirection</label>
              <input
                className="input-field"
                type="number"
                id="forced_redirection"
                name="forced_redirection"
                value={values.forced_redirection}
                onChange={handleInputChange}
              />
            </div>
          </div>
        </div>

        <button
          className="simple-button"
          onClick={() => {
            // add route to simvalues (overwrite if already exists)
            const newRoutes = simValues.routes.filter(
              (r) => r.from !== values.from && r.to !== values.to
            );
            newRoutes.push(values);
            setSimValues({ ...simValues, routes: newRoutes });
            setRouteModalOpen(false);
          }}
        >
          Save
        </button>
      </div>
    </div>
  );
}

export default RouteModal;
