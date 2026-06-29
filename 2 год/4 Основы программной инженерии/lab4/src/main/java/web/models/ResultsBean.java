package web.models;

import jakarta.enterprise.context.SessionScoped;
import jakarta.inject.Inject;
import jakarta.inject.Named;
import web.db.HitRepository;
import web.mbeans.MonitoringService;

import java.io.Serializable;
import java.util.Collections;
import java.util.List;

@Named("results")
@SessionScoped
public class ResultsBean implements Serializable {

    private static final long serialVersionUID = 1L;

    @Inject
    private HitRepository repository;

    @Inject
    private MonitoringService monitoringService;

    private int pageSize = 6;
    private int pageIndex = 0;

    public void add(HitResult r) {
        repository.save(r);
        monitoringService.onPointAdded(r);
        pageIndex = 0;
    }

    public void clear() {
        repository.clearAll();
        monitoringService.resetPointStats();
        pageIndex = 0;
    }

    public List<HitResult> getResults() {
        return getPage();
    }

    public void setResults(List<HitResult> ignored) {
        pageIndex = 0;
    }

    public HitResult getLast() {
        return repository.findLatest();
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
        normalizePageIndex();
        return pageIndex;
    }

    public void setPageIndex(int pageIndex) {
        this.pageIndex = pageIndex;
        normalizePageIndex();
    }

    public int getPageCount() {
        long total = repository.count();
        if (total <= 0) {
            return 1;
        }
        return (int) ((total + pageSize - 1) / pageSize);
    }

    public List<HitResult> getPage() {
        normalizePageIndex();
        if (repository.count() <= 0) {
            return Collections.emptyList();
        }
        return repository.findPage(pageIndex, pageSize);
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
        return this == o;
    }

    @Override
    public int hashCode() {
        return System.identityHashCode(this);
    }
}
