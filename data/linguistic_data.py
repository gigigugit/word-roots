"""
Linguistic database of roots, prefixes, and suffixes with analysis helpers.
"""

PREFIXES = {
    "anti": {
        "display": "anti-",
        "meaning": "against, opposing",
        "origin": "Greek",
        "examples": ["antibiotic", "antisocial", "antidote"],
    },
    "auto": {
        "display": "auto-",
        "meaning": "self, same",
        "origin": "Greek",
        "examples": ["automatic", "autobiography", "autopilot"],
    },
    "bi": {
        "display": "bi-",
        "meaning": "two, twice",
        "origin": "Latin",
        "examples": ["bicycle", "bilingual", "biennial"],
    },
    "co": {
        "display": "co-",
        "meaning": "together, jointly",
        "origin": "Latin",
        "examples": ["cooperate", "coexist", "coauthor"],
    },
    "de": {
        "display": "de-",
        "meaning": "away, down, undo",
        "origin": "Latin",
        "examples": ["decode", "decompose", "deflate"],
    },
    "dis": {
        "display": "dis-",
        "meaning": "not, opposite of",
        "origin": "Latin",
        "examples": ["disagree", "disconnect", "disorder"],
    },
    "ex": {
        "display": "ex-",
        "meaning": "out of, former",
        "origin": "Latin",
        "examples": ["export", "exclude", "ex-president"],
    },
    "hyper": {
        "display": "hyper-",
        "meaning": "over, above, excessive",
        "origin": "Greek",
        "examples": ["hyperactive", "hyperbole", "hyperlink"],
    },
    "hypo": {
        "display": "hypo-",
        "meaning": "under, below, deficient",
        "origin": "Greek",
        "examples": ["hypothesis", "hypoglycemia", "hypodermic"],
    },
    "in": {
        "display": "in-",
        "meaning": "not, into, within",
        "origin": "Latin",
        "examples": ["incomplete", "inject", "inland"],
    },
    "inter": {
        "display": "inter-",
        "meaning": "between, among",
        "origin": "Latin",
        "examples": ["international", "interact", "intercept"],
    },
    "micro": {
        "display": "micro-",
        "meaning": "small, very small",
        "origin": "Greek",
        "examples": ["microscope", "microphone", "microwave"],
    },
    "mis": {
        "display": "mis-",
        "meaning": "wrongly, bad",
        "origin": "Old English",
        "examples": ["mistake", "misunderstand", "misspell"],
    },
    "mono": {
        "display": "mono-",
        "meaning": "one, single",
        "origin": "Greek",
        "examples": ["monologue", "monotone", "monocle"],
    },
    "multi": {
        "display": "multi-",
        "meaning": "many, multiple",
        "origin": "Latin",
        "examples": ["multiply", "multicolor", "multimedia"],
    },
    "non": {
        "display": "non-",
        "meaning": "not, without",
        "origin": "Latin",
        "examples": ["nonfiction", "nonprofit", "nonsense"],
    },
    "poly": {
        "display": "poly-",
        "meaning": "many, several",
        "origin": "Greek",
        "examples": ["polygon", "polyglot", "polynomial"],
    },
    "post": {
        "display": "post-",
        "meaning": "after, behind",
        "origin": "Latin",
        "examples": ["postwar", "postpone", "postscript"],
    },
    "pre": {
        "display": "pre-",
        "meaning": "before, in advance",
        "origin": "Latin",
        "examples": ["preview", "predict", "prepare"],
    },
    "pro": {
        "display": "pro-",
        "meaning": "for, forward, in favour of",
        "origin": "Latin/Greek",
        "examples": ["progress", "promote", "prologue"],
    },
    "re": {
        "display": "re-",
        "meaning": "again, back",
        "origin": "Latin",
        "examples": ["return", "rebuild", "recycle"],
    },
    "semi": {
        "display": "semi-",
        "meaning": "half, partly",
        "origin": "Latin",
        "examples": ["semifinal", "semicircle", "semiconductor"],
    },
    "sub": {
        "display": "sub-",
        "meaning": "under, below",
        "origin": "Latin",
        "examples": ["subway", "submarine", "submerge"],
    },
    "super": {
        "display": "super-",
        "meaning": "above, over, beyond",
        "origin": "Latin",
        "examples": ["superhero", "supernatural", "supervise"],
    },
    "tele": {
        "display": "tele-",
        "meaning": "distant, far",
        "origin": "Greek",
        "examples": ["telephone", "television", "telescope"],
    },
    "trans": {
        "display": "trans-",
        "meaning": "across, beyond",
        "origin": "Latin",
        "examples": ["transport", "transfer", "transform"],
    },
    "ultra": {
        "display": "ultra-",
        "meaning": "beyond, extreme",
        "origin": "Latin",
        "examples": ["ultraviolet", "ultrasound", "ultramodern"],
    },
    "un": {
        "display": "un-",
        "meaning": "not, reverse action",
        "origin": "Old English",
        "examples": ["unhappy", "undo", "unknown"],
    },
    "uni": {
        "display": "uni-",
        "meaning": "one, single",
        "origin": "Latin",
        "examples": ["uniform", "universe", "unicorn"],
    },
}

