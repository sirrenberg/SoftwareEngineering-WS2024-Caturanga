import "../styles/Modal.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faX } from "@fortawesome/free-solid-svg-icons";
import { MapInputType, LocationType } from "../types";
import { getLocationColor } from "../helper/misc";

function MapLegendModal({
  setMapLegendModalOpen,
  mapInputType,
}: {
  setMapLegendModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
  mapInputType: MapInputType;
}) {
  return (
    <div className="modal-overlay">
      <div className="modal-container">
        <h2 className="modal-title">Map Legend</h2>
        <FontAwesomeIcon
          className="modal-close-icon"
          icon={faX}
          onClick={() => {
            setMapLegendModalOpen(false);
          }}
        />

        <div className="modal-content">
          <div className="modal-section">
            <h3 className="modal-section-title">Location Colors</h3>

            <div className="modal-section-content">
              <div className="legend-item">
                <div
                  className="legend-item-color"
                  style={{
                    backgroundColor: getLocationColor(LocationType.camp),
                  }}
                ></div>
                <div className="legend-item-text">Camp</div>
              </div>

              <div className="legend-item">
                <div
                  className="legend-item-color"
                  style={{
                    backgroundColor: getLocationColor(LocationType.town),
                  }}
                ></div>
                <div className="legend-item-text">Town</div>
              </div>

              <div className="legend-item">
                <div
                  className="legend-item-color"
                  style={{
                    backgroundColor: getLocationColor(
                      LocationType.conflict_zone
                    ),
                  }}
                ></div>
                <div className="legend-item-text">Conflict Zone</div>
              </div>

              <div className="legend-item">
                <div
                  className="legend-item-color"
                  style={{
                    backgroundColor: getLocationColor(
                      LocationType.forwarding_hub
                    ),
                  }}
                ></div>
                <div className="legend-item-text">Forwarding Hub</div>
              </div>
            </div>
          </div>

          <div className="modal-section">
            <h3 className="modal-section-title">Location Size</h3>

            <div className="modal-section-content">
              {mapInputType === MapInputType.results
                ? "The size of the location is proportional to the simulated number of IDPs"
                : "The size of the location is proportional to the initial population"}
            </div>
          </div>

          {mapInputType === MapInputType.results && (
            <div className="modal-section">
              <h3 className="modal-section-title">Play Bar Marks</h3>
              The play bar marks show dates at which validation data is
              available.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default MapLegendModal;
