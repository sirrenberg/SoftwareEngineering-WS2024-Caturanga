import "../styles/AddInput.css";
import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { useForm } from "../hooks/useForm";
import { formatDate } from "../helper/misc";
import {
  DateInputField,
  NumberInputField,
} from "../components/SimsettingField";
import { defaultValues } from "../helper/constants/InputConstants";
import {
  durationText,
  maxValues,
  minValues,
  startDateText,
} from "../helper/constants/InputConstants";

// Page to add a new input or edit an existing one
function AddInput() {
  const [submitted, setSubmitted] = useState<boolean>(false);
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const isNewInput = id === "new";

  const initialValues = defaultValues;

  const { values, handleInputChange, handlePrefillData, handleSubmit } =
    useForm(initialValues);

  useEffect(() => {
    if (!isNewInput) {
      handlePrefillData(`/simulations/${id}`);
    }
  }, []);

  // if editing existing input and data is not loaded yet
  if (!isNewInput && values._id === "") {
    return <div>Loading...</div>;
  }

  return (
    <div className="add-input-container content-page">
      <h1 className="page-title">
        {isNewInput ? "New Input: " : "Edit Input: "}
      </h1>

      <div className="duration-container add-input-section">
        <h2 className="page-subtitle">Name & Region</h2>
        <div className="name-fields-container fields-container">
          <div className="input-field-container">
            <label htmlFor="">
              Name <br />
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
          <div className="input-field-container">
            <label htmlFor="">
              Region <br />
              <input
                className="input-field"
                type="text"
                name="region"
                value={values.region}
                disabled={true}
              />
            </label>
          </div>
        </div>
      </div>

      <div className="sim-period-container add-input-section">
        <h2 className="page-subtitle">Simulation Period</h2>

        <div className="sim-period-fields-container fields-container">
          <div className="input-field-container">
            <DateInputField
              label="Start Date"
              infoText={startDateText}
              name="date"
              value={formatDate(values.sim_period["date"])}
              disabled={true}
            />
          </div>
          <div className="input-field-container">
            <NumberInputField
              label="Duration"
              infoText={durationText}
              onChange={handleInputChange}
              name="length"
              value={values.sim_period["length"]}
              disabled={false}
              min={minValues.sim_period["length"]}
              max={maxValues.sim_period["length"]}
            />
          </div>
        </div>
      </div>

      <div className="submit-button-container add-input-section">
        <button
          className="simple-button"
          disabled={submitted}
          onClick={(e) => {
            setSubmitted(true);
            handleSubmit(e, "/simulations", "POST", () => {navigate("/inputs");});
          }}
        >
          Save
        </button>
      </div>
    </div>
  );
}

export default AddInput;
