package ru.itmo.lab4.hit;

import jakarta.persistence.*;
import ru.itmo.lab4.user.UserAccount;

import java.math.BigDecimal;
import java.time.Instant;

@Entity
@Table(name = "hits")
public class Hit {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(optional = false, fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private UserAccount user;

    @Column(name = "x", nullable = false)
    private BigDecimal x;

    @Column(name = "y", nullable = false)
    private BigDecimal y;

    @Column(name = "r", nullable = false)
    private BigDecimal r;

    @Column(name = "hit", nullable = false)
    private boolean hit;

    @Column(name = "created_at", nullable = false)
    private Instant createdAt;

    @Column(name = "script_micros", nullable = false)
    private long scriptMicros;

    protected Hit() {}

    public Hit(UserAccount user, BigDecimal x, BigDecimal y, BigDecimal r, boolean hit, Instant createdAt, long scriptMicros) {
        this.user = user;
        this.x = x;
        this.y = y;
        this.r = r;
        this.hit = hit;
        this.createdAt = createdAt;
        this.scriptMicros = scriptMicros;
    }

    public Long getId() { return id; }
    public UserAccount getUser() { return user; }
    public BigDecimal getX() { return x; }
    public BigDecimal getY() { return y; }
    public BigDecimal getR() { return r; }
    public boolean isHit() { return hit; }
    public Instant getCreatedAt() { return createdAt; }
    public long getScriptMicros() { return scriptMicros; }
}
