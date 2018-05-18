# NAE Finder
Finds potential NAE signals in a given .jpg file, giving interpupillary distance and eyeshine colour. Image with circled NAEs saved as output_circled.jpg
Spectrum found and displayed for left and right eyes
Data stored as 'distcolour.csv' and 'spec.csv' for training database

## Requirements

* `python3`
* `pip`
* `virtualenv`

## Usage

1. Setup a virtual environment using the command `virtualenv venv`
2. Activate the virtual environment using `source venv/bin/activate`
3. Install package dependencies using `pip install -r requirements.txt`
4. Execute using `python3 main.py -i path-to-jpg -c class-if-training-data`