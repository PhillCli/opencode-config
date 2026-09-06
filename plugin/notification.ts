import { spawn } from "bun"

type Urgency = "low" | "normal" | "critical"

const shortenPath = (path: string) =>
  path.replace(/^\/home\/[^/]+/, "~").replace(/^\/Users\/[^/]+/, "~")

const escapeAppleScript = (value: string) => value.replace(/\\/g, "\\\\").replace(/"/g, '\\"')

const makeNotify =
  (directory: string) =>
  (title: string, urgency: Urgency, icon: string, timeoutMs: number) => {
    const message = shortenPath(directory)
    if (process.platform === "darwin") {
      const escapedMessage = escapeAppleScript(message)
      const escapedTitle = escapeAppleScript(title)
      spawn(["osascript", "-e", `display notification "${escapedMessage}" with title "${escapedTitle}"`])
    } else if (process.platform === "linux") {
      spawn(["notify-send", "-u", urgency, "-i", icon, "-t", String(timeoutMs), title, message])
    }
  }

// No runtime dependency on @opencode-ai/plugin: Plugin.define() is an identity
// function, so a plain object literal is equivalent and loads without node_modules.

// V2 (OpenCode 2.x) reads id + setup and ignores server().
export default {
  id: "notification",
  async setup(ctx: V2Context) {
    const notify = makeNotify(ctx.location.directory)
    const primarySessionCache = new Map<string, boolean>()

    const isPrimarySession = async (sessionID?: string) => {
      if (!sessionID) return false

      const cached = primarySessionCache.get(sessionID)
      if (cached !== undefined) return cached

      try {
        const session = await ctx.session.get({ sessionID })
        const isPrimary = !session.parentID
        primarySessionCache.set(sessionID, isPrimary)
        return isPrimary
      } catch {
        return false
      }
    }

    const controller = new AbortController()
    void (async () => {
      for await (const event of ctx.event.subscribe({ signal: controller.signal })) {
        if (event.type === "session.idle") {
          if (!(await isPrimarySession(event.data.sessionID))) continue
          notify("opencode ✅ Done", "low", "dialog-information", 10000)
        }
        if (event.type === "session.execution.failed") {
          if (!(await isPrimarySession(event.data.sessionID))) continue
          notify("opencode ❌ Error", "critical", "dialog-error", 30000)
        }
        if (event.type === "permission.asked") {
          if (!(await isPrimarySession(event.data.sessionID))) continue
          notify(`opencode ❓ ${event.data.action}`, "critical", "dialog-question", 30000)
        }
      }
    })().catch(() => {})

    return () => controller.abort()
  },

  // V1 (OpenCode 1.18.29+) calls server() and uses the returned hooks.
  async server({ client, directory }: V1PluginInput) {
    const notify = makeNotify(directory)
    const primarySessionCache = new Map<string, boolean>()

    const isPrimarySession = async (sessionID?: string) => {
      if (!sessionID) return false

      const cached = primarySessionCache.get(sessionID)
      if (cached !== undefined) return cached

      try {
        const { data } = await client.session.get({ path: { id: sessionID }, query: { directory } })
        const isPrimary = !!data && !data.parentID
        primarySessionCache.set(sessionID, isPrimary)
        return isPrimary
      } catch {
        return false
      }
    }

    return {
      event: async ({ event }: { event: V1Event }) => {
        if (event.type === "session.idle") {
          if (!(await isPrimarySession(event.properties.sessionID))) return
          notify("opencode ✅ Done", "low", "dialog-information", 10000)
        }
        if (event.type === "session.error") {
          if (event.properties.sessionID && !(await isPrimarySession(event.properties.sessionID))) return
          notify("opencode ❌ Error", "critical", "dialog-error", 30000)
        }
        if (event.type === "permission.updated") {
          if (!(await isPrimarySession(event.properties.sessionID))) return
          notify(`opencode ❓ ${event.properties.title}`, "critical", "dialog-question", 30000)
        }
      },
    }
  },
}

interface V2Context {
  location: { directory: string }
  session: {
    get(input: { sessionID: string }): Promise<{ parentID?: string }>
  }
  event: {
    subscribe(options?: { signal?: AbortSignal }): AsyncIterable<V2Event>
  }
}

interface V2Event {
  type: string
  data: {
    sessionID?: string
    action?: string
  }
}

interface V1PluginInput {
  client: {
    session: {
      get(input: {
        path: { id: string }
        query: { directory: string }
      }): Promise<{ data?: { parentID?: string } | null }>
    }
  }
  directory: string
}

interface V1Event {
  type: string
  properties: {
    sessionID?: string
    title?: string
  }
}
