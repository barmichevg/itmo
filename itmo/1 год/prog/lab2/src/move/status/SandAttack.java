package move.status;
import ru.ifmo.se.pokemon.*;

public class SandAttack extends StatusMove {
    public SandAttack(){
        super(Type.GROUND,0.0,100.0);
    }
    protected void applyOppEffects(Pokemon p2) {
        p2.setMod(Stat.ACCURACY, -1);
    }
    protected String describe() {
        return "использует Sand Attack";
    }
}