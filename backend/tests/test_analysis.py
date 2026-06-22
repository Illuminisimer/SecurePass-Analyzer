from backend.app.services.analysis import PasswordStrengthAnalyzer


def test_strong_password_score():
    analyzer = PasswordStrengthAnalyzer()
    result = analyzer.analyze_password(
        "V3ry$ecureP@ssw0rd!",
        name="Alice Parker",
        username="alicep",
        email="alice@example.com",
        dob="01012000",
    )

    assert result["score"] >= 80
    assert result["grade"] in {"Good", "Excellent", "Legendary"}
    assert result["common_password"] is False
    assert result["personal_info_matches"] == []


def test_common_password_detected():
    analyzer = PasswordStrengthAnalyzer()
    result = analyzer.analyze_password("password123")

    assert result["score"] <= 40
    assert result["common_password"] is True
    assert "common password" in " ".join(result["reasons"]).lower()


def test_personal_info_penalty():
    analyzer = PasswordStrengthAnalyzer()
    result = analyzer.analyze_password("johnsmith1986!", name="John Smith")

    assert result["score"] < 60
    assert "personal information" in " ".join(result["reasons"]).lower()
    assert "john" in result["personal_info_matches"]


def test_short_password_feedback():
    analyzer = PasswordStrengthAnalyzer()
    result = analyzer.analyze_password("A1!b")

    assert result["score"] < 30
    assert any("shorter than 8" in reason.lower() for reason in result["reasons"])
    assert any("use at least 12" in suggestion.lower() for suggestion in result["suggestions"])


def test_sequential_pattern_penalty():
    analyzer = PasswordStrengthAnalyzer()
    result = analyzer.analyze_password("abcd1234!@#")

    assert result["score"] < 60
    assert any("sequential patterns" in reason.lower() for reason in result["reasons"])


def test_kitchen_sink_strong_password():
    analyzer = PasswordStrengthAnalyzer()
    result = analyzer.analyze_password("QwErTy!2349@#XyZ")

    assert result["score"] >= 70
    assert result["common_password"] is False


def test_ml_confidence_range():
    analyzer = PasswordStrengthAnalyzer()
    result = analyzer.analyze_password("Th!s1sAStr0ngPassw0rd$")

    assert 0.0 <= result["ml_confidence"] <= 1.0
