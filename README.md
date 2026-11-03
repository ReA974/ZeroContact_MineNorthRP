# <img width="29" height="34" alt="vest_avs_tagilla_desert" src="https://github.com/user-attachments/assets/17c4500f-7dda-4d0f-9a9e-90ab9ac56651" /> ZeroContact 


This project is licensed under the GNU General Public License v3.0 (GPLv3).  
It also includes third-party components, which are licensed under their respective licenses.

---

## 📦 About

**ZeroContact** is a *TaCZ addon* that introduces a new armor system and combat mechanics.

It adds a collection of armor-piercing rounds and countermeasure systems, working alongside TaCZ to enhance combat interactions.

This mod also remasters how the game calculates:
- Bullet damage
- Armor durability loss
- Body part hitbox interactions

---

## ⚙️ Features

- Various types of body armor, ballistic plates, plate carriers, and accessories
- Reworked armor system for incoming bullet damage calculation
- Datapack support for customizing:
  - Geckolib-based armor models
  - Plate and plate carrier behavior
  - Bullet damage override logic

---

## 📚 Credits

### 🔗 Upstream Dependencies

#### 🧨 Timeless and Classics Zero (TaCZ) — GPLv3
- craneblock6666 — Founder  
- MaydayMemory — Developer  
- LaeDev — Member  
- TartaricAcid — Member  
- xjqsh — Member  
- F1zeiL — Stats Design  

---

#### 🏗 Architectury API — LGPLv3
- Architectury Organization

---

#### 🎒 Curios API — LGPLv3
- TheIllusiveC4 — Owner

---

#### 🦎 Geckolib — MIT
- Gecko — Owner  
- DerToaster98 — Contributor  
- KyoSleep — Contributor  
- mchorse — Contributor  
- Tslat — Maintainer  
- ZigyTheBird — Member  

---

## 👥 Contributors

- Raider Modelling — TG@Faldskimerkh  
- Item Modelling — DC@SkyRofls  

---

## 🚓 MineNorthRP – Police Nationale par grade

Grades du mod `minenorth-police` : Sous-officier, Officier, Commissaire. Objets enregistrés en Java (pas dans `default_pack`) :
- `brassard_pn_<grade>` : brassard orange POLICE de la BAC (en civil) + écusson de grade (`Armband.Series.PN_*`, modèle `brassard_pn`) ;
- `armor_jpc_v2_pn_<grade>` : gilet pare-balles JPC PN (mêmes stats que `armor_jpc_v2_pn_gs`), POLICE devant et dans le dos, écusson de grade ;
- `helmet_pn_<grade>` : casque balistique (modèle Bastion, stats du Bastion), bleu nuit, bandeau de grade, logo PN devant, POLICE sur la nuque (`PoliceHelmet`).
RAID : `armor_jpc_v2_pn_raid` (gilet noir, plus protecteur) et `helmet_pn_raid` (casque noir), POLICE devant, RAID dans le dos.
Écussons : chevrons argent (sous-officier), 2 barrettes argent (officier), 3 barrettes or (commissaire).
Textures, modèles d'objet et noms (en_us ET fr_fr, en français) : `python tools/minenorth/gen_police_pn.py`.
Aperçu hors jeu d'un modèle GeckoLib : `python tools/minenorth/apercu_geo.py <sortie.png> <geo> <texture> [...] --peau`.

---

## 🖼 Preview

![banner](https://github.com/user-attachments/assets/c1f05642-3308-4063-be00-bcd5c73dc48e)
