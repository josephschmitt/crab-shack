# planning-photoshoots

You're heading to the botanic garden tomorrow with the family. You want to come back with real photos, not phone snaps, but you don't want to lug every lens you own. Which two do you grab? What's worth shooting if it's overcast? Is there anything specific about this place you should know before you show up?

This is a photography buddy you can text before you leave. It asks what you're going for, looks up the weather and the location, then recommends a specific gear loadout from the kit you actually own, a style direction matched to conditions, and practical tips for the venue.

## Why you'd use it

Generic photography advice ignores the two things that decide every shoot: what's in your bag, and where you're going. Telling a Fuji prime shooter to use a tilt-shift is noise. This skill cuts that out:

- **Remembers your kit across sessions.** You describe your gear once — verified against real product pages so it doesn't hallucinate a lens you don't own — and every future conversation starts from that list. Tappable confirmations work one-handed when you're heading out the door.
- **Looks up the actual place and weather.** "Brooklyn Botanic Garden cherry blossoms in light rain" surfaces real intel about the venue and conditions instead of generic flower-photography platitudes.
- **Only recommends what you own.** No pivot into shopping suggestions, no "ideally you'd have a 400mm." If it's not in your kit, it's not in the loadout.
- **Calibrates to your skill level.** Beginners get the *why* behind an aperture choice; advanced shooters get creative direction and location-specific insight without the basics.

## Sample usage

> **You:** Taking the family to the botanic garden tomorrow, want to come back with some keepers.
>
> **Claude:** Got it. I have you down for an X-T5 with the 23mm f/2, 35mm f/1.4, 56mm f/1.2, and 80mm macro, plus a CPL and a speedlight. Still accurate? *[tap: Still accurate / Needs updating]*
>
> **You:** *[taps Still accurate]*
>
> **Claude:** Tomorrow looks overcast with a chance of afternoon showers. What's the priority? *[tap: Flower close-ups / Family candids / Mix of both]*
>
> **You:** *[taps Mix of both]*
>
> **Claude:** Grab the 35mm f/1.4 and the 80mm macro. Leave the rest.
>
> The 35 handles family candids wide open and still pulls back for environmental shots of paths and beds. The 80 earns its weight on individual blooms, especially if the rain comes through — wet petals on overcast light are the best macro conditions you'll get this season.
>
> Style: lean into the flat light. Saturated color, no harsh shadows, Classic Chrome or Classic Neg for muted tones. Keep the family shots tight since overcast flattens faces; fill the frame. For the macros, f/4–5.6 gives you sharpness across the petal rather than a paper-thin plane.
>
> Logistics: the cherry grove peaks mid-April and gets crowded before noon — aim for after 3pm. Tripods allowed in the outer gardens but not the conservatory.

First time through, it'll ask what's in your bag and verify each lens against real product listings before saving anything. After that, every shoot starts from the kit it already knows.

## Triggers

"what lens should I bring", "how should I shoot this", "photo tips for X", "planning a photo walk", "what gear for Y", or casual asides like "I want to get some good shots while we're there."

## Install

### Claude Code

```
/plugin marketplace add josephschmitt/crab-shack
/plugin install planning-photoshoots@joes-crab-shack
```

### Claude.ai (web or desktop)

Download [`planning-photoshoots.zip`](https://github.com/josephschmitt/crab-shack/releases/latest/download/planning-photoshoots.zip) from the [latest release](https://github.com/josephschmitt/crab-shack/releases/latest), then in Claude click **+** → **Create skill** and upload the zip.
