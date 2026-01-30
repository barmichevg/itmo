package exception;

public class NotInGroup extends RuntimeException {
    private final String Name;

    public NotInGroup(String name) {
        this.Name = name;
    }

    @Override
    public String getMessage() {
        return this.Name + " нет в группе.";
    }
}