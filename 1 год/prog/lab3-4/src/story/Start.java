package story;

import story.actions.Action;
import story.actions.IGuess;
import story.actions.Timemark;
import story.scene.Scene;

public class Start implements IGuess {
    private Scene scene;

    public Start(Scene scene) {
        this.scene = scene;
    }

    public void go() {
        this.scene.Carlson().doAct(Timemark.LATER, Action.SAY_GOODBYE);
        this.scene.boy().doAct(Timemark.HOURLATER, Action.LIE_IN_BED);
        this.scene.Basket().doAct(Timemark.NONE, Action.STAND_NEXT_TO);
        this.scene.place().addGroup(this.scene.group(), Action.SAY_GOODNIGHT);
        this.scene.boy().fightsleep(Timemark.NONE);
        this.scene.boy().think(Timemark.NONE, this.scene.Carlson());
        this.guess(Timemark.NOW, this.scene.Carlson(), this.scene.randomGuess());
    }
}