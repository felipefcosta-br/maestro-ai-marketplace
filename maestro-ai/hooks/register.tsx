import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

// The band shows once the conversation has this many user turns.
const MIN_TURNS = 15

const isHidden = atom({ plugin: 'maestro-ai', key: 'isHidden' } as const, false)
const isSaving = atom({ plugin: 'maestro-ai', key: 'isSaving' } as const, false)
// Name of the saved context to resume once the conversation is cleared ('' = none).
const resumeName = atom({ plugin: 'maestro-ai', key: 'resumeName' } as const, '')

// `/maestro-ai:resume <name>` as the save-context command prints it on its last line.
const RESUME_LINE = /\/maestro-ai:resume\s+([^\s`'"]+)/

// Runs /maestro-ai:resume <name> once, so the cleared conversation continues from the
// saved context instead of waiting for the person. The atom is emptied first, so the
// session.start path and the after-clear path never both run it.
const resumeSaved = async ($: any) => {
  const name = await read($, resumeName)
  if (!name) return
  await update($, resumeName, () => '')
  try {
    await $.command.run({ command: 'maestro-ai:resume', args: name })
  } catch {
    $.ui.toast(`Could not resume automatically. Type: /maestro-ai:resume ${name}`)
  }
}

export const register: Register = (on, options) => {
  // Option "saveAndClear" (maestro-ai config): false turns the whole feature off, and
  // the hooks of the plugin keep working without it.
  if (options.saveAndClear === false) return

  // Set when a save-and-clear was started (button or tool); cleared when the turn ends.
  let pending = false

  on('session.start', async ($, e, next) => {
    await $.tool.register({
      name: 'clear_conversation',
      description:
        'Clears this conversation (runs /clear) once the current reply ends. Call it only after /maestro-ai:save-context has saved the context and the user chose to save and clear.',
    })

    const result = await next(e)
    // A new session after /clear: pick the saved context back up.
    $.clock.after(800, () => resumeSaved($))
    return result
  })

  on('tool.call', { tool: /^mcp__maestro-ai__clear_conversation$/ }, async $ => {
    pending = true
    await update($, isSaving, () => true)

    return { result: 'The conversation will be cleared when this reply ends. Do not call other tools.' }
  })

  on('turn.complete', async ($, e, next) => {
    const result = await next(e)

    if (!pending || e.agentId !== undefined) {
      return result
    }

    pending = false
    await update($, isSaving, () => false)

    // Clear only when the save really finished. The save-context command ends with the
    // ready-to-paste `/maestro-ai:resume <name>` line, but the last message of the turn
    // may be a short closing note, so look at every assistant message of this turn.
    const found = await $.session.messages()
    const messages = 'deny' in found ? [] : found
    const lastUser = messages.map(m => m.role).lastIndexOf('user')
    const turnText = messages
      .slice(lastUser + 1)
      .filter(m => m.role === 'assistant')
      .map(m => m.text)
      .join('\n')
    // The save-context turn can precede the turn that calls the tool (button path
    // runs it as its own command), so fall back to the whole assistant tail.
    const tailText = messages
      .filter(m => m.role === 'assistant')
      .slice(-6)
      .map(m => m.text)
      .join('\n')
    const match = turnText.match(RESUME_LINE) ?? tailText.match(RESUME_LINE)

    if (!match) {
      $.ui.toast('Context not confirmed as saved, so the conversation was not cleared.')
      return result
    }

    // Remember which context to resume after the clear.
    await update($, resumeName, () => match[1])

    $.ui.toast('Context saved. Clearing the conversation...')
    // Run /clear from a timer: a hook the turn waits on cannot run a command.
    $.clock.after(400, async () => {
      try {
        await $.command.run({ command: 'clear', args: '' })
        // If the clear did not raise a new session.start, resume from here.
        $.clock.after(1200, () => resumeSaved($))
      } catch {
        $.ui.toast('Could not run /clear. Type /clear yourself; the context is saved.')
      }
    })

    return result
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const turns = await $.session.turns()
    const hidden = await read($, isHidden)
    const saving = await read($, isSaving)

    if (e.props.hasSurvey || hidden || (turns < MIN_TURNS && !saving)) {
      return next(e)
    }

    const { Box, Button, Text } = $.ui.resolve(e)

    if (saving) {
      return (
        <Box>
          <Text dimColor>Saving the context, then clearing... </Text>
        </Box>
      )
    }

    return (
      <Box>
        <Text dimColor>Long conversation ({turns} turns). </Text>
        <Button
          key="save-clear"
          label="Save context and clear"
          onPress={async () => {
            pending = true
            await update($, isSaving, () => true)
            try {
              await $.command.run({ command: 'maestro-ai:save-context', args: '' })
            } catch {
              pending = false
              await update($, isSaving, () => false)
              $.ui.toast('Could not start /maestro-ai:save-context. Is the maestro-ai plugin up to date?')
            }
          }}
        />
        <Text dimColor> </Text>
        <Button key="hide" label="Not now" onPress={() => update($, isHidden, () => true)} />
      </Box>
    )
  })
}
