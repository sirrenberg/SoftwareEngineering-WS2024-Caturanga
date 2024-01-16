import "../styles/Modal.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faX } from "@fortawesome/free-solid-svg-icons";

function DataSourceModal({
  setDataSourceModalOpen,
  acled_url,
  acled_last_update_date,
  population_url,
  population_last_update_date,
  camp_url,
  camp_last_update_date,
}: {
  setDataSourceModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
  acled_url: string;
  acled_last_update_date: string;
  population_url: string;
  population_last_update_date: string;
  camp_url: string;
  camp_last_update_date: string;
}) {
  return (
    <div className="modal-overlay">
      <div className="modal-container">
        <h2 className="modal-title">Data Sources</h2>
        <FontAwesomeIcon
          className="modal-close-icon"
          icon={faX}
          onClick={() => {
            setDataSourceModalOpen(false);
          }}
        />

        <div className="modal-content">
          <div className="modal-section">
            <h3 className="modal-section-title">Conflicts</h3>
            <p>
              <strong>Source:</strong> <a href={acled_url}>{acled_url}</a>
            </p>
            <p>
              <strong>Last updated:</strong>{" "}
              {acled_last_update_date.slice(0, 10)}
            </p>
          </div>
          <div className="modal-section">
            <h3 className="modal-section-title">Population</h3>
            <p>
              <strong>Source:</strong>{" "}
              <a href={population_url}>{population_url}</a>
            </p>
            <p>
              <strong>Last updated:</strong>{" "}
              {population_last_update_date.slice(0, 10)}
            </p>
          </div>
          <div className="modal-section">
            <h3 className="modal-section-title">Camps</h3>
            <p>
              <strong>Source:</strong> <a href={camp_url}>{camp_url}</a>
            </p>
            <p>
              <strong>Last updated:</strong>{" "}
              {camp_last_update_date.slice(0, 10)}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DataSourceModal;
