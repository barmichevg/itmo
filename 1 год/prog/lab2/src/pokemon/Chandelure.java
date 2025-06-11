package pokemon;

import move.special.DreamEater;
import move.special.NightShade;
import move.special.FireBlast;
import move.special.Overheat;
import ru.ifmo.se.pokemon.*;

public class Chandelure extends Pokemon {
    public Chandelure(String name, int level){
        super(name,level);
        setType(new Type[]{Type.GHOST, Type.FIRE});
        setStats(60.0, 55.0, 90.0, 145.0, 90.0, 80.0);
        setMove(new Move[]{new DreamEater(), new Overheat(), new NightShade(), new FireBlast()});
    }
}