package story.actions;

public enum Assumption {
    CRAFT("как раз что-нибудь мастерит...  скворечник или еще что..."),
    WENT_TO_STORE("ушел в магазин...  за хлебом или чем-нибуть еще..."),
    HID("где-нибудь спрятался...  под кроватью или еще где-то...");

    private final String description;

    private Assumption(String description) {
        this.description = description;
    }

    public String describe() {
        return this.description;
    }

    public String toString() {
        return this.name();
    }
}