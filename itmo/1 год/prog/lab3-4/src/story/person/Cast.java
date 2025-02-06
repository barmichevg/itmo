package story.person;

import exception.DublicatedName;
import java.util.ArrayList;
import java.util.List;

public class Cast {
    private List<Person> cast = new ArrayList();

    public Cast(String name) {
    }

    public void addCast(Person person) {
        if (!this.cast.contains(person)) {
            this.cast.add(person);
        } else {
            throw new DublicatedName(person.getName());
        }
    }

    public List<Person> getName() {
        return this.cast;
    }

    public List<Person> getCast() {
        return this.cast;
    }
}