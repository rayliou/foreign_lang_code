#!/usr/local/bin/python3
import sys,json,os
import re

import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#parentdir = os.path.dirname(currentdir)
#sys.path.insert(0,parentdir)

class LoadWordList:
    def __init__(self, user='ray'):
        self.baseDir_ = '{}/{}'.format(currentdir,'WordLists')
        self.stopDir_ = '{}/stop/{}'.format(self.baseDir_, user)

        self.idiomFile_      = '{}/idioms_cmbrdg_v1.txt'.format(self.baseDir_)
        self.phrasalVerbFile = '{}/phrasalverbs_lgmn_cmbrdg_v1.txt'.format(self.baseDir_)

        self.stopWords_ = set()
        self.stopPhrasalVerbs_ = set()
        self.stopIdioms_ = set()

        self.parseStopFiles()
        self.includePhrasalVSet_  = None
        self.includeIdiomsSet_ = None

        self.genIncludePhrasalV()
        assert 'average out at' in self.includePhrasalVSet_
        self.genIncludeIdioms()
        pass

    def parseStopFiles(self):
        WORD = 0
        PHRASAL = 1
        IDIOM   = 2
        for root, dirs, files in os.walk(self.stopDir_):
            for file in files:
                path  = '{}/{}'.format(root,file)
                fp  = open(path,"r")
                parseType = -1
                for line in fp:
                    line=line.strip()
                    if  line == '':
                        continue
                    if line[0] == '#':
                        cmd = line[1:].strip().lower()
                        if cmd.startswith('word'):
                            parseType = WORD
                            continue
                        elif cmd.startswith('phra'):
                            parseType = PHRASAL
                            continue
                        elif cmd.startswith('idiom'):
                            parseType = IDIOM
                            continue
                        else:
                            continue
                    else:
                        if parseType == WORD:
                            self.stopWords_ = self.stopWords_.union( line.split())
                        elif parseType == PHRASAL:
                            self.stopPhrasalVerbs_.add(line)
                        elif parseType == IDIOM:
                            self.stopIdioms_.add(line)
                        else:
                            assert False
                fp.close()
        #print('stop words {}'.format((self.stopWords_))); print('stop phrasal {}'.format(self.stopPhrasalVerbs_)); print('stop idioms {}'.format(self.stopIdioms_)); sys.exit(0)
        pass


    def isStopWord(self,w):
        return w in self.stopWords_

    def isStopPhrasalVerb(self,w):
        return w in self.stopPhrasalVerbs_

    def isStopIdiom(self,w):
        return w in self.stopIdioms_

    def getIncludeIdioms(self):
        return list(self.includeIdiomsSet_)

    def genIncludePhrasalV(self):
        out  = set()
        fp  = open (self.phrasalVerbFile, "r")
        for line in fp:
            line  = line.strip()
            r = re.search(r'\w+/[/\w]+', line)
            if   r is None:
                out.add(line)
                continue
            s = r.span()
            b  =  s[0]
            e  =  s[1]
            for m in  r.group(0).split('/'):
                m = m.strip()
                newLine =  '{} {} {}'.format(line[0:b].strip(), m, line[e:].strip())
                out.add(newLine)
                # if 'average out at' in line:
                    # print(newLine)
                    # print('average out at' in out)
        self.includePhrasalVSet_  = out
        pass

    def getExactLemma(self,lemma):
        """
>>> l = LoadWordList()
>>> l.getExactLemma('average out xx at')
'average out at'
>>> l.getExactLemma('get')
'get'
        """
        o = ''
        for p in self.includePhrasalVSet_:
            nextPhrase = False
            ps  = p.strip().split()
            p   = " ".join(ps)
            if  not lemma.startswith(ps[0]) or not lemma.endswith(ps[-1]):
                continue
            phralen  = 0
            for i in ps:
                if -1 == lemma.find(i):
                    nextPhrase = True
                    break
            if nextPhrase:
                continue
            o = p if len(p) > len(o) else o
        return o if o is not None and o != '' else lemma


    def genIncludeIdioms(self):
        out  = set()
        fp  = open (self.idiomFile_, "r")
        for line in fp:
            line  = line.strip()
            if '[' in line:
                assert '/' in line  and ']' in line, 'line ={}'.format(line)
                b  = line.index('[')
                e  = line.index(']')
                for m in line[b:e].replace('etc.', '').split('/'):
                    m = m.strip()
                    newLine =  '{} {} {}'.format(line[0:b].strip(), m, line[e:].strip())
                    if newLine not in self.includePhrasalVSet_ and newLine not in self.stopIdioms_:
                        out.add(newLine)
            elif line not in self.includePhrasalVSet_ and line not in self.stopIdioms_:
                    out.add(line)
            pass
        fp.close()
        self.includeIdiomsSet_  = out
        pass

    def getADPVocabulary(self):
        return {
        "aback" ,"about" ,"above" ,"across" ,"after" ,"against" ,"ahead" ,"all" ,"along"
        ,"alongside" ,"also" ,"among" ,"apart" ,"around" ,"as" ,"aside" ,"astray" ,"at" ,"attuned" ,"awa"
        ,"away" ,"back" ,"backwards" ,"bathed" ,"be" ,"beered" ,"before" ,"behind" ,"beneath"
        ,"bent" ,"beside" ,"between" ,"bevvied" ,"beyond" ,"bombed" ,"booked" ,"bound" ,"brassed" ,"browned" ,"bunged" ,"by" ,"called" ,"carried" ,"cast" ,"caught" ,"cheesed" ,"cling" ,"composed" ,"cooped" ,"count"
        ,"crawling" ,"cursed" ,"damp" ,"dampen" ,"doped" ,"dotted" ,"down" ,"drugged" ,"dying" ,"embroiled" ,"enamoured" ,"engrossed" ,"entitled" ,"faced" ,"fogged" ,"for" ,"forth" ,"forward" ,"from" ,"gagging" ,"get" ,"glued" ,"grounded" ,"gunning" ,"had" ,"hardened" ,"hedged" ,"hold" ,"in" ,"interspersed" ,"into" ,"inured" ,"invalided" ,"it" ,"juggle" ,"kitted" ,"labor" ,"lagered" ,"larded" ,"leave" ,"left" ,"liquored" ,"littered" ,"locked" ,"loved" ,"of" ,"off" ,"on" ,"onto" ,"opposed" ,"out" ,"over" ,"overboard" ,"packed" ,"parted" ,"past" ,"poshed" ,"possessed" ,"predisposed" ,"put" ,"rained" ,"ranged" ,"revenged" ,"riddled" ,"rooted" ,"round" ,"sandwiched" ,"sb" ,"schooled" ,"seconded" ,"set" ,"shagged" ,"shinny" ,"shorn" ,"shot" ,"shrouded" ,"shut"
        ,"slated" ,"snow" ,"snowed" ,"soaked" ,"socked" ,"spoiling" ,"spout" ,"sprawled" ,"steeped" ,"strewn" ,"struck" ,"stuffed" ,"stumped" ,"sucked" ,"swathed" ,"swept" ,"swimming" ,"taken" ,"through" ,"thrown" ,"tied" ,"to" ,"together" ,"togged" ,"torn" ,"toward" ,"towards" ,"under" ,"up" ,"upon" ,"vested" ,"weaned" ,"wedded" ,"wedged" ,"wired" ,"with" ,"within" ,"without" ,"yourself"
        }
    pass


if __name__ == "__main__":
    import doctest;doctest.testmod();sys.exit(0)
    sys.exit(0)
    pass

