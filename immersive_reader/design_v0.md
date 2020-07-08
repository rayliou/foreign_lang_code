[toc]

# architecture 
``` dot
    digraph G {
    M -> L,S,R,W;
    L -> AudioToText -> align_subtitles -> L_P -> review;
    S -> conversation -> collect_words -> review;
    W -> edit -> predict_suggest ->wordnet,synonym, vocabulary_restrain  -> tutor_edit -> diff_highlight -> version_control -> review;
    R -> epub ,clipboard -> ray_html -> review  
}
```

# Reading Flow

``` dot
digraph G {
seqs_doc [label = "idx|seg|lemma"];
R -> S-> epub ,clipboard -> ray_html -> simplyfy -> nlp_parse -> output_type -> seqs_doc ,global_stats;
global_stats -> word_rank -> w,pos, rank, links;
global_stats -> phrase,idiom;  
R -> C-> offline ,online-> render -> cur_page,bookmark,stop_words, wods_catogrory_highlight, seqs_doc -> reading;
reading -> turn_page,click, words_rank_cur_page, add_delete_wordlist, bookmark -> sentence_word, sync ;
sentence_word -> review;
online ->  seqs_doc, global_stats;

}
```
# MD Reference
- [Markdown usage](https://shd101wyy.github.io/markdown-preview-enhanced/#/zh-cn/markdown-basics?id=%e9%93%be%e6%8e%a5)
