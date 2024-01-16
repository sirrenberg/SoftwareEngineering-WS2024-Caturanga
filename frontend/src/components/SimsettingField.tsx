import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import Tooltip from '@mui/material/Tooltip';

interface SimsettingFieldWrapperProps {
    label: string;
    infoText: string;
    children: React.ReactNode;
}

function SimsettingFieldWrapper(props: Readonly<SimsettingFieldWrapperProps>) {
    return (
        <label>
            {props.label}
            <Tooltip title={props.infoText} placement="top">
                <FontAwesomeIcon style={{paddingLeft: '10px'}} icon={faCircleInfo} className="item-icon"/>
            </Tooltip>
            <br />
            {props.children}
        </label>
    )
}

interface Props {
    label: string;
    infoText: string;
    name: string;
    disabled: boolean;
    onChange?: (e: React.ChangeEvent<HTMLInputElement> | React.ChangeEvent<HTMLSelectElement>) => void;
}

interface CheckboxInputFieldProps extends Props {
    checked: boolean;
}

interface NumberInputFieldProps extends Props {
    value: number;
    min?: number;
    max?: number;
}

interface SelectInputFieldProps extends Props {
    value: number;
    options: {value: number, label: string}[];
}

interface DateInputFieldProps extends Props {
    value: string;
    min?: string;
    max?: string;
}


export function CheckboxInputField(props: Readonly<CheckboxInputFieldProps>) {
    return (
        <SimsettingFieldWrapper label={props.label} infoText={props.infoText}>
            <input 
                className="input-field"
                type="checkbox"
                name={props.name}
                checked={props.checked}
                disabled={props.disabled}
                onChange={props.onChange}
            />
        </SimsettingFieldWrapper>
    
    )
}

export function NumberInputField(props: Readonly<NumberInputFieldProps>) {
    return (
        <SimsettingFieldWrapper label={props.label} infoText={props.infoText}>
            <input
                className="input-field"
                type="number"
                name={props.name}
                value={props.value}
                min={props.min}
                max={props.max}
                placeholder="0"
                disabled={props.disabled}
                onChange={props.onChange}
            />
        </SimsettingFieldWrapper>
    )
}

export function SelectInputField(props: Readonly<SelectInputFieldProps>) {
    return (
        <SimsettingFieldWrapper label={props.label} infoText={props.infoText}>
            <select
                className="input-field"
                name={props.name}
                disabled={props.disabled}
                onChange={props.onChange}
                value={props.value}
            >
                {props.options.map((option) => (
                    <option key={option.value} value={option.value}>
                        {option.label}
                    </option>
                ))}
            </select>
        </SimsettingFieldWrapper>
    )
}

export function DateInputField(props: Readonly<DateInputFieldProps>) {
    return (
        <SimsettingFieldWrapper label={props.label} infoText={props.infoText}>
            <input
                className="input-field"
                type="date"
                name={props.name}
                value={props.value}
                min={props.min}
                max={props.max}
                disabled={props.disabled}
                onChange={props.onChange}
            />
        </SimsettingFieldWrapper>
    )
}
