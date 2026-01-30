package common.models;

import java.io.Serializable;
import java.time.LocalDateTime;
import java.util.Objects;

/**
 * Класс Лабораторной
 */
public class LabWork implements Serializable, Comparable<LabWork> {
    private Integer id;
    private String name;
    private Coordinates coordinates;
    private LocalDateTime creationDate;
    private Long minimalPoint;
    private String description;
    private Integer tunedInWorks;
    private Difficulty difficulty;
    private Discipline discipline;
    private Integer owner; // Новый атрибут

    public void setId(Integer id) {this.id = id;}
    public void setCreationDate(LocalDateTime creationDate) {this.creationDate = creationDate;}
    public LocalDateTime getCreationDate() {return creationDate;}
    public Coordinates getCoordinates() {return coordinates;}
    public Long getMinimalPoint() {return minimalPoint;}
    public void setMinimalPoint(Long minimalPoint) {this.minimalPoint = minimalPoint;}
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
    public Integer getOwner() {return owner;}
    public void setOwner(Integer owner) {this.owner = owner;}

    /**
     * @param other the object to be compared.
     * @return возвращает на сколько один число студентов в одной группе больше, чем в другой
     */
    @Override
    public int compareTo(LabWork other) {
        return Integer.compare(this.id, other.id);
    }

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
                Objects.equals(discipline, labWork.discipline) &&
                Objects.equals(owner, labWork.owner);
    }

    /**
     * @return возвращает Хэш-код объекта
     */
    @Override
    public int hashCode() {
        return Objects.hash(id, name, coordinates, creationDate, minimalPoint, description, tunedInWorks, difficulty, discipline, owner);
    }

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
                ", owner='" + owner + '\'' +
                '}';
    }
}