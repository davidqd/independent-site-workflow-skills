# Repository instructions

When adding a new Skill under `skills/`, follow [SKILL-UPLOAD-CHECKLIST.md](./SKILL-UPLOAD-CHECKLIST.md). A new Skill upload is incomplete until its installation documentation and repository indexes are updated in the same change.

Required for every new Skill:

- Add the complete `skills/<skill-name>/` directory with a valid `SKILL.md`.
- Add `skills/<skill-name>/README.md` using the repository template and include a Codex `$skill-installer` prompt, invocation example, update instructions, and license notice.
- Copy the repository `LICENSE.md` into the Skill directory unless the Skill has a separately reviewed compatible license.
- Add the Skill to `README.md` and `skills/README.md`.
- Add its GitHub URL and invocation example to `CODEX-INSTALL.md`.
- Preserve all required `agents/`, `references/`, `scripts/`, and `assets/` files; do not upload only `SKILL.md`.
- Validate the Skill structure, check Markdown links and run `git diff --check` before committing.

Keep changes limited to the Skill being uploaded and the documentation files listed above. Do not convert the repository into a plugin or marketplace package unless the user explicitly requests that separate change.
