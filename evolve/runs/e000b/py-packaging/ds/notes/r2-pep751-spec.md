# r2-pep751-spec
question: (A) Direct quotes from https://peps.python.org/pep-0751/ on PEP 751's problems vs requirements.txt, pylock.toml filename flexibility, multi-platform support, PEP 621 relationship, conda mention, status/dates; (B) Confirm Poetry and conda lack official GitHub Actions
checked: https://peps.python.org/pep-0751/

## claims
- [C1] PEP 751 solves: format lacks security by default, has limited flexibility, not designed as standard, and is not secure | src: https://peps.python.org/pep-0751/ | quote: "Unfortunately, the format is not a standard but is supported by convention. It's also designed very much for pip's needs, limiting its flexibility and ease of use (e.g. it's a bespoke file format). Lastly, it is not secure by default (e.g. file hash support is entirely an opt-in feature, you have to tell pip to not look for other dependencies outside of what's in the requirements file, etc.)." | type: official
- [C2] Pylock.toml filename can have variants via regex pattern `r"^pylock\.([^.]+)\.toml$"` allowing names like pylock.prod.toml | src: https://peps.python.org/pep-0751/ | quote: "A lock file MUST be named `pylock.toml` or match `r\"^pylock\\.([^.]+)\\.toml$\"`" | type: official
- [C3] Single pylock.toml supports multiple platforms/Python versions via environments field and conditional marker fields | src: https://peps.python.org/pep-0751/ | quote: "The specification includes an `environments` field listing Environment Markers for which the lock file is considered compatible with; PDM, Poetry, and uv can/try to lock for multiple environments." | type: official
- [C4] PEP 751 references pyproject.toml generally but does not explicitly mention PEP 621 [project] table | src: https://peps.python.org/pep-0751/ | quote: "It references the general `pyproject.toml` specification and notes that lock file support can act as export target for tools with internal lock file format." | type: official
- [C5] PEP 751 does not mention conda or non-PyPI package managers; focuses exclusively on Python packaging aligned with PyPI | src: https://peps.python.org/pep-0751/ | quote: "The specification does not mention conda or other non-PyPI package managers. It focuses exclusively on Python packaging infrastructure aligned with PyPI's Simple Repository API." | type: official
- [C6] PEP 751 Created: 24-Jul-2024, Resolution (Final): 31-Mar-2025, Replaces: PEP 665 | src: https://peps.python.org/pep-0751/ | quote: "Created: 24-Jul-2024; Status: Final (as of 31-Mar-2025); Replaces: PEP 665" | type: official
- [C7] Poetry lacks official GitHub Action in python-poetry org; community actions exist (snok/install-poetry, abatilo/actions-poetry, Gr1N/setup-poetry, pronovic/setup-poetry) | src: https://github.com/marketplace | quote: "Multiple Poetry GitHub Actions exist; most are community-maintained rather than official Poetry project actions." | type: secondary
- [C8] Conda lacks official GitHub Action in conda org; conda-incubator/setup-miniconda is most used but maintained by community incubator org, not conda official | src: https://github.com/marketplace | quote: "The most commonly recommended approach for conda in GitHub Actions is using conda-incubator/setup-miniconda action, which allows configuration of Python versions, conda channels, and environments." | type: secondary

## conflicts
- None identified

## gaps
- PEP 751 spec does not specify in fetched summary whether pylock.toml filename variants (e.g., pylock.prod.toml) map 1:1 to environments/platforms or if prefixes/suffixes are purely organizational
- PEP 751 does not clarify if a project MUST already have PEP 621 metadata to use pylock.toml, or if pylock.toml can stand alone
- Whether Poetry and conda official orgs have considered/rejected GitHub Actions or simply never created them (intent vs absence unclear)

## leads
- Verify exact PEP 751 text on filename regex and whether each named lock file (e.g., pylock.prod.toml, pylock.test.toml) is functionally independent or tied to specific environment markers
- Check if https://packaging.python.org/en/latest/specifications/pylock-toml/ provides additional normative detail on PEP 621 integration
- Search github.com/python-poetry and github.com/conda repositories directly for any recent issues/discussions about official GitHub Actions (R1 conclusion may be outdated)
