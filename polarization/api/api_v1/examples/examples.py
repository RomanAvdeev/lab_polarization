from schemas.document import DocumentWithoutText, ManipulationIn, NelFeatures, Ngram, Topic

topics_list = [
    {
        "lvl1": {"id": "lvl1_культура", "topic_label": "культура"},
        "lvl2": {"id": "lvl2_театр", "topic_label": "театр"},
        "lvl3": {
            "id": "12bcd1de-12ce-4cd5-afbf-0d50e86b13d0",
            "topic_label": '"норма" в санктъ-петербург опере 17.07.2021 г.',
        },
        "lvl4": {
            "id": "12bcd1de-12ce-4cd5-afbf-0d50e86b13d0",
            "topic_label": '"норма" в санктъ-петербург опере 17.07.2021 г.',
        },
        "probability": "0.41997874",
    },
    {
        "lvl1": {"id": "lvl1_культура", "topic_label": "культура"},
        "lvl2": {"id": "lvl2_музыка", "topic_label": "музыка"},
        "lvl3": {
            "id": "12bcd1de-12ce-4cd5-afbf-0d50e86b13d0",
            "topic_label": '"норма" в санктъ-петербург опере 17.07.2021 г.',
        },
        "lvl4": {
            "id": "12bcd1de-12ce-4cd5-afbf-0d50e86b13d0",
            "topic_label": '"норма" в санктъ-петербург опере 17.07.2021 г.',
        },
        "probability": "0.23896752",
    },
    {
        "lvl1": {"id": "lvl1_культура", "topic_label": "культура"},
        "lvl2": {"id": "lvl2_знаменитости", "topic_label": "знаменитости"},
        "lvl3": {
            "id": "12bcd1de-12ce-4cd5-afbf-0d50e86b13d0",
            "topic_label": '"норма" в санктъ-петербург опере 17.07.2021 г.',
        },
        "lvl4": {
            "id": "12bcd1de-12ce-4cd5-afbf-0d50e86b13d0",
            "topic_label": '"норма" в санктъ-петербург опере 17.07.2021 г.',
        },
        "probability": "0.0852324",
    },
]
topics = [Topic.parse_obj(topic) for topic in topics_list]

nel_raw = {
    "other": [
        [
            [1.0, 5, 0.8299999833106995],
            [1.0, 35, 0.5799999833106995],
            [1.0, 8, 0.25],
            [1.0, 10, 0.12999999523162842],
            [1.0, 2, 0.10999999940395355],
        ],
        [[0.0, 0, 0.0]],
    ],
    "wiki_id": [["Q19915515", "Q320353", "Q1341594", "Q20587947", "Q580926"], ["not in wiki"]],
    "entities": ["норма", "санктъ-петербург опера",],
    "entities_offset": [[1, 6], [10, 32]],
    "entities_tag": ["ORG", "ORG"],
    "linked_entities": [["Норма", "Норма", "Норма", "Норма", "Норма"], ["not in wiki"]],
}
nel = NelFeatures.parse_obj(nel_raw)

ngrams_raw = [
    {
        "name": "ужасная маска",
        "ngram_words": [
            {
                "form": "ужасная",
                "upos": "ADJ",
                "xpos": None,
                "feats": {"case": "Nom", "degree": "Pos", "gender": "Fem", "number": "Sing"},
                "head": 14,
                "deprel": "amod",
                "start_idx": 70,
                "end_idx": 76,
            },
            {
                "form": "маска",
                "upos": "NOUN",
                "xpos": None,
                "feats": {"animacy": "Inan", "case": "Nom", "gender": "Fem", "number": "Sing"},
                "head": 11,
                "deprel": "nsubj",
                "start_idx": 87,
                "end_idx": 91,
            },
        ],
    }
]
ngrams = [Ngram.parse_obj(n) for n in ngrams_raw]

text = """Это был второй премьерный спектакль"""

document_without_text = DocumentWithoutText(
    document_id=204406123, sentiment=[1, 3], nel=nel, topics=topics, ngrams=ngrams
)

manipulation_in = ManipulationIn(
    document_id=204401234, text=text, nel=nel, ngrams=ngrams, sentiment=[1, 3]
)
