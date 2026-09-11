package net.zerocontact.item.uniform;

import net.minecraft.resources.ResourceLocation;

import static net.zerocontact.ZeroContact.MOD_ID;

public class HautPoliceNationale extends BaseUniformTop{
    private static final ResourceLocation texture = new ResourceLocation(MOD_ID,"textures/models/uniform/uniform_haut_pn.png");
    private static final ResourceLocation model = new ResourceLocation(MOD_ID,"geo/uniform/uniform_pn_top.geo.json");
    private static final ResourceLocation animation = new ResourceLocation(MOD_ID,"");
    public HautPoliceNationale() {
        super(texture, model, animation);
    }
}
