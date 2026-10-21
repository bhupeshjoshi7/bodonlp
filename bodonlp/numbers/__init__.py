"""
Bodo Number System: integers, word representations, ordinals, fractions,
and numeral classifiers.
"""

from typing import Union, List
from bodonlp.numbers.classifiers import (
    apply_classifier,
    get_classifier_for,
    list_classifiers,
    NUMERAL_CLASSIFIERS
)

# Digits 0 to 10
DIGITS_DEV = {
    0: "लाथिख'", 1: "से", 2: "नै", 3: "थाम", 4: "ब्रै", 5: "बा",
    6: "द'", 7: "स्नि", 8: "दाइन", 9: "गु", 10: "जि"
}

DIGITS_ROM = {
    0: "latikho", 1: "se", 2: "nwi", 3: "tham", 4: "brwi", 5: "ba",
    6: "do", 7: "sni", 8: "daen", 9: "gu", 10: "zi"
}

# Teens 11 to 19
TEENS_DEV = {
    11: "जिसे", 12: "जिनै", 13: "जिथाम", 14: "जिब्रै", 15: "जिबा",
    16: "जिद'", 17: "जिस्नि", 18: "जिदायन", 19: "जिगु"
}

TEENS_ROM = {
    11: "zise", 12: "zinwi", 13: "zitham", 14: "zibrwi", 15: "ziba",
    16: "zido", 17: "zisni", 18: "zidaen", 19: "zigu"
}

# Tens 20, 30, ... 90
TENS_PREFIX_DEV = {
    2: "नैजि", 3: "थामजि", 4: "ब्रैजि", 5: "बाजि",
    6: "द'जि", 7: "स्निजि", 8: "दाइनजि", 9: "गुजि"
}

TENS_PREFIX_ROM = {
    2: "nwizi", 3: "thamzi", 4: "brwizi", 5: "bazi",
    6: "dozi", 7: "snizi", 8: "daenzi", 9: "guzi"
}

DEVANAGARI_DIGITS = "०१२३४५६७८९"


def to_devanagari_numerals(number: Union[int, str]) -> str:
    """Convert an integer or numeric string into Devanagari numerals (e.g., 42 -> '४२')."""
    s = str(number)
    return "".join(DEVANAGARI_DIGITS[int(c)] if c.isdigit() else c for c in s)


def from_devanagari_numerals(dev_str: str) -> int:
    """Convert Devanagari numeral string back to integer (e.g., '४२' -> 42)."""
    mapping = {c: str(i) for i, c in enumerate(DEVANAGARI_DIGITS)}
    res = "".join(mapping.get(c, c) for c in dev_str if c in mapping or c.isdigit())
    return int(res) if res else 0


def num_to_words(n: int, script: str = "devanagari") -> str:
    """
    Convert an integer (0 to 999,999,999) into Bodo words.
    
    Args:
        n: Integer number.
        script: "devanagari" or "latin" / "roman".
    
    Examples:
        num_to_words(0) -> "लाथिख'"
        num_to_words(5) -> "बा"
        num_to_words(14) -> "जिब्रै"
        num_to_words(42) -> "ब्रैजिनै"
        num_to_words(100) -> "जौसे"
        num_to_words(250) -> "जौने बाजि"
        num_to_words(1000) -> "रोजासे"
    """
    is_rom = script.lower() in ("latin", "roman", "eng")
    digits = DIGITS_ROM if is_rom else DIGITS_DEV
    teens = TEENS_ROM if is_rom else TEENS_DEV
    tens = TENS_PREFIX_ROM if is_rom else TENS_PREFIX_DEV
    
    hundred_word = "zou" if is_rom else "जौ"
    thousand_word = "roza" if is_rom else "रोजा"
    lakh_word = "lakh" if is_rom else "लाख"
    crore_word = "kouti" if is_rom else "कौटि"
    one_suffix = "se" if is_rom else "से"

    if n < 0:
        neg = "Dan- " if is_rom else "दान- "
        return neg + num_to_words(-n, script=script)

    if n <= 10:
        return digits[n]

    if 11 <= n <= 19:
        return teens[n]

    if 20 <= n <= 99:
        t_digit = n // 10
        rem = n % 10
        base = tens[t_digit]
        if rem == 0:
            return base
        return f"{base}{digits[rem]}"

    if 100 <= n <= 999:
        h_digit = n // 100
        rem = n % 100
        if h_digit == 1:
            h_str = f"{hundred_word}{one_suffix}"
        else:
            h_str = f"{hundred_word}{digits[h_digit]}"
        if rem == 0:
            return h_str
        return f"{h_str} {num_to_words(rem, script=script)}"

    if 1000 <= n <= 99999:
        th_part = n // 1000
        rem = n % 1000
        if th_part == 1:
            th_str = f"{thousand_word}{one_suffix}"
        else:
            th_str = f"{thousand_word}{num_to_words(th_part, script=script)}"
        if rem == 0:
            return th_str
        return f"{th_str} {num_to_words(rem, script=script)}"

    if 100000 <= n <= 9999999:
        lakh_part = n // 100000
        rem = n % 100000
        if lakh_part == 1:
            l_str = f"{lakh_word}{one_suffix}"
        else:
            l_str = f"{lakh_word}{num_to_words(lakh_part, script=script)}"
        if rem == 0:
            return l_str
        return f"{l_str} {num_to_words(rem, script=script)}"

    # 1 Crore and above
    cr_part = n // 10000000
    rem = n % 10000000
    if cr_part == 1:
        c_str = f"{crore_word}{one_suffix}"
    else:
        c_str = f"{crore_word}{num_to_words(cr_part, script=script)}"
    if rem == 0:
        return c_str
    return f"{c_str} {num_to_words(rem, script=script)}"


def words_to_num(words: str) -> int:
    """Parse Bodo numeral words back into an integer."""
    clean = words.strip().lower()
    # Check 0-10
    for k, v in DIGITS_DEV.items():
        if v.lower() == clean:
            return k
    for k, v in DIGITS_ROM.items():
        if v == clean:
            return k
    for k, v in TEENS_DEV.items():
        if v.lower() == clean:
            return k
    for k, v in TEENS_ROM.items():
        if v == clean:
            return k
    # Common hundreds/thousands
    if clean in ("जौसे", "zouse"):
        return 100
    if clean in ("रोजासे", "rozase"):
        return 1000
    if clean in ("लाखसे", "lakhse"):
        return 100000
    return 0


def ordinal(n: int, script: str = "devanagari") -> str:
    """
    Generate the ordinal form in Bodo (e.g., 1st: सेथि / sethi, 2nd: नैथि / nwithi).
    The suffix -थि (-thi) forms ordinals in Bodo.
    """
    is_rom = script.lower() in ("latin", "roman", "eng")
    word = num_to_words(n, script=script)
    suffix = "thi" if is_rom else "थि"
    return f"{word}{suffix}"


def fraction(numerator: int, denominator: int, script: str = "devanagari") -> str:
    """Generate Bodo fraction word (e.g. 1/2 -> खावसे / khaose)."""
    is_rom = script.lower() in ("latin", "roman", "eng")
    if numerator == 1 and denominator == 2:
        return "khaose" if is_rom else "खावसे"
    if numerator == 1 and denominator == 4:
        return "khwo-se" if is_rom else "खोसे"
    if numerator == 3 and denominator == 4:
        return "khwo-tham" if is_rom else "खोथाम"
    
    num_w = num_to_words(numerator, script=script)
    den_w = num_to_words(denominator, script=script)
    of_part = "ni" if is_rom else "नि"
    return f"{den_w}{of_part} {num_w}"
