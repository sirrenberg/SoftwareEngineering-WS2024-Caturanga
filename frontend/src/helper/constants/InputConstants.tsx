import { Input } from "../../types";

export const defaultValues: Input = {
    _id: "",
    name: "untitled",
    region: "Ethiopia",
    sim_period: {
      date: "2023-01-01",
      length: 1,
    },
    locations: [],
    routes: []
};

export const minValues = {
    sim_period: {
      length: 1,
    },
};

export const maxValues = {
    sim_period: {
      length: 547,
    },
};

export const startDateText =
`
The simulation starts on this date. This date was chosen to ensure sufficient lead time for the simulation,
to be able to make a prediction on the basis of a validated simulation.
`
;

export const durationText =
`
The duration of the simulation in days. The user can choose any number between 1 and 547 days (1.5 years). 
To set the simulation period to a value, which doesn't start with 1 (e.g. 200, 300 445, 556),
please use the arrows to set the first digit before typing in the rest of your intended simulation period.
`
;