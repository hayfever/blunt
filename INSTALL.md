# How to install

The canonical skill is `skills/blunt/SKILL.md`. Every agent that reads agent skills accepts it with no conversion; plugin manifests serve the marketplaces of Claude Code, Codex, Kimi, Antigravity, and OMP.

This repository lives at `https://github.com/hayfever/blunt`. If you forked it, swap `hayfever/blunt` for your own `owner/repo` in every command below. Local copies work everywhere: the "without the CLI" fallback in each section is a folder copy, and several marketplaces accept a local path (Claude Code: the path must point at the repo root).

## Always-on snippet

Reusable in every agent's persistent rules file. One copy; each agent section below points here.

```markdown
## Output style

The reader has ADHD. Shape every response so it can be acted on:

1. Lead with the answer or next action: command, path, or snippet first.
2. Number multi-step work; one bounded action per step.
3. End with one next action doable in under two minutes.
4. Finish the current issue before raising a new one.
5. Restate progress each turn ("step 3 of 5 done").
6. Give time estimates in concrete units, never "a bit".
7. After a change, show what now works.
8. Errors: state location, cause, and fix. No drama.
9. Cap lists at 5 items.
10. No preamble, no recaps, no closers.

Write plain: active voice, imperative steps, steps of 20 words or fewer, no semicolons, one term per item, no contractions, no "e.g.", "i.e.", or "etc.". Sound human: no not-X-but-Y contrasts, one-line closers, forced triads, dashes, stock AI words, bold labels, or chatbot residue. Never invent a fact; quoted text, code, and paths stay exactly as they are.

Exceptions: explain fully when asked to explain. Confirm before destructive actions. After three failed fixes, stop and name the doubtful assumption. If the request is ambiguous, ask one short question.
```

<details>
<summary><strong>Antigravity (<code>agy</code>)</strong></summary>

### Install

```bash
agy plugin install https://github.com/hayfever/blunt
```

### Verify

```bash
agy plugin list
```

### Update

```bash
agy plugin uninstall blunt
agy plugin install https://github.com/hayfever/blunt
```

### Uninstall

```bash
agy plugin uninstall blunt
```

Or keep it installed and turn it off: `agy plugin disable blunt`.

### Always-on (optional)

