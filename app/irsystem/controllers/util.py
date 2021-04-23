import math
import numpy as np
from . import *  
from collections import defaultdict
from collections import Counter
from nltk.tokenize import TreebankWordTokenizer

def build_inverted_index(msgs):
    inverted_index = {}
    idx = 0
    for msg in msgs:
        cnt = Counter(msg['toks'])
        shoe_id = msg['shoe_id']
        for k, v in cnt.items():
            if k not in inverted_index:
                inverted_index[k] = []
            inverted_index[k].append((idx, shoe_id, v))
        idx+=1
    return inverted_index

def compute_idf(inv_idx, n_docs):
    idf = {}
    for k, v in inv_idx.items():
        # if len(v) < min_df: continue
        # if len(v) / n_docs > max_df_ratio: continue
        df_t = len(v)
        idf[k] = math.log2(n_docs/(1 + df_t))
    return idf

def compute_doc_norms(index, idf, n_docs):
    norms = np.zeros(n_docs)
    for k, v in index.items():
        if k not in idf: continue
        for tup in v: 
            (doc, shoe_id, tf) = tup
            norms[doc] += math.pow(tf * idf[k], 2)
    
    return np.sqrt(norms)

def index_search(query, index, idf, doc_norms):
    treebank_tokenizer = TreebankWordTokenizer()
    query_toks = treebank_tokenizer.tokenize(query.lower())
    scores = {}
    query_tf = Counter(query_toks)
    for term, term_tf in query_tf.items():
        if term in index:
            for (doc, shoe_id, tf) in index[term]:
                scores[doc] = scores.get(doc, 0) + term_tf * idf[term] * tf * idf[term]
    
    q_norm = 0
    for term, tf in query_tf.items():
        if term in index:
            q_norm += math.pow(tf * idf[term], 2)
    
    q_norm = math.sqrt(q_norm)
    
    res = []
    for doc, score in scores.items():
        res.append((score / (q_norm * doc_norms[doc]), doc))
    
    return sorted(res, key=lambda tup: (-tup[0], tup[1]))
                