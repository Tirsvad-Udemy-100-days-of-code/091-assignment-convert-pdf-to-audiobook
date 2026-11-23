**English** · [Dansk](Reflection-da) · [Bahasa Malaysia](Reflection-ms)

# Reflection

## How we approached it

We planned first: a Business Case, the stakeholders, a project plan and milestones with tasks, then one pull request per milestone. Every step was small and ended with tests, a security scan, a review and a green build on the host. The first five milestones built the converter and the command line. We then added four more the same way: a window where you type text and hear it, an Open PDF button with Stop, a quiet console, and a loading status.

## What was hard

- **The speech engine.** Coqui TTS does not declare PyTorch, needs `torchcodec` for audio on recent PyTorch, and an English model needs a phoneme package (`gruut`) or the `espeak-ng` program. We found this by installing it in a throw-away environment before writing any engine code.
- **Two scanners.** The host's security scan is stricter than the local one and failed two pull requests: first on shell calls, later on a lambda inside a constructor.
- **A window we may not touch.** The window is tested in a Linux container on a virtual display, never on the desktop. That proves the logic, the status text and a screenshot, but not what happens when a person closes the window. The first real close raised an error that our tests had not seen.
- **Honest evidence.** Our first screenshots of steps 2 and 3 showed an error, because the tool ran the wrong Python. A script error also cut a document short, and we noticed only later.

## What was easy

- Reading a PDF with `pypdf` and splitting text are small, pure functions that are quick to test.
- Ports with fakes: the engine, the audio player, the file chooser and the text extractor are injected, so 154 tests run in about a second with no sound, no window and no network.
- Adding a feature to a layered design: each new milestone touched few files and left the domain unchanged.

## Our biggest lesson

Check the riskiest thing first, and test where the user really acts. Everything in the plan depended on one question: does Coqui TTS install and speak on Python 3.13? Asking it first, in a scratch environment, kept the rest safe. The window-close error taught the other half: a fake of the GUI proves logic, not what a person does.

## What we would do differently

- Run the host's scan rules locally from the start.
- Test the window's close and cancel paths in a disposable Windows environment, not only in a container.
- Ask a second person to review the Business Case and the decisions; every review in this project was a stand-in for one person.
- Add an option to choose another voice model on the command line, with a short list of tested models.
- Close the small open items: the Business Case counts two required packages while the project now has more, and the status `Loading voice...` also covers the first chunk, because the engine has no "loaded" signal.
