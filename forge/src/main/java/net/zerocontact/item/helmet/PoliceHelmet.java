package net.zerocontact.item.helmet;

import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.zerocontact.api.armor.modular.ModularEquipment;
import net.zerocontact.armor.modular.model.MountCategory;
import net.zerocontact.armor.modular.model.MountDefinition;
import net.zerocontact.armor.modular.model.MountType;

import java.util.Collection;
import java.util.List;
import java.util.Set;

import static net.zerocontact.ZeroContact.MOD_ID;

/** Casque balistique Police Nationale (modèle Bastion), une texture par grade : textures/models/helmet/helmet_pn_<grade>.png (tools/minenorth/gen_police_pn.py).
 *  Mêmes points de montage que le Bastion du pack (helmet_bastion_black.json) : JVN, batterie, balise, casque radio, couvre-casque. */
public class PoliceHelmet extends BaseGeoHelmet implements ModularEquipment {
    private static final ResourceLocation model = new ResourceLocation(MOD_ID, "geo/helmet/helmet_bastion_black.geo.json");
    private static final ResourceLocation animation = new ResourceLocation(MOD_ID, "");
    private static final List<MountDefinition> MOUNTS = List.of(
            new MountDefinition(new ResourceLocation(MOD_ID, "nvg_mount"), MountType.HELMET_FRONT, "nvg_fix", Set.of(MountCategory.NIGHT_VISION)),
            new MountDefinition(new ResourceLocation(MOD_ID, "battery_mount"), MountType.HELMET_BACK, "battery_fix", Set.of(MountCategory.BATTERY)),
            new MountDefinition(new ResourceLocation(MOD_ID, "beacon_mount"), MountType.HELMET_TOP, "beacon_fix", Set.of(MountCategory.BEACON)),
            new MountDefinition(new ResourceLocation(MOD_ID, "headset_mount"), MountType.HELMET_TOP, "headset_fix", Set.of(MountCategory.HEADSET)),
            new MountDefinition(new ResourceLocation(MOD_ID, "cover_mount"), MountType.HELMET_TOP, "cover_fix", Set.of(MountCategory.HELMET_COVER)));

    public PoliceHelmet(String grade, int absorb, int defaultDurability, float bluntReduction, float penetrateReduction) {
        super(absorb, defaultDurability, new ResourceLocation(MOD_ID, "textures/models/helmet/helmet_pn_" + grade + ".png"), model, animation, bluntReduction, penetrateReduction);
    }

    @Override
    public Collection<MountDefinition> getMountDefinitions(ItemStack stack) {
        return MOUNTS;
    }
}
