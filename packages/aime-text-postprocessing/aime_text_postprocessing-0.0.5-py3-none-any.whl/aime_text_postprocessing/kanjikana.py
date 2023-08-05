import MeCab
import romkan

from . import text_replace

me = MeCab.Tagger('-Ochasen')

s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'


def to_kana(text):
    node = me.parseToNode(text)
    token_a = []
    while node:
        if node.surface == '':
            node = node.next
            continue
        feature_a = node.feature.split(',')
        kana = feature_a[-1]
        if kana == '*':
            token_a.append(node.surface)
            token_a.append(' ')
        else:
            token_a.append(kana)
        node = node.next
    return ''.join(token_a).strip()


def kana_to_romaji(text):
    return romkan.to_roma(text)


def remove_accents(text):
    s = ''
    for c in text:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s


def asciidify(text, upper=False, comp_rex=None, out_rex=None):
    if text is None:
        return None
    if comp_rex is None or out_rex is None or len(comp_rex) != len(out_rex):
        text = text_replace.replace_text(text)
    else:
        text = text_replace.process_text(text, comp_rex, out_rex)
    kana = to_kana(text)
    romanji = kana_to_romaji(kana)
    text = remove_accents(romanji)
    if upper:
        return text.upper()
    return text
