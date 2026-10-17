# Walkabout Mini Golf Avatar-Editor

[English](README.md) | **Deutsch**

Stell dir im Browser deinen eigenen [Walkabout Mini Golf](https://www.mightycoconut.com/minigolf)-Avatar zusammen, dazu deinen Lieblingsputter und -ball. Speichere dann ein Bild davon oder lade ihn als 3D-Datei mit allen Farben herunter, zum Beispiel um eine Figur von dir im 3D-Drucker zu drucken.

> [!IMPORTANT]
> **Dies ist ein inoffizielles Fanprojekt.** Es stammt nicht von Mighty Coconut, den Machern des Spiels, und hat nichts mit ihnen zu tun.
>
> **Die Modelle aus dem Spiel sind hier nicht enthalten.** Der Editor liest sie aus **deiner eigenen Kopie des Spiels** auf deinem PC. Das erledigst du einmalig mit einer Einrichtungsdatei, die alles für dich macht (siehe unten). Bitte behalte die ausgelesenen Dateien für dich und gib sie nicht weiter.

## Was du brauchst

- **Einen Windows-PC, auf dem Walkabout Mini Golf installiert ist.** Es muss die PC-Version sein, installiert über die **Meta-Quest-Link-App** (früher Oculus-App) oder über **Steam**. Direkt von der Quest-Brille kann der Editor das Spiel nicht lesen.
- **Eine Internetverbindung.**
- **Etwa 10–15 Minuten** für die erste Einrichtung. Das musst du nur einmal machen.

## Einrichtung

### Schritt 1: Python installieren

Die Einrichtung braucht ein kostenloses Programm namens **Python**, um die Spieldateien zu lesen. Du musst dich damit nicht auskennen, du installierst es nur einmal.

1. Öffne den [**Python Install Manager** im Microsoft Store](https://apps.microsoft.com/detail/9NQ7512CXL7T).
2. Klicke auf **Installieren** (manchmal heißt es **Herunterladen**) und warte, bis es fertig ist.

Das war's. Um den Rest kümmert sich die Einrichtungsdatei in Schritt 3.

<details>
<summary>Du kannst den Microsoft Store nicht nutzen oder möchtest mehr wissen?</summary>

- Du kannst den Python Install Manager auch von [python.org/downloads](https://www.python.org/downloads/) herunterladen. Klicke auf den gelben Download-Button und starte die heruntergeladene Datei.
- Die offizielle Anleitung (auf Englisch) heißt [Using Python on Windows](https://docs.python.org/3/using/windows.html).
- Du hast Python schon? Kein Problem. Die Einrichtung verwendet es, wenn es Version 3.10 bis 3.14 ist. Ist es neuer (3.15 funktioniert noch nicht), installiert die Einrichtung 3.14 zusätzlich, sofern der Python Install Manager installiert ist.

</details>

### Schritt 2: Den Editor herunterladen

1. Klicke oben auf dieser Seite auf den grünen Button **Code** und dann auf **Download ZIP**.
2. Öffne deinen Ordner **Downloads**. Klicke mit der rechten Maustaste auf die heruntergeladene Datei (`walkabout-minigolf-character-creator-main.zip`) und wähle **Alle extrahieren…**.
3. Wähle einen Ort, an dem du den Ordner wiederfindest, zum Beispiel deinen Ordner **Dokumente**, und klicke auf **Extrahieren**.

> [!TIP]
> Öffne die Dateien nicht direkt in der ZIP-Datei. Entpacke sie immer zuerst, sonst kann die Einrichtung nichts speichern.

### Schritt 3: Die Einrichtung starten

1. Öffne den entpackten Ordner und **doppelklicke auf `Extract game data.bat`**. Windows blendet die Endung `.bat` manchmal aus, dann heißt die Datei nur **Extract game data**.
2. Windows warnt dich eventuell, weil die Datei aus dem Internet stammt:
   - Wenn **„Der Computer wurde durch Windows geschützt“** erscheint, klicke auf **Weitere Informationen** und dann auf **Trotzdem ausführen**.
   - Wenn **„Datei öffnen – Sicherheitswarnung“** erscheint, klicke auf **Ausführen**.
3. Ein schwarzes Fenster öffnet sich und erledigt die Einrichtung von selbst. Es:
   - installiert bei Bedarf die passende Python-Version,
   - lädt ein paar Hilfskomponenten herunter,
   - sucht das Spiel auf deinem PC,
   - liest die Avatare, Putter und Bälle aus dem Spiel aus.

   Beim ersten Mal dauert das ein paar Minuten. Wenn das Spiel nicht automatisch gefunden wird, fragt dich ein Fenster nach dem Spielordner. Siehe [Wo ist das Spiel installiert?](#wo-ist-das-spiel-installiert)
4. Wenn **Fertig!** erscheint, öffnet sich der Editor in deinem Browser. Drücke **Enter**, um das schwarze Fenster zu schließen.

Die Einrichtung liest die Spieldateien nur. Sie verändert nie etwas am Spiel.

## Den Editor benutzen

Ab jetzt reicht ein **Doppelklick auf `index.html`** im Ordner des Editors. Er öffnet sich in deinem Browser (Chrome, Edge oder Firefox). Die Seite braucht eine Internetverbindung, weil sie eine 3D-Bibliothek aus dem Internet lädt.

Das kannst du machen:

- **Avatar**: Wähle den normalen Avatar oder eine Figur aus einem der Packs. Wähle für jede Kategorie (Kopf, Augen, Haare, Hut, Brille, Bart, Outfit und mehr) ein Teil und eine Farbe.
- **Putter und Ball**: Wähle aus allen Puttern und Bällen des Spiels. Sie werden wie auf einer Spielerkarte gezeigt. Die Hand am Putter bekommt die Hautfarbe deines Avatars, oder du schaltest auf den originalen grauen Handschuh um.
- **Vorlagen und Zufall**: Starte mit einer der Vorlagen aus dem Spiel oder lass dir einen zufälligen Avatar erstellen.
- **Kamera**: Drehe die Ansicht mit der Maus oder wähle einen fertigen Blickwinkel wie vorne, Seite oder Gesicht (nah).
- **Beleuchtung**: Wähle einen Beleuchtungsstil oder stelle Helligkeit und Lichter selbst ein.
- **PNG speichern**: Speichere ein Bild der aktuellen Ansicht, bis zur 4-fachen Größe, mit normalem, weißem oder transparentem Hintergrund.
- **Herunterladen**: Speichere ein einzelnes Teil, einen Putter oder einen Ball, oder deine ganze Figur mit Putter und Ball, als eine 3D-Datei:
  - **3MF**: Für den 3D-Druck. Öffne sie in einem Slicer wie Bambu Studio, PrusaSlicer oder OrcaSlicer. Die Farben sind enthalten, die Größe ist in Millimetern.
  - **OBJ**: Für andere 3D-Programme wie Blender.
- **Sprache**: Deutsch oder Englisch, über den Button in der oberen Leiste.

## Nach einem Spiel-Update

Wenn das Spiel neue Avatar-Teile, Figuren, Putter oder Bälle bekommt, **doppelklicke erneut auf `Extract game data.bat`**. Lade danach den Editor im Browser neu. Die neuen Sachen erscheinen automatisch.

Meldet die Einrichtung nach einem Spiel-Update einen Fehler, hat das Update vermutlich geändert, wie das Spiel seine Dateien speichert, und der Editor muss ebenfalls angepasst werden. Bitte [eröffne ein Issue](https://github.com/MaSch0212/walkabout-minigolf-character-creator/issues). Sobald es eine korrigierte Version gibt, lade sie erneut herunter (Schritt 2) und starte die Einrichtung erneut (Schritt 3).

## Hilfe

### Wo ist das Spiel installiert?

Das brauchst du nur, wenn die Einrichtung das Spiel nicht selbst findet. Wähle den Ordner aus, der `WalkaboutMiniGolf_Data` enthält.

- **Meta-Quest-Link-App**: Meistens `C:\Program Files\Oculus\Software\Software\mighty-coconut-walkabout-mini-golf`. Wenn du deine Spiele auf einem anderen Laufwerk installiert hast, suche dort nach einem Ordner `Software\mighty-coconut-walkabout-mini-golf`.
- **Steam**: Klicke in deiner Steam-Bibliothek mit der rechten Maustaste auf Walkabout Mini Golf und wähle **Verwalten → Lokale Dateien durchsuchen**. Der Ordner, der sich öffnet, ist der richtige.

### Der Editor zeigt nur „Die Spieldaten fehlen noch“

Starte die Einrichtung (Schritt 3). Der Editor kann erst etwas anzeigen, wenn er die Modelle aus deinem Spiel gelesen hat.

### Das schwarze Fenster sagt, dass Python fehlt

Installiere den Python Install Manager (Schritt 1) und doppelklicke dann erneut auf `Extract game data.bat`. Die Einrichtung öffnet dir die passende Seite im Microsoft Store.

### Das schwarze Fenster sagt, dass die Hilfskomponenten nicht heruntergeladen werden konnten

Prüfe deine Internetverbindung und starte die Einrichtung erneut.

### Etwas anderes ist schiefgegangen

Bitte [eröffne ein Issue](https://github.com/MaSch0212/walkabout-minigolf-character-creator/issues) und füge einen Screenshot des schwarzen Fensters bei.

## Für Entwickler

<details>
<summary>Manuelle Einrichtung, Projektaufbau und wie die Daten ausgelesen werden</summary>

Die Einrichtungsdatei startet `tools/setup.ps1`. Das Skript legt in `.venv` eine virtuelle Umgebung mit Python 3.10–3.14 an (die Abhängigkeiten von UnityPy gibt es für 3.15 noch nicht als Wheels) und installiert `requirements.txt`. Dann sucht es das Spiel über die Bibliothekseinträge der Meta-Quest-Link-App in der Registry oder über die Steam-Bibliotheken und startet das Build-Skript. Der gewählte Ordner wird in `.game-folder` gespeichert.

Von Hand geht es so:

```powershell
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python tools\build_data.py "C:\Program Files\Oculus\Software\Software\mighty-coconut-walkabout-mini-golf"
```

`build_data.py` sucht im angegebenen Ordner nach `avatarsandputters_assets_all.bundle` und `common_assets_all.bundle` (in `WalkaboutMiniGolf_Data\StreamingAssets\aa\StandaloneWindows64`). Es liest sie mit [UnityPy](https://github.com/K0lb3/UnityPy) und schreibt `data/`, das von Git ignoriert wird:

| Datei | Inhalt |
| --- | --- |
| `data/bundle.js` | Alle Geometrie- und Texturdaten, eingebettet, damit die Seite auch über `file://` funktioniert |
| `data/*.png` | Die Texturen als einzelne Bilder |
| `data/meta.json`, `data/geometry.bin` | Dieselben Daten wie in `bundle.js`, nicht eingebettet |

Das Skript liest alles ein, was es findet. Neue Teile, Figuren, Vorlagen, Putter und Bälle kommen deshalb ohne Codeänderung dazu. Anpassen muss man es, wenn das Spiel seine Bundles, die Objekte `Library`/`Putters`/`Balls` oder die Texturen umbenennt oder eine neue Teile-Kategorie einführt. Eine neuere Unity-Version kann außerdem ein neueres UnityPy erfordern.

```
index.html               der gesamte Editor (HTML, CSS und JavaScript, three.js vom jsdelivr-CDN)
Extract game data.bat    Einrichtung per Doppelklick, startet tools/setup.ps1
tools/setup.ps1          sucht Python und das Spiel, richtet .venv ein, startet build_data.py
tools/build_data.py      liest die Modelle und Texturen aus dem Spiel nach data/ aus
requirements.txt         Python-Abhängigkeiten des Build-Skripts
data/                    generiert, nicht Teil des Repositorys
```

Um die Seite über einen Server statt direkt von der Festplatte zu öffnen: `python -m http.server 8765`, dann http://localhost:8765 öffnen.

</details>

## Lizenz

Der Code in diesem Repository steht unter der [MIT-Lizenz](LICENSE).

Walkabout Mini Golf und alle zugehörigen Modelle, Texturen und anderen Inhalte sind Eigentum von Mighty Coconut. Sie fallen nicht unter diese Lizenz und sind nicht Teil dieses Repositorys.
