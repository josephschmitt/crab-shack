# spitballing

You've got a half-formed idea and you want to talk it through — but the moment you say "what if we…" the assistant starts building it. Or worse, it says "great idea!" and agrees with everything, which tells you nothing about whether the idea is any good.

This flips Claude into a spitballing mode where whatever you say is treated as thinking out loud — not an order, not a request to implement, not a fact to accept. Instead of running with your idea, Claude tries to break it: pokes at the hidden assumptions, names the failure modes, and pushes the premise to its extreme to see where it snaps.

## Why you'd use it

Normal assistant behavior is optimized for "do the thing." That's exactly wrong when you're still figuring out whether the thing is worth doing. In this mode Claude:

- Doesn't touch code, files, or commands — nothing you say gets acted on.
- Questions the premise instead of assuming it ("wouldn't that be cheaper?" gets interrogated, not accepted).
- Leads with the strongest objection, then offers a sharper version if the core survives.
- Follows ideas to their logical extreme to stress-test them.

It's a sparring partner, not a yes-man and not an executor.

## Sample usage

> **You:** /spitballing what if we replaced all the ice cream in the world with froyo? Wouldn't that be cheaper?
>
> **Claude:** The pitch is "froyo is cheaper to produce, so swap the whole category." Two problems. First, "cheaper" assumes the cost is in the fat — but a lot of froyo's price is live cultures and stabilizers that don't like the same cold chain, so at global scale your unit cost may actually go *up*, not down. Second, take it to the extreme: if the only goal is cheaper frozen dessert, why stop at froyo? Flavored ice is cheaper still. The fact that you wouldn't accept "replace it all with flavored ice" means cost isn't really the objective — texture and indulgence are. So the interesting question isn't froyo-vs-ice-cream, it's *which* attribute you're actually optimizing. Which one is it?

## Triggers

"/spitballing", "I'm just spitballing", "thinking out loud here, don't act on it", "brainstorming", "riff with me on this", "play devil's advocate". Claude stays in the mode until you clearly step out — "ok, actually build it", "for real this time", or "/spitballing off".

## Install

### Claude Code

```
/plugin marketplace add josephschmitt/crab-shack
/plugin install spitballing@joes-crab-shack
```

### Claude.ai (web or desktop)

Download [`spitballing.zip`](https://github.com/josephschmitt/crab-shack/releases/latest/download/spitballing.zip) from the [latest release](https://github.com/josephschmitt/crab-shack/releases/latest), then in Claude click **+** → **Create skill** and upload the zip.
