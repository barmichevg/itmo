package pokemon;

import move.physical.RockTomb;
import move.status.SandAttack;
import move.status.Swagger;
import move.special.SludgeBomb;
import ru.ifmo.se.pokemon.*;

public class Palossand extends Pokemon {
    public Palossand(String name, int level){
        super(name,level);
        setType(new Type[]{Type.GHOST, Type.FIRE});
        setStats(60.0, 55.0, 90.0, 145.0, 90.0, 80.0);
        setMove(new Move[]{new Swagger(), new SandAttack(), new RockTomb(), new SludgeBomb()});
    }
}