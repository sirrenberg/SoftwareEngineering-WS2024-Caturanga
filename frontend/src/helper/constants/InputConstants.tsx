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
      date: "2023-01-01",
      length: 1,
    },
};

export const maxValues = {
    sim_period: {
      date: "2023-06-15",
      length: 547,
    },
};

export const startDateText =
`
The simulation will start on this date. The user can choose any date between 2023-01-01 and 2023-06-15
to ensure sufficient lead time for the simulation to run.
`
;

export const durationText =
`
The duration of the simulation in days. The user can choose any number between 1 and 547 days (1.5 years). 
`
;