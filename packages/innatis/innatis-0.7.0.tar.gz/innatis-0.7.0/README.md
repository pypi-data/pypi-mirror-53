# Innatis

This is a library of custom [Rasa NLU](https://github.com/RasaHQ/rasa_nlu/) components that we (CarLabs) are building.

## What does the name mean?

_Viribus Innatis_ means "innate abilities" in Latin. It's a joke...

"Rasa" comes from "tabula rasa" - _blank slate_ in Latin. We (just Sam) thought it would be funny for this project to have the opposite name, since this is meant to be a suite of tools to fill in functionality for Rasa... that is, make it a not-blank-slate. So "Innate Abilities" -> Viribus Innatis.

## Usage

`$ pip install innatis`

Then add to your pipeline in your `rasa_config.yml`. Example pipeline can be found in [`sample_rasa_innatis_config.yml`](sample_configs/sample_rasa_innatis_config.yml).

## Components

### Classifiers

* `intent_classifier_bert` - Pulls the bert model from TF HUB and pretrains on given data.

#### Example config

```yaml
language: en
pipeline:
  - name: "tokenizer_whitespace"
  - name: "ner_crf"
  - name: "ner_synonyms"
  - name: "innatis.classifiers.BertIntentClassifier"
    pretrained_model_dir: '/path/to/uncased_L-24_H-1024_A-16'
    epochs: 10
    batch_size: 64
```

### Extractors

* `composite_entity_extractor` - Given entities extracted by another extractor (`ner_crf` seems to be the best for now), splits them into composite entities, similar to [DialogFlow](https://dialogflow.com/docs/entities/developer-entities#developer_composite).
* EntitySynonymMapper (replaces `ner_synonyms`) - this is the `ner_synonyms` adapted for `composite_entity_extractor`. You most likely need it if you use `composite_entity_extractor`. It replaces the synonyms with the original entities inside composite entities. It can also do fuzzy matching when matching synonyms (enabled by default). See example config: [`config_composite_entities.yml`](sample_configs/config_composite_entities.yml)

### Featurizers

* `universal_sentence_encoder_featurizer` - Pulls the smaller USE model from TF HUB and embeds inputs as document vectors, and that vector gets sent downstream to be used as a feature.

## Development

```sh
git clone git@github.com:Revmaker/innatis.git
cd innatis
pipenv install
# pipenv install --skip-lock if locking takes too long

# do some stuff
# write some tests

pipenv run python test.py
```

Dependencies suck, as is always the case in Python. I started out using `pipenv` because I thought that was _the_ package manager for Python. But I guess you need to put dependencies in the `install_requires` section of `setup.py`. So, the (currently manual, but automatable) process for moving dependencies from the `Pipfile` to `setup.py` is:

```sh
$ cd innatis
# you are now in parent/innatis, not innatis/innatis
$ python ir_from_pipfile.py | pbcopy
['scikit-learn', 'scipy', 'sklearn-crfsuite', 'tensorflow', 'word2number', 'rasa_nlu==0.13.8', 'tensorflow-hub', 'spacy']

# that array is copied; paste it into setup.py
```

Also, please manually bump the version in a semver-ish way.
