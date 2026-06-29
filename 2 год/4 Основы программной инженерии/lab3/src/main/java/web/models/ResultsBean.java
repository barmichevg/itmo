package web.models;

import jakarta.annotation.PostConstruct;
import jakarta.enterprise.context.SessionScoped;
import jakarta.inject.Inject;
import jakarta.inject.Named;
import web.db.HitRepository;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

@Named("results")
@SessionScoped
public class ResultsBean implements Serializable {

    @Inject
    private HitRepository repository;

    private List<HitResult> history;

    private int pageSize = 10;
    private int pageIndex = 0;

    @PostConstruct
    public void init() {
        history = new ArrayList<>(repository.findAll());
    }

    public void add(HitResult r) {
        repository.save(r);
        history.add(0, r);
        pageIndex = 0;
    }

    public void clear() {
        repository.clearAll();
        history.clear();
        pageIndex = 0;
    }

    public List<HitResult> getResults() {
        return history;
    }

    public void setResults(List<HitResult> history) {
        this.history = history;
        normalizePageIndex();
    }

    public HitResult getLast() {
        return history.isEmpty() ? null : history.get(history.size() - 1);
    }

    public int getPageSize() {
        return pageSize;
    }

    public void setPageSize(int pageSize) {
        if (pageSize <= 0) return;
        this.pageSize = pageSize;
        pageIndex = 0;
        normalizePageIndex();
    }

    public int getPageIndex() {
        return pageIndex;
    }

    public void setPageIndex(int pageIndex) {
        this.pageIndex = pageIndex;
        normalizePageIndex();
    }

    public int getPageCount() {
        if (history == null || history.isEmpty()) {
            return 1;
        }
        return (history.size() + pageSize - 1) / pageSize;
    }

    public List<HitResult> getPage() {
        if (history == null || history.isEmpty()) {
            return Collections.emptyList();
        }
        normalizePageIndex();

        int from = pageIndex * pageSize;
        int to = Math.min(from + pageSize, history.size());
        if (from < 0 || from >= to) {
            return Collections.emptyList();
        }
        return history.subList(from, to);
    }

    private void normalizePageIndex() {
        int pc = getPageCount();
        if (pageIndex < 0) pageIndex = 0;
        if (pageIndex >= pc) pageIndex = pc - 1;
    }


    public void nextPage() {
        if (pageIndex < getPageCount() - 1) {
            pageIndex++;
        }
    }

    public void prevPage() {
        if (pageIndex > 0) {
            pageIndex--;
        }
    }

    public void firstPage() {
        pageIndex = 0;
    }

    public void lastPage() {
        pageIndex = Math.max(0, getPageCount() - 1);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof ResultsBean)) return false;
        ResultsBean results = (ResultsBean) o;
        return Objects.equals(getResults(), results.getResults());
    }

    @Override
    public int hashCode() {
        return Objects.hash(getResults());
    }
}
