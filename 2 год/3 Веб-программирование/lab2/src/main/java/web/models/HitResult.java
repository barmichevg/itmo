package web.models;

import java.io.Serializable;
import java.math.BigDecimal;
import java.time.Instant;
import java.util.Objects;

public class HitResult implements Serializable {
    public BigDecimal x, y, r;
    public boolean hit;
    public Instant at;
    public long scriptMicros;

    public HitResult() {}

    public BigDecimal getX() { return x; }
    public BigDecimal getY() { return y; }
    public BigDecimal getR() { return r; }
    public boolean getHit() { return hit; }
    public Instant getAt() { return at; }
    public long getScriptMicros() { return scriptMicros; }
    public BigDecimal setX(BigDecimal x) { return this.x = x; }
    public BigDecimal setY(BigDecimal y) { return this.y = y; }
    public BigDecimal setR(BigDecimal r) { return this.r = r; }
    public boolean setHit(boolean hit) { return this.hit = hit; }
    public Instant setAt(Instant at) { return this.at = at; }
    public long setScriptMicros(long scriptMicros) { return this.scriptMicros = scriptMicros; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (! (o instanceof HitResult)) return false;
        HitResult hit = (HitResult) o;
        return (getX().compareTo(hit.getX())==0) && (getY().compareTo(hit.getY())==0) &&
               (getR().compareTo(hit.getR())==0) && (getHit() == hit.getHit()) &&
               getAt().equals(hit.getAt()) && (getScriptMicros() == hit.getScriptMicros());
    }

    @Override
    public int hashCode() {
        return Objects.hash(getX(), getY(), getR(), getHit(), getAt(), getScriptMicros());
    }
}
