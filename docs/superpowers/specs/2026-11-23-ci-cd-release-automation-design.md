# Design Document: Automação de CI/CD, Releases e Versionamento (TaipanStack)

**Data:** 2026-11-23  
**Status:** Aprovado  
**Versão Atual no Repo:** 0.6.4 (inconsistente com 0.6.3 no código)  
**Versão Alvo Imediata:** 0.7.0  

---

## 1. Contexto e Motivação
TaipanStack necessita de um ciclo automatizado e contínuo para versionamento, geração de releases categorizadas, publicação no PyPI e GHCR, e validação em ambiente protegido.
As alterações na branch principal (`main`) ou envio de tags `v*` devem produzir artefatos prontos para produção sem abortar execuções concorrentes (`cancel-in-progress: false`).

---

## 2. Decisões Acordadas e Escopo

### 2.1. Versionamento Rollover (.10)
- As versões de patch sobem até `.10`.
- Regra de transição: `vX.Y.10` avança diretamente para `vX.(Y+1).0` (ex: `v0.6.10 -> v0.7.0`, `v0.7.10 -> v0.8.0`).
- Primeira versão a aplicar imediatamente: `v0.7.0`.

### 2.2. Sincronização do Repositório (Decisão do Usuário: Opção 1)
- O pipeline calcula a nova versão baseada no histórico de tags e na regra `.10`.
- Atualiza `pyproject.toml` e `src/taipanstack/__init__.py`.
- Atualiza `CHANGELOG.md` com as alterações categorizadas.
- Realiza commit de volta na branch `main` com `[skip ci]` para evitar loops.
- Cria a tag Git `vX.Y.Z` e publica a GitHub Release.

### 2.3. Pipeline Unificada de CI/CD (Decisão Técnica / Builder Call)
- Para evitar a limitação do GitHub onde eventos criados pelo `GITHUB_TOKEN` não acionam outros workflows, a esteira é unificada:
  1. **Job `validate`:** Executa testes unitários, linting e checagem de tipos.
  2. **Job `version-and-tag` (apenas em `main` ou tag direta):** Calcula versão, gera changelog categorizado, comita com `[skip ci]`, cria a tag e a GitHub Release.
  3. **Job `pypi-publish`:** Build do pacote com Poetry, Trusted Publishing (`environment: pypi`), geração de SBOM CycloneDX e assinatura Cosign do Wheel e SBOM.
  4. **Job `ghcr-publish`:** Build da imagem Docker de produção e push no GHCR (`ghcr.io/gabrielima7/taipanstack:vX.Y.Z` e `:latest`).
  5. **Job `deploy`:** Depende de `[pypi-publish, ghcr-publish]`, roda sob `environment: production`, valida a disponibilidade pública dos artefatos e anexa os metadados finais na Release.
- Concorrência configurada com `cancel-in-progress: false`.

### 2.4. Categorização do Changelog e Release
Configurado via `.github/release.yml` e script de release com as seguintes seções:
- ✨ **Novas Funcionalidades** (`feat`, `feature`)
- 🔄 **Alterações** (`refactor`, `perf`, `chore`, `change`)
- 🐛 **Correções** (`fix`, `bug`)
- 🗑️ **Remoções e Depreciações** (`removal`, `deprecate`, `breaking`)
- 📦 **Artefatos Gerados** (links, checksums SHA-256 e assinaturas cosign)

---

## 3. Arquivos Impactados

| Arquivo | Ação |
| :--- | :--- |
| `pyproject.toml` | Atualizar versão inicial para `0.7.0`. |
| `src/taipanstack/__init__.py` | Atualizar `__version__ = "0.7.0"`. |
| `CHANGELOG.md` | Adicionar bloco `## [0.7.0] - 2026-11-23`. |
| `docs/releases/v0.7.0.md` & `mkdocs.yml` | Criar notas de release e atualizar menu. |
| `.github/release.yml` | Configurar categorias automáticas de release. |
| `.github/workflows/ci-release-publish.yml` | Reestruturar para pipeline unificada com suporte a `main`, tags, rollover `.10`, PyPI, GHCR e ambiente `production`. |
| `scripts/bump_version.py` | Script reutilizável para cálculo de versão com rollover `.10` e atualização de arquivos. |

---

## 4. Próximos Passos
Após aprovação deste design pelo usuário, invocar a skill `superpowers:writing-plans` para detalhar as tarefas de implementação orientadas a TDD.
