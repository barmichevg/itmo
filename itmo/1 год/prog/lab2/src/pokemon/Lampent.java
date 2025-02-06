package pokemon;

import move.special.DreamEater;
import move.special.NightShade;
import move.special.Overheat;
import ru.ifmo.se.pokemon.*;

public class Lampent extends Pokemon {
    public Lampent(String name, int level){
        super(name,level);
        setType(new Type[]{Type.GHOST, Type.FIRE});
        setStats(60.0, 40.0, 60.0, 95.0, 60.0, 55.0);
        setMove(new Move[]{new DreamEater(), new Overheat(), new NightShade()});
    }
}