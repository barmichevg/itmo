package pokemon;

import move.status.DragonDance;
import move.special.DracoMeteor;
import move.physical.AerialAce;
import move.special.IceBeam;
import ru.ifmo.se.pokemon.*;

public class Latios extends Pokemon {
    public Latios(String name, int level){
        super(name,level);
        setType(new Type[]{Type.DRAGON, Type.PSYCHIC});
        setStats(80.0, 90.0, 80.0, 130.0, 110.0, 110.0);
        setMove(new Move[]{new DragonDance(), new DracoMeteor(), new AerialAce(), new IceBeam()});
    }
}