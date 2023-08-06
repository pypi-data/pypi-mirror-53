"""Mecab parser."""
import subprocess
import sys
from typing import List, Optional

import MeCab
import pandas as pd

from mecab2pandas.exception import NotSupportOSError


def listup_dictionaries() -> List[str]:
    """List up available dictionaries name.

    Returns:
        The list of dictionaries name.

    """
    if sys.platform == "win32":
        raise NotSupportOSError(
            "Not support for Windows, because of mecab-config is not in windows."
        )

    return subprocess.getoutput("ls `mecab-config --dicdir`").split("\n")


class MecabParser:
    r"""Parser class by MeCab into pandas DataFrame.

    MeCab's result has format like this.

    表層形\t品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音

    Attributes:
        MECAB_COLUMNS: Columns definition.

    """

    MECAB_COLUMNS: List[str] = [
        "surface_form",
        "word_class",
        "class_detail1",
        "class_detail2",
        "class_detail3",
        "conjugational_type",
        "conjugational_form",
        "original_form",
        "how_to_read",
        "pronunciation",
    ]
    """Columns of DataFrame."""

    def __init__(self, dic_name: Optional[str] = None) -> None:
        """Initialize.

        .. Note::
            If you use in Windows, you can't use `mecab-config`, so you call with dictionary's full path.

        Args:
            dic_name: dictionary's name. if None, using default dictionary. e.g. mecab-ipadic-neologd.

        """
        if dic_name is None:
            self._mecab = MeCab.Tagger()
        else:
            if sys.platform == "win32":
                dic_path = dic_name
            else:
                dic_path = f"{subprocess.getoutput('mecab-config --dicdir')}/{dic_name}"
            self._mecab = MeCab.Tagger(f"-d {dic_path}")

    def parse(self, target: str) -> pd.DataFrame:
        """Parse Japanese sentence via MeCab into pandas DataFrame.

        Args:
            target: target sentence.

        Returns:
            pandas DataFrame.

        """
        formed: List[List[Optional[str]]] = []
        mecab_result = self._mecab.parse(target)

        for line in mecab_result.split("\n"):
            if line == "EOS":
                break

            word, properties = line.split("\t")
            properties = [value if value != "*" else None for value in properties.split(",")]
            properties_length = len(self.MECAB_COLUMNS) - 1
            if len(properties) < properties_length:
                properties.extend([None] * (properties_length - len(properties)))

            formed.append([word] + properties)

        return pd.DataFrame(formed, columns=self.MECAB_COLUMNS)
