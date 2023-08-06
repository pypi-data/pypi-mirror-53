import bleach
import unicodedata


def html_sanitize(value):
    """Sanitize HTML in value to avoid malicious usage"""
    return bleach.clean(value) if value else value


def unicode_normalize(value):
    """Normalize input to ensure clean encoding in db"""
    return unicodedata.normalize("NFKC", value) if value else value
