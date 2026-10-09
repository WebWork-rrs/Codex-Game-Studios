# Credits and provenance

## Original project

[Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios)
was created and is maintained by **[Donchitos](https://github.com/Donchitos)**
and its upstream contributors. Its studio structure, specialist agent
definitions, workflow skills, coding rules, document templates, configuration
helpers, hooks, and framework testing material are their work.

The original [MIT license](LICENSE), including
**Copyright (c) 2026 Donchitos**, is preserved without replacement. The original
Git history and commit authorship are retained. Upstream support links in
`.github/FUNDING.yml` continue to support Donchitos:

- [GitHub Sponsors](https://github.com/sponsors/Donchitos)
- [Buy Me a Coffee](https://www.buymeacoffee.com/donchitos3)

## Codex adaptation

[WebWork-rrs](https://github.com/WebWork-rrs) maintains this independent
adaptation and its Codex-specific contributions: `AGENTS.md`, the converter
and payload adapters in `tools/codex/`, generated Codex skills and roles,
compatibility tests, and the update workflow. Generated skills and roles
derive from Donchitos's originals and retain that provenance.

Original authorship remains with the upstream creator and contributors.
This adaptation does not imply their endorsement or maintenance of its
Codex-specific additions. The adaptation is distributed under the same MIT
license.

The initial adaptation used upstream commit
`be8993bbc5a1f016bc770b2846ce06272d284526` (framework 1.1.3).
`tools/codex/upstream.json` records the currently integrated upstream commit.
Future integrations preserve original commits through Git merges.

## Game-craft skills

The six native craft skills and their supporting files are unchanged selections
from [awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills),
created by **Abhishek Barali and the awesome-gamedev-agent-skills contributors**.
They supply art-production, game-feel, animation, tilemap, and audio guidance.

These files are licensed under **Apache-2.0**, separately from the MIT Studio
framework and Codex adaptation. The original [LICENSE](third_party/gamedev-skills/LICENSE)
and [NOTICE](third_party/gamedev-skills/NOTICE) are retained in their source
directory and each generated native skill folder. The exact upstream commit
and file hashes are recorded in [SOURCE.json](third_party/gamedev-skills/SOURCE.json).
Source content is unmodified; the prototype orchestration and integration
adapter are WebWork-rrs contributions. Inclusion does not imply endorsement.
