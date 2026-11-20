**English** · [Dansk](Reflection-da) · [Bahasa Malaysia](Reflection-ms)

# Reflection

## How we approached it

We planned first: a Business Case, the stakeholders, a project plan and five milestones with tasks, then one pull request per milestone. Every step was small and ended with tests, a security scan and a review.

## What was hard

- **The speech engine.** Coqui TTS does not declare PyTorch, needs `torchcodec` for audio on recent PyTorch, and an English model needs a phoneme package (`gruut`) or the `espeak-ng` program. We found this by installing it in a throw-away environment before writing any engine code.
- **Two scanners.** The host's security scan is stricter than the local one and failed our first pull request.
- **Honest screenshots.** Our first screenshots of steps 2 and 3 showed an error, because the tool ran the wrong Python. We only saw it by reading the images' text.

## What was easy

- Reading a PDF with `pypdf` and splitting text are small, pure functions that are quick to test.
- A port with a fake engine made the converter and the command line simple to test.

## Our biggest lesson

Check the riskiest dependency first. Everything else in the plan depended on one question: does Coqui TTS install and speak on Python 3.13? Asking it first, in a scratch environment, was cheap and kept the rest of the plan safe.

## What we would do differently

- Pin the dependency versions at release; the project only sets minimum versions.
- Add an option to choose another voice model on the command line together with a short list of tested models.
- Run the host's scan rules locally from the start.
