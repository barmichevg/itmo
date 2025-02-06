package move.special;

import ru.ifmo.se.pokemon.*;

public class SludgeBomb extends SpecialMove{
    public SludgeBomb(){
        super(Type.FIRE, 90.0,100.0);
    }
    private boolean flag;
    public void applyOppEffects(Pokemon p2) {
        if (Math.random() <= 0.3) {
            flag = true;
            Effect.poison(p2);
        }
    }
    protected String describe(){
        if(flag) return "использует Sludge Bomb и отравляет";
        else return "использует Sludge Bomb";
    }
}