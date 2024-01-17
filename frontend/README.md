# Caturanga - React Application Documentation

## Introduction

**Caturanga GUI** is a React-based Graphical User Interface designed to interact seamlessly with our Simulation Framework for Conflict-Driven Displacement based on the [Flee Framework](https://flee.readthedocs.io/en/master/). This GUI enables users to efficiently manage and manipulate Inputs and Settings, facilitating the start of IDP (Internally Displaced Persons) movement simulations. The simulation results are displayed on an interactive regional map, implemented using the [Leaflet library](https://leafletjs.com/reference.html).

## Codebase Overview

### Directory Structure

- `index.html`: The primary gateway to the application.
- `main.tsx`: The uppermost React component, managing the overall application behavior.
- `App.tsx`: A React component that encapsulates the entire application's functionality and routing structure.
- `src/components`: A collection of reusable components, designed for efficiency and modularity.
- `src/contexts`: Contexts crafted to facilitate the flow of information across the application.
- `src/helper`: Constants and utility functions.
- `src/hooks`: Custom hooks, tailored to extend the application's capabilities.
- `src/pages`: Page components corresponding to the navigational routes within the application.
- `src/styles`: CSS styles, enhancing the aesthetic appeal of components and pages.

### Routing

The application leverages React Router for navigational purposes:

- `/`: The Landing Page, welcoming users with its engaging interface.
- `/inputs`: The Inputs Menu for managing and choosing simulation inputs.
  The input is visualized on a map.
- `/inputs/{id}`: A specialized interface for Adding or Editing an individual Input.
- `/settings`: The Settings Menu for managing and choosing simulation settings.
  The different parameters are explained and displayed in a structured way.
- `/settings/{id}`: An interface dedicated to Adding or Editing an individual Setting.
- `/results`: The Results Menu for managing and choosing simulation results.
  The used input is visualized on a map as a preview.
- `/results/{id}`: A detailed Results Page, offering an in-depth visualization of specific simulation results.
