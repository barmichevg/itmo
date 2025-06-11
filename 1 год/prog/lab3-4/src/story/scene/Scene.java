package story.scene;

import story.actions.Assumption;
import story.person.Cast;
import story.person.Group;
import story.person.characters.Boy;
import story.person.characters.Character;
import story.place.Place;

public record Scene(Boy boy, Assumption randomGuess, Place place, Character Carlson, Character Basket, Group group, Cast cast) {
    public Scene(Boy boy, Assumption randomGuess, Place place, Character Carlson, Character Basket, Group group, Cast cast, Boolean o) {
        this(boy, randomGuess, place, Carlson, Basket, group, cast);
    }
}

//public class Scene {
//    private Boy boy;
//    private Assumption randomGuess;
//    private Place place;
//    private Character Carlson;
//    private Character Basket;
//    private Group group;
//    private Cast cast;
//
//    public Scene(Boy boy, Assumption randomGuess, Place place, Character Carlson, Character Basket, Group group, Cast cast) {
//        this.boy = boy;
//        this.randomGuess = randomGuess;
//        this.place = place;
//        this.Carlson = Carlson;
//        this.Basket = Basket;
//        this.group = group;
//        this.cast = cast;
//    }
//
//    public Boy boy() {
//        return boy;
//    }
//
//    public Assumption randomGuess() {
//        return randomGuess;
//    }
//
//    public Place place() {
//        return place;
//    }
//
//    public Character Carlson() {
//        return Carlson = Carlson;
//    }
//
//    public Character Basket() {
//        return Basket = Basket;
//    }
//
//    public Group group() {
//        return group = group;
//    }
//
//    public Cast cast() {
//        return cast = cast;
//    }
//}