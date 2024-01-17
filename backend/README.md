# Backend Architecture

## API

main.py is the entry point to our backend and serves as our API. 

## Controller

### Simulation Executor

This component is responsible for all necessary preparations required to execute a simulation.

### Data Extractor

This module is tasked with fetching the latest ACLED conflict and population data, and storing this information in the database. The stored data is subsequently utilized for simulations.

### Database Handler

This component is dedicated to the retrieval and storage of data within the database.

### Filesystem Handler

The role of this class is to store database data into the filesystem, enabling its use by FLEE.

### CSV Transformer

This class, utilized by the filesystem handler, is responsible for transforming the database data into CSV format.

## FLEE 

In our project, we utilize FLEE, an agent-based modelling toolkit specifically designed for simulating the movement of individuals across geographical locations. Our primary use case is to model the movement of Internally Displaced Persons (IDPs) in Ethiopia.

We have adapted the FLEE toolkit to better suit our specific needs. Notably, we have modified the runscript to enable execution and result retrieval without the necessity for validation files. Our customized version of FLEE is available at https://github.com/nicleosch/flee.

For comprehensive details on the FLEE toolkit, please refer to the official FLEE documentation https://flee.readthedocs.io/en/master/.

### How to use FLEE

### Submodule Instructions

You might see an empty FLEE folder when pulling the repository for the first time. To solve this problem, execute the following command in the root folder of this repository:

```git submodule update --init --recursive```

Also, in order to keep FLEE updated, run following command regularly:

```git submodule update --remote```

### FLEE Interaction

Our interface to FLEE is the FLEE Adapter, which is responsible for executing FLEE and handling any errors that may occur during its operation.
