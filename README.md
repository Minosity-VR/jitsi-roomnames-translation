# jitsi-roomnames-translation
Quick python scripts to translate Jitsi's dictionnaries with Google Cloud Translate API.

The words where taken from [Jitsi's js-util repo](https://github.com/jitsi/js-utils/blob/master/random/roomNameGenerator.js).

The Google Cloud API requesting function was taken from [Google documentation](https://cloud.google.com/translate/docs/basic/translating-text#translate_translate_text-python).

You will need an API key to launch this code, and a Translate API ready project. The steps to get one can be found [here](https://cloud.google.com/translate/docs/basic/setup-basic)

## Repo structure
```bash
.
├── LICENSE                     # Just took same license as Jitsi js-utils repo
├── README.md
├── data_en                     # Jitsi dictionnaries of words to generate room names
│   ├── adjectives.en.json
│   ├── adverbs.en.json
│   ├── pluralnouns.en.json
│   └── verbs.en.json
├── data_<lang>                 # The output folder that will contain the translated words (gitignored)
│   ├── adjectives.<lang>.json  # (gitignored)
│   ├── adverbs.<lang>.json     # (gitignored)
│   ├── pluralnouns.<lang>.json # (gitignored)
│   └── verbs.<lang>.json       # (gitignored)
├── data_managment.py           # Functions to handle JSON files
├── google-api-private-key.json # Your API key (gitignored)
└── translation.py              # Main function
```

## Env
It is advised to use a virtualenv to install pip modules, to prevent messing with your other projects.

Installing virtualenv:
```bash
pip3 install --user virtualenv
```
or
```bash
python -m pip3 install --user virtualenv
```

To create a virtualenv :
```bash
virtualenv env
```
Depending on your working environment, you may not have entered your env automatically, so do:
```bash
source env/bin/activate
```
If you leave and you come back later you will need to re-enter the virtualenv.


While in the env, install the requirements:
```bash
env/bin/pip3 install -r requirements.txt
```

# Launching
You will need to add the path to your Google Cloud API key in the environment variables.
To do it only for your terminal session (you will need to re-enter the command after you close the CLI), do:
```bash
export GOOGLE_APPLICATION_CREDENTIALS='/path/to/the/json/key'
```

You can modify the `translation.py` file and set the `test_number` (default -1) to the int value you want if you to execute a non-default behaviour (testing on a small set, comparing singlethreading ant multithreading times...)

You still need to have the virtualenv activated to launch the following commands


Help:
```bash
python3 translation.py -h
```


Default behaviour: Destination language: French, Input folder: `data_en`, Output folder: `data_fr`, use multithreading
```bash
python3 translation.py
```

# Post processing
Depending on what you want to do after that with the words, you may need to affine the translation, or to remove some of the words.

For instance, this project was created to generate a French dictionnary for the [jitsi-box](https://github.com/openfun/jitsi-box) project. For this reason, I had to remove all words containing special characters, which i did with some `sed` commands such as `sed -i '' '/\u00e7/d' ./data_fr/*.json` (This command works for MACOS. For a GNU distribution, use `sed -i '/\u00e7/d' ./data_fr/*.json`). I also had to check that words' forms (verbs, adverbs, noun) where respected.

If you wan't to use an AI or another translating API who can check itself for this, feel free do no anything you want :)
