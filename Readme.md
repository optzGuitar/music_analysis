# This is a system to analyze and compose music using Answer Set Programming

Instead of using genre-dependent constraints we use the result of our analysis to guide the search for a musical piece.
Our analysis uses pattern mining to find reoccurring patterns inside the input files. These patterns get translated into rules used by the composer.
We use MIDI files as input and output format as they are widely available and used.
We divided our system into three parts:
1. MIDI -> ASP
2. pattern mining
3. composing

For a usage example see 'usage_example.py'

## Dependencies

We use the *clingo* and *Mido* package for our system.
They can be installed using Anaconda and pip respectively.
```shell
conda install -c potassco clingo
pip install mido
```
You can find more information about *clingo* on the Potassco website [https://potassco.org/](https://potassco.org/) and about *Mido* on their GitHub [https://github.com/mido/mido](https://github.com/mido/mido)