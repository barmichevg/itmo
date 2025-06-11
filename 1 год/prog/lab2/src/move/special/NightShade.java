package move.special;

import ru.ifmo.se.pokemon.*;

public class NightShade extends SpecialMove {
    public NightShade() {
        super(Type.GHOST, 0.0, 100.0);
    };
    protected double calcBaseDamage(Pokemon p1, Pokemon p2) {
        return p1.getLevel();
    }
    protected String describe() {
        return "использует Night Shade";
    }
}