package net.zerocontact.forge_registries.item;

import dev.architectury.registry.registries.RegistrySupplier;
import net.minecraft.world.level.ItemLike;
import net.zerocontact.api.TabableItem;
import net.zerocontact.item.helmet.*;
import net.zerocontact.registries.ItemsReg;

import java.util.List;

public class Helmets implements TabableItem {
    public static RegistrySupplier<AltynVisor.WithVisor> ALTYN_VISOR_HELMET = ItemsReg.ITEMS.register("helmet_altyn_visor", () -> new AltynVisor.WithVisor(10, 72, 0.21f, 1.25f));
    public static RegistrySupplier<Berret_pn> BERET_PN = ItemsReg.ITEMS.register("helmet_berret_pn", () -> new Berret_pn(10, 72, 0.21f, 1.25f));
    // Police Nationale : casque balistique par grade de minenorth-police (stats du casque Bastion)
    public static RegistrySupplier<PoliceHelmet> HELMET_PN_SOUS_OFFICIER = ItemsReg.ITEMS.register("helmet_pn_sous_officier", () -> new PoliceHelmet("sous_officier", 8, 64, 0.33f, 0.84f));
    public static RegistrySupplier<PoliceHelmet> HELMET_PN_OFFICIER = ItemsReg.ITEMS.register("helmet_pn_officier", () -> new PoliceHelmet("officier", 8, 64, 0.33f, 0.84f));
    public static RegistrySupplier<PoliceHelmet> HELMET_PN_RAID = ItemsReg.ITEMS.register("helmet_pn_raid", () -> new PoliceHelmet("raid", 10, 80, 0.3f, 0.8f));
    public static RegistrySupplier<PoliceHelmet> HELMET_PN_COMMISSAIRE = ItemsReg.ITEMS.register("helmet_pn_commissaire", () -> new PoliceHelmet("commissaire", 8, 64, 0.33f, 0.84f));

    private static final List<RegistrySupplier<? extends ItemLike>> items = List.of(
            ALTYN_VISOR_HELMET,BERET_PN,HELMET_PN_SOUS_OFFICIER,HELMET_PN_OFFICIER,HELMET_PN_COMMISSAIRE,HELMET_PN_RAID
    );

    @Override
    public List<RegistrySupplier<? extends ItemLike>> getItems() {
        return items;
    }
}
