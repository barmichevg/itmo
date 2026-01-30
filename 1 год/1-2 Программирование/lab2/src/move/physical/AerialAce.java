package move.physical;

import ru.ifmo.se.pokemon.*;

public class AerialAce extends SpecialMove {
    public AerialAce() {
        super(Type.FLYING, 60.0, 99999.0);
    }
    protected String describe() {
        return "использует Aerial Ace";
    }
}