SUFFIXES = {
    "able": {
        "display": "-able",
        "meaning": "capable of, able to be",
        "origin": "Latin",
        "part_of_speech": "adjective",
        "examples": ["readable", "teachable", "drinkable"],
    },
    "al": {
        "display": "-al",
        "meaning": "relating to, pertaining to",
        "origin": "Latin",
        "part_of_speech": "adjective",
        "examples": ["natural", "musical", "educational"],
    },
    "ance": {
        "display": "-ance",
        "meaning": "state of, quality of",
        "origin": "Latin",
        "part_of_speech": "noun",
        "examples": ["guidance", "performance", "resistance"],
    },
    "ate": {
        "display": "-ate",
        "meaning": "to make, to cause",
        "origin": "Latin",
        "part_of_speech": "verb",
        "examples": ["create", "activate", "educate"],
    },
    "ation": {
        "display": "-ation",
        "meaning": "action or process of",
        "origin": "Latin",
        "part_of_speech": "noun",
        "examples": ["creation", "education", "exploration"],
    },
    "cy": {
        "display": "-cy",
        "meaning": "state, quality of",
        "origin": "Greek/Latin",
        "part_of_speech": "noun",
        "examples": ["democracy", "literacy", "accuracy"],
    },
    "dom": {
        "display": "-dom",
        "meaning": "state of, domain of",
        "origin": "Old English",
        "part_of_speech": "noun",
        "examples": ["freedom", "wisdom", "kingdom"],
    },
    "er": {
        "display": "-er",
        "meaning": "one who, that which",
        "origin": "Old English",
        "part_of_speech": "noun",
        "examples": ["teacher", "writer", "runner"],
    },
    "ful": {
        "display": "-ful",
        "meaning": "full of, characterised by",
        "origin": "Old English",
        "part_of_speech": "adjective",
        "examples": ["helpful", "powerful", "thoughtful"],
    },
    "graphy": {
        "display": "-graphy",
        "meaning": "process of recording or writing",
        "origin": "Greek",
        "part_of_speech": "noun",
        "examples": ["biography", "photography", "geography"],
    },
    "ic": {
        "display": "-ic",
        "meaning": "relating to, of the nature of",
        "origin": "Greek/Latin",
        "part_of_speech": "adjective",
        "examples": ["magnetic", "organic", "photogenic"],
    },
    "ing": {
        "display": "-ing",
        "meaning": "action or process of",
        "origin": "Old English",
        "part_of_speech": "verb/noun",
        "examples": ["running", "speaking", "writing"],
    },
    "ion": {
        "display": "-ion",
        "meaning": "act of, state of",
        "origin": "Latin",
        "part_of_speech": "noun",
        "examples": ["action", "education", "relation"],
    },
    "ism": {
        "display": "-ism",
        "meaning": "belief, practice, doctrine",
        "origin": "Greek",
        "part_of_speech": "noun",
        "examples": ["patriotism", "socialism", "journalism"],
    },
    "ist": {
        "display": "-ist",
        "meaning": "one who practises or believes",
        "origin": "Greek",
        "part_of_speech": "noun",
        "examples": ["artist", "scientist", "journalist"],
    },
    "ity": {
        "display": "-ity",
        "meaning": "state, quality, condition",
        "origin": "Latin",
        "part_of_speech": "noun",
        "examples": ["creativity", "diversity", "activity"],
    },
    "ize": {
        "display": "-ize",
        "meaning": "to make, to become",
        "origin": "Greek",
        "part_of_speech": "verb",
        "examples": ["organize", "modernize", "energize"],
    },
    "less": {
        "display": "-less",
        "meaning": "without, lacking",
        "origin": "Old English",
        "part_of_speech": "adjective",
        "examples": ["hopeless", "careless", "wireless"],
    },
    "logy": {
        "display": "-logy",
        "meaning": "study of, science of",
        "origin": "Greek",
        "part_of_speech": "noun",
        "examples": ["biology", "psychology", "technology"],
    },
    "ly": {
        "display": "-ly",
        "meaning": "in the manner of, having the qualities of",
        "origin": "Old English",
        "part_of_speech": "adverb",
        "examples": ["quickly", "carefully", "beautifully"],
    },
    "ment": {
        "display": "-ment",
        "meaning": "result of, means of",
        "origin": "Latin",
        "part_of_speech": "noun",
        "examples": ["development", "movement", "entertainment"],
    },
    "ness": {
        "display": "-ness",
        "meaning": "state, quality of",
        "origin": "Old English",
        "part_of_speech": "noun",
        "examples": ["happiness", "darkness", "kindness"],
    },
    "ous": {
        "display": "-ous",
        "meaning": "having, full of, characterised by",
        "origin": "Latin",
        "part_of_speech": "adjective",
        "examples": ["dangerous", "famous", "nervous"],
    },
    "ship": {
        "display": "-ship",
        "meaning": "state, condition, skill",
        "origin": "Old English",
        "part_of_speech": "noun",
        "examples": ["friendship", "leadership", "scholarship"],
    },
    "tion": {
        "display": "-tion",
        "meaning": "act, process, state of",
        "origin": "Latin",
        "part_of_speech": "noun",
        "examples": ["action", "direction", "solution"],
    },
}

