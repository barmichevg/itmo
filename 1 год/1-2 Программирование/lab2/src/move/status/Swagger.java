package move.status;
import ru.ifmo.se.pokemon.*;

public class Swagger extends StatusMove {
    public Swagger(){
        super(Type.NORMAL,0.0,85.0);
    }
    protected void applyOppEffects(Pokemon p2) {
        p2.setMod(Stat.ATTACK, 2);
        Effect.confuse(p2);
    }
    protected String describe() {
        return "использует Swagger";
    }
}