import story.Start;
import story.actions.Assumption;
import story.person.Cast;
import story.person.Group;
import story.person.characters.Boy;
import story.person.characters.Character;
import story.place.Place;
import story.scene.Scene;

public class Main {
    public static void main(String[] args) {
        Cast cast = new Cast("cast");
        Place room = new Place("комната");
        Boy LittleOne = new Boy("Малыш");
        room.add(LittleOne);
        cast.addCast(LittleOne);
        Character Carlson = new Character("Карлсон");
        cast.addCast(Carlson);
        Character Basket = new Character("Корзинка");
        cast.addCast(Basket);
        room.add(Basket);
        Group all = new Group("Все");
        Character Ch1 = new Character("мама");
        all.addMember(Ch1);
        cast.addCast(Ch1);
        Character Ch2 = new Character("папа");
        all.addMember(Ch2);
        cast.addCast(Ch2);
        Character Ch3 = new Character("Боссе");
        all.addMember(Ch3);
        cast.addCast(Ch3);
        Character Ch4 = new Character("Бетан");
        all.addMember(Ch4);
        cast.addCast(Ch4);
        Assumption randomGuess = LittleOne.getRandomAssumption(LittleOne);

        Scene scene = new Scene(LittleOne, randomGuess, room, Carlson, Basket, all, cast);

        Start start = new Start(scene);
        start.go();
    }
}