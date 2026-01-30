package models;

import exceptions.ValidationException;
import utility.Validatable;

import java.util.Objects;

/**
 * Класс дисциплина
 */
public class Discipline implements Validatable {
    private String name; //Поле не может быть null, Строка не может быть пустой
    private Long practiceHours; //Поле не может быть null

    public Discipline (String name, Long practiceHours) {
        this.name = name;
        this.practiceHours = practiceHours;
        if (!validate()){throw new ValidationException("Discipline");}
    }

    public Discipline(String s) {
        try {
            this.name = (s.split(";")[0]);
            try { this.practiceHours = Long.parseLong(s.split(";")[1]); } catch (NumberFormatException e) { }
        } catch (ArrayIndexOutOfBoundsException e) {}
    }

    /**
     * Метод, возвращающий поле name
     * @return name
     */
    public String getName() {
        return name;
    }

    /**
     * Метод, возвращающий поле practiceHours
     * @return practiceHours
     */
    public Long getPracticeHours() {
        return practiceHours;
    }

    @Override
    public boolean validate() {
        if (name == null || name.isEmpty()) return false;
        return practiceHours != null;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Discipline that = (Discipline) o;
        return (Objects.equals(name, that.getName()) && Objects.equals(practiceHours, that.getPracticeHours()));
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, practiceHours);
    }

    @Override
    public String toString() {
        return name + ";" + practiceHours;
    }
}