package web.models;

import jakarta.enterprise.context.SessionScoped;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

@SessionScoped
public class ResultsBean implements Serializable {
    private List<HitResult> history = new ArrayList<>();

    public void add(HitResult r) { history.add(r); }
    public List<HitResult> getResults() { return history; }
    public void setResults(List<HitResult> history) {this.history = history;}
    public void clear() { history.clear(); }
    public HitResult getLast() { return history.isEmpty() ? null : history.get(history.size()-1); }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (! (o instanceof ResultsBean)) return false;
        ResultsBean results = (ResultsBean) o;
        return Objects.equals(getResults(), results.getResults());
    }

    @Override
    public int hashCode() {
        return Objects.hash(getResults());
    }
}

