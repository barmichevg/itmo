package models;

import utility.Element;
import utility.Validatable;

import java.time.LocalDate;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.Objects;
import java.time.format.DateTimeFormatter;

/**
 * Класс лабораторной работы
 */
public class LabWork implements Comparable<Element>, Validatable {
    private Integer id; //Значение поля должно быть больше 0, Значение этого поля должно быть уникальным, Значение этого поля должно генерироваться автоматически
    private String name; //Поле не может быть null, Строка не может быть пустой
    private Coordinates coordinates; //Поле не может быть null
    private LocalDate creationDate; //Поле не может быть null, Значение этого поля должно генерироваться автоматически
    private Double minimalPoint; //Поле может быть null, Значение поля должно быть больше 0
    private String description; //Длина строки не должна быть больше 5287, Поле не может быть null
    private int tunedInWorks;
    private Difficulty difficulty; //Поле не может быть null
    private Discipline discipline; //Поле не может быть null

    public LabWork(int id, String name, Coordinates coordinates, LocalDate creationDate, Double minimalPoint, String description, int tunedInWorks, Difficulty difficulty, Discipline discipline) {
        this.id = id;
        this.name = name;
        this.coordinates = coordinates;
        this.creationDate = creationDate;
        this.minimalPoint = minimalPoint;
        this.description = description;
        this.tunedInWorks = tunedInWorks;
        this.difficulty = difficulty;
        this.discipline = discipline;
    }

    public LabWork(int id, String name, Coordinates coordinates, Double minimalPoint, String description, int tunedInWorks, Difficulty difficulty, Discipline discipline) {
        this(id, name, coordinates, LocalDate.now(), minimalPoint, description, tunedInWorks, difficulty, discipline);
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public Coordinates getCoordinates() {
        return coordinates;
    }

    public LocalDate getCreationDate() {
        return creationDate;
    }

    public Double getMinimalPoint() {
        return minimalPoint;
    }

    public String getDescription() {
        return description;
    }

    public int getTunedInWorks() {
        return tunedInWorks;
    }

    public Difficulty getDifficulty() {
        return difficulty;
    }

    public Discipline getDiscipline() {
        return discipline;
    }

    public void update(LabWork labWork) {
        this.name = labWork.name;
        this.coordinates = labWork.coordinates;
        this.creationDate = labWork.creationDate;
        this.minimalPoint = labWork.minimalPoint;
        this.description = labWork.description;
        this.tunedInWorks = labWork.tunedInWorks;
        this.difficulty = labWork.difficulty;
        this.discipline = labWork.discipline;
    }

    public static LabWork fromArray(String[] a) {
        int id;
        String name;
        Coordinates coordinates;
        LocalDate creationDate;
        Double minimalPoint;
        String description;
        int tunedInWorks;
        Difficulty difficulty;
        Discipline discipline;
        try {
            try { id = Integer.parseInt(a[0]); } catch (NumberFormatException e) { id = Integer.parseInt(null); }
            name = a[1];
            coordinates = new Coordinates(a[2]);
            try { creationDate = LocalDate.parse(a[3], DateTimeFormatter.ofPattern("dd-MM-yyyy")); } catch (DateTimeParseException e) { creationDate = null; }
            try { minimalPoint = (a[4].equals("null") ? null : Double.parseDouble(a[4])); } catch (NumberFormatException e) { minimalPoint = null; }
            description = a[5];
            try { tunedInWorks = Integer.parseInt(a[6]); } catch (NumberFormatException e) { tunedInWorks = Integer.parseInt(null); }
            try { difficulty = Difficulty.valueOf(a[7]); } catch (NullPointerException | IllegalArgumentException  e) { difficulty = null; }
            discipline = new Discipline(a[8]);
            return new LabWork(id, name, coordinates, creationDate, minimalPoint, description, tunedInWorks, difficulty, discipline);
        }catch (ArrayIndexOutOfBoundsException e) {}
        return null;
    }

    public static String[] toArray(LabWork e) {
        ArrayList<String> list = new ArrayList<String>();
        list.add(Integer.toString(e.getId()));
        list.add(e.getName());
        list.add(e.getCoordinates().toString());
        list.add(e.getCreationDate().format(DateTimeFormatter.ofPattern("dd-MM-yyyy")));
        list.add(e.getMinimalPoint() == null ? "null" : e.getMinimalPoint().toString());
        list.add(e.getDescription());
        list.add(Integer.toString(e.getTunedInWorks()));
        list.add(e.getDifficulty().toString());
        list.add(e.getDiscipline().toString());
        return list.toArray(new String[0]);
    }

    @Override
    public boolean validate() {
        if (id <= 0) return false;
        if (name == null || name.isEmpty()) return false;
        if (coordinates == null || !coordinates.validate()) return false;
        if (creationDate == null) return false;
        if (minimalPoint != null && minimalPoint <= 0) return false;
        if (description == null || description.length() >= 5287) return false;
        if (difficulty == null) return false;
        if (discipline == null || !discipline.validate()) return false;
        return true;
    }

    @Override
    public int compareTo(Element element) {
        return (this.id - element.getId());
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        LabWork that = (LabWork) o;
        return Objects.equals(id, that.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, name, coordinates, creationDate, minimalPoint, description, tunedInWorks, difficulty, discipline);
    }

    @Override
    public String toString() {
        return String.format(
                "+-------------------------------------+----------------------+ \n" +
                "| %-35s | %-20s | \n" +
                "| %-35s | %-20s | \n" +
                "| %-35s | %-20s | \n" +
                "| %-35s | %-20s | \n" +
                "| %-35s | %-20s | \n" +
                "| %-35s | %-20s | \n" +
                "| %-35s | %-20s | \n" +
                "| %-35s | %-20s | \n" +
                "| %-35s | %-20s | \n" +
                "+-------------------------------------+----------------------+",
                "id", id,
                "name", name,
                "coordinates (x;y)", coordinates,
                "creationDate (dd-MM-yyyy)", creationDate.format(DateTimeFormatter.ofPattern("dd-MM-yyyy")),
                "minimalPoint", (minimalPoint == null ? "null" : minimalPoint.toString()),
                "description", description,
                "tunedInWorks", tunedInWorks,
                "difficulty", difficulty,
                "discipline (name;practiceHours)", discipline
        );
    }

//    public String toString() {
//        return "{\"id\": " + id + ", " +
//                "\"name\": " + name + ", " +
//                "\"coordinates\" (x;y): " + coordinates + ", " +
//                "\"creationDate\": " + creationDate.format(DateTimeFormatter.ofPattern("dd-MM-yyyy")) + ", " +
//                "\"minimalPoint\": " + (minimalPoint == null ? "null" : minimalPoint.toString()) + ", " +
//                "\"description\": " + description + ", " +
//                "\"tunedInWorks\": " + tunedInWorks + ", " +
//                "\"difficulty\": " + difficulty + ", " +
//                "\"discipline\" (name;practiceHours): " + discipline + "}";
//    }
}