package net.zerocontact.item.helmet;

import net.minecraft.resources.ResourceLocation;

import static net.zerocontact.ZeroContact.MOD_ID;

public class Berret_pn extends BaseGeoHelmet {
    private static final ResourceLocation texture = new ResourceLocation(MOD_ID, "textures/models/helmet/helmet_berret_pn.png");
    private static final ResourceLocation model = new ResourceLocation(MOD_ID, "geo/helmet/helmet_berret_pn.geo.json");
    private static final ResourceLocation animation = new ResourceLocation(MOD_ID, "");

    public Berret_pn(int absorb, int defaultDurability, float bluntReduction, float penetrateReduction) {
        super(absorb, defaultDurability, texture, model, animation, bluntReduction, penetrateReduction);
    }
}
