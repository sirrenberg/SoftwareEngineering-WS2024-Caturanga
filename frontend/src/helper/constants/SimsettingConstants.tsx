import { SimSettings } from "../../types";

export const defaultValues: SimSettings = {
    _id: "",
    name: "untitled",
    spawn_rules: {
        conflict_driven_spawning: {
            spawn_mode: "pop_ratio",
            displaced_per_conflict_day: 0.01
        },
        insert_day0: false,
    },
    move_rules: {
      max_move_speed: 360,
      max_walk_speed: 35,
      foreign_weight: 1,
      conflict_weight: 0.25,
      camp_weight: 1,
      use_pop_for_loc_weight: false,
      pop_power_for_loc_weight: 0.1,
      conflict_movechance: 1,
      camp_movechance: 0.001,
      idpcamp_movechance: 0.1,
      default_movechance: 0.3,
      awareness_level: 1,
      capacity_scaling: 1,
      avoid_short_stints: false,
      start_on_foot: false,
      weight_power: 1,
    },
    optimisations: {
      hasten: 1,
    },
  };

  export const maxValues = {
    spawn_rules: {
        conflict_driven_spawning: {
            displaced_per_conflict_day: 0.1
        }
    },
    move_rules: {
      max_move_speed: 1000,
      max_walk_speed: 1000,
      foreign_weight: 100,
      conflict_weight: 100,
      camp_weight: 100,
      pop_power_for_loc_weight: 100,
      conflict_movechance: 1,
      idpcamp_movechance: 1,
      camp_movechance: 1,
      default_movechance: 1,
      capacity_scaling: 10,
      weight_power: 10,
    },
    optimisations: {
      hasten: 1000,
    },
  };

export const awarenessLevelOptions = 
[{value: -1, label: "No awareness"},
 {value: 0, label: "The length of the road to the closest settlement"}, 
 {value: 1, label: "The type of the closest settlement"},
 {value: 2, label: "The type of the settlement adjacent to neighboring settlements"},
 {value: 3, label: "The type of the settlements neighboring neighbors of neighbors"}]

export const moveSpeedText = 
    `
    This refers to the maximum number of kilometers (km) that the simulated IDPs can travel per day.
    The default value is ${defaultValues.move_rules.max_move_speed} km per day,
    which corresponds to a speed of 30 km/hour for 12 hours.
    `
;

export const walkSpeedText = 
    `
    This refers to the maximum number of kilometers (km) that simulated IDPs are able to walk per day. 
    This speed applies only when leaving an IDP camp and only for the first route traveled.
    The default value is ${defaultValues.move_rules.max_walk_speed} km per day,
    which corresponds to a speed of 3.5 km/hour for 10 hours.
    `
;

export const conflictWeightText =
    `
    This refers to the attraction multiplier for conflict zones.
    The default is ${defaultValues.move_rules.conflict_weight}.
    `
;

export const campWeightText =
    `
    This refers to the attraction multiplier for IDP camps.
    The default is ${defaultValues.move_rules.camp_weight}, which means there is no effect.
    `
;

export const foreignWeightText =
    `
    This refers to the attraction multiplier for foreign locations, which is added to the camp multiplier.
    The default is ${defaultValues.move_rules.foreign_weight}, which means there is no effect.
    `
;

export const usePopForLocWeightText =
    `
    This parameter, if checked, includes location population as a weighting factor for non-camp locations.
    See "Population Power For Location Weight" for more details.
    By default this is ${defaultValues.move_rules.use_pop_for_loc_weight ? "checked" : "NOT checked"}.
    `
;

export const popPowerForLocWeightText =
    `
    This refers to a power factor that adjusts how heavily population is accounted for,
    when "Use Population For Location Weight" is enabled. 
    By default it is set to ${defaultValues.move_rules.pop_power_for_loc_weight}, 
    which weights a location with 1M population twice as heavily as a location with 1000 population. 
    I.e.: 1000^0.1 = 1.99, 1000000^0.1 = 3.98.
    `
;

export const conflictMovechanceText =
    `
    This is the chance (probability) of simulated IDPs leaving a conflict zone per day.
    The default value is ${defaultValues.move_rules.conflict_movechance}, i.e., 100%. 
    Therefore simulated IDPs will always leave conflict zones.
    `
;

export const idpcampMovechanceText = 
    `
    This is the chance (probability) of simulated IDPs leaving an IDP camp per day.
    The default value is ${defaultValues.move_rules.idpcamp_movechance}, i.e., 10%.
    Therefore, simulated IDPs tend to stay in camps.
    `
;

export const defaultMovechanceText =
    `
    This is the chance (probability) of simulated IDPs leaving a regular location (i.e., town) per day.
    The default value is ${defaultValues.move_rules.default_movechance}, i.e., 30%.
    `
;

export const awarenessLevelText =
    `
    This parameter is used to adjust the simulated IDPs' awareness for neighboring locations by setting a wider or narrower awareness level. 
    Settlements are divided into following three types: camps, towns, conflict zones. 
    The default value is: "${awarenessLevelOptions[defaultValues.move_rules.awareness_level+1].label}".
    `
;

export const startOnFootText =
    `
    This parameter, if checked, forces simulated IDPs to start their journey on foot.
    By default it is ${defaultValues.move_rules.start_on_foot ? "checked" : "NOT checked"}.
    `
;


export const displacedPerConflictDayText =
    `
    This parameter refers to the percentage of the population in a conflict zone that are displaced per day. 
    The default value is ${defaultValues.spawn_rules.conflict_driven_spawning.displaced_per_conflict_day},
    which means that 1% of the population is displaced per day, for a conflict weight of 1.0.
    Warning: The higher the value, the more  simulated IDPs will be spawned, and the longer the simulation will take.
    Thus the maximum value is limited to 10%. Be careful when increasing this value, and consider adjusting
    the hasten parameter accordingly.
    `
;

export const hastenText =
    `
    This parameter can be used to speed up the simulation. 
    The default is ${defaultValues.optimisations.hasten}. 
    Setting it to a higher value will proportionally reduce the number of simulated IDPs, speeding up execution.
    Warning: When using a value greater than 1.0, 
    the simulation will gradually become less accurate and 
    will show more variability in its results when comparing multiple runs.
    `
;

export const movementRulesText =
    `
    The following section contains the parameters that influence simulated IDPs' movement during the simulation.
    Each parameter is explained in detail by clicking on the information icon next to it.
    `
;

export const optimisationsText =
    `
    The following section contains the parameter that can improve the simulation's runtime.
    `
;

export const spawnRulesText = 
    `
    To be considered for the simulation, simulated IDP have to be spawned within the region first. 
    The following section contains the parameters that influence their spawning during the simulation.
    `
;