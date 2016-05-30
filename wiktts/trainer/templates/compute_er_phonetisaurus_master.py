#!/usr/bin/python
# coding=utf-8

from __future__ import absolute_import
from __future__ import print_function

# Copyright (c) [2012-], Josef Robert Novak
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
#  modification, are permitted #provided that the following conditions
#  are met:
#
#  * Redistributions of source code must retain the above copyright 
#    notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above 
#    copyright notice, this list of #conditions and the following 
#    disclaimer in the documentation and/or other materials provided 
#    with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) 
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, 
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED 
# OF THE POSSIBILITY OF SUCH DAMAGE.

# NOTE 2016-05-30, modified by Alberto Pettarin (alberto@albertopettarin.it)

import io, re, operator, sys
from collections import defaultdict


class ErrorRater( ):
    """
      This class provides tools suitable for computing the Word Error Rate (WER)
       or Pronunciation Error Rate (PER) of one or more hypothesis-reference
       transcription pairs.
       
      Specifically it provides functions to compute Levenshtein penalty matrix,
       a non-recursive traceback function, WER/PER computation function, and 
       several formatting convenience functions.
    """

    def __init__( self, ignore="", regex_ignore="", ignore_both=False ):
        self.ignore = re.split(r"\s+", ignore)
        self.regex_ignore = regex_ignore
        self.ignore_both = ignore_both
        #The 'totals' array tracks [ TotalChars, Matches, Substitutions, Insertions, Deletions ] 
        # over a test set.  This information is used to compute WER/PER scores for 
        # the entire test set in the standard manner.
        self.totals = [ 0., 0., 0., 0., 0. ]

        #A running count of the number of hyp/ref pairs that were NOT perfectly aligned
        #For ASR this corresponds to SENTENCE ERRORS, for G2P this corresponds to WORD ERRORS
        self.sequence_errors = 0.
        self.total_sequences = 0.
        
    def compute_penalty_matrix( self, hyp, ref ):
        """
          Compute the penalty matrix using the levenshtein algorithm.  
          The edit distance between the two sequences will be stored 
            in the last entry in the matrix.
        """
        matrix = [ [0 for x in range(len(ref)+1)] for y in range(len(hyp)+1) ]
        for i in range(len(hyp)+1):
            matrix[i][0] = i
        for j in range(len(ref)+1):
            matrix[0][j] = j

        for i in range(1,len(hyp)+1):
            for j in range(1,len(ref)+1):
                if hyp[i-1]==ref[j-1]:
                    matrix[i][j] = matrix[i-1][j-1]
                else:
                    matrix[i][j] = min( matrix[i-1][j]+1, matrix[i][j-1]+1, matrix[i-1][j-1]+1 )

        return [matrix,hyp,ref]


    def compute_traceback( self, matrix, hyp, ref ):
        """
          Compute the traceback and align the two input sequences.
          Also compute the Insertions, Deletions, and Substitutions.
          Note that there is often more than one valid alignment for 
           a given alignment score.  In these cases the order of operations
           below determines whether an 'S', 'I' or 'D' will be chosen.
        """
        alignment = []
        # [ TotalChars, Match, Substitution, Insertion, Deletion ]
        scores    = [0.,0.,0.,0.,0.]
    
        i = len(hyp); j = len(ref)
        while i>0 and j>0:
            if hyp[i-1]==ref[j-1]:
                alignment.append( self._normalize([ hyp[i-1], "|", ref[j-1] ]) )
                i-= 1; j-=1; scores[1]+=1
            elif matrix[i][j]==matrix[i-1][j-1]+1:
                alignment.append( self._normalize([ hyp[i-1], " ", ref[j-1] ]) )
                i-=1; j-=1; scores[2]+=1
            elif matrix[i][j]==matrix[i-1][j]+1:
                alignment.append( self._normalize([ hyp[i-1], " ", "*" ]) )
                i-=1; scores[3]+=1
            else:
                alignment.append( self._normalize([ "-", " ", ref[j-1] ]) )
                j-=1; scores[4]+=1
        while i>0:
            alignment.append( self._normalize([ hyp[i-1], " ", "*" ]) )
            i-=1; scores[3]+=1
        while j>0:
            alignment.append( self._normalize([ "-", " ", ref[j-1] ]) )
            j-=1; scores[4]+=1

        alignment.reverse()
        scores[0] = len(ref)
        
        return alignment, scores

    def _normalize( self, units ):
        """
          Normalize the length of the individual units/words being aligned.
          We want each unit of the REF, CONN, and HYP arrays to be the same 
           length, mainly because it makes the alignment output easier on the 
           eyes.
        """

        max_unit = max( units, key=lambda unit:len(unit) )
        for i,unit in enumerate(units):
            diff = len(max_unit) - len(unit)
            units[i] = unit.center(len(unit)+diff, " ")
        
        return units

    def print_alignment( self, alignment, scores ):
        """
          Print out an alignment.  The alignment information is stored in a 
           2D array where each element stores a triple consisting of: 
             [ HypothesisToken, Connector, ReferenceToken ]
          These sequences will be printed out in reverse order so that the 
           reference sequence is on top.
        """
        
        print(u" ".join([ x[2] for x in alignment ]))
        print(u" ".join([ x[1] for x in alignment ]))
        print(u" ".join([ x[0] for x in alignment ]))
        self.print_ER( scores )
        print("")

        return

    def _filter_ignore_list( self, flist ):
        """
          Filter out any unwanted characters as specified 
           in the ignore values.
        """
        
        if type(flist[0]).__name__=="str":
            for ig in self.ignore:
                flist = list(filter(lambda ch: ch!=ig, flist))
        else:
            for i in range(len(flist)):
                for ig in self.ignore:
                    flist[i] = list(filter(lambda ch: ch!=ig, flist[i]))
        return flist

    def _filter_regex_ignore( self, flist ):
        """
          Filter out any unwanted characters as specified
           in the regex_ignore variable. 
        """

        if type(flist[0]).__name__=="str":
            flist = [ re.sub(self.regex_ignore,"",ch) for ch in flist ]
            flist = list(filter(lambda ch: ch!="", flist))
        else:
            for i in range(len(flist)):
                flist[i] = [ re.sub(self.regex_ignore,"",ch) for ch in  flist[i] ]
                flist[i] = list(filter(lambda ch: ch!="", flist[i]))
        return flist

    def _filter_ignore( self, flist ):

        if not self.regex_ignore=="":
            flist = self._filter_regex_ignore( flist )
        if not len(self.ignore)==0:
            flist = self._filter_ignore_list( flist )

        return flist

    def align_sequences( self, hyps, refs, verbose=False ):
        """
          Align one or more hypothesis sequence with one or more references.
          If more than one hypothesis and/or more than one reference is supplied
           then only the BEST match will be passed on for scoring.
        """

        if not type(hyps).__name__=="list" or not type(refs).__name__=="list":
            raise TypeError("Hypothesis and reference(s) must be lists!")

        hyps = self._filter_ignore( hyps )
        if self.ignore_both:
            refs = self._filter_ignore( refs )
        if len(refs)==0 or len(hyps)==0 or len(refs[0])==0 or len(hyps[0])==0:
            return

        if type(refs[0]).__name__=="str" and type(hyps[0]).__name__=="str":
            #Both the REFS and HYPS lists are of length 1. So we don't need
            # to look for the 'best' combination.  We only have one choice.
            matrix, hyp, ref = self.compute_penalty_matrix( hyps, refs )
        elif not type(refs[0]).__name__=="str" and not type(hyps[0]).__name__=="str":
            #Both the REFS and HYPS lists are of length>1. We have to search
            # all possible combinations for the best match.  This is coded below 
            # as a nested call to min().  This means we have to look at 
            #  len(REFS)*len(HYPS) combinations for the best matching pair.
            matrix, hyp, ref = min( [  
                    min(
                        [ self.compute_penalty_matrix( hyp, ref ) for ref in refs ], 
                        key=lambda mat:mat[0][-1][-1] 
                        ) for hyp in hyps ],
                                    key=lambda mat:mat[0][-1][-1] )         
        elif type(hyps[0]).__name__=="str" and not type(refs[0]).__name__=="str":
            #The REFS list contains just one reference.  The HYPS list contains 
            # more than one hypothesis.  
            matrix, hyp, ref = min( 
                  [ self.compute_penalty_matrix( hyps, ref ) for ref in refs ], 
                  key=lambda mat:mat[0][-1][-1] 
                )
        elif not type(hyps[0]).__name__=="str" and type(refs[0]).__name__=="str":
            #The REFS list contains more than one reference transcription.
            #The HYPS list contains just one hypothesis.
            matrix, hyp, ref = min(
                [ self.compute_penalty_matrix( hyp, refs ) for hyp in hyps ],
                key=lambda mat:mat[0][-1][-1]
                )
            
        alignment, scores = self.compute_traceback( matrix, hyp, ref )
        self.total_sequences += 1
        if matrix[-1][-1]>0: 
            self.sequence_errors += 1
        if verbose: 
            self.print_alignment( alignment, scores )

        self.totals = [ scores[i]+self.totals[i] for i in range(len(scores)) ]
    
        return alignment, scores
    
    def split_sequence( self, sequence, usep=" ", fsep="\t" ):
        """
          Split an input string into one or more sequences, and return a 
           1D or 2D array containing the results.
        """

        if not type(sequence).__name__=="str":
            raise TypeError("Input sequence must be of type string ('str')!")
        
        if usep=="":
            sequences = [
                  [ unit for unit in list(seq) ] 
                    for seq in re.split( fsep, sequence )
                ]
        else:
            sequences = [ 
                  [ unit for unit in re.split( usep, seq ) ] 
                    for seq in re.split( fsep, sequence ) 
                ]
        if len(sequences)==1: 
            return sequences[0]
        else: 
            return sequences
    
    def compute_PER_phonetisaurus( self, hypfile, reffile, usep=" ", fsep="\t", verbose=False ):
        """
          Compute the total PER for Phonetisaurus input test files.
          Standard Phonetisaurus output format is:
            hypfile: 
             WORD SCORE PRON
            reffile:
             WORD PRON1, ..., PRONn
          Fields are separated by 'tab', and phoneme tokens in each PRON are 
           separated by a single space, ' '.
          
          PER is computed in the standard manner:
              (S+I+D)/(T)
           where T=TotalTokens, S=Substitutions, I=Insertions, D=Deletions
        """

        words = []; hyps = []; refs = []
        rejected = []
        for i,line in enumerate(io.open(hypfile, "r", encoding="utf-8")):
            #There should be three fields
            try:
                word, score, pron = line.strip().split(fsep)
                phons = re.split(usep, pron)
                #This assumes that we will never have a test situation
                # where the input list intentionally contains 2 repetitions
                # of the same test words, e.g.,
                #   TESTWORD
                #   TESTWORD
                #It assumes that if we find such a sequence in a hypothesis
                # file that this means we have N-best results for one 
                # instance of TESTWORD.
                #This assumption is fine for G2P evaluations, but will 
                # not hold for ASR where we might have multiple speakers
                # producing utterances with the same content and would 
                # certainly need to distinguish between them.
                #TLDR use the 'cmu' or 'htk' functions for ASR - not this one!
                if len(words)>0 and words[-1]==word:
                    hyps[-1].append( phons )
                else:
                    hyps.append( [ re.split(usep, pron) ] )
                    words.append(word)
            except:
                print(line)
                rejected.append(i)
        for i,line in enumerate(io.open(reffile, "r", encoding="utf-8")):
            if i not in rejected:
                #There should be at least 2 fields.  
                # Word, Hyp1, ..., HypN
                fields = line.strip().split(fsep)
                refs.append( [ re.split(usep, field) for field in fields[1:] ] )
            
        #Make sure we have the same number of entries
        print("Words:", len(words), " Hyps:", len(hyps), "Refs:", len(refs))
        assert len(words)==len(hyps) and len(hyps)==len(refs)
        
        for i, word in enumerate(words):
            if verbose: print(word)
            self.align_sequences( hyps[i], refs[i], verbose=verbose )
            
        self.print_ER(self.totals)

        return

    def print_ER( self, totals ):
        """
          PrettyPrint out the Word/Pronunciation Error Rate and information about
           the relative number of Matches, Substitutions, Insertions and Deletions.
        """
        width = 70
        if totals==self.totals: print("".join(["#" for i in range(width)]))
        print("EVALUATION RESULTS".center(width," "))
        if totals==self.totals: print("".join(["-" for i in range(width)]))
        print("(T)otal tokens in reference: %d" % (int(totals[0])))
        print("(M)atches: %d  (S)ubstitutions: %d  (I)nsertions: %d  (D)eletions: %d" %\
            (int(totals[1]), int(totals[2]), int(totals[3]), int(totals[4])))
        print("%% Correct (M/T)           -- %%%0.2f" % ( 100*totals[1]/totals[0] ))
        print("%% Token ER ((S+I+D)/T)    -- %%%0.2f" % ( 100*        (sum(totals[2:])/totals[0])   ))
        print("%% Accuracy 1.0-ER         -- %%%0.2f" % ( 100*(1.0 - (sum(totals[2:])/totals[0]) ) ))
        if totals==self.totals: print("".join(["-" for i in range(int((float(width)/5)*4))]).center(width," "))
        print("(S)equences: %d  (C)orrect sequences: %d  (E)rror sequences: %d" %\
            (int(self.total_sequences), int(self.total_sequences - self.sequence_errors), int(self.sequence_errors)))
        print("%% Sequence ER (E/S)       -- %%%0.2f" % ( 100*(self.sequence_errors/self.total_sequences) ))
        print("%% Sequence Acc (1.0-E/S)  -- %%%0.2f" % ( 100*(1.0-(self.sequence_errors/self.total_sequences)) ))
        if totals==self.totals: print("".join(["#" for i in range(width)]))
        return



if __name__=="__main__":
    """
    Usage: python compute_er_phonetisaurus_master.py file.hyp file.ref
    """
    error_rater = ErrorRater(ignore="", regex_ignore="", ignore_both=False)
    hyp = sys.argv[1]
    ref = sys.argv[2]
    usep = u" "
    fsep = u"\t"
    verbose = False
    error_rater.compute_PER_phonetisaurus(hyp, ref, usep, fsep, verbose)



