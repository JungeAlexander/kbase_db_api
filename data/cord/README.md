# Load CORD-19 dataset into DB

```
wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/historical_releases/cord-19_2020-07-04.tar.gz
tar xzf cord-19_2020-07-04.tar.gz 2020-07-04/metadata.csv
python load_cord.py 2020-07-04/metadata.csv 1>load_cord.out 2>load_cord.err
```


```
wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/historical_releases/cord-19_2020-10-07.tar.gz
tar xzf cord-19_2020-10-07.tar.gz 2020-10-07/metadata.csv
head -n 200 2020-10-07/metadata.csv > 2020-10-07/metadata_subset.csv
python load_cord.py 2020-10-07/metadata_subset.csv 1>load_cord_subset.out 2>load_cord_subset.err
```
