# pandapower_test_network

A small electrical power network model built with [pandapower](https://www.pandapower.org/).

The project is a simple engineering playground for power-flow calculations, network modelling, and result visualisation.

## Network

The model represents a simple hierarchical grid:

```text
110 kV HV Grid
      │
      ▼
  110/20 kV
 Transformer
      │
      ▼
    20 kV MV
   ┌───┼────┐
   │   │    │
 Feeder A  Feeder B + PV
   │
 Loads
   │
 Feeder C
   │
 20/0.4 kV
 Transformer
   │
 0.4 kV LV
   │
  Load
```

The network includes:

- 110 kV high-voltage grid connection
- 20 kV medium-voltage feeders
- 0.4 kV low-voltage network
- HV/MV and MV/LV transformers
- Multiple loads
- A PV generator connected to the MV network
- AC power-flow calculation
- Bus voltage and equipment loading visualisation

## Requirements

- Python 3.10+
- pandapower
- matplotlib

## Installation

```bash
pip install -e .
```

## Usage

Run the model with:

```bash
python main.py
```

The program runs a power-flow calculation, prints the main results, and generates files in `results/`:

- `network.html` — interactive network view and result tables
- `voltage_profile.png` — bus voltage profile

## Project Structure

```text
pandapower_test_network/
├── constants.py
├── network.py
├── analysis.py
├── main.py
├── results/
├── pyproject.toml
└── README.md
```

## Purpose

This is a small test project focused on applying Python to electrical power-system modelling with pandapower.
