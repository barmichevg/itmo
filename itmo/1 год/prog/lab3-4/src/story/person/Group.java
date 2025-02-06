package story.person;

import exception.AlreadyInGroup;
import exception.NotInGroup;
import java.util.ArrayList;
import java.util.List;
import story.actions.Action;
import story.actions.IDoAct;
import story.actions.Timemark;

public class Group implements IDoAct {
    private String name;
    private List<Person> members = new ArrayList();

    public Group(String name) {
        this.name = name;
    }

    public void addMember(Person person) {
        if (!this.members.contains(person)) {
            this.members.add(person);
        } else {
            throw new AlreadyInGroup(person.getName());
        }
    }

    public void rmMember(Person person) {
        if (this.members.contains(person)) {
            this.members.remove(person);
        } else {
            throw new NotInGroup(person.getName());
        }
    }

    @Override
    public String toString() {
        return this.name + " --" + members + "--";
    }

    public String getName() {
        return this.toString();
    }

    public void setName(String name) {
        this.name = name;
    }

    public List<Person> getMembers() {
        return members;
    }

    @Override
    public void doAct(Timemark timemark, Action action) {
        String answer = timemark.Time() + " " + this.toString() + " " + action.Text();
        if (timemark.Time() == "") {
            answer = this.toString() + " " + action.Text();
        }
        System.out.println(answer);
    }
}