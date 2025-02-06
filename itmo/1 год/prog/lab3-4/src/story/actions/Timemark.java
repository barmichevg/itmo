package story.actions;

public enum Timemark {
    NOW("Сейчас"),
    LATER("Потом"),
    HOURLATER("Час спустя"),
    NONE("");

    private String time;

    private Timemark(String time) {
        this.time = time;
    }

    public String Time() {
        return this.time;
    }
}