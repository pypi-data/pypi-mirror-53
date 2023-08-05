from ._cpinyin import Pinyin

def install():
    """Replace xpinyin.Pinyin with cpinyin.Pinyin"""
    import xpinyin
    xpinyin.Pinyin = Pinyin