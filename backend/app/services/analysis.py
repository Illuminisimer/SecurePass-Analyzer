from __future__ import annotations

import math
import pickle
import random
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

try:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

COMMON_PASSWORD_FILE = Path(__file__).resolve().parents[3] / "common_passwords.txt"
MODEL_FILE = Path(__file__).resolve().with_name("strength_model.pkl")
SPECIAL_CHARS = "!@#$%^&*()-_=+[]{}|\\:;\"'<>,.?/"
KEYBOARD_PATTERNS = [
    "qwerty",
    "asdfgh",
    "zxcvbn",
    "1q2w3e",
    "password",
    "admin",
    "letmein",
    "iloveyou",
]
GRADE_LABELS = [
    (0, 20, "Critical"),
    (21, 40, "Weak"),
    (41, 60, "Fair"),
    (61, 80, "Good"),
    (81, 90, "Excellent"),
    (91, 100, "Legendary"),
]
FEATURE_ORDER = [
    "length",
    "entropy",
    "charset_count",
    "uppercase",
    "lowercase",
    "digits",
    "special",
    "unique_chars",
    "repeated_sequences",
    "keyboard_walk",
    "personal_info_matches",
    "common_password",
]


def _load_common_passwords() -> set[str]:
    if not COMMON_PASSWORD_FILE.exists():
        return set()

    with COMMON_PASSWORD_FILE.open("r", encoding="utf-8", errors="ignore") as handle:
        return {line.strip().lower() for line in handle if line.strip()}


COMMON_PASSWORDS = _load_common_passwords()


def _clamp_score(value: float) -> int:
    return int(max(0, min(100, round(value))))


def _normalize_password(password: str) -> str:
    return password.strip()


def _extract_personal_terms(name: Optional[str], username: Optional[str], email: Optional[str], dob: Optional[str]) -> list[str]:
    terms: list[str] = []
    if username:
        terms.append(username.lower())

    if name:
        terms.extend(part.lower() for part in re.split(r"\s+", name) if part)

    if email and "@" in email:
        prefix = email.split("@", 1)[0].strip().lower()
        if prefix:
            terms.append(prefix)

    if dob and re.fullmatch(r"\d{6,8}", dob.strip()):
        terms.append(dob.strip())
        terms.extend(re.findall(r"\d{2,4}", dob.strip()))

    return [term for term in terms if term]


def _has_keyboard_walk(password: str) -> bool:
    lower = password.lower()
    return any(pattern in lower for pattern in KEYBOARD_PATTERNS)


def _count_repeated_sequences(password: str) -> int:
    return len(re.findall(r"(.)\1{2,}", password))


def _count_sequential_charsets(password: str) -> int:
    password_lower = password.lower()
    count = 0
    for i in range(len(password_lower) - 2):
        chunk = password_lower[i : i + 3]
        if chunk.isalpha() or chunk.isdigit():
            if chunk in "abcdefghijklmnopqrstuvwxyz" or chunk in "0123456789":
                count += 1
            if chunk[::-1] in "abcdefghijklmnopqrstuvwxyz" or chunk[::-1] in "0123456789":
                count += 1
    return count


def _charset_count(password: str) -> int:
    return sum(
        bool(password)
        for password in (
            re.search(r"[a-z]", password),
            re.search(r"[A-Z]", password),
            re.search(r"[0-9]", password),
            re.search(r"[{}]".format(re.escape(SPECIAL_CHARS)), password),
        )
    )


def _calculate_entropy(password: str) -> float:
    if not password:
        return 0.0

    size = 0
    if re.search(r"[a-z]", password):
        size += 26
    if re.search(r"[A-Z]", password):
        size += 26
    if re.search(r"[0-9]", password):
        size += 10
    if re.search(r"[{}]".format(re.escape(SPECIAL_CHARS)), password):
        size += len(SPECIAL_CHARS)

    return float(len(password) * math.log2(size or 1)) if size else 0.0


def _grade_from_score(score: int) -> str:
    for minimum, maximum, label in GRADE_LABELS:
        if minimum <= score <= maximum:
            return label
    return "Unknown"


def _build_features(password: str, personal_terms: list[str], common_password: bool) -> list[float]:
    normalized = _normalize_password(password)
    unique_chars = len(set(normalized)) / max(1, len(normalized))
    return [
        len(normalized),
        _calculate_entropy(normalized),
        _charset_count(normalized),
        float(bool(re.search(r"[A-Z]", normalized))),
        float(bool(re.search(r"[a-z]", normalized))),
        float(bool(re.search(r"[0-9]", normalized))),
        float(bool(re.search(r"[{}]".format(re.escape(SPECIAL_CHARS)), normalized))),
        unique_chars,
        float(_count_repeated_sequences(normalized)),
        float(_has_keyboard_walk(normalized)),
        float(bool(personal_terms and any(term in normalized.lower() for term in personal_terms))),
        float(common_password),
    ]


def _score_rule_based(password: str, personal_terms: list[str]) -> int:
    normalized = _normalize_password(password)
    score = 0

    entropy = _calculate_entropy(normalized)
    charset_count = _charset_count(normalized)
    length = len(normalized)

    if length >= 8:
        score += 20
    if length >= 12:
        score += 10
    if length >= 16:
        score += 10

    score += min(30, int(entropy / 8))
    score += 8 * charset_count

    if _count_repeated_sequences(normalized) > 0:
        score -= 20

    if _count_sequential_charsets(normalized) > 0:
        score -= 5

    if _has_keyboard_walk(normalized):
        score -= 10

    if any(term in normalized.lower() for term in personal_terms):
        score -= 30

    if normalized.lower() in COMMON_PASSWORDS:
        score -= 40

    if length < 8:
        score -= 30

    return _clamp_score(score)


