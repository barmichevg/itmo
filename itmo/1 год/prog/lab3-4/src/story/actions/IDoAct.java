package story.actions;

import java.io.PrintStream;

public interface IDoAct {
    default void doAct(Timemark timemark, Action action) {
        System.out.println(timemark.Time() + " он " + action.Text());
    }
}