ROOTS = {
    "aud": {
        "display": "aud",
        "meaning": "hear, listen",
        "origin": "Latin",
        "examples": ["audible", "audio", "audience", "audit"],
    },
    "bio": {
        "display": "bio",
        "meaning": "life, living organisms",
        "origin": "Greek",
        "examples": ["biology", "biography", "biosphere"],
    },
    "chron": {
        "display": "chron",
        "meaning": "time",
        "origin": "Greek",
        "examples": ["chronology", "chronic", "synchronize"],
    },
    "cogn": {
        "display": "cogn",
        "meaning": "know, recognise",
        "origin": "Latin",
        "examples": ["cognitive", "recognize", "incognito"],
    },
    "dict": {
        "display": "dict",
        "meaning": "say, tell, declare",
        "origin": "Latin",
        "examples": ["dictionary", "predict", "contradict"],
    },
    "duc": {
        "display": "duc",
        "meaning": "lead, bring",
        "origin": "Latin",
        "examples": ["produce", "reduce", "introduce", "educate"],
    },
    "fac": {
        "display": "fac",
        "meaning": "make, do",
        "origin": "Latin",
        "examples": ["factory", "manufacture", "artifact"],
    },
    "gen": {
        "display": "gen",
        "meaning": "birth, origin, kind",
        "origin": "Greek/Latin",
        "examples": ["generate", "genetics", "genuine"],
    },
    "geo": {
        "display": "geo",
        "meaning": "earth, ground",
        "origin": "Greek",
        "examples": ["geography", "geology", "geometry"],
    },
    "graph": {
        "display": "graph",
        "meaning": "write, draw, record",
        "origin": "Greek",
        "examples": ["photograph", "biography", "autograph"],
    },
    "log": {
        "display": "log",
        "meaning": "word, reason, study",
        "origin": "Greek",
        "examples": ["logic", "dialogue", "catalogue"],
    },
    "luc": {
        "display": "luc",
        "meaning": "light",
        "origin": "Latin",
        "examples": ["lucid", "translucent", "elucidate"],
    },
    "man": {
        "display": "man",
        "meaning": "hand",
        "origin": "Latin",
        "examples": ["manual", "manuscript", "manufacture"],
    },
    "mort": {
        "display": "mort",
        "meaning": "death",
        "origin": "Latin",
        "examples": ["mortal", "immortal", "mortify"],
    },
    "mot": {
        "display": "mot",
        "meaning": "move",
        "origin": "Latin",
        "examples": ["motion", "promote", "remote", "emotion"],
    },
    "nov": {
        "display": "nov",
        "meaning": "new",
        "origin": "Latin",
        "examples": ["novel", "novice", "innovate", "renovate"],
    },
    "path": {
        "display": "path",
        "meaning": "feeling, suffering, disease",
        "origin": "Greek",
        "examples": ["sympathy", "empathy", "pathology"],
    },
    "ped": {
        "display": "ped",
        "meaning": "foot, child",
        "origin": "Latin/Greek",
        "examples": ["pedestrian", "pedal", "pediatrics"],
    },
    "phon": {
        "display": "phon",
        "meaning": "sound, voice",
        "origin": "Greek",
        "examples": ["phone", "microphone", "symphony"],
    },
    "port": {
        "display": "port",
        "meaning": "carry, bring",
        "origin": "Latin",
        "examples": ["transport", "import", "portable"],
    },
    "psych": {
        "display": "psych",
        "meaning": "mind, soul",
        "origin": "Greek",
        "examples": ["psychology", "psychiatry", "psychic"],
    },
    "rupt": {
        "display": "rupt",
        "meaning": "break, burst",
        "origin": "Latin",
        "examples": ["rupture", "interrupt", "disrupt", "erupt"],
    },
    "scrib": {
        "display": "scrib",
        "meaning": "write",
        "origin": "Latin",
        "examples": ["describe", "prescribe", "inscribe"],
    },
    "sens": {
        "display": "sens",
        "meaning": "feel, sense",
        "origin": "Latin",
        "examples": ["sense", "sensitive", "sensation"],
    },
    "spec": {
        "display": "spec",
        "meaning": "see, look, observe",
        "origin": "Latin",
        "examples": ["spectacle", "inspect", "perspective"],
    },
    "struct": {
        "display": "struct",
        "meaning": "build, arrange",
        "origin": "Latin",
        "examples": ["structure", "construct", "destruct"],
    },
    "terr": {
        "display": "terr",
        "meaning": "earth, land",
        "origin": "Latin",
        "examples": ["terrain", "territory", "terrestrial"],
    },
    "therm": {
        "display": "therm",
        "meaning": "heat, temperature",
        "origin": "Greek",
        "examples": ["thermometer", "thermal", "thermostat"],
    },
    "tract": {
        "display": "tract",
        "meaning": "pull, draw, drag",
        "origin": "Latin",
        "examples": ["tractor", "subtract", "extract", "attract"],
    },
    "vid": {
        "display": "vid",
        "meaning": "see, look",
        "origin": "Latin",
        "examples": ["video", "evidence", "provide"],
    },
    "voc": {
        "display": "voc",
        "meaning": "voice, call",
        "origin": "Latin",
        "examples": ["vocal", "vocabulary", "invoke"],
    },
}


