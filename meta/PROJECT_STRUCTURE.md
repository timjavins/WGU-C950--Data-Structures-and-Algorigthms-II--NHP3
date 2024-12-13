# Project Structure

This document explains the structure of the WGUPS Package Routing project.

## Root Directory

- `.gitignore`: Specifies files and directories to be ignored by Git.
- `LICENSE.md`: Contains the license information for the project.
- `Makefile`: Defines tasks for building, running, and generating PDFs.
- `README.md`: Provides an overview and documentation for the project.
- `requirements.txt`: Lists the Python dependencies required for the project.

## Directories

### inputs/

Contains raw data files used by the application.

- `WGUPS Distance Table.csv`: CSV file containing distance data.
- `WGUPS Package File.csv`: CSV file containing package data.

### meta/

Contains documentation for the project.

- `C950 Task 1 Overview.md`: Provides an overview of the C950 Task 1 project.
- `C950 Task 1 Rubric.md`: Contains the rubric for evaluating the C950 Task 1 project.
- `PROJECT_STRUCTURE.md`: Explains the structure of the WGUPS Package Routing project.
- `Summary and Plan of Action.md`: Summarizes the plan of action for the C950 Task 1 project.
- `WGU C950 Task 1 Overview.md`: Another overview document for the C950 Task 1 project.

### originals/

Contains original documents and resources related to the project.

- `C950 Task 1 overview.html`: HTML version of the C950 Task 1 overview.
- `Sample Core Algorithm Overview.docx`: Sample document providing an overview of a core algorithm.
- `Sample Core Algorithm Overview.md`: Markdown version of the sample core algorithm overview.
- `SLC downtown map.docx`: Document containing a map of downtown Salt Lake City.
- `styles.3b37ccb6cd4e0563.css`: CSS file for styling the HTML documents.
- `WGUPS Distance Table.xlsx`: Excel file containing the distance table.
- `WGUPS Package File.xlsx`: Excel file containing the package data.

### scripts/

Contains scripts for generating assets and converting markdown to PDF.

- `chapter_break.tex`: LaTeX file for chapter breaks in the PDF.
- `inline_code.tex`: LaTeX file for inline code formatting in the PDF.
- `md2pdf.sh`: Shell script for converting markdown to PDF using Pandoc.

### wgups/

Main application directory, further divided into subdirectories.

- `__init__.py`: Initializes the wgups package.
- `__main__.py`: Entry point for running the application.

#### wgups/data/

Handles data loading and storage.

- `__init__.py`: Initializes the data package.
- `data_loader.py`: Loads external data into the application.
- `distance_table.py`: Stores distances between destinations.
- `package_table.py`: Manages packages to be delivered.

#### wgups/routing/

Manages routing logic and entities.

- `__init__.py`: Initializes the routing package.
- `depot.py`: Central hub for route planning and package distribution.
- `package.py`: Represents individual packages.
- `truck.py`: Represents delivery trucks.

#### wgups/structures/

Contains custom data structures.

- `__init__.py`: Initializes the structures package.
- `clock.py`: Represents a time in minutes since the start of the delivery period.
- `hash_set.py`: Implementation of a hash table using linear probing.

#### wgups/utils/

Utility classes and functions.

- `__init__.py`: Initializes the utils package.
- `application.py`: Main application class that initializes and runs the program.
- `commander.py`: Handles command-line commands.
- `prompter.py`: Manages user input.
- `spinner.py`: Displays a loading spinner in the console.

## Example Usage

To run the application, use the following command:

```sh
python3 -m wgups