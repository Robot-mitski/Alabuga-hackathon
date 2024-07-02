from natasha import (Doc, NewsNERTagger, NewsEmbedding,
                     Segmenter, MorphVocab,NewsMorphTagger,
                     NewsSyntaxParser)

from collections import defaultdict

from typing import Dict, List, Optional

from itertools import chain

from transformers import pipeline


class NERTagger:
    def __init__(self):
        self.morph_vocab = MorphVocab()

        emb = NewsEmbedding()
        self.ner_tagger = NewsNERTagger(emb)
        self.segmenter = Segmenter()
        self.morph_tagger = NewsMorphTagger(emb)
        self.syntax_parser = NewsSyntaxParser(emb)

    def get_samples(self, text:str, mask: bool = True, force: bool = False) -> Dict[str, List[str]]:
        """
        Calculates data for model inference

        If mask=True, replace organization name to [MASK].

        Output format:
        {
            "OrgName 1": ["Sample1", "Sample 2"],
            "OrgName 2": ["Sample1", "Sample 2"]
        }
        """
        doc = Doc(text)
        
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        doc.parse_syntax(self.syntax_parser)
        doc.tag_ner(self.ner_tagger)

        orgs = defaultdict(list)

        for sent in doc.sents:
            for span in sent.spans:
                if span.type != "ORG":
                    continue

                text = sent.text
                if mask:
                    text = text[:span.start - sent.start] + "[MASK]" + text[span.stop - sent.start:]

                span.normalize(self.morph_vocab)
                orgs[span.normal].append(text)

        return dict(**orgs)


class Prediction:
    """
    Класс для хранения предсказаний модели

    Можно объединять два предсказания (& - пересечение, | - объединение)

    Примеры:
    >>> p1 = Prediction({"org1": [1, 0, 1, 2]})
    >>> p2 = Prediction({"org1": [1], "org2": [0]})
    >>> p1 | p2
    Prediction({"org1": [1, 0, 1, 2, 1]})
    >>> p1 & p2
    Prediction({"org1": [1, 0, 1, 2, 1], "org2": [0]})
    """

    data: Optional[Dict[str, List[int]]] = None

    def __init__(self, data=None):
        if data is None:
            data = dict()
        self.data = data
    
    def get_labels(self) -> Dict[str, List[int]]:
        """Возвращает человеко-читаемые результаты"""
        cls_labels = ["Negative", "Neutral", "Positive"]
        return {k: [cls_labels[x] for x in v] for k, v in self.data.items()}

    def get_rate(self) -> Dict[str, float]:
        """
        Возвращает усреднённое значение, где ближе к -1 -- отрицательная,
        а ближе к 1 -- положительная
        """
        return {k: sum(v) / len(v) - 1 for k, v in self.data.items()}

    def __and__(self, other):
        result = dict()
        for k, v in self.data.items():
            if k in other.data:
                result[k] = v + other.data[k]
        return Prediction(result)
    
    def __or__(self, other):
        result = dict()
        for k in chain(self.data.keys(), other.data.keys()):
            result[k] = self.data.get(k, []) + other.data.get(k, [])
        return Prediction(result)

    def __str__(self):
        return f"Prediction({str(self.data)})"

    def __repr__(self):
        return str(self)


class SAModel:
    def __init__(self, model_path):
        self.pipe = pipeline("text-classification", model=model_path)
        self.tagger = NERTagger()
 
    def predict(self, text: str) -> Prediction:
        samples = self.tagger.get_samples(text)
        texts = sum((x[1] for x in list(samples.items())), start=[])
 
        preds = [int(x["label"][-1]) for x in self.pipe(texts)]
 
        result = dict()
        i = 0
        for org, org_texts in samples.items():
            result[org] = [preds[i] for i in range(i, i + len(org_texts))]
        
        return Prediction(result)
