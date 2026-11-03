package net.zerocontact.item.helmet;

import net.minecraft.resources.ResourceLocation;

import static net.zerocontact.ZeroContact.MOD_ID;

/** Casque balistique Police Nationale (modèle Bastion), une texture par grade : textures/models/helmet/helmet_pn_<grade>.png (tools/minenorth/gen_police_pn.py). */
public class PoliceHelmet extends BaseGeoHelmet {
    private static final ResourceLocation model = new ResourceLocation(MOD_ID, "geo/helmet/helmet_bastion_black.geo.json");
    private static final ResourceLocation animation = new ResourceLocation(MOD_ID, "");

    public PoliceHelmet(String grade, int absorb, int defaultDurability, float bluntReduction, float penetrateReduction) {
        super(absorb, defaultDurability, new ResourceLocation(MOD_ID, "textures/models/helmet/helmet_pn_" + grade + ".png"), model, animation, bluntReduction, penetrateReduction);
    }
}