def analyze_word(word):
    """
    Analyse a word to identify its prefix, root, and suffix.

    Strategy:
      1. Iterate over every (prefix, suffix) pair — longest first — and see
         whether the text left between them matches a known root.
      2. If a known root is found, return that decomposition immediately.
      3. Otherwise fall back to a greedy prefix-then-suffix strip and return
         the remaining string as an unrecognised root.

    Returns a dict with keys:
      original_word, prefix, root, suffix,
      prefix_info, root_info, suffix_info, root_in_database
    """
    word = word.lower().strip()

    sorted_prefixes = sorted(PREFIXES.keys(), key=len, reverse=True)
    sorted_suffixes = sorted(SUFFIXES.keys(), key=len, reverse=True)

    # --- Pass 1: look for a decomposition where the middle is a known root ---
    for prefix in [None] + sorted_prefixes:
        if prefix and not word.startswith(prefix):
            continue
        after_prefix = word[len(prefix):] if prefix else word
        if len(after_prefix) < 2:
            continue

        for suffix in [None] + sorted_suffixes:
            if suffix and not after_prefix.endswith(suffix):
                continue
            root = after_prefix[: len(after_prefix) - len(suffix)] if suffix else after_prefix
            if len(root) < 2:
                continue

            # Direct match
            if root in ROOTS:
                return _make_result(word, prefix, root, suffix, True)

            # Try stripping a trailing epenthetic vowel.
            # Greek/Latin compounds often add a connecting vowel (usually 'o')
            # between the root and the following element, e.g. "psycho-logy"
            # is built from root "psych" + connecting "o" + suffix "logy".
            # Removing that vowel lets us match the canonical root form.
            if root and root[-1] in "aeiou" and root[:-1] in ROOTS:
                return _make_result(word, prefix, root[:-1], suffix, True)

    # --- Pass 2: greedy fallback ---
    found_prefix = None
    found_suffix = None
    remaining = word

    for prefix in sorted_prefixes:
        if remaining.startswith(prefix) and len(remaining) - len(prefix) >= 2:
            found_prefix = prefix
            remaining = remaining[len(prefix):]
            break

    for suffix in sorted_suffixes:
        if remaining.endswith(suffix) and len(remaining) - len(suffix) >= 2:
            found_suffix = suffix
            remaining = remaining[: -len(suffix)]
            break

    root = remaining if remaining else word
    return _make_result(word, found_prefix, root, found_suffix, root in ROOTS)


