[English](Reflection) · **Dansk** · [Bahasa Malaysia](Reflection-ms)

# Refleksion

## Hvordan vi greb det an

Vi planlagde først: en business case, interessenterne, en projektplan og milepæle med opgaver, derefter én pull request pr. milepæl. Hvert trin var lille og sluttede med tests, en sikkerhedsscanning, en gennemgang og et grønt byg på værten. De første fem milepæle byggede konverteren og kommandolinjen. Derefter tilføjede vi fire mere på samme måde: et vindue hvor man skriver tekst og hører den, en Open PDF-knap med Stop, en rolig konsol og en indlæsningsstatus.

## Hvad der var svært

- **Talemotoren.** Coqui TTS erklærer ikke PyTorch, skal bruge `torchcodec` til lyd på nyere PyTorch, og en engelsk model skal bruge en fonempakke (`gruut`) eller programmet `espeak-ng`. Det fandt vi ud af ved at installere den i et midlertidigt miljø, før vi skrev motorkode.
- **To scannere.** Værtens sikkerhedsscanning er strengere end den lokale og afviste to pull requests: først på shell-kald, senere på en lambda i en konstruktør.
- **Et vindue vi ikke må røre.** Vinduet testes i en Linux-container på en virtuel skærm, aldrig på skrivebordet. Det beviser logikken, statusteksten og et skærmbillede, men ikke hvad der sker, når et menneske lukker vinduet. Den første rigtige lukning gav en fejl, som vores tests ikke havde set.
- **Ærlig dokumentation.** Vores første skærmbilleder af trin 2 og 3 viste en fejl, fordi værktøjet kørte den forkerte Python. En scriptfejl afkortede også et dokument, og det opdagede vi først senere.

## Hvad der var let

- At læse en PDF med `pypdf` og dele tekst er små, rene funktioner, der er hurtige at teste.
- Porte med falske objekter: motoren, lydafspilleren, filvælgeren og tekstudtrækkeren injiceres, så 154 tests kører på omkring et sekund uden lyd, vindue eller netværk.
- At tilføje en funktion til et lagdelt design: hver ny milepæl rørte få filer og lod domænet være uændret.

## Vores største lærdom

Tjek det mest risikable først, og test der hvor brugeren virkelig handler. Hele planen afhang af ét spørgsmål: kan Coqui TTS installeres og tale på Python 3.13? At stille det først i et midlertidigt miljø holdt resten sikkert. Fejlen ved lukning af vinduet lærte os den anden halvdel: en falsk grafisk brugerflade beviser logik, ikke hvad et menneske gør.

## Hvad vi ville gøre anderledes

- Køre værtens scanningsregler lokalt fra starten.
- Teste vinduets luk- og annuller-veje i et midlertidigt Windows-miljø, ikke kun i en container.
- Bede en anden person gennemgå business casen og beslutningerne; alle gennemgange i projektet var stedfortræder for én person.
- Tilføje en mulighed for at vælge en anden stemmemodel på kommandolinjen med en kort liste over afprøvede modeller.
- Lukke de små åbne punkter: business casen tæller to krævede pakker, mens projektet nu har flere, og statussen `Loading voice...` dækker også den første bid, fordi motoren ikke har et "indlæst"-signal.
