package ru.itmo.lab4.hit;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ru.itmo.lab4.api.HitRequest;
import ru.itmo.lab4.common.DecimalParser;
import ru.itmo.lab4.common.ValidationException;
import ru.itmo.lab4.user.UserAccount;
import ru.itmo.lab4.user.UserRepository;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

@Service
public class HitService {

    private static final BigDecimal MIN_X = BigDecimal.valueOf(-5);
    private static final BigDecimal MAX_X = BigDecimal.valueOf(5);
    private static final BigDecimal MIN_Y = BigDecimal.valueOf(-5);
    private static final BigDecimal MAX_Y = BigDecimal.valueOf(3);
    private static final BigDecimal MAX_R = BigDecimal.valueOf(5);

    private final HitRepository hitRepository;
    private final UserRepository userRepository;

    public HitService(HitRepository hitRepository, UserRepository userRepository) {
        this.hitRepository = hitRepository;
        this.userRepository = userRepository;
    }

    @Transactional(readOnly = true)
    public List<Hit> listForUser(String login) {
        UserAccount user = userRepository.findByLogin(login).orElseThrow();
        return hitRepository.findAllByUserOrderByCreatedAtDesc(user);
    }

    @Transactional
    public void clearForUser(String login) {
        UserAccount user = userRepository.findByLogin(login).orElseThrow();
        hitRepository.deleteByUser(user);
    }

    @Transactional
    public Hit create(String login, HitRequest req) {
        BigDecimal x;
        BigDecimal y;
        BigDecimal r;

        List<String> errors = new ArrayList<>();

        try { x = DecimalParser.parse(req.x()); }
        catch (Exception e) { x = null; errors.add("X: некорректное число"); }

        try { y = DecimalParser.parse(req.y()); }
        catch (Exception e) { y = null; errors.add("Y: некорректное число"); }

        try { r = DecimalParser.parse(req.r()); }
        catch (Exception e) { r = null; errors.add("R: некорректное число"); }

        if (!errors.isEmpty()) {
            throw new ValidationException(errors);
        }

        boolean fromGraph = Boolean.TRUE.equals(req.fromGraph());

        if (!fromGraph) {
            if (x.compareTo(MIN_X) < 0 || x.compareTo(MAX_X) > 0) {
                errors.add("X должен быть в диапазоне [-5; 5]");
            }
            if (y.compareTo(MIN_Y) < 0 || y.compareTo(MAX_Y) > 0) {
                errors.add("Y должен быть в диапазоне [-5; 3]");
            }
        }


        if (r.compareTo(BigDecimal.ZERO) <= 0) {
            errors.add("R должен быть положительным");
        }
        if (r.compareTo(MAX_R) > 0) {
            errors.add("R должен быть <= 5");
        }

        if (!errors.isEmpty()) {
            throw new ValidationException(errors);
        }

        long t0 = System.nanoTime();
        boolean hit = isInArea(x, y, r);
        long micros = (System.nanoTime() - t0) / 1_000L;

        UserAccount user = userRepository.findByLogin(login).orElseThrow();
        Hit entity = new Hit(user, x, y, r, hit, Instant.now(), micros);
        return hitRepository.save(entity);
    }

    public static boolean isInArea(BigDecimal x, BigDecimal y, BigDecimal r) {
        BigDecimal rHalf = r.divide(BigDecimal.valueOf(2), 10, RoundingMode.HALF_UP);

        // Q2
        boolean q2 = x.compareTo(BigDecimal.ZERO) <= 0
                && y.compareTo(BigDecimal.ZERO) >= 0
                && x.compareTo(rHalf.negate()) >= 0
                && y.compareTo(r) <= 0;

        // Q3
        boolean q3 = x.compareTo(BigDecimal.ZERO) <= 0
                && y.compareTo(BigDecimal.ZERO) <= 0
                && x.compareTo(rHalf.negate()) >= 0
                && BigDecimal.valueOf(2).multiply(x).add(y).add(r).compareTo(BigDecimal.ZERO) >= 0;

        // Q4
        boolean q4 = x.compareTo(BigDecimal.ZERO) >= 0
                && y.compareTo(BigDecimal.ZERO) <= 0
                && x.multiply(x).add(y.multiply(y)).compareTo(rHalf.multiply(rHalf)) <= 0;

        return q2 || q4 || q3;
    }
}
