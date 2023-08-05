import io
import re
import sys
cimport cython
import posixpath
import pkg_resources

try:
    BASE_DIR = posixpath.dirname(posixpath.abspath(__file__))
except NameError:
    BASE_DIR = pkg_resources.resource_filename('cpinyin', '')

cdef dict PinyinToneMark = {
    0: u"aoeiuv\u00fc",
    1: u"\u0101\u014d\u0113\u012b\u016b\u01d6\u01d6",
    2: u"\u00e1\u00f3\u00e9\u00ed\u00fa\u01d8\u01d8",
    3: u"\u01ce\u01d2\u011b\u01d0\u01d4\u01da\u01da",
    4: u"\u00e0\u00f2\u00e8\u00ec\u00f9\u01dc\u01dc",
}
cdef tuple VOWELS = (u'a', u'o', u'e', u'ui', u'iu')

cdef class Pinyin(object):

    """
    Rewrite lxneng's xpinyin by cython.

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
    """

    cdef public dict dict
    cdef public unicode data_path

    def __init__(self, unicode data_path=None):
        data_path = self.data_path
        if data_path is None:
            self.data_path = data_path \
                = posixpath.join(BASE_DIR, u'Mandarin.dat')
            self.dict = self.load_data(data_path)

    cdef dict load_data(self, unicode path):
        cdef dict d
        cdef unicode line, k, v
        cdef object f
        d = {}
        with io.open(path, mode='r', encoding='utf-8') as f:
            for line in f:
                k, v = line.split(u'\t')
                d[k] = v
        return d

    cpdef unicode get_pinyin(self, unicode chars=u'你好',
                             unicode splitter=u'-', unicode tone_marks=None,
                             unicode convert=u'lower'):
        cdef int flag, key_ord
        cdef list result, pinyins
        cdef unicode c, key, word
        result = []
        flag = 1
        for c in chars:
            key_ord = ord(c)
            key = (u'%x' % key_ord).upper()
            try:
                pinyins = self.dict[key].split()
                if tone_marks == u'marks':
                    word = Pinyin.decode_pinyin(pinyins[0].strip())
                elif tone_marks == u'number':
                    word = pinyins[0].strip()
                else:
                    word = pinyins[0].strip()[:-1]
                word = Pinyin.convert_pinyin(word, convert)
                result.append(word)
                flag = 1
            except KeyError:
                if flag:
                    result.append(c)
                else:
                    result[-1] += c
                flag = 0
        return splitter.join(result)

    cpdef unicode get_initial(self, unicode char=u'你'):
        try:
            return self.dict['%X' % ord(char)].split(' ')[0][0]
        except KeyError:
            return char

    cpdef unicode get_initials(self, unicode chars=u'你好',
                                     unicode splitter=u'-'):
        cdef list result
        result = []
        flag = 1
        for char in chars:
            try:
                result.append(self.dict['%X' % ord(char)].split(' ')[0][0])
                flag = 1
            except KeyError:
                if flag:
                    result.append(char)
                else:
                    result[-1] += char

        return splitter.join(result)

    @staticmethod
    @cython.binding(True)
    cdef unicode convert_pinyin(unicode word, unicode convert):
        if convert == u'capitalize':
            return word.capitalize()
        if convert == u'lower':
            return word.lower()
        if convert == u'upper':
            return word.upper()

    @staticmethod
    @cython.binding(True)
    cdef unicode decode_pinyin(unicode s):
        cdef unicode t, c
        cdef list result
        cdef int tone
        s = s.lower()
        result = []
        t = u''
        for c in s:
            if u'a' <= c <= u'z':
                t += c
                continue
            if c == u':':
                assert t[-1] == u'u'
                t = t[:-1] + '\u00fc'
                continue
            if u'0' <= c <= u'5':
                tone = int(c) % 5
                if tone != 0:
                    m = re.search(u'[aoeiuv\u00fc]+', t)
                    if m is None:
                        # pass when no vowels find yet
                        t += c
                    elif len(m.group(0)) == 1:
                        # if just find one vowels, put the mark on it
                        t = t[:m.start(0)] \
                            + PinyinToneMark[tone][PinyinToneMark[0].index(m.group(0))] \
                            + t[m.end(0):]
                    else:
                        # mark on vowels which search with "a, o, e" one by one
                        # when "i" and "u" stand together, make the vowels behind
                        for num, vowels in enumerate(VOWELS):
                            if vowels in t:
                                t = t.replace(vowels[-1], PinyinToneMark[tone][num])
                                break
            result.append(t)
            t = u''
        result.append(t)
        return u''.join(result)