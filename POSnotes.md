## Types of Intentional Sentences
(Ordered by their structure)

1. Verb indicates belief.
2. Verb indicates desire.
3. Belief/desire is subject of sentence.
4. Belief/desire is direct object in "it is..." sentence.

- - - -

## Intention Detection Errors:

A,B Didn’t detect: “I have come to tell you that it is my longing to…”

X A,B Didn’t detect: “My desire is to become a Samana.”
	Drat, it looks like the POS tagger mistagged the “my” in “my desire” as a proper noun. No amount of regex work will make that work. Oh well, throwing this out.

X False positive: “He remembered that he had often felt a slight pain in bed…”
	This is debatable though, seeing as how it could be interpreted as showing intent, even though the author’s purpose was probably just to evoke an empathetic imagining in the reader.
	I think I will call this as no longer a false positive.

A,B,C Didn’t detect: “He did not have the slightest doubt that…”
	This is also debatable, but should have been picked up.
	Unfortunately, there is a mislabelling from the nltk, which didn’t notice that that “did not have” as the entire verb construction.
	Perhaps can compensate for these sorts of constructions.
	Would require chunking/entity detection, too, but then it would be fixed.

X Didn’t detect: ”She understanding I was a printer, WOULD HAVE HAD ME stay at that town and follow my business, being ignorant of the stock necessary to begin with." ?
	Not concerned with this, the second part is the action associated with the intention, not the intention itself. No longer marking as an error.

A,B Any way to detect: "and about midnight, not having yet seen the city, some of the company were confident we must have passed it, and would row no farther;" ?
	Maybe ascribe belief and attitude descriptions to entities (through “is” verbs)?
	If entity detection / chunking is done right, the program should recognize that (some of the company) (were) (confident), where “confident” is an ascription of a belief.

X A,D Didn’t detect: “…he had started to feel that the love of his father and…”
	Again, requires good verb deconstruction.
	Should I detect “feel that…” as a special case? It seems to denote a cognitive quality that simply “feel…” doesn’t.
	(feel that, sense that, discern that, notice that, aware that, conscious that, hold that, maintain that, get the impression that, have a hunch that)

A,D False Positive: “How deaf and stupid have I been!” he THOUGHT, walking swiftly along.
	To fix this, I am going to move “thought” to the category of verbs that only is triggered when it is accompanied with the word “that”. It might be used sometimes in intentional ways without the “that”, but it is more of a phenomenal word than one with cognitive content.

X Didn’t catch: “No, this is over, I have awakened, I have indeed awakened and have not been born before this very day.” (The context is that he is remarking to himself that he has been blind to the truth of things, and he is here deciding to change his ways.)
	This one is exceedingly tricky, and I don’t think I have any particular method for having the system detect this. The intention in this sentence is communicated implicitly instead of outright stated, and I don’t think there is any way to have a script catch this since all of the intention is hidden in the context, rather than explicitly stated.
	Marking unable to fix.

A,B Doesn’t catch: “I am going to…”


- - - -

Fixes:

A. Chunking / entity detection
B. Detect beliefs/attitudes that are nouns/objects
C. Verb cluster intelligence
D. Cognitive versions of emotion words (i.e. “feels that…”)

A) Good resource: http://www.eecis.udel.edu/~trnka/CISC889-11S/lectures/dongqing-chunking.pdf
	Okay, so unfortunately it looks like there is no “one size fits all” solution here. The solutions that exist are useful only in domains they were designed/trained for.
	Two ways to about it: regex and training a chunk parser.
	Probably need to look at doing regex parsing on a case-by-case basis instead of trying to create a master chunk regex grammar for all cases. When I need it for a specific application, I just call the appropriate regex grammars.
	Those cases are: “it (is/are/were) (PRP) (belief/attitude)”, “(PRP) (belief/attitude) is…”, “have (belief/attitude)”, “(NN) (is/are/were) (belief/attitude/‘confident’)”, “(phenomenal verb) that”