def _make_result(original_word, prefix, root, suffix, root_in_database):
    return {
        "original_word": original_word,
        "prefix": prefix,
        "root": root,
        "suffix": suffix,
        "prefix_info": PREFIXES.get(prefix) if prefix else None,
        "root_info": ROOTS.get(root) if root else None,
        "suffix_info": SUFFIXES.get(suffix) if suffix else None,
        "root_in_database": root_in_database,
    }


def create_word(prefix, root, suffix):
    """Concatenate prefix + root + suffix into a new word string."""
    parts = []
    if prefix:
        parts.append(prefix)
    if root:
        parts.append(root)
    if suffix:
        parts.append(suffix)
    return "".join(parts)


def generate_definition(prefix, root, suffix):
    """
    Build a human-readable definition from the component meanings.
    """
    prefix_info = PREFIXES.get(prefix) if prefix else None
    root_info = ROOTS.get(root) if root else None
    suffix_info = SUFFIXES.get(suffix) if suffix else None

    pos = suffix_info.get("part_of_speech", "word") if suffix_info else "word"
    root_meaning = root_info["meaning"] if root_info else f"'{root}'"
    prefix_meaning = prefix_info["meaning"] if prefix_info else (prefix or "")
    suffix_meaning = suffix_info["meaning"] if suffix_info else (suffix or "")

    if prefix_meaning and root_meaning and suffix_meaning:
        return (
            f"A {pos} meaning '{prefix_meaning}' the quality of '{root_meaning}'; "
            f"{suffix_meaning}."
        )
    if prefix_meaning and root_meaning:
        return f"Relating to '{prefix_meaning}' applied to {root_meaning}."
    if root_meaning and suffix_meaning:
        return f"A {pos} of {root_meaning}; {suffix_meaning}."
    return f"Relating to {root_meaning}."


def generate_example(word, prefix, root, suffix):
    """
    Generate a simple illustrative sentence for the new word.
    """
    root_info = ROOTS.get(root) if root else None
    root_meaning = root_info["meaning"] if root_info else root or "the concept"
    prefix_info = PREFIXES.get(prefix) if prefix else None
    suffix_info = SUFFIXES.get(suffix) if suffix else None
    pos = suffix_info.get("part_of_speech", "word") if suffix_info else "word"

    if prefix_info and suffix_info:
        return (
            f"The {pos} '{word}' describes something that is "
            f"{prefix_info['meaning']} and related to {root_meaning}."
        )
    if prefix_info:
        return (
            f"'{word}' refers to the {prefix_info['meaning']} aspect of {root_meaning}."
        )
    if suffix_info:
        return f"'{word}' is a {pos} derived from '{root}' ({root_meaning})."
    return f"'{word}' is related to {root_meaning}."
