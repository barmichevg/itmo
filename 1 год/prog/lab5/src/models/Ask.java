package models;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;

import managers.CollectionManager;
import utility.Console;
import java.util.NoSuchElementException;
import java.lang.IllegalArgumentException;

/**
 * Класс чтения объекта
 */
public class Ask {
    public static class AskBreak extends Exception {}
    public static LabWork askLabWork(Console console, CollectionManager collectionManager) throws AskBreak {
        /**
         * String name; //Поле не может быть null, Строка не может быть пустой
         * Coordinates coordinates; //Поле не может быть null
         * LocalDate creationDate; //Поле не может быть null, Значение этого поля должно генерироваться автоматически
         * Double minimalPoint; //Поле может быть null, Значение поля должно быть больше 0
         * String description; //Длина строки не должна быть больше 5287, Поле не может быть null
         * int tunedInWorks;
         * Difficulty difficulty; //Поле не может быть null
         * Discipline discipline; //Поле не может быть null
         */
        try {
            console.print("name: ");
            String name;
            while (true) {
                name = console.readln().trim();
                if (name.equals("exit")) throw new AskBreak();
                if (!name.equals("")) break;
                console.print("name: ");
            }
            Coordinates coordinates = askCoordinates(console);
            LocalDate creationDate;
            while (true) {
                console.print("creationDate (dd-MM-yyyy): ");
                String line = console.readln().trim();
                if (line.equals("exit")) throw new AskBreak();
                if (line.equals("")) {
                    creationDate = null;
                    break;
                }
                try {
                    creationDate = LocalDate.parse(line, DateTimeFormatter.ofPattern("dd-MM-yyyy"));
                    break;
                } catch (DateTimeParseException e) {}
                try {
                    creationDate = LocalDate.parse(line + "T00:00:00.0000", DateTimeFormatter.ofPattern("dd-MM-yyyy"));
                    break;
                } catch (DateTimeParseException e) {}
                console.print("Некорректный ввод \ncreationDate (dd-MM-yyyy): ");
            }
            console.print("minimalPoint: ");
            Double minimalPoint;
            while (true) {
                String line = console.readln().trim();
                if (line.equals("exit")) throw new AskBreak();
                if (line.isEmpty()) {
                    minimalPoint = null;
                    break;
                }
                try {
                    minimalPoint = Double.parseDouble(line);
                    if (minimalPoint > 0) break;
                } catch (NumberFormatException e) {}
                console.print("Некорректный ввод \nminimalPoint: ");
            }
            console.print("description: ");
            String description;
            while (true) {
                description = console.readln().trim();
                if (description.equals("exit")) throw new AskBreak();
                if (!description.isEmpty()) break;
                if (description.length() <= 5287) break;
                console.print("Некорректный ввод \ndescription: ");
            }
            console.print("tunedInWorks: ");
            int tunedInWorks;
            while (true) {
                String line = console.readln().trim();
                if (line.equals("exit")) throw new AskBreak();
                try {
                    tunedInWorks = Integer.parseInt(line);
                    break;
                } catch (NumberFormatException e) {}
                console.print("Некорректный ввод \ntunedInWorks: ");
            }
            Difficulty difficulty = askDifficulty(console);
            Discipline discipline = askDiscipline(console);
            return new LabWork(collectionManager.getFreeId(), name, coordinates, creationDate, minimalPoint, description, tunedInWorks, difficulty, discipline);
        } catch (NoSuchElementException | IllegalStateException e) {
            console.printError("Ошибка чтения");
            return null;
        }
    }

    public static Coordinates askCoordinates(Console console) throws AskBreak {
        try {
            console.print("coordinates.x: ");
            int x;
            while (true) {
                String line = console.readln().trim();
                if (line.equals("exit")) throw new AskBreak();
                if (!line.equals("")) {
                    try { x = Integer.parseInt(line); break; } catch (NumberFormatException e) {}
                }
                console.print("Некорректный ввод \ncoordinates.x: ");
            }
            console.print("coordinates.y: ");
            float y;
            while (true) {
                String line = console.readln().trim();
                if (line.equals("exit")) throw new AskBreak();
                if (!line.equals("")) {
                    try { y = Float.parseFloat(line); if (y<=654) break; } catch (NumberFormatException e) { }
                }
                console.print("Некорректный ввод \ncoordinates.y: ");
            }
            return new Coordinates(x, y);
        } catch (NoSuchElementException | IllegalStateException e) {
            console.printError("Ошибка чтения");
            return null;
        }
    }

    public static Difficulty askDifficulty(Console console) throws AskBreak {
        try {
            console.print("Difficulty ("+Difficulty.names()+"): ");
            Difficulty r;
            while (true) {
                String line = console.readln().trim();
                if (line.equals("exit")) throw new AskBreak();
                if (!line.isEmpty()) {
                    try { r = Difficulty.valueOf(line); break; } catch (NullPointerException | IllegalArgumentException  e) {}
                }
                console.print("Некорректный ввод \nDifficulty: ");
            }
            return r;
        } catch (NoSuchElementException | IllegalStateException e) {
            console.printError("Ошибка чтения");
            return null;
        }
    }

    public static Discipline askDiscipline(Console console) throws AskBreak {
        try {
            console.print("Discipline.name: ");
            String name;
            while (true) {
                name = console.readln().trim();
                if (name.equals("exit")) throw new AskBreak();
                if (!name.isEmpty()) break;
            }
            console.print("Discipline.practiceHours: ");
            long practiceHours;
            while (true) {
                String line = console.readln().trim();
                if (line.equals("exit")) throw new AskBreak();
                if (!line.isEmpty()) {
                    try { practiceHours = Long.parseLong(line); break; } catch (NumberFormatException e) {}
                }
                console.print("Некорректный ввод \nDiscipline.practiceHours: ");
            }
            return new Discipline(name, practiceHours);
        } catch (NoSuchElementException | IllegalStateException e) {
            console.printError("Ошибка чтения");
            return null;
        }
    }
}