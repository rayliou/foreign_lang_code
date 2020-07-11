#!/usr/local/bin/python3
from __future__ import print_function

import spacy,sys,re,os
from spacy import displacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from spacy.tokens import Token,Span
from LoadWordList import LoadWordList
import inspect
try:
    from html import escape  # python 3.x
except ImportError:
    from cgi import escape  # python 2.x
from FilterHtml import FilterHtml

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    pass

def showDep(txt, nlp):
    doc = nlp(txt)
    sentence_spans = list(doc.sents)
    displacy.serve(sentence_spans, style="dep")
    pass

def longSentence(nlp):
    #nlp = spacy.load("en_core_web_sm")
    text = """In ancient Rome, some neighbors live in three adjacent houses. In the center is the house of Senex, who lives there with wife Domina, son Hero, and several slaves, including head slave Hysterium and the musical's main character Pseudolus. A slave belonging to Hero, Pseudolus wishes to buy, win, or steal his freedom. One of the neighboring houses is owned by Marcus Lycus, who is a buyer and seller of beautiful women; the other belongs to the ancient Erronius, who is abroad searching for his long-lost children (stolen in infancy by pirates). One day, Senex and Domina go on a trip and leave Pseudolus in charge of Hero. Hero confides in Pseudolus that he is in love with the lovely Philia, one of the courtesans in the House of Lycus (albeit still a virgin)."""
    doc = nlp(text)
    sentence_spans = list(doc.sents)
    displacy.serve(sentence_spans, style="dep")
    pass

class PseudoSpan:
    def __init__(self, span):
        self.start = span.end -1
        self.end   =  span.start
        self.span   =  span
        pass
    def __repr__(self):
        return self.span.text
    pass

#nlp = spacy.load("en_core_web_sm")
##matcherTest(nlp)
#phrasalVerbsSents(nlp)
#phrasalVerbs(nlp)
#longSentence(nlp)
class WordOrSpanReferences:
    SINGLE_WORD  = 0
    PHRASAL_VERB = 1
    IDIOM        = 2
    SENTENCE        = 3
    def __init__(self,w):
        self.w_ = w
        self.r_ = []
        self.len_ = 0
        pass
    def addSpanorIndex(self,tple):
        self.r_.append(tple)
        self.len_ +=1
        return self.len_
    pass

