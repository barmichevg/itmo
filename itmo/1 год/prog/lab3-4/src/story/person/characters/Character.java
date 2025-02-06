package story.person.characters;

import java.util.Objects;
import story.actions.Action;
import story.actions.IDoAct;
import story.actions.Timemark;
import story.person.Person;

public class Character extends Person implements IDoAct {
    public Character(String name) {
        super(name);
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
        return this.getName();
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Character character = (Character) o;
        return (Objects.equals(this.name, character.name));
    }

    @Override
    public int hashCode() {
        return Objects.hash(name);
    }

    @Override
    public void doAct(Timemark timemark, Action action) {
        String answer = timemark.Time() + " " + this.toString() + " " + action.Text();
        if (timemark.Time() == "") {
            answer = this.toString() + " " + action.Text();
        }
        System.out.println(answer);
    }
}