package pokemon;

import move.status.Swagger;
import move.status.SandAttack;
import move.physical.RockTomb;
import ru.ifmo.se.pokemon.*;

public class Sandygast extends Pokemon {
    public Sandygast(String name, int level){
        super(name,level);
        setType(new Type[]{Type.GHOST, Type.GROUND});
        setStats(55.0, 55.0, 80.0, 70.0, 45.0, 15.0);
        setMove(new Move[]{new Swagger(), new SandAttack(), new RockTomb()});
    }
}