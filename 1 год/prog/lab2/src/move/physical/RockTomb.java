package move.physical;

import ru.ifmo.se.pokemon.*;

public class RockTomb extends PhysicalMove {
    public RockTomb(){
        super(Type.ROCK,60.0,95.0);
    }
    protected void applyOppEffects(Pokemon p2) {
        p2.setMod(Stat.SPEED, -1);
    }
    protected String describe() {
        return "использует Rock Tomb";
    }
}

