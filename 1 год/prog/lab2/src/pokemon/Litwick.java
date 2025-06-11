package pokemon;

import move.special.DreamEater;
import move.special.Overheat;
import ru.ifmo.se.pokemon.*;

public class Litwick extends Pokemon {
    public Litwick(String name, int level){
        super(name,level);
        setType(new Type[]{Type.GHOST, Type.FIRE});
        setStats(50.0, 30.0, 55.0, 65.0, 55.0, 20.0);
        setMove(new Move[]{new DreamEater(), new Overheat()});
    }
}