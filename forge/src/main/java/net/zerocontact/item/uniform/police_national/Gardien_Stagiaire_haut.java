package net.zerocontact.item.uniform.police_national;

import net.minecraft.resources.ResourceLocation;
import net.zerocontact.item.uniform.BaseUniformTop;
import net.zerocontact.item.uniform.HautPoliceNationale;

import static net.zerocontact.ZeroContact.MOD_ID;

public class Gardien_Stagiaire_haut extends HautPoliceNationale {
    private static final ResourceLocation texture = new ResourceLocation(MOD_ID,"textures/models/uniform/police_national/uniform_haut_pn_gardien_s.png");
    public Gardien_Stagiaire_haut() {
        super(texture);
    }
}
