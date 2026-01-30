package move.special;

import ru.ifmo.se.pokemon.*;

public class DracoMeteor extends SpecialMove {
    public DracoMeteor() {
        super(Type.DRAGON, 130.0, 90.0);
    }
    public void applySelfEffects(Pokemon p1) {
        p1.setMod(Stat.SPECIAL_ATTACK, -2);
    }
    protected String describe() {
        return "использует Draco Meteor";
    }
}