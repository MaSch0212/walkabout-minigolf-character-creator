# Walkabout Mini Golf Character Creator

**English** | [Deutsch](README.de.md)

Build your own [Walkabout Mini Golf](https://www.mightycoconut.com/minigolf) avatar in your web browser, together with your favorite putter and ball. Then save a picture of it, or download it as a 3D file with all its colors, for example to 3D-print a figure of yourself.

> [!IMPORTANT]
> **This is an unofficial fan project.** It is not made by or connected to Mighty Coconut, the makers of the game.
>
> **The game's models are not included here.** The creator reads them from **your own copy of the game** on your PC. You do this once with a setup file that takes care of everything (see below). Please keep the extracted files to yourself and don't share them.

## What you need

- **A Windows PC with Walkabout Mini Golf installed.** It has to be the PC version, installed either through the **Meta Quest Link app** (formerly Oculus app) or through **Steam**. The creator can't read the game from the Quest headset itself.
- **An internet connection.**
- **About 10–15 minutes** for the first setup. You only have to do it once.

## Setup

### Step 1: Install Python

The setup needs a free program called **Python** to read the game files. You don't need to know anything about it; you just install it once.

1. Open the [**Python Install Manager** in the Microsoft Store](https://apps.microsoft.com/detail/9NQ7512CXL7T).
2. Click **Install** (sometimes called **Get**) and wait until it's done.

That's all. The setup file in step 3 takes care of the rest.

<details>
<summary>Can't use the Microsoft Store, or want more details?</summary>

- You can also download the Python Install Manager from [python.org/downloads](https://www.python.org/downloads/). Click the yellow download button and run the downloaded file.
- The official guide is [Using Python on Windows](https://docs.python.org/3/using/windows.html).
- Already have Python? That's fine. The setup uses it if it's version 3.10 to 3.14. If it's newer (3.15 doesn't work yet), the setup installs 3.14 alongside it, as long as the Python Install Manager is installed.

</details>

### Step 2: Download the creator

1. **[Click here to download the creator](https://github.com/MaSch0212/walkabout-minigolf-character-creator/archive/refs/heads/main.zip)** (a ZIP file).
2. Open your **Downloads** folder. Right-click the downloaded file (`walkabout-minigolf-character-creator-main.zip`) and choose **Extract All…**.
3. Pick a place where you'll find it again, for example your **Documents** folder, and click **Extract**.

> [!TIP]
> Don't open the files directly inside the ZIP. Always extract it first, otherwise the setup can't save anything.

### Step 3: Run the setup

1. Open the extracted folder and **double-click `Extract game data.bat`**. Windows may hide the `.bat` ending, so it can also appear as just **Extract game data**.
2. Windows may warn you because the file comes from the internet:
   - If you see **"Windows protected your PC"**, click **More info**, then **Run anyway**.
   - If you see **"Open File – Security Warning"**, click **Run**.
3. A black window opens and works through the setup on its own. It:
   - installs the right Python version, if needed,
   - downloads a few helper components,
   - finds the game on your PC,
   - reads the avatars, putters and balls from the game.

   The first time, this takes a few minutes. If the game isn't found automatically, a window asks you to select the game folder. See [Where is the game installed?](#where-is-the-game-installed)
4. When it says **Done!**, the creator opens in your browser. Press **Enter** to close the black window.

The setup only reads the game files. It never changes the game.

## Using the creator

From now on, just **double-click `index.html`** in the creator's folder. It opens in your browser (Chrome, Edge or Firefox). The page needs an internet connection, because it loads a 3D library from the web.

What you can do:

- **Avatar**: Pick the normal avatar or a character from one of the packs. For each category (head, eyes, hair, hat, glasses, beard, outfit and more), choose a part and a color.
- **Putter and ball**: Choose from every putter and ball in the game. They're shown like on a player card. The hand on the putter takes your avatar's skin color, or you can switch to the original gray glove.
- **Templates and randomize**: Start from one of the game's templates, or roll a random avatar.
- **Camera**: Turn the view with your mouse, or pick a ready-made angle such as front, side or face close-up.
- **Lighting**: Choose a lighting style or adjust the brightness and the lights yourself.
- **Save PNG**: Save a picture of the current view, in up to 4 times the size, with the normal, a white or a transparent background.
- **Download**: Save a single part, putter or ball, or your whole character with putter and ball, as one 3D file:
  - **3MF**: For 3D printing. Open it in a slicer such as Bambu Studio, PrusaSlicer or OrcaSlicer. The colors are included, and the size is in millimeters.
  - **OBJ**: For other 3D programs, such as Blender.
- **Language**: English or German, using the button in the top bar.

## After a game update

When the game gets new avatar parts, characters, putters or balls, **double-click `Extract game data.bat` again**. Then reload the creator in your browser. New items appear automatically.

If the setup reports an error after a game update, the update probably changed how the game stores its files, and the creator has to be updated too. Please [open an issue](https://github.com/MaSch0212/walkabout-minigolf-character-creator/issues). When a fixed version is available, download it again (step 2) and run the setup again (step 3).

## Help

### Where is the game installed?

You only need this if the setup can't find the game itself. Select the folder that contains `WalkaboutMiniGolf_Data`.

- **Meta Quest Link app**: Usually `C:\Program Files\Oculus\Software\Software\mighty-coconut-walkabout-mini-golf`. If you installed your games on another drive, look there for a folder named `Software\mighty-coconut-walkabout-mini-golf`.
- **Steam**: In your Steam library, right-click Walkabout Mini Golf and choose **Manage → Browse local files**. The folder that opens is the one you need.

### The creator only says "The game data is missing"

Run the setup (step 3). The creator can't show anything until it has read the models from your game.

### The black window says Python is missing

Install the Python Install Manager (step 1), then double-click `Extract game data.bat` again. The setup opens its Microsoft Store page for you.

### The black window says it couldn't download the helper components

Check your internet connection and run the setup again.

### Something else went wrong

Please [open an issue](https://github.com/MaSch0212/walkabout-minigolf-character-creator/issues) and include a screenshot of the black window.

## For developers

<details>
<summary>Manual setup, project layout and how the data is extracted</summary>

The setup file runs `tools/setup.ps1`. That script creates a virtual environment in `.venv` with Python 3.10–3.14 (UnityPy's dependencies don't ship wheels for 3.15 yet) and installs `requirements.txt`. It then finds the game through the Meta Quest Link library entries in the registry or the Steam libraries, and runs the build script. The selected folder is remembered in `.game-folder`.

To do it by hand:

```powershell
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python tools\build_data.py "C:\Program Files\Oculus\Software\Software\mighty-coconut-walkabout-mini-golf"
```

`build_data.py` searches the given folder for `avatarsandputters_assets_all.bundle` and `common_assets_all.bundle` (in `WalkaboutMiniGolf_Data\StreamingAssets\aa\StandaloneWindows64`). It reads them with [UnityPy](https://github.com/K0lb3/UnityPy) and writes `data/`, which git ignores:

| File | Contents |
| --- | --- |
| `data/bundle.js` | All geometry and textures, embedded so the page also works from `file://` |
| `data/*.png` | The textures as separate images |
| `data/meta.json`, `data/geometry.bin` | The same data as `bundle.js`, not embedded |

The script reads everything it finds, so new parts, characters, templates, putters and balls come in without code changes. It needs updating if the game renames its bundles, the `Library`/`Putters`/`Balls` objects or the textures, or adds a new part category. A newer Unity version may also need a newer UnityPy.

```
index.html               the whole creator (HTML, CSS and JavaScript, three.js from the jsdelivr CDN)
Extract game data.bat    double-click setup, starts tools/setup.ps1
tools/setup.ps1          finds Python and the game, sets up .venv, runs build_data.py
tools/build_data.py      extracts the models and textures from the game into data/
requirements.txt         Python dependencies of the build script
data/                    generated, not part of the repository
```

To serve the page instead of opening it from disk: `python -m http.server 8765`, then open http://localhost:8765.

</details>

## License

The code in this repository is licensed under the [MIT License](LICENSE).

Walkabout Mini Golf and all of its models, textures and other assets are the property of Mighty Coconut. They are not covered by this license and are not part of this repository.
