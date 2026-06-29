package web.models;

import org.junit.Test;
import java.math.BigDecimal;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

public class HitBeanTest {

    private static BigDecimal bd(String value) {
        return new BigDecimal(value);
    }

    @Test
    public void pointInsideFirstQuadrantCircleShouldHit() {
        assertTrue(HitBean.inArea(
                bd("1"),
                bd("1"),
                bd("4")
        ));
    }

    @Test
    public void pointOnCircleBorderShouldHit() {
        assertTrue(HitBean.inArea(
                bd("2"),
                bd("0"),
                bd("4")
        ));
    }

    @Test
    public void pointOutsideFirstQuadrantCircleShouldMiss() {
        assertFalse(HitBean.inArea(
                bd("2"),
                bd("1"),
                bd("4")
        ));
    }

    @Test
    public void pointInsideSecondQuadrantRectangleShouldHit() {
        assertTrue(HitBean.inArea(
                bd("-1"),
                bd("3"),
                bd("4")
        ));
    }

    @Test
    public void pointOnSecondQuadrantRectangleBorderShouldHit() {
        assertTrue(HitBean.inArea(
                bd("-2"),
                bd("4"),
                bd("4")
        ));
    }

    @Test
    public void pointOutsideSecondQuadrantRectangleShouldMiss() {
        assertFalse(HitBean.inArea(
                bd("-3"),
                bd("3"),
                bd("4")
        ));
    }

    @Test
    public void pointInsideThirdQuadrantTriangleShouldHit() {
        assertTrue(HitBean.inArea(
                bd("-0.5"),
                bd("-0.5"),
                bd("4")
        ));
    }

    @Test
    public void pointOnThirdQuadrantTriangleBorderShouldHit() {
        assertTrue(HitBean.inArea(
                bd("-1"),
                bd("-1"),
                bd("4")
        ));
    }

    @Test
    public void pointOutsideThirdQuadrantTriangleShouldMiss() {
        assertFalse(HitBean.inArea(
                bd("-1.5"),
                bd("-1"),
                bd("4")
        ));
    }

    @Test
    public void pointInFourthQuadrantShouldMiss() {
        assertFalse(HitBean.inArea(
                bd("1"),
                bd("-1"),
                bd("4")
        ));
    }
}