# This is only the UI layer of the imot tracker application
The data population part is handled in a separate repo. 
## Purpose is to only start a localhost server and visualize the data that was collected in the database
# Usage
1) Setup environment : ```python -m venv <envrionment name> ```
2) Activate environment
3) Install dependancies: ``` pip install -r depencencies.txt ```
4) Generate test data: ``` python generate_test_db.py ```
5) Run the app: ``` python app.py ```

# Any new crawlers added in the data collection layer must also include their corresponding:
        1) css specifics that will be used in the templates (styles.css)
        2) constants file definition