package models;

import exceptions.ValidationException;
import utility.Validatable;
import java.util.Objects;

/**
 * Класс координаты
 */
public class Coordinates implements Validatable{
    private Integer x; //Поле не может быть null
    private float y; //Максимальное значение поля: 654

    public Coordinates (Integer x, float y) {
        this.x = x;
        this.y = y;
        if (!validate()){throw new ValidationException("Coordinates");}
    }

    public Coordinates(String s) {
        try {
            try { this.x = Integer.parseInt(s.split(";")[0]); } catch (NumberFormatException e) { }
            try { this.y = Float.parseFloat(s.split(";")[1]); } catch (NumberFormatException e) { }
        } catch (ArrayIndexOutOfBoundsException e) {}
    }


    /**
     * Метод, возвращающий значение поля x
     * @return возвращает x
     */
    public Integer getx() {
        return x;
    }

    /**
     * Метод, возвращающий значение поля y
     * @return возвращает y
     */
    public float gety() {
        return y;
    }

    @Override
    public boolean validate() {
        if (x == null) return false;
        return y <= 654;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Coordinates that = (Coordinates) o;
        return Objects.equals(x, that.x) && Objects.equals(y, that.y);
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }

    @Override
    public String toString() {
        return x + ";" + y;
    }
}