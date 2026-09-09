import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import {
  getAgentDir,
  type ExtensionAPI,
  type ExtensionContext,
} from "@earendil-works/pi-coding-agent";
import {
  contextMessages,
  latestMarkerIsActive,
} from "./context-compat";

const EXTENSION_DIR = dirname(fileURLToPath(import.meta.url));
const SKILL_PATH = join(
  EXTENSION_DIR,
  "..",
  "skills",
  "blunt",
  "SKILL.md",
);
const STATE_ENTRY_TYPE = "blunt-state";
const RULES_MESSAGE_TYPE = "blunt-rules";
const DISABLED_MESSAGE_TYPE = "blunt-disabled";
const STATUS_KEY = "blunt";
const DISABLE_CONFIRMATION = "Blunt mode disabled.";
const STOP_PHRASES: Record<string, true> = {
  "stop blunt mode": true,
  "normal mode": true,
};
const RULES_HEADER =
  'BLUNT MODE ACTIVE. The ruleset below applies to every response until turned off. "stop blunt mode" or "normal mode" turns it off for this session.';
const DISABLED_NOTICE =
  "BLUNT MODE OFF. Ignore the blunt ruleset injected earlier in this conversation and return to your default response style.";

type BluntModeState = {
  enabled: boolean;
};

type BluntConfig = {
  alwaysOn?: boolean;
  hideStatus?: boolean;
};

function loadConfig(): BluntConfig {
  try {
    return JSON.parse(
      readFileSync(join(getAgentDir(), "blunt.json"), "utf8"),
    );
  } catch {
    return {};
  }
}

function stripFrontmatter(content: string): string {
  return content
    .replace(
      /^---[^\S\r\n]*\r?\n[\s\S]*?\r?\n---[^\S\r\n]*(?:\r?\n|$)/,
      "",
    )
    .trim();
}

function loadRules(): string {
  let content: string;

  try {
    content = readFileSync(SKILL_PATH, "utf8");
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    throw new Error(
      `Unable to load blunt rules from ${SKILL_PATH}: ${reason}`,
    );
  }

  const rules = stripFrontmatter(content);
  if (!rules) {
    throw new Error(`The blunt rules file is empty: ${SKILL_PATH}`);
  }

  return rules;
}

function getSavedState(ctx: ExtensionContext): boolean | undefined {
  let savedState: boolean | undefined;

  for (const entry of ctx.sessionManager.getBranch()) {
    if (entry.type !== "custom" || entry.customType !== STATE_ENTRY_TYPE) {
      continue;
    }

    const data = entry.data as Partial<BluntModeState> | undefined;
    if (typeof data?.enabled === "boolean") {
      savedState = data.enabled;
    }
  }

  return savedState;
}

/**
 * Whether the rules are still live in the context the model actually receives.
 *
 * Only the newest marker counts: a later "disabled" notice cancels an earlier
 * ruleset, and compaction drops summarized entries so the ruleset has to be
 * injected again.
 */
function rulesAreInContext(ctx: ExtensionContext): boolean {
  return latestMarkerIsActive(
    contextMessages(ctx.sessionManager),
    RULES_MESSAGE_TYPE,
    DISABLED_MESSAGE_TYPE,
  );
}

export default function bluntExtension(pi: ExtensionAPI) {
  const rules = loadRules();
  const alwaysOnFlag = join(getAgentDir(), ".blunt-always");
  const config = loadConfig();
  let enabled = false;

  const updateStatus = (ctx: ExtensionContext): void => {
    if (!enabled || config.hideStatus) {
      ctx.ui.setStatus(STATUS_KEY, undefined);
      return;
    }

    const dot = ctx.ui.theme.fg("success", "●");
    const label = ctx.ui.theme.fg("accent", "BLUNT ON");
    ctx.ui.setStatus(STATUS_KEY, `${dot} ${label}`);
  };

  /**
   * Keep the conversation in sync with the current mode: inject the ruleset
   * once, never per request.
   */
  const syncContext = (ctx: ExtensionContext): void => {
    const injected = rulesAreInContext(ctx);

    if (enabled && !injected) {
      pi.sendMessage(
        {
          customType: RULES_MESSAGE_TYPE,
          content: `${RULES_HEADER}\n\n${rules}`,
          display: false,
        },
        { triggerTurn: false },
      );
      return;
    }

    if (!enabled && injected) {
      pi.sendMessage(
        {
          customType: DISABLED_MESSAGE_TYPE,
          content: DISABLED_NOTICE,
          display: false,
        },
        { triggerTurn: false },
      );
    }
  };

  const restoreState = (ctx: ExtensionContext): void => {
    const savedState = getSavedState(ctx);
    const enabledByDefault =
      pi.getFlag("blunt") === true ||
      config.alwaysOn === true ||
      existsSync(alwaysOnFlag);

    enabled = savedState ?? enabledByDefault;
    updateStatus(ctx);
    syncContext(ctx);
  };

  const setEnabled = (nextEnabled: boolean, ctx: ExtensionContext): void => {
    enabled = nextEnabled;
    pi.appendEntry(STATE_ENTRY_TYPE, { enabled } satisfies BluntModeState);
    updateStatus(ctx);
    syncContext(ctx);
    ctx.ui.notify(`Blunt mode ${enabled ? "enabled" : "disabled"}`, "info");
  };

  pi.registerFlag("blunt", {
    description: "Start with blunt output enabled",
    type: "boolean",
    default: false,
  });

  pi.registerCommand("blunt", {
    description: "Toggle blunt output for this session",
    handler: async (args, ctx) => {
      const argument = args.trim().toLowerCase();

      if (argument === "") {
        setEnabled(!enabled, ctx);
        return;
      }

      if (argument === "on") {
        setEnabled(true, ctx);
        return;
      }

      if (argument === "off" || argument === "stop") {
        setEnabled(false, ctx);
        return;
      }

      ctx.ui.notify("Usage: /blunt [on|off]", "warning");
    },
  });

  pi.on("input", async (event, ctx) => {
    const input = event.text.trim().toLowerCase();

    // Keep the built-in skill command working as an alias without letting the
    // runtime expand a second copy of the same rules into the conversation.
    if (input === "/skill:blunt") {
      setEnabled(true, ctx);
      return { action: "handled" };
    }

    if (enabled && STOP_PHRASES[input]) {
      setEnabled(false, ctx);

      if (ctx.hasUI) {
        return { action: "handled" };
      }

      return {
        action: "transform",
        text: `Reply with exactly: ${DISABLE_CONFIRMATION}`,
      };
    }

    return { action: "continue" };
  });

  pi.on("session_start", async (_event, ctx) => restoreState(ctx));
  pi.on("session_tree", async (_event, ctx) => restoreState(ctx));
  pi.on("session_compact", async (_event, ctx) => syncContext(ctx));
}