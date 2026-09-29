package net.zerocontact.item.uniform.police_national;

import net.minecraft.resources.ResourceLocation;
import net.zerocontact.item.uniform.BasPoliceNationale;

import static net.zerocontact.ZeroContact.MOD_ID;

public class Uniform_Gardien_bas extends BasPoliceNationale {
    private static final ResourceLocation texture = new ResourceLocation(MOD_ID,"textures/models/uniform/police_national/uniform_bas_pn_gardien.png");
    public Uniform_Gardien_bas() {
        super(texture);
    }
}
