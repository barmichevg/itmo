package move.special;

import ru.ifmo.se.pokemon.*;

public class DreamEater extends SpecialMove {
    public DreamEater() {
        super(Type.PSYCHIC, 100.0, 100.0);
    }
    public void applySelfEffects(Pokemon p1,Pokemon p2) {
        p1.setMod(Stat.HP, -(int)((p2.getStat(Stat.HP)-p2.getHP())/2));
    }
    protected String describe() {
        return "использует Dream Eater";
    }
}