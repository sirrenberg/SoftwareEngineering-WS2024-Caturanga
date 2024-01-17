import { faX } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

function InputDeletionConfirmation({
  performInputDeletion,
  abortInputDeletion,
} : {
  performInputDeletion : () => void,
  abortInputDeletion : () => void,
}) {

  return (
    <div className="modal-overlay">
      <div className="modal-container">
        <h2 className="modal-title">Attention!</h2>
        <FontAwesomeIcon
          className="modal-close-icon"
          icon={faX}
          onClick={() => {abortInputDeletion();}}
        />

        <div className="model-content">
          <div className="modal-section">
            <p>
              Deleting this input will also delete all simulation results that were generated based on this input.
              <br/><br/>
              Are you sure?
            </p>
            <button
              className="simple-button"
              onClick={() => {performInputDeletion();}}
            >
              <p>I am sure</p>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default InputDeletionConfirmation;
