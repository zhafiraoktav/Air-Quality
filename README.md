## Setup Environment

### Using Anaconda
conda create --name air-quality-ds python=3.9

conda activate air-quality-ds

pip install -r requirements.txt

## Using Shell/Terminal
mkdir Proyek_Analisis_Data

cd Proyek_Analisis_Data

pipenv install

pipenv shell

pip install -r requirements.txt

## Run the Dashboard
streamlit run dashboard.py
