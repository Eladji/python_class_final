
# Space Fleet Manager

A Python-based space fleet management system with a Text User Interface (TUI), built using the [Textual](https://textual.textualize.io/) library.

## Features

### Fleet Management
- Create and manage multiple fleets
- Add/remove spaceships to fleets
- Track fleet statistics
- Rename fleets

### Ship Management
- Add different types of ships (Transport, War)
- Track ship status (Operational, Damaged)
- Manage crew assignments
- Check ship preparation status

### Crew Management
- Add crew members with different roles:
  - **Operators** (Pilots, Technicians, Merchants, Armourers)
  - **Mentalists** (Special crew with mana abilities)
- Track crew experience and statistics
- Manage crew assignments

### Data Persistence
- Save and load fleet configurations
- Support for multiple save files
- JSON-based storage for fleet and crew data

## Installation

### Prerequisites
Ensure you have **Python 3.11+** installed.

### Steps to Install
1. Clone the repository to your local machine:
   ```sh
   git clone https://github.com/yourusername/python_class_final.git
   cd python_class_final
   ```

2. Install dependencies listed in the `requirements.txt`:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```sh
python main.py
```

The Text User Interface (TUI) will guide you through:
- Fleet creation and management
- Ship operations
- Crew assignments
- Save/load operations

## Requirements

- Python 3.11+
- Textual library
- Other dependencies as listed in `requirements.txt`

## Build

The project includes GitHub Actions workflows to build standalone executables for:
- Windows
- macOS
- Linux

> **Note**: Currently, the build feature is not fully functional. also the GUI does not support all the basic functionality to try all the basic use the sub-main.py

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
