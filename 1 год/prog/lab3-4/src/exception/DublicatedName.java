package exception;

public class DublicatedName extends RuntimeException {
    private final String Name;

    public DublicatedName(String name) {
        this.Name = name;
    }

    @Override
    public String getMessage() {
        return "Персонаж с именем " + this.Name + " уже создан.";
    }
}