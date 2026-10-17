# Walkabout Mini Golf Character Creator

A browser-based character creator for the avatars, putters and balls of [Walkabout Mini Golf](https://www.mightycoconut.com/minigolf), built with [three.js](https://threejs.org/). Put together an avatar, then save a picture of it or download it as a single 3D file with colors (3MF or OBJ), for example for 3D printing.

> **This is an unofficial fan project.** It is not affiliated with or endorsed by Mighty Coconut. **No game assets are included in this repository.** You need your own copy of the game and have to extract the models yourself with the included script (see below). Keep the extracted files to yourself and don't redistribute them.

## Features

- **Avatar**: pick the human avatar or any pack character, then a part and a color for each category (head, eyes, hair, hat, glasses, beard, outfit and more). Hair and glasses squash under caps and visors, like in the game.
- **Putters and balls**: every putter and ball from the game, with previews. They are posed like on a player card. The putter hand takes the avatar's skin tone (optional).
- **Templates**: the game's built-in presets, plus a randomize button.
- **Downloads**: each part, putter or ball separately, or the whole character (optionally with putter and ball) as one file:
  - **3MF**: per-triangle colors, in millimetres. Works with slicers such as Bambu Studio, PrusaSlicer or OrcaSlicer.
  - **OBJ**: vertex colors, in metres.
- **Rendering**: the game's materials, including metallic and glowing putters and balls.
- **Camera**: preset angles such as front, 3/4, side, back, top and face close-up.
- **Lighting**: presets and sliders, remembered per browser.
- **Save PNG**: the current view at 1x, 2x or 4x, on the default background, white or transparent.
- **Languages**: English and German.

## Setup

### 1. Requirements

- Walkabout Mini Golf installed on a Windows PC (the PC VR version, e.g. from the Meta Quest Link app or Steam).
- [Python](https://www.python.org/downloads/) 3.10 or newer.
- A current Chrome, Edge or Firefox. The page loads three.js from the jsdelivr CDN, so it needs an internet connection.

### 2. Find the game folder

The script needs the game's install folder, the one that contains `WalkaboutMiniGolf_Data`.

- **Meta Quest Link app**: by default `C:\Program Files\Oculus\Software\Software\mighty-coconut-walkabout-mini-golf`. If you use a different library location, it is `<library>\Software\mighty-coconut-walkabout-mini-golf`.
- **Steam**: right-click the game in your library, then choose **Manage → Browse local files**.

The models come from these two files in that folder:

```
WalkaboutMiniGolf_Data\StreamingAssets\aa\StandaloneWindows64\avatarsandputters_assets_all.bundle
WalkaboutMiniGolf_Data\StreamingAssets\aa\StandaloneWindows64\common_assets_all.bundle
```

You don't have to point at them directly: the script searches the folder you pass for them. The script was developed against the Meta version; the Steam version should use the same files.

### 3. Extract the game data

Open PowerShell in the repository folder. Create a virtual environment and install the dependencies ([UnityPy](https://github.com/K0lb3/UnityPy), numpy and Pillow):

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

Then run the script with your game folder:

```powershell
.venv\Scripts\python tools\build_data.py "C:\Program Files\Oculus\Software\Software\mighty-coconut-walkabout-mini-golf"
```

The script only reads the game files and never changes them. It takes a minute or two and writes the extracted data to `data\`. That folder is ignored by git.

| File | Contents |
| --- | --- |
| `data\bundle.js` | All geometry and textures, embedded so the page also works from `file://` |
| `data\*.png` | The textures as separate images |
| `data\meta.json`, `data\geometry.bin` | The same data as `bundle.js`, unembedded |

### 4. Open the creator

Open `index.html` in your browser. No server is needed.

If you prefer serving it locally:

```powershell
python -m http.server 8765
```

Then open http://localhost:8765.

## After a game update

Run the script again (step 3) and reload the page. New avatar parts, pack characters, templates, putters and balls are picked up automatically, because the script reads everything it finds in the game files instead of using a fixed list.

The script may need an update if the game changes how its files are structured. That includes:

- different bundle file names
- renamed internal objects (`Library`, `Putters`, `Balls`) or textures
- a new avatar part category
- a newer Unity version that needs a newer UnityPy (`pip install -U UnityPy`)

In those cases the script stops with an error or the new content is missing from the creator. Please open an issue.

## Project layout

```
index.html            the whole creator (HTML, CSS and JavaScript)
tools/build_data.py   extracts the models and textures from the game into data/
requirements.txt      Python dependencies of the build script
data/                 generated, not part of the repository
```

## License

The code in this repository is licensed under the [MIT License](LICENSE).

Walkabout Mini Golf and all of its models, textures and other assets are the property of Mighty Coconut. They are not covered by this license and are not part of this repository.
