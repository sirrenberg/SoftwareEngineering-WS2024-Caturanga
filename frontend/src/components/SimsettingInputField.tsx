import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import Tooltip from '@mui/material/Tooltip';

interface props {
    label: string;
    infoText: string;
    checkBox: boolean;
    name: string;
    value?: number;
    checked?: boolean;
    disabled: boolean;
    onChange?: (e: React.ChangeEvent<HTMLInputElement> | React.ChangeEvent<HTMLSelectElement>) => void;
}

function SimsettingInputField(props: props) {
    return (
        <label htmlFor="">
            {props.label}
            <Tooltip title={props.infoText} placement="top">
                <FontAwesomeIcon style={{paddingLeft: '10px'}} icon={faCircleInfo} className="item-icon"/>
            </Tooltip>
            <br />
            <input
                className="input-field"
                type={props.checkBox ? "checkbox" : "number"}
                placeholder="0"
                name={props.name}
                value={props.checkBox ? undefined : props.value}
                checked={props.checkBox ? props.checked : undefined}
                disabled={props.disabled}
                onChange={props.onChange}
            />
        </label>
    )
}

export default SimsettingInputField;