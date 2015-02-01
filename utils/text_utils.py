import re
import translitcodec


_PUNCT_RE = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delimiter=u'-'):
    result = []
    for word in _PUNCT_RE.split(text.lower()):
        word = word.encode('translit/long')
        if word:
            result.append(word)
    return unicode(delimiter.join(result))
