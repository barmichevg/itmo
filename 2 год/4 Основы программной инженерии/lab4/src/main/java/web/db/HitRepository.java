package web.db;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.PersistenceUnit;
import web.models.HitResult;

import java.util.List;

@ApplicationScoped
public class HitRepository {

    @PersistenceUnit(unitName = "hitsPU")
    private EntityManagerFactory emf;

    private EntityManager em() {
        return emf.createEntityManager();
    }

    public void save(HitResult hit) {
        EntityManager em = em();
        try {
            em.getTransaction().begin();
            em.persist(hit);
            em.getTransaction().commit();
        } finally {
            em.close();
        }
    }

    public List<HitResult> findAll() {
        EntityManager em = em();
        try {
            return em.createQuery(
                    "select h from HitResult h order by h.at desc",
                    HitResult.class
            ).getResultList();
        } finally {
            em.close();
        }
    }

    public List<HitResult> findPage(int pageIndex, int pageSize) {
        EntityManager em = em();
        try {
            int safePageIndex = Math.max(0, pageIndex);
            int safePageSize = Math.max(1, pageSize);

            return em.createQuery(
                    "select h from HitResult h order by h.at desc",
                    HitResult.class
            ).setFirstResult(safePageIndex * safePageSize)
             .setMaxResults(safePageSize)
             .getResultList();
        } finally {
            em.close();
        }
    }

    public HitResult findLatest() {
        EntityManager em = em();
        try {
            List<HitResult> latest = em.createQuery(
                    "select h from HitResult h order by h.at desc",
                    HitResult.class
            ).setMaxResults(1)
             .getResultList();

            return latest.isEmpty() ? null : latest.get(0);
        } finally {
            em.close();
        }
    }

    public long count() {
        EntityManager em = em();
        try {
            return em.createQuery(
                    "select count(h) from HitResult h",
                    Long.class
            ).getSingleResult();
        } finally {
            em.close();
        }
    }

    public void clearAll() {
        EntityManager em = em();
        try {
            em.getTransaction().begin();
            em.createQuery("delete from HitResult").executeUpdate();
            em.getTransaction().commit();
        } finally {
            em.close();
        }
    }
}
