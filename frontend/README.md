# Caturanga - Enhanced React Application Documentation

## Introduction

**Caturanga GUI** is a React-based Graphical User Interface designed to interact seamlessly with the [Flee Framework](https://flee.readthedocs.io/en/master/). This GUI empowers users to efficiently manage and manipulate Inputs and Settings, facilitating the start of IDP (Internally Displaced Persons) movement simulations. The simulation results are displayed on an interactive regional map, implemented using the [Leaflet library](https://leafletjs.com/reference.html).

## Codebase Overview

### Directory Structure

- `index.html`: The primary gateway to the application, setting the stage for user interaction.
- `main.tsx`: The uppermost React component, orchestrating the overall application behavior.
- `App.tsx`: A React component that encapsulates the entire application's functionality.
- `src/components`: A collection of reusable components, designed for efficiency and modularity.
- `src/contexts`: Contexts crafted to facilitate the flow of information across the application.
- `src/helper`: A repository of constants and utility functions, serving as the backbone for the application’s operations.
- `src/hooks`: Custom hooks, tailored to extend the application's capabilities.
- `src/pages`: Full-fledged page components corresponding to various navigational routes within the application.
- `src/styles`: CSS styles, enhancing the aesthetic appeal of components and pages.

### Routing

The application leverages React Router for navigational excellence:

- `/`: The Landing Page, welcoming users with its engaging interface.
- `/inputs`: The Inputs Menu, a hub for managing simulation inputs.
- `/inputs/{id}`: A specialized interface for Adding or Editing an individual Input.
- `/settings`: The Settings Menu, where users choose simulation parameters.
- `/settings/{id}`: An interface dedicated to Adding or Editing a specific Setting.
- `/results`: The Results Menu, showcasing simulation outcomes.
- `/results/{id}`: A detailed Results Page, offering an in-depth view of specific simulation results.
