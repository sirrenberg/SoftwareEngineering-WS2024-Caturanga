export const moveSpeedText = 
    `
    This refers to the most number of kilometers (km) to be traversed by IDPs per day. 
    The default value is 360 km per day, which refers to a speed of 30 km/hour for 12 hours.
    `
;

export const walkSpeedText = 
    `
    This refers to the most number of kilometers (km) to be traversed by IDPs per day on foot. 
    The default value is 35 km per day, which refers to a speed of 3.5 km/hour for 10 hours.
    `
;


// Location weights
// defaults? 

export const conflictWeightText =
    `
    This refers to the attraction multiplier for conflict locations (conflict zones).
    `
;

export const campWeightText =
    `
    This refers to the attraction multiplier for camp locations (camps).
    `
;

// what does foreign location mean? and what does stacked mean
export const foreignWeightText =
    `
    This refers to the attraction multiplier for foreign locations, which is added to the camp multiplier.
    `
;

export const usePopForLocWeightText =
    `
    This parameter, if checked, includes location population as a weighting factor for non-camp locations.
    `
;

export const popPowerForLocWeightText =
    `
    This refers to a power factor that adjusts how heavily population is accounted for,
    when "Use Population For Location Weight" is enabled. 
    By default it is set to 0.1, 
    which weights a location with 1M population twice as heavily as a location with 1000 population. 
    I.e.: 1000^0.1 = 1.99, 1000000^0.1 = 3.98.
    `
;

export const conflictMovechanceText =
    `
    This is the chance (probability) of IDPs leaving a conflict location (conflict zone) per day.
    `
;

export const campMovechanceText = 
    `
    This is the chance (probability) of IDPs leaving a camp location per day.
    `
;

export const defaultMovechanceText =
    `
    This is the chance (probability) of IDPs leaving a regular location (i.e., town) per day.
    `
;

export const awarenessLevelText =
    `
    This parameter is used to adjust the IDPs awareness of locations by incorporating a more wide or narrow awareness level.
    `
;

export const capacityScalingText =
    `
    This refers to the scaling factor for the capacity of camp locations.
    `
;

export const avoidShortStintsText =
    `
    This parameter, if checked, prevents IDPs from moving to a location for less than 1 day.
    `
;

export const startOnFootText =
    `
    This parameter, if checked, forces IDPs to start their journey on foot.
    `
;

export const weightPowerText =
    `
    This refers to the power factor that adjusts how heavily the distance between locations is accounted for.
    `
;

export const hastenText =
    `
    This is a parameter that can be used to speed up the simulation. 
    The default is 1.0. 
    By setting it to a larger value, the simulation will proportionally reduce its number of IDPs,
    speeding up execution. When using a value for hasten larger than 1.0, 
    the simulation becomes gradually less accurate and 
    will exhibit more variability in its results between individual runs.
    `
;