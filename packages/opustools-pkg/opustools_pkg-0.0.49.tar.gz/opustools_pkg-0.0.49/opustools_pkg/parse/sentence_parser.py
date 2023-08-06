import xml.parsers.expat
import html

class SentenceParser:

    def __init__(self, document, direction, preprocessing, wmode,
            language, annotations, anno_attrs, delimiter, preserve):
        self.document = document
        self.direction = direction
        self.pre = preprocessing
        self.annotations = annotations
        if self.annotations:
            self.anno_attrs = anno_attrs
        self.delimiter = delimiter
        self.preserve = preserve

        self.start = ''
        self.sid = ''
        self.chara = ''
        self.end = ''

        self.posses = []

        self.parser = xml.parsers.expat.ParserCreate()
        self.parser.StartElementHandler = self.start_element
        self.parser.CharacterDataHandler = self.char_data
        self.parser.EndElementHandler = self.end_element

        self.sfound = False
        self.efound = False

        self.oneLineSStart = False
        self.oneLineSEnd = False

        self.wmode = wmode
        self.language = language

        self.attrs = {}

        self.processSentence = {'parsed':self.processTokenizedSentence,
                                'xml':self.processTokenizedSentence,
                                'raw':self.processRawSentence,
                                'rawos':self.processRawSentenceOS}

    def start_element(self, name, attrs):
        self.start = name
        if 'id' in attrs.keys() and name == 's':
            self.attrs = attrs
            self.sfound = True
            self.oneLineSStart = True
            self.sid = attrs['id']
        if name == 'w' and self.annotations:
            self.posses = []
            if self.anno_attrs[0] == 'all_attrs':
                attributes = list(attrs.keys())
                attributes.sort()
                for a in attributes:
                    self.posses.append(attrs[a])
            for a in self.anno_attrs:
                if a in attrs.keys():
                    self.posses.append(attrs[a])

    def char_data(self, data):
        if self.sfound:
            self.chara += data

    def end_element(self, name):
        self.end = name
        if name == 's':
            self.efound = True
            self.oneLineSEnd = True

    def parseLine(self, line):
        self.parser.Parse(line.strip())

    def addToken(self, sentence):
        newSentence = sentence
        if self.sfound and  self.start == 'w' and self.end == 'w':
            newSentence = sentence + ' ' + self.chara
            self.chara = ''
            if self.annotations:
                for a in self.posses:
                    newSentence += self.delimiter + a
                self.posses = []
        return newSentence

    def processTokenizedSentence(self, sentence, ids, line):
        newSentence, stop = sentence, 0
        if self.efound:
            self.sfound = False
            self.efound = False
            if self.sid in ids:
                stop = -1
            self.chara = ''
        if self.sid in ids:
            newSentence = self.addToken(sentence)
        if self.preserve and self.sfound and self.start not in ['s', 'w']:
            if type(line) == bytes:
                line = line.decode('utf-8')
            newSentence += line.strip()

        return newSentence, stop

    def processRawSentenceOS(self, sentence, ids, line):
        newSentence, stop = sentence, 0
        if self.efound:
            self.sfound = False
            self.efound = False
            if self.sid in ids:
                stop = -1
                self.chara = ''
        if self.sfound and self.sid in ids:
            if self.preserve:
                if self.start not in ['s', 'w']:
                    if type(line) == bytes:
                        line = line.decode('utf-8')
                    newSentence += line.strip()
            else:
                if self.start == 's' or self.start == 'time':
                    newSentence = self.chara
        return newSentence, stop

    def processRawSentence(self, sentence, ids, line):
        if self.start == 's' and self.sid in ids:
            newSentence = self.chara
            self.chara = ''
            return newSentence, -1
        else:
            self.chara = ''
            return sentence, 0

    def addTuBeginning(self):
        sentences = ' '
        if self.direction == 'src':
            sentences = sentences + '\t\t<tu>\n'
        sentences = (sentences + '\t\t\t<tuv xml:lang="' + self.language +
            '"><seg>')
        return sentences

    def addSentence(self, sentences, sentence, sid):
        if self.wmode == 'normal':
            sentences = (sentences + '\n(' + self.direction + ')="' +
                str(sid) + '">' + sentence)
        elif self.wmode == 'tmx':
            sentences = sentences + ' ' + html.escape(sentence, quote=False)
            sentences = sentences.replace('<seg> ', '<seg>')
        elif self.wmode == 'moses':
            sentences = sentences + ' ' + sentence
        return sentences

    def addTuEnding(self, sentences):
        sentences = sentences + '</seg></tuv>'
        if self.direction == 'trg':
            sentences = sentences + '\n\t\t</tu>'
        return sentences

    def readSentence(self, ids):
        if len(ids) == 0 or ids[0] == '':
            return '', {}
        sentences = ''
        attrsList = []

        if self.wmode == 'tmx':
            sentences = self.addTuBeginning()

        for i in ids:
            sentence = ''
            while True:
                line = self.document.readline()
                self.parseLine(line)
                newSentence, stop = self.processSentence[self.pre](
                    sentence, ids, line)
                sentence = newSentence
                if stop == -1:
                    break

            if self.pre == 'xml' or self.pre == 'parsed':
                sentence = sentence.lstrip()

            sentences = self.addSentence(sentences, sentence, self.sid)
            attrsList.append(self.attrs)

        if self.wmode == 'tmx':
            sentences = self.addTuEnding(sentences)

        return sentences[1:], attrsList
