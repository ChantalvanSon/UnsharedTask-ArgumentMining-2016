# Data VUA-Perspectives for the Unshared Task on Argument Mining (ACL 2016)

THIS IS A DRAFT VERSION

Editorial articles (Variant C):

1. Tokenization: The texts are tokenized using the [IXA-pipe-tokenizer](https://github.com/ixa-ehu/ixa-pipe-tok). The output of this tokenizer is NAF.
2. Convert NAF > CAT for annotation: The propositions are annotated using [CAT](https://dh.fbk.eu/resources/cat-content-annotation-tool))(acronym for CELCT/Content Annotation Tool). We use the script naf2cat.py to produce the simple tokenized input format for CAT (one token per line and <EOS> between sentences) from the tokenized NAF files. The output of the annotations is in CAT XML format.
