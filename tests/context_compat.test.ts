import { describe, expect, test } from "bun:test";
import { contextMessages, latestMarkerIsActive } from "../extensions/context-compat";

describe("contextMessages", () => {
  test("reads buildSessionContext", () => {
    const manager = {
      buildSessionContext: () => ({
        messages: [{ role: "custom", customType: "blunt-rules" }],
      }),
    };
    expect(contextMessages(manager)).toHaveLength(1);
  });

  test("falls back to buildContextEntries", () => {
    const manager = {
      buildContextEntries: () => [
        { type: "custom_message", customType: "blunt-disabled" },
      ],
    };
    expect(contextMessages(manager)).toHaveLength(1);
  });

  test("returns empty for unusable session managers", () => {
    expect(contextMessages(null)).toHaveLength(0);
    expect(contextMessages({})).toHaveLength(0);
    expect(
      contextMessages({
        buildSessionContext: () => {
          throw new Error("runtime changed");
        },
      }),
    ).toHaveLength(0);
  });
});

describe("latestMarkerIsActive", () => {
  test("rules message activates, disabled notice deactivates", () => {
    const messages = [
      { role: "custom", customType: "blunt-rules" },
      { role: "custom", customType: "blunt-disabled" },
      { role: "custom", customType: "blunt-rules" },
    ];
    expect(latestMarkerIsActive(messages, "blunt-rules", "blunt-disabled")).toBe(true);
    expect(
      latestMarkerIsActive(messages.slice(0, 2), "blunt-rules", "blunt-disabled"),
    ).toBe(false);
    expect(latestMarkerIsActive([], "blunt-rules", "blunt-disabled")).toBe(false);
  });

  test("ignores non-custom entries", () => {
    const messages = [
      { type: "text", customType: "blunt-rules" },
      { role: "user", customType: "blunt-disabled" },
    ];
    expect(latestMarkerIsActive(messages, "blunt-rules", "blunt-disabled")).toBe(false);
  });
});