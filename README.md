
### Introduction
This repository provides the data and code used for the work described in:

> C. van Son, T. Caselli, A. Fokkens, I. Maks, R. Morante, L. Aroyo, and P. Vossen (2016). "Unshared Task at the 3rd Workshop on Argument Mining: perspective based local agreement and disagreement in online debate." In *Proceedings of the 3rd Workshop on Argument Mining*, Berlin, Germany.

This work was conducted in the context of [the Unshared Task of the 3rd Workshop on Argument Mining](http://argmining2016.arg.tech/index.php/home/call-for-papers/unshared-task/). The supplementary data for the Unshared Task was provided [here]( https://github.com/UKPLab/argmin2016-unshared-task). For the annotations described in our paper, we used the development sets of Variants C (editorial articles) and D (discussions).

The annotations were done using the [Content Annotation Tool (CAT)](https://dh.fbk.eu/resources/cat-content-annotation-tool) [2].

### Data
The folder `data` contains the texts that were annotated as described in our paper. The texts have been pre-processed in several steps, resulting in different formats.

1. `editorial_articles`: this folder contains a set of 8 editorial articles (the development set of Variant D of the Unshared Task). More specifically, it contains 4 subfolders resulting from several pre-processing steps:
  * `original`: contains the original plain text files as provided for the Unshared Task.
  * `stripped`: contains plain text files containing the title and the paragraphs of the editorial article. Created by removing 'meaningless' new lines and meta-data from the original text files.
  * `NAF-tokenized`: contains tokenized texts in NAF format. The English version of the  [ixa-pipe-tok](https://github.com/ixa-ehu/ixa-pipe-tok) module was used for the tokenization and sentence splitting.
  * `CAT-tokenized`: contains tokenized texts in CAT input format. They were created using the `naf2cat.py` script.
2. `discussions`: this folder contains a corresponding set of 8 discussions about the editorial articles (as originally provided for the Unshared Task). In total, the discussions contain 62 comments.
3. `Task1-annotations`: this folder contains the documents as they were annotated (including both the raw input and the annotated versions).
  * `CAT-input-format`: contains files consisting of a comment (first sentence  in CAT format) and the corresponding editorial article (the remaining sentences). They were created using the `write_cat_files.py` script
  * `CAT-Round-1`: contains the annotations of Round 1 in CAT XML format.
  * `CAT-Round-2`: contains the annotations of Round 2 in CAT XML format.

### Code & Replication

The documents were pre-processed for the annotations using the following scripts and modules in this order:

* `1-write_stripped_articles.py`
* `2-ixa-pipe-tok`
* `3-naf2cat.py`
* `4-write_cat_files.py`

Some of these scripts make use of the following two general modules:

* `cat-information.py`: contains general functions for getting information from CAT XML files
* `naf-information.py`: contains general functions for getting information from NAF files

To get the distributions of the annotations as described in our paper, the following script was used:
* `get_distribution_annotations.py`




### References
 [1] C. van Son, T. Caselli, A. Fokkens, I. Maks, R. Morante, L. Aroyo, and P. Vossen (2016). "Unshared Task at the 3rd Workshop on Argument Mining: perspective based local agreement and disagreement in online debate." In *Proceedings of the 3rd Workshop on Argument Mining*, Berlin, Germany.

 [2] V. B. Lenzi, G. Moretti, and R. Sprugnoli (2012). "CAT: the CELCT Annotation Tool". In *Proceedings of the 8th International Conference on Language Resources and Evaluation (LREC 2012)*, Istanbul, Turkey. ([pdf](http://www.lrec-conf.org/proceedings/lrec2012/pdf/216_Paper.pdf))
