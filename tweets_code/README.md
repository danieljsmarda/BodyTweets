## File Descriptions

In addition to the files stated on the main README of the repo, this folder also contains the following helper files:

- `file_utils.py` for specific file processing use-cases, and 
- `tokenizer.py`, which was borrowed from the [TorchMoji](https://github.com/huggingface/torchMoji) project.
- and `external_locations.ipynb`. This notebook contains the (clean) backbone of the geolocation algorithm described in the paper. In this notebook, the location data from different governmental census data sources are processed into simple lookup tables. `geolocate.py` matches the tweets to these lookup tables and saves them in a form fit for [analysis](../analysis).

