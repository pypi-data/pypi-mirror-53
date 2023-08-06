from mecab cimport mecab_new2, mecab_sparse_tostr2, mecab_t, mecab_node_t, mecab_sparse_tonode
from collections import namedtuple

# field names come from here:
# https://unidic.ninjal.ac.jp/faq
UnidicFeatures = namedtuple('UnidicFeatures', 
        ('pos1 pos2 pos3 pos4 cType cForm lForm lemma orth pron ' 
        'orthBase pronBase goshu iType iForm fType fForm').split(' '))

cdef class Node:
    cdef const mecab_node_t* c_node
    cdef str surface
    cdef str feature_str
    cdef object features
    cdef unsigned int id
    cdef unsigned short length
    cdef unsigned short rlength
    cdef unsigned short posid
    cdef unsigned char char_type
    cdef unsigned char stat

    def __init__(self):
        pass

    def __repr__(self):
        if self.stat == 0:
            return self.surface
        elif self.stat == 2:
            return '<BOS>'
        elif self.stat == 3:
            return '<EOS>'
        elif self.stat == 1:
            return '<UNK>' + self.surface
        else:
            return self.surface

    @property
    def surface(self):
        return self.surface
    
    @property
    def feature(self):
        if self.features is None:
            self.set_feature(self.feature_str)
        return self.features
    
    @property
    def posid(self):
        return self.posid

    @property
    def char_type(self):
        return self.char_type

    @property
    def stat(self):
        return self.stat

    @property
    def pos(self):
        return "{},{},{},{}".format(*self.feature[:4])

    @property
    def is_unk(self):
        return self.stat == 1

    @property
    def white_space(self):
        # The half-width spaces before the token, if any.
        if self.length == self.rlength:
            return ''
        else:
            return ' ' * (self.rlength - self.length)

    cdef void set_feature(self, str feature):
        fields = feature.split(',')
        if self.stat == 1: 
            # unks have fewer fields
            #XXX should this be '*' or ''?
            fields = fields + ([None] * 11)
        self.features = UnidicFeatures(*fields)

    @staticmethod
    cdef Node wrap(const mecab_node_t* c_node):
        cdef Node node = Node.__new__(Node)
        node.c_node = c_node

        # The surface gets freed so we need to copy it here
        # Also note it's not zero terminated.
        node.surface = c_node.surface[:c_node.length].decode('utf-8')

        node.id = c_node.id
        node.length = c_node.length
        node.rlength = c_node.rlength
        node.posid = c_node.posid
        node.char_type = c_node.char_type
        node.stat = c_node.stat

        # This is null terminated.
        # The features are lazily initialized so that it's faster 
        # if you just want a list of words.
        node.feature_str = c_node.feature.decode('utf-8')
        return node

cdef class Tagger:
    cdef mecab_t* c_tagger

    def __init__(self, arg=''):
        arg = bytes(arg, 'utf-8')
        self.c_tagger = mecab_new2(arg)

    def parse(self, str text):
        btext = bytes(text, 'utf-8')
        return mecab_sparse_tostr2(self.c_tagger, btext, len(btext)).decode('utf-8')

    def parseToNodeList(self, text):
        cstr = bytes(text, 'utf-8')
        cdef const mecab_node_t* node = mecab_sparse_tonode(self.c_tagger, cstr)

        out = [Node.wrap(node)]
        while node.next:
            node = node.next
            out.append(Node.wrap(node))
        return out

