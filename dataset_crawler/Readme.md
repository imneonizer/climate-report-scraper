## Climate Report Scraper

Use ``climate_report_scraper.py`` to scrape climate report for particular weather station. This is a very hard & fast code, mainly implemented to collect some data set on the go, if you want to collect data for some other weather station or different time ranges don't hesitate to play with the code.

May the comments be with you.

Here is the pipeline on how to execute the operation:

**Step 1**: collect data in json format

````
python climate_report_scraper.py
````

this will give you ``climate_report.json`` file.

**Step 2**: convert json file to csv file

````
python parse_json.py
````

this will give you ``climate_report.csv`` file

**Final Step**: cleaning the csv file

````
jupyter notebook
````

follow the ``csv_cleaner.ipynb`` to clean the data inside csv file, you will end up with ``climate_report.csv`` (this is your data set file).