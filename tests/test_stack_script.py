import sys
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Adiciona o diretório raiz ao path para que o `stack` possa ser importado
sys.path.insert(0, str(Path(__file__).parent.parent))

import stack


@pytest.fixture(autouse=True)
def setup_teardown(tmp_path, monkeypatch):
    """
    Fixture para isolar cada teste em um diretório temporário
    e mockar chamadas de sistema perigosas.
    """
    # Muda o diretório de trabalho atual para o diretório temporário
    monkeypatch.chdir(tmp_path)

    # Mocka subprocess.run para evitar execuções de comandos reais (como poetry)
    mock_run = MagicMock(return_value=subprocess.CompletedProcess([], 0))
    with patch("subprocess.run", mock_run):
        yield mock_run


def run_main_with_args(args):
    """Helper para rodar a função main do script com argumentos específicos."""
    with patch.object(sys, "argv", ["stack.py"] + args):
        stack.main()


def test_dry_run_does_not_create_files(tmp_path):
    """
    Verifica se rodar com --dry-run não cria nenhum arquivo de configuração.
    """
    run_main_with_args(["--dry-run"])

    # Garante que nenhum dos arquivos principais foi criado
    assert not (tmp_path / "pyproject.toml").exists()
    assert not (tmp_path / ".pre-commit-config.yaml").exists()
    assert not (tmp_path / "SECURITY.md").exists()
    assert not (tmp_path / ".github" / "dependabot.yml").exists()


def test_safe_write_creates_backup(tmp_path):
    """
    Verifica se o backup (.bak) é criado quando um arquivo de configuração já existe.
    """
    # Cria um arquivo dummy para simular uma configuração existente
    dummy_file = tmp_path / ".pre-commit-config.yaml"
    dummy_file.write_text("old content")

    run_main_with_args([])  # Execução normal, sem flags

    # Verifica se o backup foi criado
    backup_file = tmp_path / ".pre-commit-config.yaml.bak"
    assert backup_file.exists()
    assert backup_file.read_text() == "old content"

    # Verifica se o novo arquivo também foi criado
    assert dummy_file.exists()
    assert "pre-commit-hooks" in dummy_file.read_text()  # Verifica conteúdo do novo arquivo


def test_force_mode_overwrites_without_backup(tmp_path):
    """
    Verifica se a flag --force sobrescreve o arquivo diretamente, sem criar backup.
    """
    dummy_file = tmp_path / ".pre-commit-config.yaml"
    dummy_file.write_text("old content")

    run_main_with_args(["--force"])

    # Garante que o arquivo de backup NÃO foi criado
    backup_file = tmp_path / ".pre-commit-config.yaml.bak"
    assert not backup_file.exists()

    # Garante que o arquivo original foi sobrescrito
    assert dummy_file.exists()
    assert "pre-commit-hooks" in dummy_file.read_text()


def test_idempotency_for_pyproject_toml(tmp_path):
    """
    Verifica se rodar o script duas vezes não duplica as seções no pyproject.toml.
    """
    # Cria um pyproject.toml inicial, como se `poetry init` tivesse rodado
    pyproject_toml = tmp_path / "pyproject.toml"
    pyproject_toml.write_text('[tool.poetry]\nname = "test"\n')

    # Primeira execução
    run_main_with_args([])
    content_after_first_run = pyproject_toml.read_text()

    # Verifica se as seções foram adicionadas
    assert "[tool.ruff]" in content_after_first_run
    assert "[tool.mypy]" in content_after_first_run
    assert content_after_first_run.count("[tool.ruff]") == 1

    # Segunda execução
    run_main_with_args([])
    content_after_second_run = pyproject_toml.read_text()

    # Compara o conteúdo e garante que não houve duplicação
    assert content_after_first_run == content_after_second_run
    assert content_after_second_run.count("[tool.ruff]") == 1
