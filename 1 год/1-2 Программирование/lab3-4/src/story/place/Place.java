package story.place;

import java.io.PrintStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import story.actions.Action;
import story.person.Group;
import story.person.Person;

public class Place {
    private List<Person> peopleInside;
    private String name;

    public Place(String name) {
        this.name = name;
        this.peopleInside = new ArrayList();
    }

    public void addPerson(Person person, Action action) {
        if (!this.peopleInside.contains(person)) {
            this.peopleInside.add(person);
        }
        System.out.println(person.getName() + " пришел в " + this.toString() + " " + action.Text());
    }

    public void rmPerson(Person person, Action action) {
        if (this.peopleInside.contains(person)) {
            this.peopleInside.remove(person);
        }
        System.out.println(person.getName() + " вышел из" + this.toString() + " " + action.Text());
    }

    public void addGroup(Group group, Action action) {
        for(int i = 0; i < group.getMembers().size(); ++i) {
            if (!this.peopleInside.contains(group.getMembers().get(i))) {
                this.peopleInside.add(group.getMembers().get(i));
            }
        }
        System.out.println(group.getName() + " пришли в " + this.toString() + " " + action.Text());
    }

    public void rmGroup(Group group, Action action) {
        for(int i = 0; i < group.getMembers().size(); ++i) {
            if (this.peopleInside.contains(group.getMembers().get(i))) {
                this.peopleInside.remove(group.getMembers().get(i));
            }
        }
        System.out.println(group.getName() + "  вышли в " + this.toString() + " " + action.Text());
    }

    public void add(Person person) {
        if (!this.peopleInside.contains(person)) {
            this.peopleInside.add(person);
        }

    }

    public List<Person> getPeopleInside() {
        return this.peopleInside;
    }

    public String toString() {
        return this.name;
    }

    public boolean equals(Object o) {
        if (this == o) {
            return true;
        } else if (o != null && this.getClass() == o.getClass()) {
            Place room = (Place)o;
            return Objects.equals(this.name, room.name) && Objects.equals(this.peopleInside, room.peopleInside);
        } else {
            return false;
        }
    }

    public int hashCode() {
        return Objects.hash(new Object[]{this.name, this.peopleInside});
    }
}