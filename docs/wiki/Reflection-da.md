[English](Reflection) · **Dansk** · [Bahasa Malaysia](Reflection-ms)

# Refleksion

## Sådan greb vi det an

Vi planlagde først: en Business Case, interessenterne, en projektplan og fem milepæle med opgaver, og derefter én pull request pr. milepæl. Hvert trin var lille og sluttede med tests, en sikkerhedsscanning og en gennemgang.

## Hvad der var svært

- **Talemotoren.** Coqui TTS angiver ikke PyTorch, kræver `torchcodec` til lyd på nyere PyTorch, og en engelsk model kræver en fonempakke (`gruut`) eller programmet `espeak-ng`. Det fandt vi ud af ved at installere den i et midlertidigt miljø, før vi skrev nogen motorkode.
- **To scannere.** Værtens sikkerhedsscanning er strengere end den lokale og fik vores første pull request til at fejle.
- **Ærlige skærmbilleder.** Vores første skærmbilleder af trin 2 og 3 viste en fejl, fordi værktøjet kørte den forkerte Python. Vi opdagede det kun ved at læse billedernes tekst.

## Hvad der var let

- At læse en PDF med `pypdf` og dele tekst op er små, rene funktioner, der hurtigt kan testes.
- En port med en falsk motor gjorde konverteren og kommandolinjen enkle at teste.

## Vores største lærdom

Tjek den mest risikable afhængighed først. Alt andet i planen afhang af ét spørgsmål: kan Coqui TTS installeres og tale på Python 3.13? At stille det først, i et midlertidigt miljø, var billigt og holdt resten af planen sikker.

## Hvad vi ville gøre anderledes

- Fastlåse afhængighedernes versioner ved udgivelsen; projektet angiver kun mindsteversioner.
- Tilføje en indstilling til at vælge en anden stemmemodel på kommandolinjen sammen med en kort liste over testede modeller.
- Køre værtens scanningsregler lokalt fra starten.
