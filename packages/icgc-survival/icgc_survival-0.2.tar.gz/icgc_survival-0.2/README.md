# Random Survival Forest

The ICGC-survival package provides an easy oppurtinity to perform survival prediction on ICGC datasets.

## Installation
```sh
$ pip install icgc-survival
```

## Contribute

- Source Code: https://github.com/julianspaeth/icgc-survival

## Getting Started

```python
>>> from download_helper import login, download_file_by_project
>>> from feature_creator import extract_gene_affected_counts
>>> from label_creator import extract_survival_labels

>>> token = login(username, password)
>>> df = download_file_by_project(token=token, filetype="simple_somatic_mutation", release=28, project_code="ALL-US")
>>> ssm_gene_affected_counts = extract_gene_affected_counts(df)
>>> labels, features = extract_survival_labels(ssm_gene_affected_counts, donors)

>>> x, x_test, y, y_test = train_test_split(features, labels, shuffle=True, test_size=0.33, random_state=10)
...
```

## Support

If you are having issues or feedback, please let me know.

julian.spaeth@student.uni-tuebinden.de

## License
MIT