package common.models;

import java.io.Serializable;

/**
 * Класс Дисциплины
 */
public class Discipline implements Serializable {
    private String name;
    private Long practiceHours;

    /**
     * Конструктор
     * @param name название
     * @param practiceHours часы практики
     */
    public Discipline(String name, Long practiceHours) {
        this.name = name;
        this.practiceHours = practiceHours;
    }

    public String getName() { return name; }

    public Long getPracticeHours() { return practiceHours; }

    public void setName(String name) { this.name = name; }

    public void setPracticeHours(Long practiceHours) { this.practiceHours = practiceHours; }

    /**
     * @return возвращает объект, переведенный в строковое представление
     */
    @Override
    public String toString() {
        return name + " (" + practiceHours + ")";
    }
}