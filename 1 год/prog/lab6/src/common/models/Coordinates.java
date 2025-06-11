package common.models;

import java.io.Serializable;

public class Coordinates implements Serializable {
    private Integer x; // Максимум 589
    private Float y;   // Максимум 654

    public Coordinates(Integer x, Float y) {
        this.x = x;
        this.y = y;
    }

    public Integer getX() { return x; }
    public Float getY() { return y; }

    public void setX(Integer x) { this.x = x; }
    public void setY(Float y) { this.y = y; }

    @Override
    public String toString() {
        return "(" + x + ", " + y + ")";
    }
}