"""Brand and style keywords, matched against the item description (regex, case-insensitive).

Rough by design: a description has to name the brand for it to count, and a few
patterns can over-match (e.g. "lane" also catches "Lane" in a person's name).
"""
import pandas as pd

BRANDS = {
    "Gus Modern": r"\bgus\b",
    "Article": r"\barticle\b",
    "West Elm": r"west\s*elm",
    "CB2": r"\bcb2\b",
    "Crate & Barrel": r"crate",
    "Restoration Hardware": r"restoration|\brh\b",
    "Pottery Barn": r"pottery\s*barn",
    "Room & Board": r"room\s*(&|and)\s*board|r&b",
    "Blu Dot": r"blu\s*dot",
    "DWR": r"\bdwr\b|design within reach",
    "Herman Miller": r"herman\s*miller",
    "Knoll": r"\bknoll\b",
    "Eames": r"\beames\b",
    "Timothy Oulton": r"oulton",
    "Milo Baughman": r"baughman",
    "Ligne Roset": r"roset",
    "Vitra": r"\bvitra\b",
    "Wegner": r"wegner",
    "Saarinen": r"saarinen|tulip",
    "George Nelson": r"\bnelson\b",
    "Paul McCobb": r"mccobb",
    "Drexel": r"drexel",
    "Lane": r"\blane\b",
    "Brownstone": r"brownstone",
    "Arper": r"\barper\b",
    "Fermob": r"fermob",
    "Muuto": r"muuto",
    "Hay": r"\bhay\b",
    "EQ3": r"\beq3\b",
    "Innovation": r"innovation",
}
STYLES = {
    "Danish": r"danish",
    "Mid-century": r"mid\s*-?\s*century|midcentury|\bmcm\b",
    "Teak": r"\bteak\b",
    "Walnut": r"walnut",
    "Rosewood": r"rosewood",
    "Leather": r"leather",
    "Velvet": r"velvet",
    "Vintage": r"vintage",
    "Antique": r"antique",
    "Italian": r"italian|italia",
    "Brass": r"brass",
    "Marble": r"marble",
    "Rattan / cane": r"rattan|\bcane\b|caned",
    "Brutalist": r"brutalist",
    "Custom": r"custom",
    "New": r"\bnew\b",
    "Pair": r"\bpair\b",
    "Set of": r"set of|\bset\b",
}


def tag(desc: pd.Series, patterns: dict) -> pd.DataFrame:
    d = desc.fillna("").str.lower()
    return pd.DataFrame({k: d.str.contains(p, regex=True) for k, p in patterns.items()})
