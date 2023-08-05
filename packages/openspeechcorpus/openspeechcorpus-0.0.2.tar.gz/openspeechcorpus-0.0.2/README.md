# Open Speech Corpus CLI

This repository contains the code required to download audiodata from openspeechcorpus.com


To download files from the Isolated Words Project use

```bash
ops  \
    --output_folder isolated_words/ \
    --output_file isolated_words.txt  \
    --corpus words
```


To download files from the Aphasia Project use

```bash
ops  \
    --output_folder aphasia/ \
    --output_file aphasia.txt  \
    --corpus aphasia
```

By default the page size is 500, to modify it use the args `--from` and `--to` i.e:

```bash
ops  \
    --from 500 \
    --to 1000 \
    --output_folder aphasia/ \
    --output_file aphasia.txt  \
    --corpus aphasia
```