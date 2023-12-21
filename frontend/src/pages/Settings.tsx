import { InputAdornment, Stack } from "@mui/material";
import TextField from "@mui/material/TextField";

function Settings() {
  return (
    <div className="content-page">
      <Stack spacing={3}>
        <TextField
          id="max-move-speed"
          label="Max Move Speed"
          type="number"
          defaultValue="360"
          InputProps={{
            endAdornment: <InputAdornment position="end">km</InputAdornment>
          }}
          helperText="the maximum number of kilometers expected to be travelled by IDPs per time step (30 km /h for 12 hours)"
        />
        <TextField
          id="max-walk-speed"
          label="Max Walk Speed"
          type="number"
          defaultValue="35"
          InputProps={{
            endAdornment: <InputAdornment position="end">km</InputAdornment>
          }}
          helperText="the maximum number of kilometers expected to be travelled per time step on foot (3.5 km/h for 10 hours)"
        />
      </Stack>
    </div>
  );
}

export default Settings;
