# USFDA Medical Device Cleaner

Downloads and cleans 315,000 medical devices registered with the United States Food and Drug Administration (USFDA).  

### Input
* JSON from the [openFDA Device API](https://open.fda.gov/apis/device/)

### Output
* A CSV of 315,000 medical devices. [See the cleaned data on Kaggle here.](https://www.kaggle.com/datasets/protobioengineering/usfda-medical-devices-2023)

### Usage
Run the scripts in the following order.
```
./openfda_data_downloader.sh
python3 device_json_to_csv.py
```

### Disclaimer
Do not rely on openFDA nor on this dataset to make decisions regarding medical care. Always speak to your health provider about the risks and benefits of FDA-regulated products.