Add the [always-on snippet](#always-on-snippet) to `~/.gemini/GEMINI.md`.

</details>

<details>
<summary><strong>Claude Code</strong></summary>

### Install

```bash
claude plugin marketplace add hayfever/blunt
claude plugin install blunt@blunt
```

Type `/blunt`.

### Verify

```bash
claude plugin list
```

### Update

```bash
claude plugin marketplace update blunt
```

### Uninstall

```bash
claude plugin uninstall blunt
claude plugin marketplace remove blunt
```

Or keep it installed and turn it off: `claude plugin disable blunt`.

### Always-on (optional)

A `SessionStart` hook loads the full ruleset at the start of every session, no `/blunt` needed:

```bash
touch ~/.claude/.blunt-always
```

If you use a custom Claude configuration directory, create the flag there instead:

```bash
touch "$CLAUDE_CONFIG_DIR/.blunt-always"
```

Back to on-demand:

```bash
rm ~/.claude/.blunt-always
```

The hook only fires when the flag file exists, so installing the plugin changes nothing by itself. "stop blunt mode" still turns it off for the current session.

</details>

<details>
<summary><strong>Codex</strong></summary>

### Install

```bash
codex plugin marketplace add hayfever/blunt --ref main
codex plugin add blunt@blunt
```

Invoke the skill explicitly by typing `$blunt`. Codex will not activate it automatically.

### Verify

```bash
codex plugin list
```

### Update

```bash
codex plugin marketplace upgrade blunt
codex plugin remove blunt
codex plugin add blunt@blunt
```

### Uninstall

```bash
codex plugin remove blunt
codex plugin marketplace remove blunt
```

### Always-on (optional)

Add the [always-on snippet](#always-on-snippet) to `~/.codex/AGENTS.md`.

</details>

<details>
<summary><strong>Gemini CLI</strong></summary>

Gemini CLI has no plugin marketplace, so there are two native routes: a **custom command** (opt-in, off until you invoke it) or an **extension** (always-on once installed). The command route matches this skill's default posture; pick it unless you want the rules on every session.

### Install (command, opt-in)

```bash
mkdir -p ~/.gemini/commands
curl -fsSL https://raw.githubusercontent.com/hayfever/blunt/main/skills/blunt/agents/gemini.toml \
  -o ~/.gemini/commands/blunt.toml
```

Start a new session, type `/blunt`. It stays on for that session.

### Install (extension, always-on)

```bash
gemini extensions install https://github.com/hayfever/blunt
```

The extension loads `GEMINI.md`, which imports the full skill, so the rules apply from message one. `git` must be installed.

### Verify

```bash
gemini extensions list          # extension route
ls ~/.gemini/commands           # command route: blunt.toml present
```

Or type `/` in a session and confirm `blunt` is listed.

### Update

```bash
gemini extensions update blunt    # extension route
# command route: re-run the curl above
```

### Uninstall

```bash
gemini extensions uninstall blunt    # extension route
rm ~/.gemini/commands/blunt.toml     # command route
```

</details>

<details>
<summary><strong>GitHub Copilot (VS Code and Copilot CLI)</strong></summary>

Copilot reads Agent Skills natively: the same `SKILL.md`, no conversion. It scans `.github/skills/`, `.claude/skills/`, and `.agents/skills/` in the project, and `~/.copilot/skills/`, `~/.claude/skills/`, and `~/.agents/skills/` globally.

### Install

```bash
npx skills add hayfever/blunt -a github-copilot        # this project
npx skills add hayfever/blunt -a github-copilot -g     # all projects
```

Without the CLI, copy the skill folder into any directory Copilot scans:

```bash
git clone https://github.com/hayfever/blunt
mkdir -p ~/.copilot/skills
cp -R blunt/skills/blunt ~/.copilot/skills/
```

### Verify

Type `/` in the chat input and confirm `blunt` appears. Or:

```bash
npx skills list
npx skills ls -g    # if installed globally
```

### Update

```bash
npx skills update blunt
```

Or re-copy the folder after `git pull`.

### Uninstall

```bash
npx skills remove blunt
```

Or delete the `blunt` folder from the skills directory it landed in.

### Activation note

Copilot respects `disable-model-invocation`: nothing applies until you invoke the skill, same as Claude Code.

### Always-on (optional)

Add the [always-on snippet](#always-on-snippet) to `.github/copilot-instructions.md` in the project.

</details>

<details>
<summary><strong>Hermes</strong></summary>

### Install

```bash
hermes skills install hayfever/blunt/skills/blunt
```

Type `/blunt`. The skill installs into `~/.hermes/skills/` and is exposed as a slash command at the next session start.

Prefer to browse first? Add this repo as a skill source (a "tap"), then search and install:

```bash
hermes skills tap add hayfever/blunt
hermes skills search blunt
hermes skills install hayfever/blunt/skills/blunt
```

### Verify

```bash
hermes skills list
```

### Update

```bash
hermes skills update blunt
```

### Uninstall

```bash
hermes skills uninstall blunt
```

Or remove the tap too: `hermes skills tap remove hayfever/blunt`.

### Always-on (optional)

Add the [always-on snippet](#always-on-snippet) to the `AGENTS.md` in your working directory, or to your persona `SOUL.md` for every session.

</details>

<details>
<summary><strong>Kimi Code CLI</strong></summary>

### Install

Start a Kimi Code session, then:

1. Run `/plugins`.
2. Choose **Custom**.
3. Paste `https://github.com/hayfever/blunt` and press `Enter`.
4. Choose **Trust and install**.

Use slash command `/skill:blunt` to invoke the skill explicitly.

### Update

`/plugins` in a Kimi Code session, cursor to **Blunt**, press `R`.

### Uninstall

`/plugins` in a Kimi Code session, cursor to **Blunt**, press `D`.

</details>

<details>
<summary><strong>OpenCode</strong></summary>

OpenCode loads this repository as a server plugin: `.opencode/plugins/blunt.mjs` registers the `skills/` entry point and the `/blunt` command, and injects the ruleset when always-on is enabled. OpenCode also reads `skills/` natively, so the skill still works even without the plugin; the plugin adds the `/blunt` command and the always-on flag.

### Install

Clone the repo and point OpenCode at the plugin. An absolute path shares one checkout across every project:

```bash
git clone https://github.com/hayfever/blunt ~/.config/opencode/vendor/blunt
```

Add to your `opencode.json` (global: `~/.config/opencode/opencode.json`):

```json
{ "plugin": ["/absolute/path/to/blunt/.opencode/plugins/blunt.mjs"] }
```

Or run OpenCode from the checkout; it ships a root `opencode.json` with the plugin already wired up.

Start a new session and turn on blunt output for the session:

```text
/blunt
```

Rules stay on until `stop blunt mode` or `normal mode`.

### Verify

Start OpenCode, type `/`, and confirm `blunt` appears in the command list.

### Update

```bash
git -C ~/.config/opencode/vendor/blunt pull
```

### Uninstall

Remove the `plugin` entry from `opencode.json`.

### Always-on (optional)

```bash
touch ~/.config/opencode/.blunt-always
```

While the flag exists, the plugin appends the full ruleset to the system prompt every turn. `stop blunt mode` or `normal mode` disables it for the current session; delete the flag to turn always-on off for good:

```bash
rm ~/.config/opencode/.blunt-always
```

</details>

<details>
<summary><strong>Pi</strong></summary>

Pi discovers this repository as a native package: `extensions/` provides the session-persistent mode and `skills/` keeps the Agent Skills entry point available.

### Install

```bash
pi install https://github.com/hayfever/blunt
```

Start a new Pi session. Toggle blunt output for the current session:

```text
/blunt
```

The footer shows `● BLUNT ON` while the mode is active. Run the command again to turn it off, or be explicit:

```text
/blunt on
/blunt off
stop blunt mode
```

The extension adds the ruleset to the conversation once instead of rewriting the system prompt on every request, and adds it again after compaction drops it. The existing Agent Skills command remains available as an alias:

```text
/skill:blunt
```

Start a new Pi session with the mode enabled by default:

```bash
pi --blunt
```

### Verify

```bash
pi list
```

Confirm the GitHub package is listed, then type `/blunt` and check that `● BLUNT ON` appears in the footer.

### Update

```bash
pi update https://github.com/hayfever/blunt
```

Or update every unpinned Pi package with `pi update --extensions`.

### Uninstall

```bash
pi remove https://github.com/hayfever/blunt
```

### Always-on (optional)

Create a flag in Pi's agent configuration directory:

```bash
touch ~/.pi/agent/.blunt-always
```

The extension checks the flag at every new, resumed, forked, or reloaded session. A saved choice for the current session wins over this default, so `stop blunt mode` keeps that session disabled.

Back to on-demand:

```bash
rm ~/.pi/agent/.blunt-always
```

### Config file (optional)

Create `~/.pi/agent/blunt.json` in Pi's agent configuration directory:

```json
{
  "alwaysOn": true,
  "hideStatus": true
}
```

- `alwaysOn`: start every session with the rules active, same as the `.blunt-always` flag file, which still works
- `hideStatus`: keep the `● BLUNT ON` status-bar entry hidden; the rules and the `/blunt` command still work

Read once at extension startup, so restart Pi after changing it. If `PI_CODING_AGENT_DIR` is set, put `.blunt-always` in that directory instead. Run `/reload` or start a new session after changing the flag.

</details>

<details>
<summary><strong>Oh My Pi (OMP)</strong></summary>

### Install

```bash
omp plugin marketplace add hayfever/blunt
omp plugin install --scope user blunt@blunt
```

Start a new OMP session and run `/blunt` to toggle the mode. The footer shows `● BLUNT ON` while the mode is active.

### Update

```bash
omp plugin marketplace update blunt
omp plugin upgrade --scope user blunt@blunt
```

### Uninstall

```bash
omp plugin uninstall --scope user blunt@blunt
omp plugin marketplace remove blunt
```

### Always-on (optional)

Create a flag in OMP's agent configuration directory:

```bash
touch ~/.omp/agent/.blunt-always
```

Or set `"alwaysOn": true` in `~/.omp/agent/blunt.json`. A saved choice for the current session wins over the default, so `stop blunt mode` keeps that session disabled. Run `/reload` or start a new session after changing the flag.

</details>

<details>
<summary><strong>Qwen Code</strong></summary>

### Install

```bash
qwen extensions install hayfever/blunt
```

Qwen Code supports the GitHub shorthand and installs the repository as a native extension. The extension discovers the skill under `skills/`.

Type `/blunt` to invoke the skill explicitly. Installing the extension does not change output until the skill is invoked.

### Verify

```bash
qwen extensions list
```

Then start a new Qwen Code session and run `/skills`. Confirm that `blunt` appears in the list.

### Update

```bash
qwen extensions update blunt
```

### Uninstall

```bash
qwen extensions uninstall blunt
```

</details>

<details>
<summary><strong>Zed</strong></summary>

Zed's Agent reads Agent Skills natively: the same `SKILL.md`, no conversion.

### Install

In the Agent Panel, open the Skills manager and choose **Create skill from URL** (also in the command palette as `agent: create skill from url`), then paste:

```
https://github.com/hayfever/blunt/blob/main/skills/blunt/SKILL.md
```

Save it in **User** scope for every project, or **Project** scope for one. Then type `/blunt` in the Agent Panel.

Prefer the filesystem? Clone the repo and drop the skill folder into your user skills directory:

```bash
git clone https://github.com/hayfever/blunt
cp -R blunt/skills/blunt ~/.config/zed/skills/
```

### Verify

Open the Skills manager in the Agent Panel and confirm `blunt` is listed. Or type `/` and confirm it appears.

### Update

Re-import from the same URL (overwrites), or re-copy the folder after `git pull`.

### Uninstall

Remove `blunt` from the Skills manager, or delete `~/.config/zed/skills/blunt`.

### Always-on (optional)

Add the [always-on snippet](#always-on-snippet) to your personal `~/.config/zed/AGENTS.md`.

</details>

<details>
<summary><strong>Cursor, Amp, and any other agent-skills harness</strong></summary>

Works with any harness that reads agent skills. Swap `-a <agent>` for yours.

### Install

```bash
npx skills add hayfever/blunt                  # this workspace
npx skills add hayfever/blunt -g               # all projects
npx skills add hayfever/blunt -a cursor -y     # one agent only
npx skills add hayfever/blunt -a opencode -y
```

New agent chat, type `/blunt`.

Without the CLI, copy the skill folder into whatever path your agent scans:

```bash
git clone https://github.com/hayfever/blunt
mkdir -p ~/.cursor/skills     # Cursor. Use .agents/skills for OpenCode, or your agent's own path
cp -R blunt/skills/blunt ~/.cursor/skills/
```

### Verify

```bash
npx skills list
npx skills ls -g    # if installed globally
```

### Update

```bash
npx skills update blunt
npx skills update -g    # if installed globally
```

### Uninstall

```bash
npx skills remove blunt
npx skills remove blunt -g    # if installed globally
```

### Always-on (optional)

Paste the [always-on snippet](#always-on-snippet) into your agent's persistent rules file. Cursor: **Settings, Rules, User Rules**, or a project rule under `.cursor/rules/` with `alwaysApply: true`. OpenCode: `~/.config/opencode/AGENTS.md`.

</details>

## How activation works

1. **Installed, not invoked.** In Claude Code, Qwen Code, and Codex, nothing happens until you invoke the skill explicitly. Claude Code and Qwen Code honor `disable-model-invocation: true` in `SKILL.md`; Codex honors `policy.allow_implicit_invocation: false` in `skills/blunt/agents/openai.yaml`. Other harnesses may load every skill's description at startup and activate the skill themselves.
2. **You invoke it explicitly.** Type `/blunt` in Claude Code or Qwen Code, or `$blunt` in Codex. Rules stay on for that session. "stop blunt mode" or "normal mode" turns them off.
3. **You touch `~/.claude/.blunt-always`** (Claude Code, Codex) or `~/.config/opencode/.blunt-always` (OpenCode) or `~/.pi/agent/.blunt-always` (Pi, OMP). A hook or extension loads the full ruleset from message one, every session.
4. **You add the always-on snippet** (other harnesses). Keeps the core rules in your agent's persistent context.

In Claude Code, Qwen Code, and Codex, no middle ground: if you did not turn it on, it is off.

## Troubleshooting

**`/blunt` not in autocomplete.** Restart the agent. The plugin index is read at startup.

**Always-on flag has no effect.** Update the plugin (`claude plugin marketplace update blunt`) and restart. Hooks are read at startup, and the flag needs the plugin version that ships `hooks/hooks.json`.

**`claude plugin marketplace add` fails.** Use the `owner/repo` form. A local path must point at the repo root, not `.claude-plugin/`.

**Installed but replies still preamble.** Open a new session. If it still drifts, tighten the wording in `skills/blunt/SKILL.md`.

**Want different rules.** Fork, edit `skills/blunt/SKILL.md`, then swap your copy in (see [README](README.md#tune-it)). Restart, then re-invoke `/blunt`.

**Skill missing after `npx skills add`.** Start a new agent chat. Skills are indexed at session start. Confirm the folder landed where your agent scans (`~/.cursor/skills/` for Cursor, `.agents/skills/` for OpenCode) and that the frontmatter `name` matches the folder name.