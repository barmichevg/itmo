package move.special;

import ru.ifmo.se.pokemon.*;

public class IceBeam extends SpecialMove{
    public IceBeam(){
        super(Type.ICE, 90.0,100.0);
    }
    private boolean flag;
    public void applyOppEffects(Pokemon p2) {
        if (Math.random() <= 0.1) {
            flag = true;
            Effect.freeze(p2);
        }
    }
    protected String describe(){
        if(flag) return "использует Ice Beam и замораживает";
        else return "использует Ice Beam";
    }
}