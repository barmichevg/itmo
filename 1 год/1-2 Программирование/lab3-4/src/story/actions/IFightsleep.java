package story.actions;

public interface IFightsleep {
    default void fightsleep(Timemark timemark) {
        System.out.println("Его одолевал сон. Но он еще не спал.");
    }
}