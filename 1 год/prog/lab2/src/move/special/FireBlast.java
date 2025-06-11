package move.special;

import ru.ifmo.se.pokemon.*;

public class FireBlast extends SpecialMove{
    public FireBlast(){
        super(Type.FIRE, 110.0,85.0);
    }
    private boolean flag;
    public void applyOppEffects(Pokemon p2) {
        if (Math.random() <= 0.3) {
            flag = true;
            Effect.burn(p2);
        }
    }
    protected String describe(){
        if(flag) return "использует Fire Blast и поджигает";
        else return "использует Fire Blast";
    }
}