class IntensiveRL:
    def __init__(self):
        self.wl_ = LoadWordList()
        self.adpVocas_ = self.wl_.getADPVocabulary()
        self.idiomsIncludes_ = self.wl_.getIncludeIdioms()


        self.nlp_ = spacy.load("en_core_web_sm")
        self.nlp_.max_length *= 3
        self.doc_ = None

        self.idiomsMatcher_ = PhraseMatcher(self.nlp_.vocab, attr='LEMMA')
        #patterns = [self.nlp_.make_doc(text) for text in self.idiomsIncludes_]
        patterns = [self.nlp_(text) for text in self.idiomsIncludes_]
        self.idiomsMatcher_ .add('idiomMatcher', None, *patterns)

        #for single Word
        self.singleWordsList_ = []
        self.singleWordsDict_ = dict()
        #for phrasal verbs
        self.prVerbsList_ = []
        self.prVerbsDict_ = dict()
        #for idioms
        self.idiomsList_ = []
        self.idiomsDict_ = dict()
        Token.set_extension(name='freq',default=None)
        Span.set_extension(name='freq', default=None)
        self.outputObj_ = None
        self.wordRe_    = r"""^[a-zàâçéèêëîïôûùüÿñæœ .-]+$"""
        self.wordRe_    = re.compile(self.wordRe_,re.I)
        #for idioms
        pass

    def processWholeText(self):
        self.nlp_ = spacy.load("en_core_web_sm")
        pass
    def processStdin(self):
        #FIXME: txt = sys.stdin.read()
        filePath  = f'{currentdir}/../IntensiveRL_test_data/GitHub Flavored Markdown Spec.md'
        txt = open(filePath,'r').read()
        txt = FilterHtml(txt).plainTxt
        self.doc_ = self.nlp_(txt)
        for token in self.doc_:
            self.matchForSingWord(token)
            self.matchPhrasalVerbs(token)
        self.gatherStatForPhrasalVerbs()

        self.matchIdioms(token)
        self.renderOutputBySentences()
        pass

    def renderOutputBySentences(self):
        outList  = []
        def sortFunction(i):
            if type(i) == spacy.tokens.token.Token:
                return (i.i, -i.i)
            return (i.start, -i.end)
        #sort all token and span
        for k,t in self.idiomsDict_.items():
            for span in t.r_:
                outList.append(span)
                outList.append(PseudoSpan(span))
        for k,t in self.singleWordsDict_.items():
            #print('{},{}'.format(t.len_,k))
            for token in t.r_:
                outList.append(token)
        for k,t in self.prVerbsDict_.items():
            #print('{},{}'.format(t.len_,k))
            for span in t.r_:
                outList.append(span)
                outList.append(PseudoSpan(span))
        #shorter range is following the longer one.
        for span in self.doc_.sents:
            span._.freq  = { 'type': WordOrSpanReferences.SENTENCE, }
            outList.append(span)
            outList.append(PseudoSpan(span))
            # print(f'[{span.text}]')
        outList= sorted(outList, key=sortFunction)
        self.outputSegments(outList, 0, 0)
        pass

    def debug(self,outList):
        for o in outList:
            if type(o)  == PseudoSpan:
                print(f'P\t{o.span.start},{o.span.end}\t{o}')
            elif type(o) == spacy.tokens.token.Token:
                print(f'W\t{o.i},{o.i}')
            else:
                print(f'I\t{o.start},{o.end}')
        pass

    def matchForSingWord(self,token):
        ignorePoses_ = { 'DET','SPACE','AUX', 'PRON', 'PUNCT', 'NUM' }
        if token.pos_ in  ignorePoses_:
            return
        if len(token.text ) == 1:
            return
        if re.match(self.wordRe_,token.text) is None:
            return
        if len(token.text ) == 2 and \
        not (token.text[0].isalpha() and token.text[1].isalpha() ):
            return
        if self.wl_.isStopWord(token.lemma_):
            return
        w = '{} .{}'.format(token.lemma_, token.pos_)
        if w in self.singleWordsDict_ :
            ref = self.singleWordsDict_[w]
        else:
            ref = WordOrSpanReferences(w)
            self.singleWordsDict_[w] = ref
        token._.freq  = {
                'w':w,
                'idx_num':ref.addSpanorIndex(token),
                'type': WordOrSpanReferences. SINGLE_WORD,
                }
        pass
    def gatherStatForSingWord(self,token):
        pass

    def matchPhrasalVerbs(self,token):
        if token.pos_ != 'ADP' and token.pos_ != 'ADV':
            return
        if token.head.pos_  != 'VERB' or token.text not in self.adpVocas_:
            return

        middleToken = -1
        if len(self.prVerbsList_) > 0:
            lastOne  = self.prVerbsList_[-1]
            if lastOne[0] == token.head.i:
                middleToken = lastOne[1]
                self.prVerbsList_.pop()
        self.prVerbsList_.append( (token.head.i, token.i, middleToken))
        pass

    def gatherStatForPhrasalVerbs(self):
        for tple in self.prVerbsList_:
            w = '{}{} {}'.format(
                    self.doc_[tple[0]].lemma_,
                    (' {}'.format(self.doc_[tple[2]].text) if tple[2] != -1 else ''),
                    self.doc_[tple[1]].text,
                    )
            if self.wl_.isStopPhrasalVerb(w):
                continue
            if w in self.prVerbsDict_ :
                ref = self.prVerbsDict_[w]
            else:
                ref = WordOrSpanReferences(w)
                self.prVerbsDict_[w] = ref
            span = self.doc_[tple[0]:tple[1]+1]
            span._.freq  = {
                    'w':w,
                    'idx_num': ref.addSpanorIndex(span),
                    'type': WordOrSpanReferences. PHRASAL_VERB,
                    }
        self.prVerbsList_ = []
        pass

    def matchIdioms(self,token):
        matches = self.idiomsMatcher_(self.doc_)
        for id,start, end in matches:
            span = self.doc_[start:end]
            w  = span.lemma_
            if self.wl_.isStopIdiom(w):
                continue
            if w in self.idiomsDict_ :
                ref = self.idiomsDict_[w]
            else:
                ref = WordOrSpanReferences(w)
                self.idiomsDict_[w] = ref
            span._.freq  = {
                    'w':w,
                    'idx_num': ref.addSpanorIndex(span),
                    'type': WordOrSpanReferences.IDIOM,
                    }
        pass
    def outputString(self, s):
        print(s,end = '')
        pass

    def startSpan(self, seg, prevOffset):
        if seg._.freq['type']  == WordOrSpanReferences.SENTENCE:
            self.outputString(f'[{seg.text}]\t\t')
            self.outputString('<span class="s">')
            return prevOffset
        phrase_idiom  = 'PHRASAL' if seg._.freq['type']  ==  WordOrSpanReferences. PHRASAL_VERB else 'IDIOM'
        if prevOffset <= seg.start:
            self.outputString(self.doc_[prevOffset:seg.start])
        l = f'<span class="lemma" lemma="{escape(self.wl_.getExactLemma(seg.lemma_))}"></span>'
        c  = escape(phrase_idiom)
        s = f'<span class="{c}" ">{l}'
        # s = '<span class="{}_lemma"> lemma=[{}]</span><span class="{}" id="{}{}">'.format(
        #         phrase_idiom,
        #         self.wl_.getExactLemma(seg.lemma_),
        #         phrase_idiom
        #         , seg._.freq['w'].replace(' ', '_')
        #         , seg._.freq['idx_num']
        #         )
        self.outputString(s)
        return seg.start

    def writeWord(self, seg, prevOffset):
        #TODO: lack of word frequency.
        rank_exam_cat = ''
        #TODO
        normLemma     = seg.lemma_
        clsSpan  = f'{seg.pos_} {rank_exam_cat} {normLemma}'
        clsSpan  = escape(clsSpan)
        idSpan   = f''
        l = f'<span class="lemma" lemma="{escape(seg.lemma_)}"></span>'
        s = f'<span class="{clsSpan}" id="{idSpan}">{l}{seg.text}</span>'
        if prevOffset <= seg.i:
            self.outputString(self.doc_[prevOffset:seg.i])
        self.outputString(s)
        return seg.i+1

    def closeSpan(self, seg, prevOffset):
        seg = seg.span
        self.outputString(self.doc_[prevOffset:seg.end])
        self.outputString('</span>')
        if seg._.freq['type']  == WordOrSpanReferences.SENTENCE:
            self.outputString('\n@@@@@@@@@@@@@@@@@@@@\n')
        return seg.end

    def outputSegments(self, outList, prevOffset, i= 0):
        for o in outList:
            if type(o)  == PseudoSpan:
                prevOffset = self.closeSpan(o,prevOffset)
            elif type(o) == spacy.tokens.token.Token:
                prevOffset = self.writeWord(o,prevOffset)
            else:
                prevOffset = self.startSpan(o,prevOffset)

        self.outputString(self.doc_[prevOffset:])
        return prevOffset


    pass

if __name__ == "__main__":
    # nlp_ = spacy.load("en_core_web_sm"); showDep(sys.stdin.read(), nlp_); sys.exit(0)
    #stdIn(); sys.exit(0)
    iRL  = IntensiveRL()
    iRL.processStdin()
    sys.exit(0)
    pass

