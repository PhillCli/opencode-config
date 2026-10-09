import { Plugin } from "@opencode/plugin"

// Subagents whose unset model is rewritten from the session model.
const downgrade = ["explore"]

// Same-provider lower sibling. Key is the current session model.
// A missing key leaves the child on the session model.
const models: Record<string, string> = {
  "opencode-go/glm-5.3": "opencode-go/glm-5.3-flash",
  "opencode/glm-5.3": "opencode/glm-5.3-flash",
  "opencode/claude-opus-5-5": "opencode/claude-sonnet-5-5",
  "opencode/claude-fable-5-1": "opencode/claude-opus-5-5",
  "amazon-bedrock/global.anthropic.claude-opus-5-5":
    "amazon-bedrock/anthropic.claude-sonnet-5-5",
  "github-copilot/claude-opus-5.5": "github-copilot/claude-sonnet-5.5",
}

function refOf(model: { providerID?: string; id?: string } | undefined) {
  if (!model?.providerID || !model.id) return
  return `${model.providerID}/${model.id}`
}

function asRecord(value: unknown): Record<string, unknown> | undefined {
  if (!value || typeof value !== "object") return
  return value as Record<string, unknown>
}

export default Plugin.define({
  id: "subagent-model",
  async setup(ctx) {
    await ctx.tool.hook("execute.before", async (event) => {
      try {
        if (event.tool !== "subagent") return
        const bag = asRecord(event)
        const input = asRecord(bag?.input) ?? asRecord(bag?.args)
        if (!input || input.model) return
        if (typeof input.agent !== "string" || !downgrade.includes(input.agent)) return
        const sessionID = typeof bag?.sessionID === "string" ? bag.sessionID : undefined
        if (!sessionID) return
        const session = await ctx.session.get({ sessionID })
        const sibling = models[refOf(session.model) ?? ""]
        if (!sibling) return
        input.model = sibling
      } catch {
        // A failed rewrite must not block the tool call.
      }
    })
  },
})
