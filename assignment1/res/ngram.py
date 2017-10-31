from __future__ import unicode_literals

from nltk.probability import ConditionalProbDist, ConditionalFreqDist
from nltk.util import ngrams
from nltk import compat


@compat.python_2_unicode_compatible
class NgramModel:
    def __init__(self, n, train, estimator, *estimator_args, **estimator_kwargs):
        """
        Minimalistic "ngram model" based on the broken NLTK implementation. Stripped
        of pretty much all functionality except for generating. Check out the
        "generate_one" method for that.
        NOTE a model created for some n will also create models for all smaller values
        of n down to 1 to use as backoff (in case an unseen context is encountered).
        So instead of creating separate models for n=2,3,4 you can just create one for
        n=4 and access the n=3 one via this model's backoff attribute. And then get
        the n=2 model via the backoff for the n=3 one.

        Parameters:
        n: The order of the language model (ngram size). Must be integer.
        train: The training text. Can be a list of strings (words), or a list of lists of
               strings. In the latter case, each inner list is treated as an independent 
               sentence.
        estimator: A function for generating a probability distribution. 
                   Something like MLEProbDist, LaplaceProbDist etc.
                   Check out nltk.probability for these.
                   Some of them are probably broken though.
        estimator_args: Extra arguments for estimator. You can pretty much ignore these.
        estimator_kwargs: Extra keyword arguments for the estimator. For example,
                          a LidstoneProbDist requires a gamma argument. So you
                          should pass gamma=0.01 (or whatever value you want)
                          to the constructor of the NgramModel.
        """
        # make sure n is greater than zero, otherwise print it
        assert (n > 0), n

        # For explicitness save the check whether this is a unigram model
        self.is_unigram_model = (n == 1)
        # save the ngram order number
        self._n = n
        cfd = ConditionalFreqDist()

        # set read-only ngrams set (see property declaration below to reconfigure)
        self._ngrams = set()

        # If given a list of strings instead of a list of lists, create enclosing list
        if (train is not None) and isinstance(train[0], compat.string_types):
            train = [train]

        # this is the actual "training" part
        for sent in train:
            raw_ngrams = ngrams(sent, n)
            for ngram in raw_ngrams:
                self._ngrams.add(ngram)
                context = tuple(ngram[:-1])
                token = ngram[-1]
                cfd[context][token] += 1

        self._probdist = ConditionalProbDist(cfd, estimator, *estimator_args, **estimator_kwargs)

        # recursively construct the lower-order models
        if not self.is_unigram_model:
            self._backoff = NgramModel(n-1, train,
                                       estimator,
                                       *estimator_args,
                                       **estimator_kwargs)

    @property
    def ngrams(self):
        return self._ngrams

    @property
    def backoff(self):
        return self._backoff

    @property
    def probdist(self):
        return self._probdist

    def generate_one(self, context):
        """
        Generates one word from the ngram's probability distribution given
        some context. The context should be a tuple of length n-1. E.g.
        3-grams need a context of length 2. So for starting the process,
        either choose some random context yourself, or just empty strings.
        If a context is unknown to this model, it will automatically pick
        a smaller context, down to generating a unigram if necessary.
        """
        context = tuple(context)
        if len(context) != self._n - 1:
            raise ValueError("Context length does not match ngram length!")
        if context in self:
            return self[context].generate()
        elif self._n > 1:
            return self._backoff.generate_one(context[1:])
        else:
            return "<ERROR>"

    def __contains__(self, item):
        return tuple(item) in self._probdist

    def __getitem__(self, item):
        return self._probdist[tuple(item)]

    def __repr__(self):
        return '<NgramModel with %d %d-grams>' % (len(self._ngrams), self._n)
