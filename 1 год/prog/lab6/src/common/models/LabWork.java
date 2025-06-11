package common.models;

import common.models.Coordinates;
import common.models.Difficulty;
import common.models.Discipline;

import java.io.Serializable;
import java.time.LocalDateTime;
import java.util.Objects;

/**
 * Класс Лабораторной
 */
public class LabWork implements Serializable, Comparable<LabWork> {
    private Integer id; //Значение поля должно быть больше 0, Значение этого поля должно быть уникальным, Значение этого поля должно генерироваться автоматически
    private String name; //Поле не может быть null, Строка не может быть пустой
    private Coordinates coordinates; //Поле не может быть null
    private LocalDateTime creationDate; //Поле не может быть null, Значение этого поля должно генерироваться автоматически
    private Long minimalPoint; //Поле может быть null, Значение поля должно быть больше 0
    private String description; //Длина строки не должна быть больше 5287, Поле не может быть null
    private Integer tunedInWorks;
    private Difficulty difficulty; //Поле не может быть null
    private Discipline discipline; //Поле не может быть null

    public void setId(Integer id) {this.id = id;}

    public void setCreationDate(LocalDateTime creationDate) {this.creationDate = creationDate;}

    public LocalDateTime getCreationDate() {return creationDate;}

    public Coordinates getCoordinates() {return coordinates;}

    public long getMinimalPoint() {return minimalPoint;}

    public void setMinimalPoint(long minimalPoint) {this.minimalPoint = minimalPoint;}

    public void setDescription(String description) {this.description = description;}

    public Integer getId() {return id;}

    public void setDiscipline(Discipline discipline) {this.discipline = discipline;}

    public void setDifficulty(Difficulty difficulty) {this.difficulty = difficulty;}

    public void setTunedInWorks(Integer tunedInWorks) {this.tunedInWorks = tunedInWorks;}

    public void setCoordinates(Coordinates coordinates) {this.coordinates = coordinates;}

    public void setName(String name) {this.name = name;}

    public String getName() {return name;}

    public String getDescription() {return description;}

    public Integer getTunedInWorks() {return tunedInWorks;}

    public Difficulty getDifficulty() {return difficulty;}

    public Discipline getDiscipline() {return discipline;}


    /**
     * @param other the object to be compared.
     * @return возвращает на сколько один число студентов в одной группе больше, чем в другой
     */
    @Override
    public int compareTo(LabWork other) {
        return Integer.compare(this.id, other.id);
    }
//    @Override
//    public int compareTo(LabWork other) {
//        return Long.compare(this.minimalPoint, other.minimalPoint);
//    }

    /**
     * Переопределение метода эквивалентности объект
     *
     * @param obj сравниваемый объект
     * @return true, если объекты эквивалентны
     */
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        LabWork labWork = (LabWork) obj;
        return Objects.equals(id, labWork.id) &&
                Objects.equals(name, labWork.name) &&
                Objects.equals(coordinates, labWork.coordinates) &&
                Objects.equals(creationDate, labWork.creationDate) &&
                Objects.equals(minimalPoint, labWork.minimalPoint) &&
                Objects.equals(description, labWork.description) &&
                Objects.equals(tunedInWorks, labWork.tunedInWorks) &&
                Objects.equals(difficulty, labWork.difficulty) &&
                Objects.equals(discipline, labWork.discipline);
    }

    /**
     * @return возвращает Хэш-код объекта
     */
    @Override
    public int hashCode() {return Objects.hash(id, name, coordinates, creationDate, minimalPoint, description, tunedInWorks, difficulty, discipline);}

    /**
     * @return возвращает объект, переведенный в строковое представление
     */
    @Override
    public String toString() {
        return "LabWork{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", coordinates=" + coordinates +
                ", creationDate=" + creationDate +
                ", minimalPoint=" + minimalPoint +
                ", description='" + description + '\'' +
                ", tunedInWorks=" + tunedInWorks +
                ", difficulty=" + difficulty +
                ", discipline=" + discipline +
                '}';
    }
}