def _generate_strong_password(length: int = 18) -> str:
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" + SPECIAL_CHARS
    return "".join(random.choice(charset) for _ in range(length))


def _generate_medium_password(length: int = 12) -> str:
    pieces = [
        random.choice("abcdefghijklmnopqrstuvwxyz"),
        random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        random.choice("0123456789"),
        random.choice(SPECIAL_CHARS),
    ]
    while len(pieces) < length:
        pieces.append(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"))
    random.shuffle(pieces)
    return "".join(pieces)


def _train_model() -> Optional[object]:
    if not SKLEARN_AVAILABLE:
        return None

    samples: list[list[float]] = []
    targets: list[float] = []
    training_passwords: set[str] = set()

    if COMMON_PASSWORDS:
        for password in list(COMMON_PASSWORDS)[:2500]:
            if password in training_passwords:
                continue
            training_passwords.add(password)
            samples.append(_build_features(password, [], True))
            targets.append(random.uniform(5, 20))

    for _ in range(3000):
        password = _generate_medium_password(random.randint(10, 14))
        if password in training_passwords:
            continue
        training_passwords.add(password)
        samples.append(_build_features(password, [], False))
        targets.append(random.uniform(40, 60))

    for _ in range(3000):
        password = _generate_strong_password(random.randint(16, 24))
        if password in training_passwords:
            continue
        training_passwords.add(password)
        samples.append(_build_features(password, [], False))
        targets.append(random.uniform(82, 98))

    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=100,
                    random_state=42,
                    n_jobs=-1,
                    min_samples_leaf=3,
                ),
            ),
        ]
    )
    model.fit(samples, targets)

    try:
        with MODEL_FILE.open("wb") as handle:
            pickle.dump(model, handle)
    except OSError:
        pass

    return model


def _load_or_train_model() -> Optional[object]:
    if MODEL_FILE.exists():
        try:
            with MODEL_FILE.open("rb") as handle:
                model = pickle.load(handle)
                return model
        except (OSError, pickle.UnpicklingError):
            pass
    return _train_model()


class PasswordStrengthAnalyzer:
    def __init__(self) -> None:
        self.model = _load_or_train_model()

    def _estimate_confidence(self, feature_vector: list[float]) -> float:
        try:
            regressor = self.model.named_steps["regressor"]
            if not hasattr(regressor, "estimators_"):
                return 0.6
            predictions = [tree.predict([feature_vector])[0] for tree in regressor.estimators_]
            std_dev = float(np.std(predictions))
            confidence = max(0.0, min(1.0, 1.0 - std_dev / 20.0))
            return confidence
        except Exception:
            return 0.6

    def analyze_password(
        self,
        password: str,
        name: Optional[str] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
        dob: Optional[str] = None,
    ) -> Dict[str, Any]:
        normalized = _normalize_password(password)
        personal_terms = _extract_personal_terms(name, username, email, dob)
        common_password = normalized.lower() in COMMON_PASSWORDS
        features = _build_features(normalized, personal_terms, common_password)

        if self.model is not None and SKLEARN_AVAILABLE:
            score = _clamp_score(int(self.model.predict([features])[0]))
            ml_confidence = self._estimate_confidence(features)
        else:
            score = _score_rule_based(normalized, personal_terms)
            ml_confidence = 0.6

        reason_items: list[str] = []
        suggestion_items: list[str] = []

        if len(normalized) < 8:
            reason_items.append("Password is shorter than 8 characters.")
            suggestion_items.append("Use at least 12 characters for better security.")
            score -= 20
        if _charset_count(normalized) < 3:
            reason_items.append("Password lacks character set variety.")
            suggestion_items.append("Include uppercase, lowercase, digits, and symbols.")
        if _count_repeated_sequences(normalized) > 0:
            reason_items.append("Password contains repeated characters.")
            suggestion_items.append("Avoid repeated sequences like 'aaa' or '111'.")
        if _count_sequential_charsets(normalized) > 0:
            reason_items.append("Password has sequential patterns.")
            suggestion_items.append("Avoid sequences like '1234' or 'abcd'.")
        if _has_keyboard_walk(normalized):
            reason_items.append("Password contains keyboard walk patterns.")
            suggestion_items.append("Use a random password with no obvious keyboard patterns.")
        if common_password:
            reason_items.append("Password is found in common password lists.")
            suggestion_items.append("Change the password to something unique and complex.")
        if personal_terms and any(term in normalized.lower() for term in personal_terms):
            reason_items.append("Password contains personal information.")
            suggestion_items.append("Remove names, usernames, emails, and birth dates from passwords.")

        if not reason_items:
            reason_items.append("Password passed the core strength checks.")
            suggestion_items.append("Maintain this password style for future entries.")

        if len(suggestion_items) > 3:
            suggestion_items = suggestion_items[:3]

        if score < 40 and "Use at least 12 characters" not in suggestion_items:
            suggestion_items.append("Use at least 12 characters for better security.")

        return {
            "score": score,
            "grade": _grade_from_score(score),
            "entropy": round(_calculate_entropy(normalized), 1),
            "reasons": reason_items,
            "suggestions": suggestion_items,
            "ml_confidence": round(ml_confidence, 2),
            "common_password": common_password,
            "personal_info_matches": [term for term in personal_terms if term and term in normalized.lower()],
        }


def analyze_password(password: str, **kwargs: Any) -> Dict[str, Any]:
    analyzer = PasswordStrengthAnalyzer()
    return analyzer.analyze_password(password, **kwargs)
