package exception;

public class AlreadyInGroup extends RuntimeException {
    private final String Name;

    public AlreadyInGroup(String name) {
        this.Name = name;
    }

    @Override
    public String getMessage() {
        return this.Name + " уже в группе.";
    }
}