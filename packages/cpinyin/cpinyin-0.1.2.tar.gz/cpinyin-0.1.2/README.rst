cpinyin
=========

Rewrite `lxneng`'s `xpinyin` by cython since by commit `3599c101f659bb7cfbc7e5c5c5684206e4fab5f9 <https://github.com/lxneng/xpinyin/commit/3599c101f659bb7cfbc7e5c5c5684206e4fab5f9>`.

The interfaces are completely consistent and can be seamlessly switched with `xpinyin`;

Install
--------

::

    pip install cpinyin

Usage
------

Replace xpinyin.Pinyin with cpinyin.Pinyin

::

    >>> import cpinyin
    >>> cpinyin.install()
    >>> from xpinyin import Pinyin
    >>> p = Pinyin()
    >>> p.get_pinyin(u"上海")
    'shang-hai'

Consistent with the `xpinyin` Api.

::

    >>> from cpinyin import Pinyin
    >>> p = Pinyin()
    >>> # default splitter is `-`
    >>> p.get_pinyin(u"上海")
    'shang-hai'
    >>> # show tone marks
    >>> p.get_pinyin(u"上海", tone_marks=u'marks')
    'shàng-hǎi'
    >>> p.get_pinyin(u"上海", tone_marks=u'numbers')
    >>> 'shang4-hai3'
    >>> # remove splitter
    >>> p.get_pinyin(u"上海", u'')
    'shanghai'
    >>> # set splitter as whitespace
    >>> p.get_pinyin(u"上海", u' ')
    'shang hai'
    >>> p.get_initial(u"上")
    'S'
    >>> p.get_initials(u"上海")
    'S-H'
    >>> p.get_initials(u"上海", u'')
    'SH'
    >>> p.get_initials(u"上海", u' ')
    'S H'
    
Please enter Chinese characters encoding by utf8.

    >>> wordvalue = '中国'
    >>> wordvalue= unicode(wordvalue, 'utf-8')
    >>> s = p.get_initials(wordvalue, u'').lower()
    'zg'


.. _lxneng: https://github.com/lxneng
.. _xpinyin: https://github.com/lxneng/xpinyin