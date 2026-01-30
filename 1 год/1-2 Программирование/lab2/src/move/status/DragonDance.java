package move.status;

import ru.ifmo.se.pokemon.*;

public class DragonDance extends StatusMove{
    public DragonDance() {
        super(Type.DRAGON, 0.0, 0.0);
    }
    public void applySelfEffects(Pokemon p1) {
        p1.setMod(Stat.ATTACK, 1);
        p1.setMod(Stat.SPEED, 1);
    }
    protected String describe() {
        return "использует Dragon Dance";
    }
}