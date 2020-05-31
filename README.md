# ChatBot_DL

This my app deploying - .... Model from this repo: https://github.com/ldulcic/chatbot

Python 3x

## Installation
```bash
pip3 install -r requirements.txt

python3 -m spacy download en
```

## Run with Pre-trained models
Run following commands in root of this repository to download pre-trained customer service chatbots.
```bash
wget https://www.dropbox.com/s/ibm49gx1gefpqju/pretrained-models.zip

unzip pretrained-models.zip

rm pretrained-models.zip

sudo chmod +x predict.py
```
After....
Try by running: `main.py`
