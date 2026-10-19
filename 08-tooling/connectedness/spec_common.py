"""Shared helpers of the connectedness specs. A relation is P(id, label, domain, range, claim, basis...) where each basis is (class label, verbatim quote of the chapter's own text);
the generator refuses a quote that is not found word for word in the chapter's A-Box, research or document file (no claim without a source text)."""
NOTE = "Version {v} repairs connectedness (discipline version 2.18.0 BP-D56 and version 2.19.0 BP-D57): the subject branches of the chapter are now linked to one another by the relations the chapter's own definitions state, chx:hasOwner has the domain and range its use shows where the file declares it, and chx:input and chx:output are declared. No class was added, removed or renamed, so MINOR."
def P(i, label, dom, rng, claim, *basis):
    why = claim.rstrip(".") + ". Basis: " + "; ".join("the chapter says of %s: '%s'" % (b[0], b[1]) for b in basis) + "."
    return dict(id=i, label=label, dom=dom, rng=rng, why=why, quotes=[b[1] for b in basis], basis=basis)
