from __future__ import annotations

import json
import pickle
from dataclasses import dataclass
from pathlib import Path
from threading import Lock

import numpy as np
from django.conf import settings


@dataclass
class PredictionResult:
    label: str
    confidence: float


class LSTMClassifierService:
    def __init__(self):
        self._model = None
        self._tokenizer = None
        self._labels = None
        self._max_len = None
        self._lock = Lock()

    def _assets_dir(self) -> Path:
        return Path(settings.BASE_DIR) / 'ml_assets'

    def _load_assets(self):
        with self._lock:
            if self._model is not None:
                return

            assets = self._assets_dir()
            model_path = assets / 'model.keras'
            tokenizer_path = assets / 'tokenizer.pkl'
            labels_path = assets / 'labels.json'
            max_len_path = assets / 'max_len.txt'

            if not model_path.exists():
                raise FileNotFoundError(f'Model not found at {model_path}. Place your existing Keras model there.')
            if not tokenizer_path.exists():
                raise FileNotFoundError(f'Tokenizer not found at {tokenizer_path}.')

            from keras.models import load_model

            self._model = load_model(model_path)
            with tokenizer_path.open('rb') as f:
                self._tokenizer = pickle.load(f)

            if labels_path.exists():
                with labels_path.open('r', encoding='utf-8') as f:
                    self._labels = json.load(f)
            else:
                self._labels = None

            if max_len_path.exists():
                self._max_len = int(max_len_path.read_text(encoding='utf-8').strip())
            else:
                self._max_len = 200

    def predict(self, text: str) -> PredictionResult:
        self._load_assets()

        sequence = self._tokenizer.texts_to_sequences([text])
        from keras.preprocessing.sequence import pad_sequences

        padded = pad_sequences(sequence, maxlen=self._max_len, padding='post', truncating='post')

        raw_pred = self._model.predict(padded, verbose=0)
        pred_array = np.array(raw_pred)

        if pred_array.ndim == 2 and pred_array.shape[1] > 1:
            index = int(np.argmax(pred_array[0]))
            confidence = float(pred_array[0][index])
        else:
            confidence = float(pred_array.flatten()[0])
            index = 1 if confidence >= 0.5 else 0

        if self._labels:
            label = self._labels[index] if index < len(self._labels) else str(index)
        else:
            label = str(index)

        return PredictionResult(label=label, confidence=confidence)


service = LSTMClassifierService()
