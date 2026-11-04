# Sansad Showdown — Political Satire Fighter (fightkaro.com Recreation)

A complete, standalone 2.5D arcade fighting game recreation of **Sansad Showdown** (*fightkaro.com*), created by ShivamBuilds. Built with **Three.js**, **WebGL**, **Vite**, and **TypeScript**.

---

## 🎮 Quick Start & Running the Game

The game is pre-configured and ready to play locally:

```bash
cd sansad-showdown
npm install
npm run dev
```

Open your browser at: **`http://localhost:5173/`**

---

## 🕹️ Controls

### Keyboard (Player 1)
| Key | Action |
| :--- | :--- |
| **A / D** or **← / →** | Move Left / Right |
| **W** or **↑** | Jump |
| **S** or **↓** | Crouch |
| **Hold Back (away from foe)** | High Block / Guard |
| **Down + Back** | Low Block |
| **J** | Punch / Jab |
| **K** | Kick |
| **I** or **J + K** | Grab / Throw |
| **L** or **Space** | **SUPER MOVE** (Requires 100% SHAKTI Meter) |
| **Esc** | Pause ("Chai Break ☕") |
| **M** | Toggle BGM Music |
| **N** | Mute Sound Effects |

### Combos & Specials
* **Combos**: `J, J, J` · `J, J, K` · `J, K, K` · `K, K`
* **Specials**: `→ + J` · `→ + K` · `↓ + K` (Sweep knockdown) · `↓ + J` (Uppercut launcher)

### Touch / Mobile
* On-screen virtual analog joystick on the left.
* Action buttons on the right: **PUNCH**, **KICK**, **GRAB**, and **SUPER**.

---

## 🥊 Roster & Signature Super Moves

| Character | Title | Faction | Accent | Super Move & Satirical Effect |
| :--- | :--- | :--- | :--- | :--- |
| **MitraMan** | Narendra Modi | Team Vaada | `#ff9933` | **Mitra Chakra**: Levitates into the sky, gathers a spinning energy wheel, and hurls it across the arena. |
| **Yatra Boy** | Rahul Gandhi | Team Yatra | `#2e9bff` | **Aloo Se Sona**: Zaps opponent into a potato, feeds it into his machine, and shoots a beam of pure gold. |
| **Deedee** | Mamata Banerjee | Team Dharna | `#22b35e` | **Jadu Hobe**: Bubbling black cauldron chant ("humba humba") that transforms opponent into a frog. |
| **Tariff Taau** | Donald Trump | Team Tariff | `#e0262f` | **Tariff Tsunami**: Signs executive orders, summons shipping crate vortex, slams a massive tariff stamp. |
| **Dozer Dada** | Yogi Adityanath | Team Dozer | `#f05a00` | **Dozer Ka Dhamaka**: Red laser eyes, bulldozer charge, and triple front loader bucket slam. |
| **Toll Man** | Nitin Gadkari | Team Highway | `#ff9a1f` | **Gaddha Blast**: Sugarcane-to-E20 ethanol combustion in a pothole with a slow-motion explosion walk. |
| **Mbapu** *(Boss)* | Mahatma Gandhi | Shanti Akhada | `#ffd700` | **Manch Chhodo**: Spinning charkha wheel of light, cloth vortex throw, non-violence Shanti meter. |

---

## 🏛️ Stages

1. **Sansad Bhavan**: Parliament courtyard at sunset with grand classical pillars and warm atmospheric lighting.
2. **Jantar Mantar**: Delhi protest grounds with vibrant evening sky and rally atmosphere.
3. **Desi Sadak**: Bustling street corner with street lamps, barricades, and roadside chai stalls.

---

## ⚙️ How the Engine is Built

### 1. 2.5D Combat State Machine
* **Frame Data**: Every attack has strict `startup`, `active`, and `recovery` frames.
* **Hitstop**: 3 to 5 frames of freeze upon impact to give weight and punchiness to strikes.
* **Hitstun & Blockstun**: Prevents action while reeling from hits or guarding against attacks.
* **Damage Scaling**: Combos deal scaled damage to prevent infinite 100-to-0 touch-of-death chains.

### 2. Procedural 35-Bone Skeletal Animator
Instead of storing bulky animation files, characters share a unified 35-property humanoid pose system:
* Legs use a **2-Bone Analytical Inverse Kinematics (IK)** solver (`femur` & `tibia`) for natural foot planting during walks and squats.
* Exponential smoothing (`blendTo`) transitions poses smoothly at 60 FPS:
  $$\text{Pose}_{t+1} = \text{Pose}_t + (\text{Target} - \text{Pose}_t) \cdot (1 - e^{-k \cdot \Delta t})$$

### 3. Satire Engine & Newsdesk
* Dual TV news commentary at the bottom of the screen featuring **Godi Anchor** and **Troll Anchor** firing contextual lines on counters, low HP, and super finishes.
* **The Daily Jumla** procedural post-game newspaper generator with satirical headlines, defeat excuses, and screenshot snapshots.

---

## 📁 Project Structure

```
sansad-showdown/
├── public/
│   ├── assets/       # All 57 SFX files, Draco WASM decoders, styles
│   ├── faces/        # High-resolution character portraits (.png)
│   ├── models/       # 3D GLTF/GLB character meshes (.glb)
│   └── favicon.svg   # Game icons & webmanifest
├── src/
│   ├── main.ts       # Application entry point
│   └── style.css     # Complete arcade UI styling
├── index.html        # Game canvas, HUD, newsdesk, modal overlays
├── package.json      # Dependencies (Three.js, Vite, TypeScript)
└── tsconfig.json     # TypeScript configuration
```

