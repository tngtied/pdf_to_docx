# hooks/hook-tkdnd.py
from PyInstaller.utils.hooks import collect_data_files

# Collect all data files from tkdnd
datas = collect_data_files('tkdnd')
