package story.actions;

public enum Action {
    SAY_GOODBYE("прощается."),
    SAY_GOODNIGHT("пожелать спокойной ночи."),
    STAND_NEXT_TO("стоять рядом."),
    LIE_IN_BED("лежать в кроватке."),
    NONE("");

    private String text;

    private Action(String text) {
        this.text = text;
    }

    public String Text() {
        return this.text;
    }
}