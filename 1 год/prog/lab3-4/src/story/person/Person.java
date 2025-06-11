package story.person;

import java.util.Objects;

public abstract class Person {
    public String name;
    public Person(String name) {
        this.name = name;
    }

    public abstract String getName();
    public abstract void setName(String var1);

    @Override
    public String toString() {
        return this.name;
    }

    @Override
    public int hashCode() {
        return name.hashCode();
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Person person = (Person) o;
        return (Objects.equals(this.name, person.name));
    }
}