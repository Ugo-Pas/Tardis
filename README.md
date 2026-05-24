# Tardis

<div align="center">
  
  *"Sorry, i'm late"*

  ![image](https://github.com/user-attachments/assets/3526ee07-10e7-4bf7-a369-e051d2771329)
  
</div>

Tardis is a project that analyzes large amounts of data to predict future train movements.


## Features

With this project you can:

- parse a CSV dataset and clean it
- train/use a model to make predictions from the dataset
- explore results in an interactive Streamlit dashboard



## Tech Stack

Main tools used in this project:

- Python
- Jupyter Notebook
- Streamlit
- Matplotlib
- scikit-learn
- XGBoost
- Seaborn

## Getting Started

### Installation and environement

Install dependencies and set up the local virtual environment:

```bash
source ./Init_env.sh
```

### Lauch the Website

Launch the dashboard with:
```bash
streamlit run tardis_dashboard.py
``` 

If Streamlit opens on a different port, it will print the local URL in the terminal.

## Project Tree

Project structure:

```
├── README.md
├── Init_env.sh                     # local env setup
├── requirements.txt                # Python dependencies
├── cleaned_dataset.csv             # cleaned dataset
├── tardis_eda.ipynb                # exploratory analysis notebook
├── tardis_model.ipynb              # model notebook
├── tardis_dashboard.py             # Streamlit app entrypoint
├── model.pkl                       # trained model used for prediction
├── src/                            # All file for dashboard
|   ├── Bonus/
|   |   └── ...
|   ├── tools/
|   |   └── ...
│   ├── accueil.py
|   ├── info_generale.py
│   ├── info_utilisateur.py
|   ├── README.md
|   └── screen_prediction.py
├── datasets/                       
|   └── dataset.csv                 # raw dataset
├── tests/                          # Folder for unit tests
|   └── ...
```

## UNIT TESTS

This project have unit test. Check with :

```bash
python -m pytest -v
```

## Lint

This project uses `ruff`:

```bash
ruff check .
```

---
