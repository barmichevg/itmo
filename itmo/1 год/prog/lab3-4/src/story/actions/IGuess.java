package story.actions;

import java.io.PrintStream;
import story.person.Person;

public interface IGuess {
    default void guess(Timemark timemark, Person guessabout, Assumption assumption) {
        System.out.println("Что " + guessabout.getName() + " " + timemark.Time() + " делает? Может, " + assumption.describe());
    }
}