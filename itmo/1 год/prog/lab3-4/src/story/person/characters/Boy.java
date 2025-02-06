package story.person.characters;

import java.util.Objects;
import story.actions.Assumption;
import story.actions.IFightsleep;
import story.actions.IGuess;
import story.actions.IThink;
import story.actions.Timemark;
import story.person.Person;

public class Boy extends Character implements IFightsleep, IThink, IGuess {
    private Assumption assumption;

    public Boy(String name) {
        super(name);
    }

    @Override
    public void think(Timemark timemark,Person thinkabout) {
        String answer = timemark.Time() + " " + this.name +  " думал о " + thinkabout.getName() + ".";
        if (timemark.Time() == "") {
            answer = this.name +  " думал о " + thinkabout.getName() + ".";
        }
        System.out.println(answer);
    }

    @Override
    public void fightsleep(Timemark timemark) {
        String answer = timemark.Time() + " " + this.name +  " одолевал сон. Но " + this.name + " еще не спал.";
        if (timemark.Time() == "") {
            answer = this.name +  " уже одолевал сон. Но " + this.name + " еще не спал.";
        }
        System.out.println(answer);
    }

    public void guess(Timemark timemark, Person guessabout, Assumption assumption) {
        String answer = "Что " + guessabout.getName() + " " + timemark.Time() + " делает? Может, " + assumption.describe();
        if (timemark.Time() == "") {
            answer = "Что " + guessabout.getName() + " делает? Может, " + assumption.describe();
        }
        System.out.println(answer);
    }

    public Assumption getRandomAssumption(Boy boy) {
        int rnd = (int) (Math.random() * Assumption.values().length);
        return Assumption.values()[rnd];
    }

    @Override
    public String getName() {
        return this.name;
    }

    @Override
    public void setName(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return this.name;
    }

    @Override
    public int hashCode() {
        return Objects.hash(name);
    }
}