# Project Structure

This document explains the structure of the Parcel Pilot application for the WGUPS Package Routing project.

## Root Directory

- `.gitignore`: Specifies files and directories to be ignored by Git.
- `README.md`: Provides an overview and documentation for the project.
- `requirements.txt`: Lists the Python dependencies required for the project.

## Directories

### inputs/

Contains raw data files used by the application.

- `WGUPS Distance Table.csv`: CSV file containing distance data.
- `WGUPS Package File.csv`: CSV file containing package data.

### meta/

Contains documentation for the project.

- `C950 Planning Requirements Overview (Task 1).md`: Provides an overview of the C950 Task 1 planning requirements.
- `C950 Software Requirements Overview (Task 2).md`: Provides an overview of the C950 Task 2 software requirements.
- `C950 Task 1 Rubric.md`: Contains the rubric for evaluating the C950 Task 1 project.
- `Javins C950 Core Algorithm Overview (Task 1).md`: Overview of the core algorithm for Task 1.
- `Notes.md`: Contains notes related to the project.
- `PROJECT_STRUCTURE.md`: Explains the structure of the WGUPS Package Routing project.
- `Summary and Plan of Action.md`: Summarizes the plan of action for the C950 Task 1 project.
- `WGU C950 Task 1 Overview.md`: Another overview document for the C950 Task 1 project.

### originals/

Contains original documents and resources related to the project.

- `C950 Task 1 overview.html`: HTML version of the C950 Task 1 overview.
- `Example Dijkstra's Algorithm.py`: Example implementation of Dijkstra's algorithm.
- `Sample Core Algorithm Overview.docx`: Sample document providing an overview of a core algorithm.
- `Sample Core Algorithm Overview.md`: Markdown version of the sample core algorithm overview.
- `SLC downtown map.docx`: Document containing a map of downtown Salt Lake City.
- `styles.3b37ccb6cd4e0563.css`: CSS file for styling the HTML documents.
- `WGUPS Distance Table.xlsx`: Excel file containing the distance table.
- `WGUPS Package File.xlsx`: Excel file containing the package data.

### parcel_pilot/

Main application directory, further divided into subdirectories.

- `__init__.py`: Initializes the parcel_pilot package.
- `helpers.py`: Provides utility functions for various tasks.
- `main.py`: The main entry point for running the application.

#### parcel_pilot/data/

Handles data loading and storage.

- `__init__.py`: Initializes the data package.
- `package_hash.py`: Implements a hash table for storing packages.
- `packages.py`: Represents individual packages.
- `graph.py`: Represents a directed graph with weighted edges.
- `truck_hash.py`: Implements a hash table for storing truck data.
- `trucks.py`: Manages truck data and operations.

#### parcel_pilot/router/

Manages routing logic and entities.

- `__init__.py`: Initializes the routing package.
- `distributor.py`: Manages the distribution of packages to trucks.
- `dijkstras_algorithm.py`: Implements Dijkstra's algorithm for finding the shortest path.
- `nearest_neighbor.py`: Implements the nearest neighbor algorithm for route planning.
- `nearness.py`: Implements an algorithm for sorting packages based on their proximity to a the depot.
- `package_handler.py`: Handles package data operations.

#### parcel_pilot/simulator/

Contains simulation-related classes and functions.

- `__init__.py`: Initializes the simulator package.
- `interface.py`: Provides the user interface for the time simulator and Parcel Pilot Dashboard.
- `time_sim.py`: Precomputes all simulation states and handles time calculations based on user input.
- `minutes.py`: Represents the state of packages and trucks for each minute in the simulation.