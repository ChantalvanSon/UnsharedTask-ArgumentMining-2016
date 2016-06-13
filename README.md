
### Introduction
This repository provides the data and code used for the work described in [1]. If you use this data, please cite our paper.

This work was conducted in the context of [the Unshared Task of the 3rd Workshop on Argument Mining](http://argmining2016.arg.tech/index.php/home/call-for-papers/unshared-task/). The supplementary data for the Unshared Task was provided [here]( https://github.com/UKPLab/argmin2016-unshared-task).


### Data
The folder `data` contains the texts that were annotated as described in our paper. The texts have been pre-processed in several steps, resulting in different formats.

1. `editorial_articles`: this folder contains a set of 8 editorial articles (the development set of Variant D of the Unshared Task). More specifically, it contains 4 subfolders showing the pre-processing steps that were used for these texts:
  * `original`: contains the original plain text files as provided for the Unshared Task.
  * `stripped`: contains plain text files containing the title and the paragraphs of the editorial article. Created by removing 'meaningless' new lines and meta-data from the original text files.
  * `NAF-tokenized`: contains tokenized texts in NAF format. The English version of the  [ixa-pipe-tok](https://github.com/ixa-ehu/ixa-pipe-tok) module was used for the tokenization and sentence splitting.
  * `CAT-tokenized`: contains tokenized texts in CAT format. They were created using the `text2naf` script.
2. `discussions`: this folder contains a corresponding set of 8 discussions about the editorial articles (as originally provided for the Unshared Task). In total, the discussions contain 62 comments.
3. `Task1-annotations`: this folder contains the documents as they were annotated (including both the raw input and the annotated versions).
  * `CAT-input-format`: the files in this folder contain a comment (first sentence  in CAT format) and the corresponding editorial article (the remaining sentences).
  * `CAT-Round-1`: contains the annotations of Round 1 in CAT XML format.
  * `CAT-Round-2`: contains the annotations of Round 2 in CAT XML format.

### Code
to be added soon

### References
 [1] C. van Son, T. Caselli, A. Fokkens, I. Maks, R. Morante, L. Aroyo, and P. Vossen. Unshared Task at the 3rd Workshop on Argument Mining: perspective based local agreement and disagreement in online debate. In *Proceedings of the 3rd Workshop on Argument Mining*, Berlin, Germany, 2016. Association for Computational Linguistics.
