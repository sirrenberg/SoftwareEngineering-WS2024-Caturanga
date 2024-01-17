import { faX } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

function InputDeletionConfirmation({
  setInputDeletionConfirmationActive,
  performInputDeletion,
} : {
  setInputDeletionConfirmationActive : React.Dispatch<React.SetStateAction<boolean>>,
  performInputDeletion : () => void
}) {

  return (
    <div className="modal-overlay">
      <div className="modal-container">
        <FontAwesomeIcon
          className="modal-close-icon"
          icon={faX}
          onClick={() => {setInputDeletionConfirmationActive(false);}}
        />

        <div className="modal-content">
          <div className="modal-section">
            <p>
              <strong>Attention! </strong>
              Deleting this input will also delete all simulation results that were generated based on this input.
              Are you sure you want to delete the input along with all results generated based on it?
            </p>
            <button
              className="simple-button"
              onClick={() => {
                performInputDeletion();
                setInputDeletionConfirmationActive(false);
              }}
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
