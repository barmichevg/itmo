import pokemon.*;
import ru.ifmo.se.pokemon.Battle;

public class Main {
    public Main() {
    }
    public static void main(String[] var0) {
        Battle b = new Battle();
        Latios p1 = new Latios("Латиос", 2);
        Sandygast p2 = new Sandygast("Сандигаст", 2);
        Palossand p3 = new Palossand("Палоссанд", 2);
        Litwick p4 = new Litwick("Литвик", 2);
        Lampent p5 = new Lampent("Лампент", 2);
        Chandelure p6 = new Chandelure("Чанделур", 2);
        b.addAlly(p1);
        b.addAlly(p3);
        b.addAlly(p5);
        b.addFoe(p2);
        b.addFoe(p4);
        b.addFoe(p6);
        b.go();
    }
}