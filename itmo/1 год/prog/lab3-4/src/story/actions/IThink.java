package story.actions;

import story.person.Person;

public interface IThink {
    default void think(Timemark timemark, Person thinkabout) {
        System.out.println("Oн думал о " + thinkabout.getName() + ".");
    }
}